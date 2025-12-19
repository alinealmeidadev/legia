"""
LEGIA PLATFORM - Modelo Tenant (Escritório)
Schema: public
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Tenant(Base):
    """
    Modelo Tenant - Representa um escritório contábil (cliente B2B da Legia)

    Cada tenant tem um schema separado no PostgreSQL com todos os seus dados
    """

    __tablename__ = "tenants"
    __table_args__ = {"schema": "public"}

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, comment="Nome do escritório")
    subdomain = Column(String(100), unique=True, nullable=False, index=True,
                      comment="Subdomínio único (ex: escritorio-abc)")
    cnpj = Column(String(18), unique=True, nullable=False, index=True,
                 comment="CNPJ do escritório")
    crc = Column(String(50), nullable=True, comment="CRC do escritório")

    # Status
    status = Column(String(50), nullable=False, default="trial", index=True,
                   comment="Status: trial, active, suspended, canceled")

    # Plano e assinatura
    plan_id = Column(Integer, ForeignKey("public.plans.id"), nullable=True)

    # Datas
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       comment="Data de criação")
    trial_ends_at = Column(DateTime, nullable=True,
                          comment="Fim do período de trial")
    activated_at = Column(DateTime, nullable=True,
                         comment="Data de ativação")
    suspended_at = Column(DateTime, nullable=True,
                         comment="Data de suspensão")
    canceled_at = Column(DateTime, nullable=True,
                        comment="Data de cancelamento")

    # Personalização (branding)
    logo_url = Column(String(500), nullable=True,
                     comment="URL do logo do escritório")
    primary_color = Column(String(7), default="#004E89",
                          comment="Cor primária (hex)")
    secondary_color = Column(String(7), default="#FF6B35",
                            comment="Cor secundária (hex)")

    # Contato
    email = Column(String(255), nullable=False,
                  comment="Email principal do escritório")
    phone = Column(String(20), nullable=True,
                  comment="Telefone")
    website = Column(String(255), nullable=True,
                    comment="Website do escritório")

    # Endereço
    address_street = Column(String(255), nullable=True)
    address_number = Column(String(20), nullable=True)
    address_complement = Column(String(100), nullable=True)
    address_neighborhood = Column(String(100), nullable=True)
    address_city = Column(String(100), nullable=True)
    address_state = Column(String(2), nullable=True)
    address_zipcode = Column(String(10), nullable=True)

    # Domínio customizado (futuro - white label)
    custom_domain = Column(String(255), nullable=True,
                          comment="Domínio customizado (white label)")
    custom_domain_verified = Column(Boolean, default=False,
                                   comment="Se o domínio foi verificado")

    # Configurações (JSON)
    settings = Column(JSON, default={},
                     comment="Configurações diversas em JSON")

    # Extra Data (JSON)
    extra_data = Column(JSON, default={},
                       comment="Dados adicionais em JSON")

    # Relacionamentos
    plan = relationship("Plan", back_populates="tenants")
    subscriptions = relationship("Subscription", back_populates="tenant",
                                cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="tenant",
                          cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tenant {self.id}: {self.name} ({self.subdomain})>"

    @property
    def schema_name(self) -> str:
        """Retorna o nome do schema PostgreSQL deste tenant"""
        return f"tenant_{self.id}"

    @property
    def is_active(self) -> bool:
        """Verifica se o tenant está ativo"""
        return self.status in ["trial", "active"]

    @property
    def is_trial(self) -> bool:
        """Verifica se está em período de trial"""
        return self.status == "trial"
