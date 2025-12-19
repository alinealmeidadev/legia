"""
Endpoints para Workflows Automatizados
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.deps import get_current_tenant_user, get_db
from app.agents.workflow_engine import workflow_engine


router = APIRouter()


# Schemas
class CreateWorkflowRequest(BaseModel):
    """Request para criar workflow"""
    workflow_type: str
    client_id: int
    initial_data: dict = {}


class AdvanceStageRequest(BaseModel):
    """Request para avançar estágio"""
    completion_data: Optional[dict] = None


class WorkflowResponse(BaseModel):
    """Resposta com dados do workflow"""
    id: str
    type: str
    client_id: int
    tenant_id: int
    current_stage: str
    stages: List[dict]
    data: dict
    forms: List[dict]
    documents: List[dict]
    history: List[dict]
    status: str
    created_at: str
    updated_at: str


class FormSubmitRequest(BaseModel):
    """Request para submeter formulário"""
    form_id: str
    responses: dict


# Endpoints
@router.post("/", response_model=WorkflowResponse)
def create_workflow(
    request: CreateWorkflowRequest,
    user_tenant: tuple = Depends(get_current_tenant_user),
    db: Session = Depends(get_db)
):
    """
    Cria novo workflow automatizado

    Este endpoint inicia um workflow que coordena múltiplos agentes
    para executar um processo completo automaticamente.
    """
    user_dict, tenant = user_tenant

    # Criar workflow
    workflow = workflow_engine.create_workflow(
        workflow_type=request.workflow_type,
        client_id=request.client_id,
        tenant_id=tenant.id,
        initial_data=request.initial_data
    )

    return workflow


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(
    workflow_id: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Retorna dados de um workflow
    """
    user_dict, tenant = user_tenant

    workflow = workflow_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    # Verificar se pertence ao tenant
    if workflow["tenant_id"] != tenant.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return workflow


@router.post("/{workflow_id}/advance", response_model=WorkflowResponse)
def advance_workflow_stage(
    workflow_id: str,
    request: AdvanceStageRequest,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Avança workflow para próximo estágio
    """
    user_dict, tenant = user_tenant

    workflow = workflow_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    if workflow["tenant_id"] != tenant.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Avançar estágio
    updated_workflow = workflow_engine.advance_stage(
        workflow_id,
        request.completion_data
    )

    return updated_workflow


@router.post("/{workflow_id}/forms/submit")
def submit_form(
    workflow_id: str,
    request: FormSubmitRequest,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Submete respostas de formulário do cliente
    """
    user_dict, tenant = user_tenant

    workflow = workflow_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    if workflow["tenant_id"] != tenant.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    # Atualizar dados do workflow
    if "form_responses" not in workflow["data"]:
        workflow["data"]["form_responses"] = {}

    workflow["data"]["form_responses"].update(request.responses)
    workflow_engine.update_workflow_data(workflow_id, workflow["data"])

    # Marcar formulário como completo
    from datetime import datetime
    for form in workflow["forms"]:
        if form["id"] == request.form_id:
            form["status"] = "completed"
            form["responses"] = request.responses
            form["completed_at"] = datetime.now().isoformat()

    return {
        "success": True,
        "message": "Formulário submetido com sucesso",
        "workflow_id": workflow_id
    }


@router.get("/{workflow_id}/forms/latest")
def get_latest_form(
    workflow_id: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Retorna último formulário gerado para o cliente
    """
    user_dict, tenant = user_tenant

    workflow = workflow_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    if workflow["tenant_id"] != tenant.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    if not workflow["forms"]:
        raise HTTPException(status_code=404, detail="Nenhum formulário encontrado")

    # Retornar último formulário pendente
    for form in reversed(workflow["forms"]):
        if form["status"] == "pending":
            return form

    # Se não houver pendente, retornar o último
    return workflow["forms"][-1]


@router.get("/{workflow_id}/documents")
def get_documents_checklist(
    workflow_id: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Retorna checklist de documentos necessários
    """
    user_dict, tenant = user_tenant

    workflow = workflow_engine.get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow não encontrado")

    if workflow["tenant_id"] != tenant.id:
        raise HTTPException(status_code=403, detail="Acesso negado")

    return {
        "workflow_id": workflow_id,
        "documents": workflow["documents"],
        "total": len(workflow["documents"]),
        "pending": len([d for d in workflow["documents"] if d["status"] == "pending"]),
        "completed": len([d for d in workflow["documents"] if d["status"] == "completed"])
    }


@router.get("/")
def list_workflows(
    status: Optional[str] = None,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Lista todos os workflows do tenant
    """
    user_dict, tenant = user_tenant

    # Filtrar workflows do tenant
    tenant_workflows = [
        w for w in workflow_engine.workflows.values()
        if w["tenant_id"] == tenant.id
    ]

    # Filtrar por status se especificado
    if status:
        tenant_workflows = [w for w in tenant_workflows if w["status"] == status]

    return {
        "workflows": tenant_workflows,
        "total": len(tenant_workflows)
    }
