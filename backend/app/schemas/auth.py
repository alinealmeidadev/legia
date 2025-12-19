"""
LEGIA PLATFORM - Schemas de Autenticação
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    """Schema para resposta de token JWT"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema para payload do token JWT"""
    sub: str  # user_id ou email
    user_type: str  # "legia_user" ou "tenant_user"
    tenant_id: Optional[int] = None
    exp: Optional[int] = None


class LoginRequest(BaseModel):
    """Schema para request de login"""
    email: EmailStr
    password: str = Field(..., min_length=6)
    two_factor_code: Optional[str] = Field(None, min_length=6, max_length=6)


class LoginResponse(BaseModel):
    """Schema para response de login"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict  # Dados básicos do usuário


class RefreshTokenRequest(BaseModel):
    """Schema para request de refresh token"""
    refresh_token: str


class RegisterTenantRequest(BaseModel):
    """Schema para registro de novo tenant"""
    # Dados do escritório
    name: str = Field(..., min_length=3, max_length=255)
    cnpj: str = Field(..., pattern=r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")
    email: EmailStr
    phone: Optional[str] = None

    # Dados do admin
    admin_name: str = Field(..., min_length=3, max_length=255)
    admin_email: EmailStr
    admin_password: str = Field(..., min_length=8)

    # Plano
    plan_id: int = Field(..., gt=0)


class ForgotPasswordRequest(BaseModel):
    """Schema para esqueci senha"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema para resetar senha"""
    token: str
    new_password: str = Field(..., min_length=8)


class ChangePasswordRequest(BaseModel):
    """Schema para trocar senha"""
    current_password: str
    new_password: str = Field(..., min_length=8)


class Enable2FAResponse(BaseModel):
    """Schema para resposta de habilitação 2FA"""
    secret: str
    qr_code_url: str
    backup_codes: list[str]


class Verify2FARequest(BaseModel):
    """Schema para verificação 2FA"""
    code: str = Field(..., min_length=6, max_length=6)
