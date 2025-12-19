"""
LEGIA PLATFORM - Rotas de Autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    Token,
    RegisterTenantRequest
)
from app.services.auth_service import AuthService


router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
    x_tenant_id: Optional[int] = Header(None, alias="X-Tenant-ID")
):
    """
    Login - Autentica usuário Legia ou Tenant

    - **Legia User**: Não enviar header X-Tenant-ID
    - **Tenant User**: Enviar header X-Tenant-ID com o ID do tenant
    """
    # Se não tem tenant_id, é login de Legia user
    if x_tenant_id is None:
        return AuthService.login_legia_user(db, login_data)

    # Login de tenant user
    return AuthService.login_tenant_user(db, login_data, x_tenant_id)


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh Token - Gera novo access token

    Envia o refresh_token para obter novo access_token
    """
    return AuthService.refresh_access_token(db, refresh_data.refresh_token)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_tenant(
    register_data: RegisterTenantRequest,
    db: Session = Depends(get_db)
):
    """
    Registro de Novo Tenant

    Cria um novo escritório contábil na plataforma
    """
    return AuthService.register_tenant(db, register_data)


@router.post("/logout")
def logout():
    """
    Logout

    No JWT stateless, o logout é feito no frontend removendo o token.
    Este endpoint é mantido por compatibilidade.
    """
    return {"message": "Logout realizado com sucesso"}


@router.get("/me")
def get_current_user_info(
    db: Session = Depends(get_db),
    # TODO: Adicionar dependency para extrair usuário do token
):
    """
    Informações do Usuário Atual

    Retorna dados do usuário autenticado
    """
    # TODO: Implementar extração do usuário do token
    return {"message": "Endpoint em desenvolvimento"}
