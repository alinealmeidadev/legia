"""
LEGIA PLATFORM - Dependências FastAPI
"""
from typing import Optional, Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import SessionLocal
from app.models.public.legia_user import LegiaUser
from app.models.public.tenant import Tenant
from app.schemas.auth import TokenPayload
from app.utils.tenant_schema import validate_schema_name


# OAuth2 scheme para extrair token do header Authorization
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)


def get_db() -> Generator:
    """
    Dependency para obter sessão do banco de dados

    Yields:
        Session do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_token(
    token: str = Depends(oauth2_scheme)
) -> TokenPayload:
    """
    Extrai e valida o token JWT

    Args:
        token: Token JWT do header Authorization

    Returns:
        TokenPayload com dados do usuário

    Raises:
        HTTPException: Se o token for inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        if payload is None:
            raise credentials_exception

        # Verificar se é access token
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )

        token_data = TokenPayload(**payload)

        if token_data.sub is None:
            raise credentials_exception

        return token_data

    except (JWTError, ValueError):
        raise credentials_exception


def get_current_legia_user(
    db: Session = Depends(get_db),
    token_data: TokenPayload = Depends(get_current_user_token)
) -> LegiaUser:
    """
    Obtém o usuário Legia (Super Admin) atual

    Args:
        db: Sessão do banco de dados
        token_data: Dados do token JWT

    Returns:
        LegiaUser autenticado

    Raises:
        HTTPException: Se o usuário não for encontrado ou não for Legia user
    """
    if token_data.user_type != "legia_user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: usuário não é Super Admin"
        )

    user = db.query(LegiaUser).filter(
        LegiaUser.email == token_data.sub
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    return user


def get_current_tenant_user(
    db: Session = Depends(get_db),
    token_data: TokenPayload = Depends(get_current_user_token)
) -> tuple:
    """
    Obtém o usuário do tenant (escritório) atual

    Args:
        db: Sessão do banco de dados
        token_data: Dados do token JWT

    Returns:
        Tupla (TenantUser, Tenant)

    Raises:
        HTTPException: Se o usuário ou tenant não for encontrado
    """
    if token_data.user_type != "tenant_user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: usuário não é de um tenant"
        )

    if not token_data.tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token não contém tenant_id"
        )

    # Buscar tenant
    tenant = db.query(Tenant).filter(Tenant.id == token_data.tenant_id).first()
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

    # Importar aqui para evitar import circular
    from app.models.tenant.user import TenantUser

    # Buscar usuário no schema do tenant
    schema_name = validate_schema_name(tenant.schema_name)

    # Usar raw SQL para consultar no schema correto
    from sqlalchemy import text
    result = db.execute(
        text(f"SELECT * FROM {schema_name}.users WHERE email = :email"),
        {"email": token_data.sub}
    )
    user_data = result.fetchone()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado no tenant"
        )

    # Converter para dict
    user_dict = dict(user_data._mapping)

    if not user_dict.get('is_active'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo"
        )

    return user_dict, tenant


def get_current_active_superadmin(
    current_user: LegiaUser = Depends(get_current_legia_user)
) -> LegiaUser:
    """
    Verifica se o usuário é superadmin

    Args:
        current_user: Usuário Legia atual

    Returns:
        LegiaUser se for superadmin

    Raises:
        HTTPException: Se não for superadmin
    """
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas superadmins"
        )
    return current_user


def get_current_tenant_admin(
    user_tenant: tuple = Depends(get_current_tenant_user)
) -> tuple:
    """
    Verifica se o usuário do tenant é admin

    Args:
        user_tenant: Tupla (user_dict, tenant)

    Returns:
        Tupla (user_dict, tenant) se for admin

    Raises:
        HTTPException: Se não for admin
    """
    user_dict, tenant = user_tenant

    if user_dict.get('role') != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: apenas administradores do escritório"
        )

    return user_dict, tenant
