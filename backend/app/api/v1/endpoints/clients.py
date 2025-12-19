"""
LEGIA PLATFORM - Rotas de Clientes (Tenant)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional

from app.core.deps import get_db, get_current_tenant_user
from app.models.public.tenant import Tenant
from app.schemas.client import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientListResponse
)


router = APIRouter()


@router.get("/", response_model=ClientListResponse)
def list_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Lista clientes do tenant

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    # Montar query
    where_clauses = []
    params = {"skip": skip, "limit": limit}

    if status:
        where_clauses.append("status = :status")
        params["status"] = status

    if search:
        where_clauses.append(
            "(name ILIKE :search OR document ILIKE :search OR email ILIKE :search)"
        )
        params["search"] = f"%{search}%"

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Contar total
    count_result = db.execute(
        text(f"SELECT COUNT(*) FROM {schema_name}.clients WHERE {where_sql}"),
        params
    )
    total = count_result.scalar()

    # Buscar clientes
    result = db.execute(
        text(f"""
            SELECT * FROM {schema_name}.clients
            WHERE {where_sql}
            ORDER BY created_at DESC
            OFFSET :skip LIMIT :limit
        """),
        params
    )

    clients = [dict(row._mapping) for row in result.fetchall()]

    return ClientListResponse(
        clients=clients,
        total=total,
        page=skip // limit + 1,
        per_page=limit
    )


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(
    client_id: int,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Busca cliente por ID

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    result = db.execute(
        text(f"SELECT * FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    )

    client = result.fetchone()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return dict(client._mapping)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Cria novo cliente

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    # Verificar se documento já existe
    existing = db.execute(
        text(f"SELECT id FROM {schema_name}.clients WHERE document = :document"),
        {"document": client_data.document}
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente com este documento já cadastrado"
        )

    # Preparar dados
    data = client_data.model_dump()
    columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{k}" for k in data.keys()])

    # Inserir cliente
    result = db.execute(
        text(f"""
            INSERT INTO {schema_name}.clients ({columns})
            VALUES ({placeholders})
            RETURNING id
        """),
        data
    )

    client_id = result.scalar()
    db.commit()

    # Buscar cliente criado
    result = db.execute(
        text(f"SELECT * FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    )

    return dict(result.fetchone()._mapping)


@router.patch("/{client_id}")
def update_client(
    client_id: int,
    client_data: ClientUpdate,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Atualiza cliente

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    # Verificar se existe
    existing = db.execute(
        text(f"SELECT id FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    ).fetchone()

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    # Preparar dados de atualização
    update_data = client_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nenhum campo para atualizar"
        )

    # Montar SET clause
    set_clauses = [f"{k} = :{k}" for k in update_data.keys()]
    set_sql = ", ".join(set_clauses)
    update_data["client_id"] = client_id
    update_data["updated_at"] = "NOW()"

    # Atualizar
    db.execute(
        text(f"""
            UPDATE {schema_name}.clients
            SET {set_sql}, updated_at = NOW()
            WHERE id = :client_id
        """),
        update_data
    )
    db.commit()

    # Buscar cliente atualizado
    result = db.execute(
        text(f"SELECT * FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    )

    return dict(result.fetchone()._mapping)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Remove cliente

    **Acesso:** Admin do tenant apenas
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    # Verificar se é admin
    if user_dict.get('role') != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem excluir clientes"
        )

    # Verificar se existe
    existing = db.execute(
        text(f"SELECT id FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    ).fetchone()

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    # Deletar
    db.execute(
        text(f"DELETE FROM {schema_name}.clients WHERE id = :client_id"),
        {"client_id": client_id}
    )
    db.commit()

    return None
