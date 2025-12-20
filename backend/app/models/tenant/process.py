"""
LEGIA PLATFORM - Modelo Process (Processo de Legalização)
Schema: tenant_XXX
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class Process(Base):
    """
    Modelo Process - Representa um processo de legalização

    Tipos: abertura, alteracao, regularizacao, encerramento
    """

    __tablename__ = "processes"
    # Schema será definido dinamicamente em runtime

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False,
                      index=True)

    # Informações principais
    process_type = Column(String(100), nullable=False,
                         comment="Tipo: abertura, alteracao, regularizacao, encerramento")
    title = Column(String(200), nullable=False,
                  comment="Título do processo")
    description = Column(String, nullable=True,
                        comment="Descrição detalhada")

    # Prioridade e prazo
    priority = Column(String(20), nullable=False, default="normal",
                     comment="Prioridade: baixa, normal, alta")
    estimated_days = Column(Integer, nullable=False, default=30,
                           comment="Prazo estimado em dias")

    # Status
    status = Column(String(50), nullable=False, default="aguardando", index=True,
                   comment="Status: aguardando, em_andamento, protocolado, concluido, cancelado")

    # Alterações específicas (para processos de alteração contratual)
    alteration_types = Column(JSON, nullable=True,
                             comment="Lista de alterações solicitadas: ['endereco', 'socios', 'capital', 'atividade']")

    # Atribuição
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True,
                        comment="Usuário responsável")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True,
                       comment="Usuário que criou")

    # Datas
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow,
                       onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True,
                       comment="Data de início")
    completed_at = Column(DateTime, nullable=True,
                         comment="Data de conclusão")

    def __repr__(self):
        return f"<Process {self.id}: {self.title} - {self.status}>"

    @property
    def is_active(self) -> bool:
        """Verifica se está ativo"""
        return self.status not in ["concluido", "cancelado", "archived"]

    @property
    def is_completed(self) -> bool:
        """Verifica se foi concluído"""
        return self.status == "concluido"

    @property
    def is_canceled(self) -> bool:
        """Verifica se foi cancelado"""
        return self.status == "cancelado"

    @property
    def display_type(self) -> str:
        """Retorna tipo formatado"""
        types = {
            "abertura": "Abertura de Empresa",
            "alteracao": "Alteração Contratual",
            "regularizacao": "Regularização",
            "encerramento": "Encerramento"
        }
        return types.get(self.process_type, self.process_type)

    @property
    def display_status(self) -> str:
        """Retorna status formatado"""
        statuses = {
            "aguardando": "Aguardando",
            "em_andamento": "Em Andamento",
            "protocolado": "Protocolado",
            "concluido": "Concluído",
            "cancelado": "Cancelado"
        }
        return statuses.get(self.status, self.status)
