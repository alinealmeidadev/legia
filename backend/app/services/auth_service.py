"""
LEGIA PLATFORM - Serviço de Autenticação
"""
from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException, status

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_2fa_token,
    generate_2fa_secret,
    get_2fa_qr_code_url
)
from app.core.config import settings
from app.models.public.legia_user import LegiaUser
from app.models.public.tenant import Tenant
from app.models.public.plan import Plan
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterTenantRequest,
    Token
)
from app.utils.tenant_schema import create_tenant_schema


class AuthService:
    """Serviço de autenticação"""

    @staticmethod
    def login_legia_user(
        db: Session,
        login_data: LoginRequest
    ) -> LoginResponse:
        """
        Autentica um usuário Legia (Super Admin)

        Args:
            db: Sessão do banco
            login_data: Dados de login

        Returns:
            LoginResponse com tokens e dados do usuário

        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        # Buscar usuário
        user = db.query(LegiaUser).filter(
            LegiaUser.email == login_data.email
        ).first()

        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo"
            )

        # Verificar 2FA se habilitado
        if user.two_factor_enabled:
            if not login_data.two_factor_code:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Código 2FA requerido",
                    headers={"X-Require-2FA": "true"}
                )

            if not verify_2fa_token(user.two_factor_secret, login_data.two_factor_code):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Código 2FA inválido"
                )

        # Criar tokens
        token_data = {
            "sub": user.email,
            "user_type": "legia_user",
            "role": user.role
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # Atualizar último login
        user.last_login_at = datetime.now(timezone.utc)
        db.commit()

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "user_type": "legia_user"
            }
        )

    @staticmethod
    def login_tenant_user(
        db: Session,
        login_data: LoginRequest,
        tenant_id: int
    ) -> LoginResponse:
        """
        Autentica um usuário de tenant (escritório)

        Args:
            db: Sessão do banco
            login_data: Dados de login
            tenant_id: ID do tenant

        Returns:
            LoginResponse com tokens e dados do usuário

        Raises:
            HTTPException: Se as credenciais forem inválidas
        """
        # Buscar tenant
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant não encontrado"
            )

        if not tenant.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tenant inativo ou suspenso"
            )

        # Buscar usuário no schema do tenant
        schema_name = tenant.schema_name
        result = db.execute(
            text(f"""
                SELECT * FROM {schema_name}.users
                WHERE email = :email
            """),
            {"email": login_data.email}
        )
        user_data = result.fetchone()

        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        user_dict = dict(user_data._mapping)

        # Verificar senha
        if not verify_password(login_data.password, user_dict['password_hash']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )

        if not user_dict['is_active']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo"
            )

        # Verificar 2FA se habilitado
        if user_dict.get('two_factor_enabled'):
            if not login_data.two_factor_code:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Código 2FA requerido",
                    headers={"X-Require-2FA": "true"}
                )

            if not verify_2fa_token(
                user_dict['two_factor_secret'],
                login_data.two_factor_code
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Código 2FA inválido"
                )

        # Criar tokens
        token_data = {
            "sub": user_dict['email'],
            "user_type": "tenant_user",
            "tenant_id": tenant_id,
            "role": user_dict['role']
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # Atualizar último login
        db.execute(
            text(f"""
                UPDATE {schema_name}.users
                SET last_login_at = :now
                WHERE id = :user_id
            """),
            {"now": datetime.now(timezone.utc), "user_id": user_dict['id']}
        )
        db.commit()

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user={
                "id": user_dict['id'],
                "email": user_dict['email'],
                "name": user_dict['name'],
                "role": user_dict['role'],
                "user_type": "tenant_user",
                "tenant_id": tenant_id,
                "tenant_name": tenant.name
            }
        )

    @staticmethod
    def refresh_access_token(
        db: Session,
        refresh_token: str
    ) -> Token:
        """
        Gera novo access token a partir de refresh token

        Args:
            db: Sessão do banco
            refresh_token: Refresh token válido

        Returns:
            Token com novo access_token e refresh_token

        Raises:
            HTTPException: Se o refresh token for inválido
        """
        payload = decode_token(refresh_token)

        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )

        # Criar novos tokens
        token_data = {
            "sub": payload["sub"],
            "user_type": payload["user_type"]
        }

        if payload.get("tenant_id"):
            token_data["tenant_id"] = payload["tenant_id"]

        if payload.get("role"):
            token_data["role"] = payload["role"]

        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)

        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token
        )

    @staticmethod
    def register_tenant(
        db: Session,
        register_data: RegisterTenantRequest
    ) -> dict:
        """
        Registra um novo tenant (escritório)

        Args:
            db: Sessão do banco
            register_data: Dados de registro

        Returns:
            Dict com dados do tenant e admin criados

        Raises:
            HTTPException: Se houver erro no registro
        """
        # Verificar se CNPJ já existe
        existing_tenant = db.query(Tenant).filter(
            Tenant.cnpj == register_data.cnpj
        ).first()

        if existing_tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CNPJ já cadastrado"
            )

        # Verificar se email já existe
        existing_email = db.query(Tenant).filter(
            Tenant.email == register_data.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

        # Gerar subdomínio a partir do nome
        subdomain = register_data.name.lower()
        subdomain = subdomain.replace(" ", "-")
        subdomain = "".join(c for c in subdomain if c.isalnum() or c == "-")
        subdomain = subdomain[:50]  # Limitar tamanho

        # Verificar se subdomínio já existe
        counter = 1
        original_subdomain = subdomain
        while db.query(Tenant).filter(Tenant.subdomain == subdomain).first():
            subdomain = f"{original_subdomain}-{counter}"
            counter += 1

        # Verificar se plano existe
        plan = db.query(Plan).filter(Plan.id == register_data.plan_id).first()
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plano não encontrado"
            )

        # Criar tenant
        tenant = Tenant(
            name=register_data.name,
            subdomain=subdomain,
            cnpj=register_data.cnpj,
            email=register_data.email,
            phone=register_data.phone,
            plan_id=register_data.plan_id,
            status="trial",
            trial_ends_at=datetime.now(timezone.utc) + timedelta(days=14)  # 14 dias de trial
        )

        db.add(tenant)
        db.flush()  # Para obter o ID

        # Criar schema do tenant
        if not create_tenant_schema(tenant.id, db):
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar schema do tenant"
            )

        # Criar usuário admin no schema do tenant
        schema_name = tenant.schema_name
        password_hash = get_password_hash(register_data.admin_password)

        db.execute(
            text(f"""
                INSERT INTO {schema_name}.users
                (email, password_hash, name, role, is_active, is_verified)
                VALUES (:email, :password_hash, :name, 'admin', TRUE, TRUE)
            """),
            {
                "email": register_data.admin_email,
                "password_hash": password_hash,
                "name": register_data.admin_name
            }
        )

        db.commit()

        return {
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "subdomain": tenant.subdomain,
                "email": tenant.email,
                "status": tenant.status
            },
            "admin": {
                "email": register_data.admin_email,
                "name": register_data.admin_name
            },
            "message": "Tenant criado com sucesso! Você pode fazer login agora."
        }
