"""
LEGIA PLATFORM - Modelo Plan (Plano de Assinatura)
Schema: public
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Plan(Base):
    """
    Modelo Plan - Representa um plano de assinatura disponível

    Planos: Básico (R$ 297), Pro (R$ 597), Premium (R$ 997)
    """

    __tablename__ = "plans"
    __table_args__ = {"schema": "public"}

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="Nome do plano")
    slug = Column(String(50), unique=True, nullable=False, index=True,
                 comment="Slug único (basico, pro, premium)")
    description = Column(Text, nullable=True, comment="Descrição do plano")

    # Precificação
    price_monthly = Column(Numeric(10, 2), nullable=False,
                          comment="Preço mensal em reais")
    price_yearly = Column(Numeric(10, 2), nullable=True,
                         comment="Preço anual (com desconto)")

    # Limites
    max_users = Column(Integer, nullable=True,
                      comment="Máximo de usuários (NULL = ilimitado)")
    max_clients = Column(Integer, nullable=True,
                        comment="Máximo de clientes (NULL = ilimitado)")
    max_storage_gb = Column(Integer, nullable=True,
                           comment="Máximo de armazenamento em GB")
    max_processes_month = Column(Integer, nullable=True,
                                comment="Máximo de processos por mês")

    # Features (lista JSON)
    features = Column(JSON, nullable=False, default=[],
                     comment="Lista de features do plano")
    # Exemplo: ["leg_agents", "whatsapp_api", "email_marketing"]

    # UI/UX
    color = Column(String(7), nullable=True, comment="Cor do plano (hex)")
    icon = Column(String(50), nullable=True, comment="Ícone do plano")
    display_order = Column(Integer, default=0, comment="Ordem de exibição")

    # Visibilidade
    is_public = Column(Boolean, default=True,
                      comment="Se o plano é público (visível)")
    is_active = Column(Boolean, default=True,
                      comment="Se o plano está ativo")

    # Metadata
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    # Relacionamentos
    tenants = relationship("Tenant", back_populates="plan")
    subscriptions = relationship("Subscription", back_populates="plan")

    def __repr__(self):
        return f"<Plan {self.id}: {self.name} (R$ {self.price_monthly})>"

    @property
    def has_limit(self) -> bool:
        """Verifica se o plano tem limites definidos"""
        return any([self.max_users, self.max_clients, self.max_storage_gb])

    @property
    def is_unlimited(self) -> bool:
        """Verifica se é um plano ilimitado"""
        return not self.has_limit
