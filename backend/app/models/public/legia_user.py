"""
LEGIA PLATFORM - Modelo LegiaUser (Super Admin da Legia)
Schema: public
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON

from app.db.base import Base


class LegiaUser(Base):
    """
    Modelo LegiaUser - Representa um usuário da Legia (super admin)

    Estes usuários têm acesso ao painel administrativo global e podem
    gerenciar todos os tenants, planos, pagamentos, etc.
    """

    __tablename__ = "legia_users"
    __table_args__ = {"schema": "public"}

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True,
                  comment="Email único do super admin")
    password_hash = Column(String(255), nullable=False,
                          comment="Hash bcrypt da senha")
    name = Column(String(255), nullable=False, comment="Nome completo")

    # Função
    role = Column(String(50), nullable=False, default="support",
                 comment="Papel: superadmin, support, financial, technical")

    # 2FA (obrigatório para superadmins)
    two_factor_enabled = Column(Boolean, default=False,
                               comment="Se 2FA está habilitado")
    two_factor_secret = Column(String(255), nullable=True,
                              comment="Secret do 2FA (TOTP)")

    # Status
    is_active = Column(Boolean, default=True, comment="Se está ativo")
    is_verified = Column(Boolean, default=False,
                        comment="Se o email foi verificado")

    # Datas
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       comment="Data de criação")
    last_login_at = Column(DateTime, nullable=True,
                          comment="Último login")

    # Permissões granulares (JSON)
    permissions = Column(JSON, default={},
                        comment="Permissões específicas em JSON")
    # Exemplo: {"can_delete_tenant": true, "can_manage_billing": true}

    def __repr__(self):
        return f"<LegiaUser {self.id}: {self.name} ({self.email})>"

    @property
    def is_superadmin(self) -> bool:
        """Verifica se é superadmin"""
        return self.role == "superadmin"

    @property
    def requires_2fa(self) -> bool:
        """Verifica se requer 2FA (obrigatório para superadmins)"""
        return self.is_superadmin

    @property
    def can_access_all_tenants(self) -> bool:
        """Verifica se pode acessar todos os tenants"""
        return self.role in ["superadmin", "support"]

    @property
    def display_role(self) -> str:
        """Retorna nome amigável do papel"""
        roles = {
            "superadmin": "Super Administrador",
            "support": "Suporte",
            "financial": "Financeiro",
            "technical": "Técnico"
        }
        return roles.get(self.role, self.role)
