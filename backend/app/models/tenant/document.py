"""
LEGIA PLATFORM - Modelo Document (Documento)
Schema: tenant_XXX
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, JSON, ARRAY
from sqlalchemy.orm import relationship

from app.db.base import Base


class Document(Base):
    """
    Modelo Document - Representa um documento armazenado

    Tipos: contrato, certidao, alvara, rg, cpf, comprovante, etc
    """

    __tablename__ = "documents"
    # Schema será definido dinamicamente em runtime

    # Identificação
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    process_id = Column(Integer, ForeignKey("processes.id"), nullable=True)

    # Arquivo
    name = Column(String(255), nullable=False, comment="Nome do arquivo")
    type = Column(String(100), nullable=False, index=True,
                 comment="Tipo do documento")
    # Type: contrato, certidao, alvara, rg, cpf, comprovante, etc

    file_path = Column(String(500), nullable=False,
                      comment="Caminho do arquivo no storage")
    file_size = Column(Integer, nullable=True, comment="Tamanho em bytes")
    mime_type = Column(String(100), nullable=True,
                      comment="Tipo MIME do arquivo")

    # Categorização
    category = Column(String(100), nullable=True,
                     comment="Categoria do documento")
    # Category: societario, tributario, licencas, etc

    tags = Column(ARRAY(String), nullable=True,
                 comment="Tags para busca")

    # Validade (para certidões, etc)
    issue_date = Column(Date, nullable=True,
                       comment="Data de emissão")
    expiry_date = Column(Date, nullable=True, index=True,
                        comment="Data de vencimento")

    # Upload
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Versioning
    version = Column(Integer, default=1, comment="Versão do documento")
    replaces = Column(Integer, ForeignKey("documents.id"), nullable=True,
                     comment="ID do documento que este substitui")

    # Status
    is_active = Column(Boolean, default=True,
                      comment="Se está ativo (não foi deletado)")

    # Extra Data
    extra_data = Column(JSON, default={})

    def __repr__(self):
        return f"<Document {self.id}: {self.name} ({self.type})>"

    @property
    def is_expired(self) -> bool:
        """Verifica se o documento está vencido"""
        if not self.expiry_date:
            return False
        return date.today() > self.expiry_date

    @property
    def expires_soon(self) -> bool:
        """Verifica se vence nos próximos 30 dias"""
        if not self.expiry_date or self.is_expired:
            return False
        days_until_expiry = (self.expiry_date - date.today()).days
        return days_until_expiry <= 30

    @property
    def file_size_mb(self) -> float:
        """Retorna tamanho em MB"""
        if not self.file_size:
            return 0
        return round(self.file_size / (1024 * 1024), 2)

    @property
    def file_extension(self) -> str:
        """Retorna extensão do arquivo"""
        if "." not in self.name:
            return ""
        return self.name.rsplit(".", 1)[-1].lower()

    @property
    def display_category(self) -> str:
        """Retorna categoria formatada"""
        categories = {
            "societario": "Societário",
            "tributario": "Tributário",
            "licencas": "Licenças e Alvarás",
            "contratos": "Contratos",
            "processos": "Processos",
            "comunicacoes": "Comunicações",
            "diversos": "Diversos"
        }
        return categories.get(self.category, self.category or "Sem Categoria")
