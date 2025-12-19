"""
LEGIA PLATFORM - Modelo Subscription (Assinatura)
Schema: public
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Subscription(Base):
    """
    Modelo Subscription - Representa uma assinatura de tenant

    Cada tenant tem uma assinatura ativa que define seu plano e período de cobrança
    """

    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "public"}

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("public.tenants.id", ondelete="CASCADE"),
                      nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("public.plans.id"), nullable=False)

    # Status
    status = Column(String(50), nullable=False, default="active", index=True,
                   comment="Status: active, past_due, canceled, expired")

    # Período de cobrança
    billing_cycle = Column(String(20), nullable=False, default="monthly",
                          comment="Ciclo: monthly, yearly")
    current_period_start = Column(Date, nullable=False,
                                 comment="Início do período atual")
    current_period_end = Column(Date, nullable=False,
                               comment="Fim do período atual")

    # Cancelamento
    cancel_at_period_end = Column(Boolean, default=False,
                                 comment="Se deve cancelar no fim do período")
    canceled_at = Column(DateTime, nullable=True,
                        comment="Data de cancelamento")
    cancellation_reason = Column(Text, nullable=True,
                                comment="Motivo do cancelamento")

    # Valores
    amount = Column(Numeric(10, 2), nullable=False,
                   comment="Valor da assinatura")
    currency = Column(String(3), default="BRL",
                     comment="Moeda (BRL)")

    # Usuários extras
    extra_users = Column(Integer, default=0,
                        comment="Quantidade de usuários extras contratados")
    extra_users_price = Column(Numeric(10, 2), default=0,
                              comment="Valor total dos usuários extras")

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    # Relacionamentos
    tenant = relationship("Tenant", back_populates="subscriptions")
    plan = relationship("Plan", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription")

    def __repr__(self):
        return f"<Subscription {self.id}: Tenant {self.tenant_id} - {self.status}>"

    @property
    def is_active(self) -> bool:
        """Verifica se a assinatura está ativa"""
        return self.status == "active"

    @property
    def is_overdue(self) -> bool:
        """Verifica se está em atraso"""
        return self.status == "past_due"

    @property
    def total_amount(self) -> float:
        """Calcula o valor total (plano + extras)"""
        return float(self.amount) + float(self.extra_users_price)

    @property
    def is_monthly(self) -> bool:
        """Verifica se é assinatura mensal"""
        return self.billing_cycle == "monthly"

    @property
    def is_yearly(self) -> bool:
        """Verifica se é assinatura anual"""
        return self.billing_cycle == "yearly"
