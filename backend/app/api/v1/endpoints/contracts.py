"""
Endpoints para Agente de Contratos
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.core.deps import get_current_tenant_user, get_db
from app.agents.contracts_agent import ContractsAgent


router = APIRouter()


# Schemas
class ActListResponse(BaseModel):
    """Resposta com lista de atos"""
    id: str
    nome: str
    descricao: str
    prazo: str
    documentos: int


class ActDetailsResponse(BaseModel):
    """Detalhes completos de um ato"""
    nome: str
    descricao: str
    campos_necessarios: List[str]
    documentos_necessarios: List[str]
    prazo_medio: str
    orgaos: List[str]


class GenerateClauseRequest(BaseModel):
    """Request para gerar cláusula"""
    act_type: str
    data: dict


class GenerateClauseResponse(BaseModel):
    """Resposta com cláusula gerada"""
    success: bool
    clause: Optional[str] = None
    act_type: Optional[str] = None
    generated_at: Optional[str] = None
    error: Optional[str] = None


class ChecklistResponse(BaseModel):
    """Resposta com checklist de documentos"""
    success: bool
    act: Optional[str] = None
    documents: Optional[List[dict]] = None
    data_fields: Optional[List[str]] = None
    estimated_timeline: Optional[str] = None
    agencies: Optional[List[str]] = None
    error: Optional[str] = None


class AnalyzeDocumentResponse(BaseModel):
    """Resposta da análise de documento"""
    success: bool
    analysis: Optional[str] = None
    extracted_at: Optional[str] = None
    error: Optional[str] = None


class ValidateCompanyRequest(BaseModel):
    """Request para validar dados da empresa"""
    company_id: int
    act_type: str


class ValidateCompanyResponse(BaseModel):
    """Resposta da validação"""
    valid: bool
    company_id: Optional[int] = None
    act_type: Optional[str] = None
    missing_data: Optional[List[str]] = None
    missing_documents: Optional[List[str]] = None
    ready_to_generate: Optional[bool] = None
    error: Optional[str] = None


# Endpoints
@router.get("/acts", response_model=List[ActListResponse])
async def list_acts(
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Lista todos os atos disponíveis
    """
    user_dict, tenant = user_tenant
    agent = ContractsAgent()
    acts = agent.get_available_acts()
    return acts


@router.get("/acts/{act_id}", response_model=ActDetailsResponse)
async def get_act_details(
    act_id: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Obtém detalhes de um ato específico
    """
    user_dict, tenant = user_tenant
    agent = ContractsAgent()
    act_details = agent.get_act_details(act_id)

    if not act_details:
        raise HTTPException(status_code=404, detail="Ato não encontrado")

    return act_details


@router.post("/generate-clause", response_model=GenerateClauseResponse)
async def generate_clause(
    request: GenerateClauseRequest,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Gera cláusula contratual baseada em template
    """
    user_dict, tenant = user_tenant
    agent = ContractsAgent()
    result = await agent.generate_contract_clause(
        act_type=request.act_type,
        data=request.data
    )
    return result


@router.post("/analyze-document", response_model=AnalyzeDocumentResponse)
async def analyze_document(
    file: UploadFile = File(...),
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Analisa documento enviado e extrai informações
    """
    user_dict, tenant = user_tenant
    try:
        # Ler conteúdo do arquivo
        content = await file.read()
        text = content.decode('utf-8', errors='ignore')

        # Analisar com agente
        agent = ContractsAgent()
        result = await agent.analyze_contract_document(text)

        return result
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@router.get("/checklist/{act_type}", response_model=ChecklistResponse)
async def get_checklist(
    act_type: str,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Gera checklist de documentos necessários para um ato
    """
    user_dict, tenant = user_tenant
    agent = ContractsAgent()
    checklist = agent.generate_document_checklist(act_type)
    return checklist


@router.post("/validate-company", response_model=ValidateCompanyResponse)
async def validate_company(
    request: ValidateCompanyRequest,
    user_tenant: tuple = Depends(get_current_tenant_user),
    db: Session = Depends(get_db)
):
    """
    Valida se empresa tem dados suficientes para gerar o ato
    """
    user_dict, tenant = user_tenant
    agent = ContractsAgent()
    result = await agent.validate_company_data(
        company_id=request.company_id,
        act_type=request.act_type
    )
    return result
