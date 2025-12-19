"""
LEGIA PLATFORM - Modelo Client (Cliente Final)
Schema: tenant_XXX
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class Client(Base):
    """
    Modelo Client - Representa um cliente final do escritório

    Pode ser PF (pessoa física) ou PJ (pessoa jurídica)
    """

    __tablename__ = "clients"
    # Schema será definido dinamicamente em runtime

    # Identificação
    id = Column(Integer, primary_key=True, index=True)

    # Tipo
    type = Column(String(10), nullable=False,
                 comment="Tipo: pf (pessoa física), pj (pessoa jurídica)")

    # Identificação básica
    name = Column(String(255), nullable=False,
                 comment="Nome completo (PF) ou Razão Social (PJ)")
    document = Column(String(18), nullable=False, index=True,
                     comment="CPF ou CNPJ")

    # Dados PJ
    company_name = Column(String(255), nullable=True,
                         comment="Razão social")
    trade_name = Column(String(255), nullable=True,
                       comment="Nome fantasia")
    cnae_primary = Column(String(20), nullable=True,
                         comment="CNAE principal")
    cnae_secondary = Column(ARRAY(String), nullable=True,
                           comment="CNAEs secundários")
    state_registration = Column(String(50), nullable=True,
                               comment="Inscrição estadual")
    municipal_registration = Column(String(50), nullable=True,
                                   comment="Inscrição municipal")

    # Contato
    email = Column(String(255), nullable=True, comment="Email")
    phone = Column(String(20), nullable=True, comment="Telefone fixo")
    mobile = Column(String(20), nullable=True, comment="Celular")

    # Endereço
    address_street = Column(String(255), nullable=True, comment="Rua")
    address_number = Column(String(20), nullable=True, comment="Número")
    address_complement = Column(String(100), nullable=True, comment="Complemento")
    address_neighborhood = Column(String(100), nullable=True, comment="Bairro")
    address_city = Column(String(100), nullable=True, comment="Cidade")
    address_state = Column(String(2), nullable=True, comment="UF")
    address_zipcode = Column(String(10), nullable=True, comment="CEP")

    # Status
    status = Column(String(50), nullable=False, default="lead", index=True,
                   comment="Status: lead, active, inactive, suspended")

    # Relacionamento
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True,
                        comment="Usuário responsável")

    # Datas
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    activated_at = Column(DateTime, nullable=True,
                         comment="Data de ativação")

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<Client {self.id}: {self.name} ({self.document})>"

    @property
    def is_pf(self) -> bool:
        """Verifica se é pessoa física"""
        return self.type == "pf"

    @property
    def is_pj(self) -> bool:
        """Verifica se é pessoa jurídica"""
        return self.type == "pj"

    @property
    def is_active(self) -> bool:
        """Verifica se está ativo"""
        return self.status == "active"

    @property
    def is_lead(self) -> bool:
        """Verifica se é apenas um lead"""
        return self.status == "lead"

    @property
    def full_address(self) -> str:
        """Retorna endereço completo formatado"""
        parts = []
        if self.address_street:
            parts.append(self.address_street)
        if self.address_number:
            parts.append(self.address_number)
        if self.address_complement:
            parts.append(f"({self.address_complement})")
        if self.address_neighborhood:
            parts.append(f"- {self.address_neighborhood}")
        if self.address_city and self.address_state:
            parts.append(f"- {self.address_city}/{self.address_state}")
        if self.address_zipcode:
            parts.append(f"- CEP: {self.address_zipcode}")
        return " ".join(parts) if parts else ""

    @property
    def display_name(self) -> str:
        """Retorna nome de exibição apropriado"""
        if self.is_pj and self.trade_name:
            return self.trade_name
        return self.name
