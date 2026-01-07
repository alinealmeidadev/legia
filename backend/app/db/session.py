"""
LEGIA PLATFORM - Sessão do Banco de Dados
"""
from typing import Generator, Optional
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool

from app.core.config import settings
from app.utils.tenant_schema import validate_schema_name

# Engine do PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=NullPool,  # Importante para multi-tenancy
    echo=settings.DEBUG,
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency que fornece sessão do banco

    Yields:
        Sessão do SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def set_tenant_schema(db: Session, schema_name: str) -> None:
    """
    Define o schema do tenant para a sessão atual

    Args:
        db: Sessão do SQLAlchemy
        schema_name: Nome do schema (ex: tenant_001, tenant_002)
    """
    # Validar schema_name para prevenir SQL injection
    schema_name = validate_schema_name(schema_name)

    # Define search_path para o schema do tenant + public (fallback)
    db.execute(text(f"SET search_path TO {schema_name}, public"))
    db.commit()


def reset_schema(db: Session) -> None:
    """
    Reseta o schema para public (padrão)

    Args:
        db: Sessão do SQLAlchemy
    """
    db.execute(text("SET search_path TO public"))
    db.commit()


def get_tenant_db(schema_name: str) -> Generator[Session, None, None]:
    """
    Dependency que fornece sessão do banco com schema do tenant

    Args:
        schema_name: Nome do schema do tenant

    Yields:
        Sessão do SQLAlchemy configurada para o tenant
    """
    db = SessionLocal()
    try:
        set_tenant_schema(db, schema_name)
        yield db
    finally:
        reset_schema(db)
        db.close()


class TenantSession:
    """
    Context manager para trabalhar com sessão de tenant

    Exemplo:
        with TenantSession("tenant_001") as db:
            users = db.query(User).all()
    """

    def __init__(self, schema_name: str):
        self.schema_name = schema_name
        self.db: Optional[Session] = None

    def __enter__(self) -> Session:
        self.db = SessionLocal()
        set_tenant_schema(self.db, self.schema_name)
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db:
            reset_schema(self.db)
            self.db.close()
