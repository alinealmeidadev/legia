"""
LEGIA PLATFORM - Modelo ChatMessage (Mensagem de Chat)
Schema: tenant_XXX
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class ChatMessage(Base):
    """
    Modelo ChatMessage - Representa uma mensagem de chat

    Usado para comunicação com os agentes IA e clientes
    """

    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)

    # Conversa
    conversation_id = Column(UUID(as_uuid=True), nullable=False, index=True,
                            default=uuid.uuid4,
                            comment="ID da conversa (agrupa mensagens)")

    # Participantes
    sender_type = Column(String(20), nullable=False,
                        comment="Tipo: user, agent, client")
    sender_id = Column(Integer, nullable=True,
                      comment="ID do remetente")
    sender_name = Column(String(255), nullable=True,
                        comment="Nome do remetente")

    # Mensagem
    message = Column(Text, nullable=False,
                    comment="Conteúdo da mensagem")

    # Agente IA (se aplicável)
    agent_name = Column(String(100), nullable=True,
                       comment="Nome do agente IA")
    # Ex: "Orquestrador", "Agente Comercial", "Assistente ao Cliente"

    # Dados estruturados (se houver)
    data = Column(JSON, default={},
                 comment="Dados estruturados adicionais")

    # Timestamp
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       index=True)

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<ChatMessage {self.id}: {self.sender_type} - {self.agent_name or 'N/A'}>"

    @property
    def is_from_agent(self) -> bool:
        """Verifica se a mensagem é de um agente IA"""
        return self.sender_type == "agent"

    @property
    def is_from_user(self) -> bool:
        """Verifica se a mensagem é de um usuário"""
        return self.sender_type == "user"
