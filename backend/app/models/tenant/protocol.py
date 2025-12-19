"""
LEGIA PLATFORM - Modelo Protocol (Protocolo)
Schema: tenant_XXX
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Text, ForeignKey, JSON, ARRAY

from app.db.base import Base


class Protocol(Base):
    """
    Modelo Protocol - Representa um protocolo em órgão público

    Monitorado pelo Monitor de Protocolos
    """

    __tablename__ = "protocols"

    id = Column(Integer, primary_key=True, index=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=False,
                       index=True)

    # Protocolo
    protocol_number = Column(String(255), nullable=False,
                            comment="Número do protocolo")
    organ = Column(String(100), nullable=False, index=True,
                  comment="Órgão: junta, receita, prefeitura, estado, tribunal")
    organ_details = Column(String(255), nullable=True,
                          comment="Ex: JUCESP, Receita Federal")

    # Status
    status = Column(String(100), nullable=True,
                   comment="Status no órgão")

    # Datas
    protocol_date = Column(Date, nullable=False,
                          comment="Data do protocolo")
    last_check = Column(DateTime, nullable=True,
                       comment="Última consulta")
    last_update = Column(DateTime, nullable=True,
                        comment="Última atualização de status")

    # Detalhes
    data = Column(JSON, default={},
                 comment="Dados adicionais do protocolo")

    # Documentos disponíveis
    documents_available = Column(ARRAY(String), nullable=True,
                                comment="Documentos disponíveis para download")

    # Alertas
    has_alert = Column(Boolean, default=False,
                      comment="Se há algum alerta")
    alert_type = Column(String(50), nullable=True,
                       comment="Tipo de alerta")
    alert_message = Column(Text, nullable=True,
                          comment="Mensagem de alerta")

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Protocol {self.id}: {self.protocol_number} - {self.organ}>"
