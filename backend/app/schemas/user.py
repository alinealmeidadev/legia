"""
LEGIA PLATFORM - Schemas de Usuários
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ========== LEGIA USER (Super Admin) ==========

class LegiaUserBase(BaseModel):
    """Base schema para LegiaUser"""
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=255)
    role: str = Field(default="support")


class LegiaUserCreate(LegiaUserBase):
    """Schema para criar LegiaUser"""
    password: str = Field(..., min_length=8)


class LegiaUserUpdate(BaseModel):
    """Schema para atualizar LegiaUser"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    role: Optional[str] = None
    is_active: Optional[bool] = None
    two_factor_enabled: Optional[bool] = None


class LegiaUserResponse(LegiaUserBase):
    """Schema para resposta de LegiaUser"""
    id: int
    is_active: bool
    is_verified: bool
    two_factor_enabled: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ========== TENANT USER (Usuário do Escritório) ==========

class TenantUserBase(BaseModel):
    """Base schema para TenantUser"""
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=255)
    role: str = Field(default="contador")
    phone: Optional[str] = None


class TenantUserCreate(TenantUserBase):
    """Schema para criar TenantUser"""
    password: str = Field(..., min_length=8)


class TenantUserUpdate(BaseModel):
    """Schema para atualizar TenantUser"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    role: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None
    permissions: Optional[dict] = None


class TenantUserInvite(BaseModel):
    """Schema para convidar novo usuário"""
    email: EmailStr
    name: str = Field(..., min_length=3, max_length=255)
    role: str = Field(default="contador")


class TenantUserResponse(TenantUserBase):
    """Schema para resposta de TenantUser"""
    id: int
    is_active: bool
    is_verified: bool
    two_factor_enabled: bool
    permissions: dict
    created_at: datetime
    last_login_at: Optional[datetime] = None
    invited_at: Optional[datetime] = None
    invited_by: Optional[int] = None

    class Config:
        from_attributes = True


class TenantUserListResponse(BaseModel):
    """Schema para lista de TenantUsers"""
    users: list[TenantUserResponse]
    total: int
    page: int
    per_page: int
