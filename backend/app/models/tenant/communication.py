"""
LEGIA PLATFORM - Modelo Communication (Comunicação Oficial)
Schema: tenant_XXX
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, JSON

from app.db.base import Base


class Communication(Base):
    """
    Modelo Communication - Representa uma comunicação oficial

    Gerado pelo Gestor de Comunicações
    """

    __tablename__ = "communications"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=True)

    # Tipo
    type = Column(String(100), nullable=False,
                 comment="Tipo: oficio, requerimento, notificacao, resposta")

    # Destinatário
    recipient_organ = Column(String(100), nullable=True,
                            comment="Órgão destinatário")
    recipient_name = Column(String(255), nullable=True,
                           comment="Nome do destinatário")
    recipient_email = Column(String(255), nullable=True,
                            comment="Email do destinatário")

    # Conteúdo
    subject = Column(String(500), nullable=False,
                    comment="Assunto")
    body = Column(Text, nullable=False,
                 comment="Corpo da comunicação")

    # Arquivos anexos
    attachments = Column(JSON, default=[],
                        comment="Lista de anexos")

    # Protocolo (se protocolado)
    protocol_number = Column(String(255), nullable=True,
                            comment="Número do protocolo")
    protocol_date = Column(Date, nullable=True,
                          comment="Data do protocolo")

    # Status
    status = Column(String(50), nullable=False, default="draft",
                   comment="Status: draft, sent, delivered, read, responded")

    # Criação e envio
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<Communication {self.id}: {self.type} - {self.status}>"
