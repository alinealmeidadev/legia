"""
LEGIA PLATFORM - Schemas de Planos
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal


class PlanBase(BaseModel):
    """Base schema para Plan"""
    name: str = Field(..., min_length=3, max_length=100)
    slug: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-z0-9-]+$")
    description: Optional[str] = None
    price_monthly: Decimal = Field(..., gt=0)
    price_yearly: Optional[Decimal] = Field(None, gt=0)


class PlanCreate(PlanBase):
    """Schema para criar Plan"""
    max_users: Optional[int] = Field(None, gt=0)
    max_clients: Optional[int] = Field(None, gt=0)
    max_storage_gb: Optional[int] = Field(None, gt=0)
    max_processes_month: Optional[int] = Field(None, gt=0)
    features: list[str] = Field(default_factory=list)
    color: Optional[str] = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    display_order: int = Field(default=0)
    is_public: bool = Field(default=True)


class PlanUpdate(BaseModel):
    """Schema para atualizar Plan"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price_monthly: Optional[Decimal] = Field(None, gt=0)
    price_yearly: Optional[Decimal] = Field(None, gt=0)
    max_users: Optional[int] = None
    max_clients: Optional[int] = None
    max_storage_gb: Optional[int] = None
    max_processes_month: Optional[int] = None
    features: Optional[list[str]] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    display_order: Optional[int] = None
    is_public: Optional[bool] = None
    is_active: Optional[bool] = None


class PlanResponse(PlanBase):
    """Schema para resposta de Plan"""
    id: int
    max_users: Optional[int] = None
    max_clients: Optional[int] = None
    max_storage_gb: Optional[int] = None
    max_processes_month: Optional[int] = None
    features: list[str]
    color: Optional[str] = None
    icon: Optional[str] = None
    display_order: int
    is_public: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PlanListResponse(BaseModel):
    """Schema para lista de Plans"""
    plans: list[PlanResponse]
    total: int
