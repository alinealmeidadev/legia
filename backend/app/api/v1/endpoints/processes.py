"""
LEGIA PLATFORM - Rotas de Processos (Tenant)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.deps import get_db, get_current_tenant_user
from app.services.process_service import ProcessService
from app.schemas.process import (
    ProcessCreate,
    ProcessUpdate,
    ProcessResponse,
    ProcessListResponse,
    ProcessStatsResponse
)


router = APIRouter()


@router.get("/", response_model=ProcessListResponse)
def list_processes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    status: Optional[str] = Query(None),
    process_type: Optional[str] = Query(None),
    client_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Lista processos do tenant

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    processes, total = ProcessService.get_all(
        db=db,
        tenant_id=tenant.id,
        skip=skip,
        limit=limit,
        status=status,
        process_type=process_type,
        client_id=client_id
    )

    return ProcessListResponse(
        processes=processes,
        total=total,
        page=skip // limit + 1 if limit > 0 else 1,
        per_page=limit
    )


@router.post("/", response_model=ProcessResponse, status_code=status.HTTP_201_CREATED)
def create_process(
    process: ProcessCreate,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Cria um novo processo

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    new_process = ProcessService.create(
        db=db,
        process_data=process,
        tenant_id=tenant.id,
        user_id=user_dict["id"]
    )

    return ProcessResponse(**new_process)


@router.get("/stats", response_model=ProcessStatsResponse)
def get_process_stats(
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Retorna estatísticas dos processos

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    stats = ProcessService.get_stats(db=db, tenant_id=tenant.id)

    return stats


@router.get("/{process_id}", response_model=ProcessResponse)
def get_process(
    process_id: int,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Busca processo por ID

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    process = ProcessService.get_by_id(
        db=db,
        process_id=process_id,
        tenant_id=tenant.id
    )

    if not process:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processo não encontrado"
        )

    return ProcessResponse(**process)


@router.patch("/{process_id}", response_model=ProcessResponse)
def update_process(
    process_id: int,
    process: ProcessUpdate,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Atualiza um processo

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    updated_process = ProcessService.update(
        db=db,
        process_id=process_id,
        process_data=process,
        tenant_id=tenant.id
    )

    return ProcessResponse(**updated_process)


@router.delete("/{process_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_process(
    process_id: int,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Deleta um processo

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    ProcessService.delete(
        db=db,
        process_id=process_id,
        tenant_id=tenant.id
    )

    return None
