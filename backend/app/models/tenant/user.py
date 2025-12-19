"""
LEGIA PLATFORM - Modelo TenantUser (Usuário do Escritório)
Schema: tenant_XXX
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON

from app.db.base import Base


class TenantUser(Base):
    """
    Modelo TenantUser - Representa um usuário (funcionário) do escritório

    Cada tenant tem seus próprios usuários no schema tenant_XXX
    """

    __tablename__ = "users"
    # Schema será definido dinamicamente em runtime

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True,
                  comment="Email único do usuário")
    password_hash = Column(String(255), nullable=False,
                          comment="Hash bcrypt da senha")
    name = Column(String(255), nullable=False, comment="Nome completo")

    # Função no escritório
    role = Column(String(50), nullable=False, default="contador",
                 comment="Papel: admin, contador, auxiliar, atendimento")

    # Permissões granulares (JSON)
    permissions = Column(JSON, default={},
                        comment="Permissões específicas")

    # Status
    is_active = Column(Boolean, default=True, comment="Se está ativo")
    is_verified = Column(Boolean, default=False,
                        comment="Se o email foi verificado")

    # 2FA (opcional para usuários, obrigatório para admin)
    two_factor_enabled = Column(Boolean, default=False,
                               comment="Se 2FA está habilitado")
    two_factor_secret = Column(String(255), nullable=True,
                              comment="Secret do 2FA")

    # Contato
    phone = Column(String(20), nullable=True, comment="Telefone")

    # Datas
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)
    invited_at = Column(DateTime, nullable=True,
                       comment="Quando foi convidado")
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=True,
                       comment="Quem convidou")

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<TenantUser {self.id}: {self.name} ({self.role})>"

    @property
    def is_admin(self) -> bool:
        """Verifica se é admin do escritório"""
        return self.role == "admin"

    @property
    def can_manage_users(self) -> bool:
        """Verifica se pode gerenciar usuários"""
        return self.is_admin

    @property
    def display_role(self) -> str:
        """Retorna nome amigável do papel"""
        roles = {
            "admin": "Administrador",
            "contador": "Contador",
            "auxiliar": "Auxiliar Contábil",
            "atendimento": "Atendimento"
        }
        return roles.get(self.role, self.role)
