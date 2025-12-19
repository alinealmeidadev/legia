"""
LEGIA PLATFORM - Schemas de Tenants
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TenantBase(BaseModel):
    """Base schema para Tenant"""
    name: str = Field(..., min_length=3, max_length=255)
    subdomain: str = Field(..., min_length=3, max_length=100, pattern=r"^[a-z0-9-]+$")
    cnpj: str = Field(..., pattern=r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$")
    crc: Optional[str] = Field(None, max_length=50)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)


class TenantCreate(TenantBase):
    """Schema para criar Tenant"""
    plan_id: int = Field(..., gt=0)
    status: str = Field(default="trial")

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = Field(None, max_length=2)
    address_zipcode: Optional[str] = Field(None, pattern=r"^\d{5}-?\d{3}$")


class TenantUpdate(BaseModel):
    """Schema para atualizar Tenant"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    crc: Optional[str] = None
    status: Optional[str] = None
    plan_id: Optional[int] = None

    # Branding
    logo_url: Optional[str] = None
    primary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    secondary_color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zipcode: Optional[str] = None

    # Configurações
    settings: Optional[dict] = None


class TenantResponse(TenantBase):
    """Schema para resposta de Tenant"""
    id: int
    status: str
    plan_id: Optional[int] = None
    created_at: datetime
    trial_ends_at: Optional[datetime] = None
    activated_at: Optional[datetime] = None
    suspended_at: Optional[datetime] = None
    canceled_at: Optional[datetime] = None

    # Branding
    logo_url: Optional[str] = None
    primary_color: str
    secondary_color: str

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zipcode: Optional[str] = None

    # Custom domain
    custom_domain: Optional[str] = None
    custom_domain_verified: bool

    class Config:
        from_attributes = True


class TenantListResponse(BaseModel):
    """Schema para lista de Tenants"""
    tenants: list[TenantResponse]
    total: int
    page: int
    per_page: int


class TenantStats(BaseModel):
    """Schema para estatísticas do tenant"""
    total_clients: int
    active_clients: int
    total_processes: int
    active_processes: int
    total_documents: int
    storage_used_mb: float
