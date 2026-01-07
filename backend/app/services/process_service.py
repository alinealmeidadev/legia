"""
LEGIA PLATFORM - Service de Processos
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from fastapi import HTTPException, status

from app.utils.tenant_schema import validate_schema_name
from app.schemas.process import (
    ProcessCreate,
    ProcessUpdate,
    ProcessStatsResponse
)


class ProcessService:
    """Service para operações de processos"""

    @staticmethod
    def get_by_id(
        db: Session,
        process_id: int,
        tenant_id: int
    ) -> Optional[dict]:
        """
        Busca processo por ID
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        result = db.execute(
            text(f"""
                SELECT p.*, c.name as client_name, c.document as client_document
                FROM {schema_name}.processes p
                LEFT JOIN {schema_name}.clients c ON p.client_id = c.id
                WHERE p.id = :process_id
            """),
            {"process_id": process_id}
        )

        row = result.fetchone()
        if not row:
            return None

        return dict(row._mapping)

    @staticmethod
    def get_all(
        db: Session,
        tenant_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        process_type: Optional[str] = None,
        client_id: Optional[int] = None
    ) -> tuple[List[dict], int]:
        """
        Lista processos com filtros
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        # Construir WHERE clause
        where_clauses = []
        params = {"skip": skip, "limit": limit}

        if status:
            where_clauses.append("p.status = :status")
            params["status"] = status

        if process_type:
            where_clauses.append("p.process_type = :process_type")
            params["process_type"] = process_type

        if client_id:
            where_clauses.append("p.client_id = :client_id")
            params["client_id"] = client_id

        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""

        # Buscar processos
        result = db.execute(
            text(f"""
                SELECT p.*, c.name as client_name, c.document as client_document
                FROM {schema_name}.processes p
                LEFT JOIN {schema_name}.clients c ON p.client_id = c.id
                {where_clause}
                ORDER BY p.created_at DESC
                LIMIT :limit OFFSET :skip
            """),
            params
        )

        processes = [dict(row._mapping) for row in result.fetchall()]

        # Contar total
        count_result = db.execute(
            text(f"""
                SELECT COUNT(*) as total
                FROM {schema_name}.processes p
                {where_clause}
            """),
            {k: v for k, v in params.items() if k not in ["skip", "limit"]}
        )

        total = count_result.scalar()

        return processes, total

    @staticmethod
    def create(
        db: Session,
        process_data: ProcessCreate,
        tenant_id: int,
        user_id: Optional[int] = None
    ) -> dict:
        """
        Cria novo processo
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        # Verificar se cliente existe
        client_result = db.execute(
            text(f"SELECT id FROM {schema_name}.clients WHERE id = :client_id"),
            {"client_id": process_data.client_id}
        )

        if not client_result.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente não encontrado"
            )

        # Preparar alteration_types se existir
        import json
        alteration_types_json = None
        if process_data.alteration_types:
            alteration_types_json = json.dumps(process_data.alteration_types)

        # Criar processo
        result = db.execute(
            text(f"""
                INSERT INTO {schema_name}.processes (
                    client_id, process_type, title, description,
                    priority, estimated_days, status, assigned_to, created_by, alteration_types
                )
                VALUES (
                    :client_id, :process_type, :title, :description,
                    :priority, :estimated_days, :status, :assigned_to, :created_by, :alteration_types::jsonb
                )
                RETURNING id, client_id, process_type, title, description,
                          priority, estimated_days, status, assigned_to, created_by,
                          alteration_types, created_at, updated_at, started_at, completed_at
            """),
            {
                "client_id": process_data.client_id,
                "process_type": process_data.process_type,
                "title": process_data.title,
                "description": process_data.description,
                "priority": process_data.priority or "normal",
                "estimated_days": process_data.estimated_days or 30,
                "status": process_data.status or "aguardando",
                "assigned_to": process_data.assigned_to,
                "created_by": user_id,
                "alteration_types": alteration_types_json
            }
        )

        row = result.fetchone()
        process_dict = dict(row._mapping)

        db.commit()

        # Buscar nome do cliente
        client_info = db.execute(
            text(f"SELECT name, document FROM {schema_name}.clients WHERE id = :client_id"),
            {"client_id": process_data.client_id}
        ).fetchone()

        if client_info:
            process_dict["client_name"] = client_info[0]
            process_dict["client_document"] = client_info[1]

        return process_dict

    @staticmethod
    def update(
        db: Session,
        process_id: int,
        process_data: ProcessUpdate,
        tenant_id: int
    ) -> dict:
        """
        Atualiza processo
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        # Verificar se processo existe
        existing = db.execute(
            text(f"SELECT id FROM {schema_name}.processes WHERE id = :process_id"),
            {"process_id": process_id}
        ).fetchone()

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Processo não encontrado"
            )

        # Construir SET clause
        update_fields = []
        params = {"process_id": process_id}

        if process_data.title is not None:
            update_fields.append("title = :title")
            params["title"] = process_data.title

        if process_data.description is not None:
            update_fields.append("description = :description")
            params["description"] = process_data.description

        if process_data.status is not None:
            update_fields.append("status = :status")
            params["status"] = process_data.status

            # Atualizar datas baseado no status
            if process_data.status == "em_andamento":
                update_fields.append("started_at = CURRENT_TIMESTAMP")
            elif process_data.status == "concluido":
                update_fields.append("completed_at = CURRENT_TIMESTAMP")

        if process_data.priority is not None:
            update_fields.append("priority = :priority")
            params["priority"] = process_data.priority

        if process_data.estimated_days is not None:
            update_fields.append("estimated_days = :estimated_days")
            params["estimated_days"] = process_data.estimated_days

        if process_data.assigned_to is not None:
            update_fields.append("assigned_to = :assigned_to")
            params["assigned_to"] = process_data.assigned_to

        if process_data.client_id is not None:
            update_fields.append("client_id = :client_id")
            params["client_id"] = process_data.client_id

        if process_data.process_type is not None:
            update_fields.append("process_type = :process_type")
            params["process_type"] = process_data.process_type

        if process_data.alteration_types is not None:
            import json
            update_fields.append("alteration_types = :alteration_types::jsonb")
            params["alteration_types"] = json.dumps(process_data.alteration_types)

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Nenhum campo para atualizar"
            )

        set_clause = ", ".join(update_fields)

        # Atualizar
        result = db.execute(
            text(f"""
                UPDATE {schema_name}.processes
                SET {set_clause}
                WHERE id = :process_id
                RETURNING id, client_id, process_type, title, description,
                          priority, estimated_days, status, assigned_to, created_by,
                          alteration_types, created_at, updated_at, started_at, completed_at
            """),
            params
        )

        row = result.fetchone()
        process_dict = dict(row._mapping)

        db.commit()

        # Buscar nome do cliente
        client_info = db.execute(
            text(f"SELECT name, document FROM {schema_name}.clients WHERE id = :client_id"),
            {"client_id": process_dict["client_id"]}
        ).fetchone()

        if client_info:
            process_dict["client_name"] = client_info[0]
            process_dict["client_document"] = client_info[1]

        return process_dict

    @staticmethod
    def delete(
        db: Session,
        process_id: int,
        tenant_id: int
    ) -> bool:
        """
        Deleta processo
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        # Verificar se existe
        existing = db.execute(
            text(f"SELECT id FROM {schema_name}.processes WHERE id = :process_id"),
            {"process_id": process_id}
        ).fetchone()

        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Processo não encontrado"
            )

        # Deletar
        db.execute(
            text(f"DELETE FROM {schema_name}.processes WHERE id = :process_id"),
            {"process_id": process_id}
        )

        db.commit()
        return True

    @staticmethod
    def get_stats(
        db: Session,
        tenant_id: int
    ) -> ProcessStatsResponse:
        """
        Retorna estatísticas de processos
        """
        schema_name = validate_schema_name(f"tenant_{tenant_id}")

        result = db.execute(
            text(f"""
                SELECT
                    COUNT(*) as total,
                    COUNT(*) FILTER (WHERE status = 'aguardando') as aguardando,
                    COUNT(*) FILTER (WHERE status = 'em_andamento') as em_andamento,
                    COUNT(*) FILTER (WHERE status = 'concluido') as concluido,
                    COUNT(*) FILTER (WHERE status = 'cancelado') as cancelado,
                    COUNT(*) FILTER (WHERE priority = 'alta') as alta_prioridade,
                    AVG(
                        CASE
                            WHEN completed_at IS NOT NULL AND started_at IS NOT NULL
                            THEN EXTRACT(DAY FROM (completed_at - started_at))
                            ELSE NULL
                        END
                    ) as tempo_medio_dias
                FROM {schema_name}.processes
            """)
        )

        row = result.fetchone()

        return ProcessStatsResponse(
            total=row[0] or 0,
            aguardando=row[1] or 0,
            em_andamento=row[2] or 0,
            concluido=row[3] or 0,
            cancelado=row[4] or 0,
            alta_prioridade=row[5] or 0,
            tempo_medio_dias=float(row[6]) if row[6] else None
        )
