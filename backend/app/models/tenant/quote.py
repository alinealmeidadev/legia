"""
LEGIA PLATFORM - Modelo Quote (Orçamento)
Schema: tenant_XXX
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime, Text, ForeignKey, JSON

from app.db.base import Base


class Quote(Base):
    """
    Modelo Quote - Representa um orçamento gerado

    Gerado pelo Agente Comercial
    """

    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    # Serviço
    service_type = Column(String(100), nullable=False,
                         comment="Tipo de serviço")
    service_details = Column(JSON, nullable=False,
                            comment="Detalhes do serviço")

    # Valores
    amount = Column(Numeric(10, 2), nullable=False, comment="Valor total")
    discount = Column(Numeric(10, 2), default=0, comment="Desconto")
    final_amount = Column(Numeric(10, 2), nullable=False,
                         comment="Valor final")

    # Breakdown de custos
    breakdown = Column(JSON, default={},
                      comment="Detalhamento dos custos")

    # Status
    status = Column(String(50), nullable=False, default="draft", index=True,
                   comment="Status: draft, sent, viewed, approved, rejected, expired")

    # Validade
    valid_until = Column(Date, nullable=True, comment="Válido até")

    # Criação
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Interações
    sent_at = Column(DateTime, nullable=True)
    viewed_at = Column(DateTime, nullable=True)
    approved_at = Column(DateTime, nullable=True)
    rejected_at = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<Quote {self.id}: R$ {self.final_amount} - {self.status}>"

    @property
    def is_valid(self) -> bool:
        """Verifica se o orçamento ainda é válido"""
        if not self.valid_until:
            return True
        return date.today() <= self.valid_until

    @property
    def is_approved(self) -> bool:
        """Verifica se foi aprovado"""
        return self.status == "approved"
