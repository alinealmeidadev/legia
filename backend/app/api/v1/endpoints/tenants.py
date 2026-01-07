"""
LEGIA PLATFORM - Rotas de Tenants (Super Admin)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import get_db, get_current_active_superadmin
from app.models.public.legia_user import LegiaUser
from app.models.public.tenant import Tenant
from app.models.public.plan import Plan
from app.schemas.tenant import (
    TenantCreate,
    TenantUpdate,
    TenantResponse,
    TenantListResponse,
    TenantStats
)
from app.utils.tenant_schema import create_tenant_schema


router = APIRouter()


@router.get("/", response_model=TenantListResponse)
def list_tenants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: str = Query(None),
    search: str = Query(None),
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Lista todos os tenants

    **Acesso:** Super Admin apenas
    """
    query = db.query(Tenant)

    # Filtros
    if status:
        query = query.filter(Tenant.status == status)

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Tenant.name.ilike(search_term)) |
            (Tenant.email.ilike(search_term)) |
            (Tenant.cnpj.ilike(search_term))
        )

    total = query.count()
    tenants = query.offset(skip).limit(limit).all()

    return TenantListResponse(
        tenants=tenants,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Busca tenant por ID

    **Acesso:** Super Admin apenas
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )

    return tenant


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Cria novo tenant

    **Acesso:** Super Admin apenas
    """
    # Verificar se CNPJ já existe
    existing = db.query(Tenant).filter(Tenant.cnpj == tenant_data.cnpj).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já cadastrado"
        )

    # Verificar se subdomínio já existe
    existing_sub = db.query(Tenant).filter(
        Tenant.subdomain == tenant_data.subdomain
    ).first()
    if existing_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subdomínio já está em uso"
        )

    # Verificar se plano existe
    plan = db.query(Plan).filter(Plan.id == tenant_data.plan_id).first()
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plano não encontrado"
        )

    # Criar tenant
    tenant = Tenant(**tenant_data.model_dump())
    db.add(tenant)
    db.flush()

    # Criar schema do tenant
    if not create_tenant_schema(tenant.id, db):
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar schema do tenant"
        )

    db.commit()
    db.refresh(tenant)

    return tenant


@router.patch("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: int,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Atualiza tenant

    **Acesso:** Super Admin apenas
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )

    # Atualizar campos
    update_data = tenant_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(tenant, field, value)

    db.commit()
    db.refresh(tenant)

    return tenant


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Remove tenant (soft delete - marca como cancelado)

    **Acesso:** Super Admin apenas
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )

    # Soft delete
    from datetime import datetime, timezone
    tenant.status = "canceled"
    tenant.canceled_at = datetime.now(timezone.utc)

    db.commit()

    return None


@router.get("/{tenant_id}/stats", response_model=TenantStats)
def get_tenant_stats(
    tenant_id: int,
    db: Session = Depends(get_db),
    current_user: LegiaUser = Depends(get_current_active_superadmin)
):
    """
    Estatísticas do tenant

    **Acesso:** Super Admin apenas
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()

    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant não encontrado"
        )

    # TODO: Implementar queries para estatísticas reais
    # Por enquanto retorna dados mockados

    return TenantStats(
        total_clients=0,
        active_clients=0,
        total_processes=0,
        active_processes=0,
        total_documents=0,
        storage_used_mb=0.0
    )
