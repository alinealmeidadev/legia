"""
LEGIA PLATFORM - Rotas de Agentes IA
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Dict

from app.core.deps import get_current_tenant_user
from app.agents import OrchestratorAgent


router = APIRouter()


class ChatMessage(BaseModel):
    """Schema para mensagem de chat"""
    message: str
    context: Optional[Dict] = None


class ChatResponse(BaseModel):
    """Schema para resposta de chat"""
    response: str
    agent: str
    intent: str
    action: Optional[str] = None
    confidence: float
    metadata: Dict


@router.post("/chat", response_model=ChatResponse)
async def chat_with_orchestrator(
    chat_message: ChatMessage,
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Endpoint de chat com o Orquestrador

    **Acesso:** Usuário do tenant autenticado
    """
    user_dict, tenant = user_tenant

    # Criar instância do orquestrador
    orchestrator = OrchestratorAgent()

    # Adicionar informações do tenant e usuário ao contexto
    context = chat_message.context or {}
    context.update({
        "tenant_id": tenant.id,
        "tenant_name": tenant.name,
        "user_id": user_dict["id"],
        "user_name": user_dict.get("name", "Usuário")
    })

    # Processar mensagem
    result = await orchestrator.process(
        message=chat_message.message,
        context=context
    )

    return ChatResponse(**result)


@router.get("/agents/status")
async def get_agents_status(
    user_tenant: tuple = Depends(get_current_tenant_user)
):
    """
    Retorna status de todos os agentes

    **Acesso:** Usuário do tenant autenticado
    """
    orchestrator = OrchestratorAgent()

    return {
        "orchestrator": orchestrator.get_info(),
        "available_agents": orchestrator.available_agents,
        "status": "operational"
    }
