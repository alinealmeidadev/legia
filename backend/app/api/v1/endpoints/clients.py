"""
LEGIA PLATFORM - Rotas de Clientes (Tenant)
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List, Dict, Any

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


@router.get("/utils/consultar-cnpj/{cnpj}")
async def consultar_cnpj(
    cnpj: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Consulta dados do CNPJ na Receita Federal (ReceitaWS)

    **Acesso:** Usuário do tenant autenticado
    """
    from app.services.receita_service import ReceitaService

    try:
        dados = await ReceitaService.consultar_cnpj(cnpj)

        if not dados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CNPJ não encontrado"
            )

        return {
            "success": True,
            "data": dados
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/utils/consultar-cep/{cep}")
async def consultar_cep(
    cep: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Consulta endereço pelo CEP via ViaCEP

    **Acesso:** Usuário do tenant autenticado
    """
    from app.services.cep_service import CEPService

    try:
        dados = await CEPService.consultar_cep(cep)

        if not dados:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="CEP não encontrado"
            )

        return {
            "success": True,
            "data": dados
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/utils/validar-documento/{documento}")
def validar_documento(
    documento: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Valida CPF ou CNPJ

    **Acesso:** Usuário do tenant autenticado
    """
    from app.utils.validators import validar_cpf, validar_cnpj

    # Limpar documento
    doc_limpo = ''.join(filter(str.isdigit, documento))

    # Determinar tipo baseado no tamanho
    if len(doc_limpo) == 11:
        valido = validar_cpf(doc_limpo)
        tipo = "CPF"
    elif len(doc_limpo) == 14:
        valido = validar_cnpj(doc_limpo)
        tipo = "CNPJ"
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos"
        )

    return {
        "success": True,
        "valido": valido,
        "tipo": tipo,
        "documento": documento
    }


@router.get("/utils/template-excel")
def baixar_template_excel(
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Baixa template Excel para importação em lote de clientes

    **Acesso:** Usuário do tenant autenticado
    """
    from app.services.excel_service import ExcelService

    excel_bytes = ExcelService.gerar_template_excel()

    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition": "attachment; filename=template_importacao_clientes.xlsx"
        }
    )


@router.post("/utils/importar-excel")
async def importar_excel(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Processa importação em lote de clientes via Excel

    **Acesso:** Usuário do tenant autenticado
    """
    from app.services.excel_service import ExcelService

    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    # Verificar tipo de arquivo
    if not arquivo.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo deve ser Excel (.xlsx ou .xls)"
        )

    try:
        # Ler arquivo
        arquivo_bytes = await arquivo.read()

        # Processar Excel
        resultado = await ExcelService.processar_excel(arquivo_bytes, schema_name)

        if not resultado["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado.get("error", "Erro ao processar Excel")
            )

        # Retornar preview (não insere no banco ainda)
        return {
            "success": True,
            "total_linhas": resultado["total_linhas"],
            "total_validos": resultado["total_validos"],
            "total_erros": resultado["total_erros"],
            "clientes": resultado["clientes_validos"],
            "erros": resultado["erros"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )


@router.post("/utils/confirmar-importacao")
def confirmar_importacao(
    clientes: List[Dict],
    db: Session = Depends(get_db),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Confirma importação e insere clientes no banco

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant
    schema_name = tenant.schema_name

    try:
        inseridos = 0
        erros = []

        for item in clientes:
            try:
                dados = item.get("dados", {})

                # Verificar se documento já existe
                existing = db.execute(
                    text(f"SELECT id FROM {schema_name}.clients WHERE document = :document"),
                    {"document": dados.get("document")}
                ).fetchone()

                if existing:
                    erros.append({
                        "linha": item.get("linha"),
                        "erro": f"Documento {dados.get('document')} já cadastrado"
                    })
                    continue

                # Preparar dados (remover None)
                data = {k: v for k, v in dados.items() if v is not None}

                columns = ", ".join(data.keys())
                placeholders = ", ".join([f":{k}" for k in data.keys()])

                # Inserir cliente
                db.execute(
                    text(f"""
                        INSERT INTO {schema_name}.clients ({columns})
                        VALUES ({placeholders})
                    """),
                    data
                )

                inseridos += 1

            except Exception as e:
                erros.append({
                    "linha": item.get("linha"),
                    "erro": str(e)
                })

        db.commit()

        return {
            "success": True,
            "inseridos": inseridos,
            "total_erros": len(erros),
            "erros": erros
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao importar clientes: {str(e)}"
        )
