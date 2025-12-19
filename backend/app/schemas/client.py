"""
LEGIA PLATFORM - Schemas de Clientes
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class ClientBase(BaseModel):
    """Base schema para Client"""
    type: str = Field(..., pattern=r"^(pf|pj)$")
    name: str = Field(..., min_length=3, max_length=255)
    document: str = Field(..., min_length=11, max_length=18)

    # Contato
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    mobile: Optional[str] = Field(None, max_length=20)


class ClientCreate(ClientBase):
    """Schema para criar Client"""
    # Dados PJ
    company_name: Optional[str] = Field(None, max_length=255)
    trade_name: Optional[str] = Field(None, max_length=255)
    cnae_primary: Optional[str] = Field(None, max_length=20)
    cnae_secondary: Optional[list[str]] = None
    state_registration: Optional[str] = Field(None, max_length=50)
    municipal_registration: Optional[str] = Field(None, max_length=50)

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = Field(None, max_length=2)
    address_zipcode: Optional[str] = Field(None, pattern=r"^\d{5}-?\d{3}$")

    # Atribuição
    assigned_to: Optional[int] = None


class ClientUpdate(BaseModel):
    """Schema para atualizar Client"""
    name: Optional[str] = Field(None, min_length=3, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[int] = None

    # Dados PJ
    company_name: Optional[str] = None
    trade_name: Optional[str] = None
    cnae_primary: Optional[str] = None
    cnae_secondary: Optional[list[str]] = None
    state_registration: Optional[str] = None
    municipal_registration: Optional[str] = None

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zipcode: Optional[str] = None


class ClientResponse(ClientBase):
    """Schema para resposta de Client"""
    id: int
    status: str

    # Dados PJ
    company_name: Optional[str] = None
    trade_name: Optional[str] = None
    cnae_primary: Optional[str] = None
    cnae_secondary: Optional[list[str]] = None
    state_registration: Optional[str] = None
    municipal_registration: Optional[str] = None

    # Endereço
    address_street: Optional[str] = None
    address_number: Optional[str] = None
    address_complement: Optional[str] = None
    address_neighborhood: Optional[str] = None
    address_city: Optional[str] = None
    address_state: Optional[str] = None
    address_zipcode: Optional[str] = None

    # Relacionamento
    assigned_to: Optional[int] = None

    # Datas
    created_at: datetime
    updated_at: datetime
    activated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    """Schema para lista de Clients"""
    clients: list[ClientResponse]
    total: int
    page: int
    per_page: int
