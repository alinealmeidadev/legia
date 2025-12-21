"""
LEGIA PLATFORM - Utilitário para gerenciar schemas de tenants
"""
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal


def create_tenant_schema(tenant_id: int, db: Session = None) -> bool:
    """
    Cria schema completo para um novo tenant

    Args:
        tenant_id: ID do tenant
        db: Sessão do banco (opcional)

    Returns:
        True se criado com sucesso
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        schema_name = f"tenant_{tenant_id}"

        # Criar schema
        db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema_name}"))

        # Criar tabela: users
        db.execute(text(f"""
            CREATE TABLE {schema_name}.users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'contador',
                permissions JSONB DEFAULT '{{}}',
                is_active BOOLEAN DEFAULT TRUE,
                is_verified BOOLEAN DEFAULT FALSE,
                two_factor_enabled BOOLEAN DEFAULT FALSE,
                two_factor_secret VARCHAR(255),
                phone VARCHAR(20),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                last_login_at TIMESTAMP,
                invited_at TIMESTAMP,
                invited_by INTEGER REFERENCES {schema_name}.users(id),
                extra_data JSONB DEFAULT '{{}}'
            )
        """))

        # Criar tabela: clients
        db.execute(text(f"""
            CREATE TABLE {schema_name}.clients (
                id SERIAL PRIMARY KEY,
                type VARCHAR(10) NOT NULL,
                name VARCHAR(255) NOT NULL,
                document VARCHAR(18) NOT NULL,
                company_name VARCHAR(255),
                trade_name VARCHAR(255),
                cnae_primary VARCHAR(20),
                cnae_secondary TEXT[],
                state_registration VARCHAR(50),
                municipal_registration VARCHAR(50),
                email VARCHAR(255),
                phone VARCHAR(20),
                mobile VARCHAR(20),
                address_street VARCHAR(255),
                address_number VARCHAR(20),
                address_complement VARCHAR(100),
                address_neighborhood VARCHAR(100),
                address_city VARCHAR(100),
                address_state VARCHAR(2),
                address_zipcode VARCHAR(10),
                status VARCHAR(50) NOT NULL DEFAULT 'lead',
                assigned_to INTEGER REFERENCES {schema_name}.users(id),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                activated_at TIMESTAMP,
                extra_data JSONB DEFAULT '{{}}'
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_clients_document ON {schema_name}.clients(document)"))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_clients_status ON {schema_name}.clients(status)"))

        # Criar tabela: processes
        db.execute(text(f"""
            CREATE TABLE {schema_name}.processes (
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES {schema_name}.clients(id),
                process_type VARCHAR(100) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                priority VARCHAR(20) NOT NULL DEFAULT 'normal',
                estimated_days INTEGER NOT NULL DEFAULT 30,
                status VARCHAR(50) NOT NULL DEFAULT 'aguardando',
                alteration_types JSONB,
                assigned_to INTEGER REFERENCES {schema_name}.users(id),
                created_by INTEGER REFERENCES {schema_name}.users(id),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                started_at TIMESTAMP,
                completed_at TIMESTAMP
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_processes_client ON {schema_name}.processes(client_id)"))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_processes_status ON {schema_name}.processes(status)"))

        # Criar tabela: documents
        db.execute(text(f"""
            CREATE TABLE {schema_name}.documents (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES {schema_name}.clients(id),
                process_id INTEGER REFERENCES {schema_name}.processes(id),
                name VARCHAR(255) NOT NULL,
                type VARCHAR(100) NOT NULL,
                file_path VARCHAR(500) NOT NULL,
                file_size INTEGER,
                mime_type VARCHAR(100),
                category VARCHAR(100),
                tags TEXT[],
                issue_date DATE,
                expiry_date DATE,
                uploaded_by INTEGER REFERENCES {schema_name}.users(id),
                uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
                version INTEGER DEFAULT 1,
                replaces INTEGER REFERENCES {schema_name}.documents(id),
                is_active BOOLEAN DEFAULT TRUE,
                extra_data JSONB DEFAULT '{{}}'
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_documents_type ON {schema_name}.documents(type)"))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_documents_expiry ON {schema_name}.documents(expiry_date)"))

        # Criar tabela: quotes
        db.execute(text(f"""
            CREATE TABLE {schema_name}.quotes (
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES {schema_name}.clients(id),
                service_type VARCHAR(100) NOT NULL,
                service_details JSONB NOT NULL,
                amount NUMERIC(10, 2) NOT NULL,
                discount NUMERIC(10, 2) DEFAULT 0,
                final_amount NUMERIC(10, 2) NOT NULL,
                breakdown JSONB DEFAULT '{{}}',
                status VARCHAR(50) NOT NULL DEFAULT 'draft',
                valid_until DATE,
                created_by INTEGER REFERENCES {schema_name}.users(id),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                sent_at TIMESTAMP,
                viewed_at TIMESTAMP,
                approved_at TIMESTAMP,
                rejected_at TIMESTAMP,
                rejection_reason TEXT,
                extra_data JSONB DEFAULT '{{}}'
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_quotes_status ON {schema_name}.quotes(status)"))

        # Criar tabela: protocols
        db.execute(text(f"""
            CREATE TABLE {schema_name}.protocols (
                id SERIAL PRIMARY KEY,
                process_id INTEGER NOT NULL REFERENCES {schema_name}.processes(id),
                protocol_number VARCHAR(255) NOT NULL,
                organ VARCHAR(100) NOT NULL,
                organ_details VARCHAR(255),
                status VARCHAR(100),
                protocol_date DATE NOT NULL,
                last_check TIMESTAMP,
                last_update TIMESTAMP,
                data JSONB DEFAULT '{{}}',
                documents_available TEXT[],
                has_alert BOOLEAN DEFAULT FALSE,
                alert_type VARCHAR(50),
                alert_message TEXT,
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_protocols_organ ON {schema_name}.protocols(organ)"))

        # Criar tabela: communications
        db.execute(text(f"""
            CREATE TABLE {schema_name}.communications (
                id SERIAL PRIMARY KEY,
                process_id INTEGER REFERENCES {schema_name}.processes(id),
                type VARCHAR(100) NOT NULL,
                recipient_organ VARCHAR(100),
                recipient_name VARCHAR(255),
                recipient_email VARCHAR(255),
                subject VARCHAR(500) NOT NULL,
                body TEXT NOT NULL,
                attachments JSONB DEFAULT '[]',
                protocol_number VARCHAR(255),
                protocol_date DATE,
                status VARCHAR(50) NOT NULL DEFAULT 'draft',
                created_by INTEGER REFERENCES {schema_name}.users(id),
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                sent_at TIMESTAMP,
                extra_data JSONB DEFAULT '{{}}'
            )
        """))

        # Criar tabela: chat_messages
        db.execute(text(f"""
            CREATE TABLE {schema_name}.chat_messages (
                id SERIAL PRIMARY KEY,
                conversation_id UUID NOT NULL,
                sender_type VARCHAR(20) NOT NULL,
                sender_id INTEGER,
                sender_name VARCHAR(255),
                message TEXT NOT NULL,
                agent_name VARCHAR(100),
                data JSONB DEFAULT '{{}}',
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                extra_data JSONB DEFAULT '{{}}'
            )
        """))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_chat_conversation ON {schema_name}.chat_messages(conversation_id)"))
        db.execute(text(f"CREATE INDEX ix_{schema_name}_chat_created ON {schema_name}.chat_messages(created_at)"))

        db.commit()

        print(f"✅ Schema {schema_name} criado com sucesso!")
        return True

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao criar schema tenant_{tenant_id}: {e}")
        return False

    finally:
        if close_db:
            db.close()


def drop_tenant_schema(tenant_id: int, db: Session = None) -> bool:
    """
    Remove schema de um tenant

    Args:
        tenant_id: ID do tenant
        db: Sessão do banco (opcional)

    Returns:
        True se removido com sucesso
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        schema_name = f"tenant_{tenant_id}"
        db.execute(text(f"DROP SCHEMA IF EXISTS {schema_name} CASCADE"))
        db.commit()

        print(f"✅ Schema {schema_name} removido!")
        return True

    except Exception as e:
        db.rollback()
        print(f"❌ Erro ao remover schema tenant_{tenant_id}: {e}")
        return False

    finally:
        if close_db:
            db.close()


def list_tenant_schemas(db: Session = None) -> List[str]:
    """
    Lista todos os schemas de tenants

    Args:
        db: Sessão do banco (opcional)

    Returns:
        Lista de nomes de schemas
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    try:
        result = db.execute(text("""
            SELECT schema_name
            FROM information_schema.schemata
            WHERE schema_name LIKE 'tenant_%'
            ORDER BY schema_name
        """))

        schemas = [row[0] for row in result]
        return schemas

    finally:
        if close_db:
            db.close()
