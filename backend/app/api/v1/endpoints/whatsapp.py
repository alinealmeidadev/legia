"""
LEGIA PLATFORM - Endpoints WhatsApp Integration
Integração com WhatsApp Business API para atendimento
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel

from app.db.session import get_db
from app.core.auth import get_current_user
from app.models.tenant.user import User

router = APIRouter()


class WhatsAppWebhookPayload(BaseModel):
    """Payload do webhook do WhatsApp"""
    object: str
    entry: list


class WhatsAppMessage(BaseModel):
    """Mensagem WhatsApp para enviar"""
    to: str
    message: str
    client_number: int | None = None


@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Webhook para receber mensagens do WhatsApp

    Este endpoint é chamado pelo WhatsApp Business API quando:
    - Cliente envia mensagem
    - Mensagem é entregue
    - Mensagem é lida
    """
    try:
        payload = await request.json()

        # Verificar se é uma mensagem
        if payload.get('object') == 'whatsapp_business_account':
            for entry in payload.get('entry', []):
                for change in entry.get('changes', []):
                    if change.get('field') == 'messages':
                        messages = change.get('value', {}).get('messages', [])

                        for message in messages:
                            # Processar mensagem
                            await process_incoming_message(message, db)

        return {"status": "success"}

    except Exception as e:
        print(f"Erro no webhook WhatsApp: {e}")
        return {"status": "error", "message": str(e)}


async def process_incoming_message(message: Dict[str, Any], db: Session):
    """
    Processa mensagem recebida do WhatsApp

    Fluxo:
    1. Identificar cliente pelo número
    2. Buscar histórico do cliente
    3. Enviar para Agente de Atendimento (IA)
    4. Responder automaticamente
    """
    from_number = message.get('from')
    message_type = message.get('type')

    if message_type == 'text':
        text = message.get('text', {}).get('body', '')

        # TODO: Identificar cliente pelo número
        # TODO: Buscar contexto (processos ativos, histórico)
        # TODO: Enviar para Agente IA
        # TODO: Enviar resposta

        print(f"📱 Mensagem de {from_number}: {text}")


@router.get("/webhook")
async def whatsapp_webhook_verify(request: Request):
    """
    Verificação do webhook (Meta requer isso)
    """
    mode = request.query_params.get('hub.mode')
    token = request.query_params.get('hub.verify_token')
    challenge = request.query_params.get('hub.challenge')

    # Token de verificação (configurar no .env)
    VERIFY_TOKEN = "LEGIA_WEBHOOK_2025"

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Token inválido")


@router.post("/send")
async def send_whatsapp_message(
    message: WhatsAppMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Envia mensagem via WhatsApp

    Requer:
    - WhatsApp Business API configurado
    - Token de acesso válido
    """
    try:
        # TODO: Implementar envio via WhatsApp Business API
        # import requests
        # url = "https://graph.facebook.com/v18.0/PHONE_NUMBER_ID/messages"
        # headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}
        # data = {
        #     "messaging_product": "whatsapp",
        #     "to": message.to,
        #     "text": {"body": message.message}
        # }
        # response = requests.post(url, headers=headers, json=data)

        return {
            "status": "sent",
            "message": "Funcionalidade em desenvolvimento",
            "to": message.to
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/templates")
async def get_whatsapp_templates(
    current_user: User = Depends(get_current_user)
):
    """
    Lista templates de mensagem aprovados
    """
    templates = [
        {
            "id": 1,
            "name": "bem_vindo",
            "text": "Olá! Bem-vindo à LEGIA. Como posso ajudar?"
        },
        {
            "id": 2,
            "name": "processo_criado",
            "text": "Seu processo #{process_id} foi criado com sucesso!"
        },
        {
            "id": 3,
            "name": "documentos_pendentes",
            "text": "Olá! Identificamos que faltam documentos para seu processo. Acesse: {link}"
        }
    ]

    return {"templates": templates}


@router.post("/client/{client_number}/notify")
async def notify_client_whatsapp(
    client_number: int,
    message: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Notifica cliente específico via WhatsApp
    """
    # TODO: Buscar número do cliente no banco
    # TODO: Enviar mensagem

    return {
        "status": "sent",
        "client_number": client_number,
        "message": "Notificação enviada (desenvolvimento)"
    }
