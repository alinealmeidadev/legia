"""create processes table in tenant schemas

Revision ID: 20241219_0003
Revises: 20241217_0002
Create Date: 2025-12-19 08:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '20241219_0003'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Migra tabela processes da estrutura antiga para a nova em todos os schemas de tenants existentes
    """
    # Pegar conexão
    conn = op.get_bind()

    # Buscar todos os tenants
    result = conn.execute(text("SELECT id FROM public.tenants"))
    tenant_ids = [row[0] for row in result]

    for tenant_id in tenant_ids:
        schema_name = f"tenant_{tenant_id}"

        # Verificar se a tabela existe
        table_exists = conn.execute(text(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = '{schema_name}'
                AND table_name = 'processes'
            );
        """)).scalar()

        if table_exists:
            # Tabela existe - precisa migrar da estrutura antiga para nova
            print(f"  🔄 Migrando tabela processes no schema {schema_name}...")

            # Verificar se já tem a nova estrutura (coluna process_type)
            has_new_structure = conn.execute(text(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns
                    WHERE table_schema = '{schema_name}'
                    AND table_name = 'processes'
                    AND column_name = 'process_type'
                );
            """)).scalar()

            if has_new_structure:
                print(f"  ⏭️  Schema {schema_name} já tem a nova estrutura")
                continue

            # Adicionar novas colunas
            conn.execute(text(f"""
                -- Renomear coluna type para process_type
                ALTER TABLE {schema_name}.processes RENAME COLUMN type TO process_type;

                -- Adicionar novas colunas
                ALTER TABLE {schema_name}.processes ADD COLUMN IF NOT EXISTS title VARCHAR(200);
                ALTER TABLE {schema_name}.processes ADD COLUMN IF NOT EXISTS description TEXT;
                ALTER TABLE {schema_name}.processes ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'normal';
                ALTER TABLE {schema_name}.processes ADD COLUMN IF NOT EXISTS estimated_days INTEGER DEFAULT 30;

                -- Preencher colunas title e description de dados existentes
                UPDATE {schema_name}.processes SET
                    title = COALESCE(data->>'title', 'Processo ' || process_type),
                    description = COALESCE(data->>'description', ''),
                    priority = COALESCE(data->>'priority', 'normal'),
                    estimated_days = COALESCE((data->>'estimated_days')::INTEGER, 30)
                WHERE title IS NULL;

                -- Tornar title NOT NULL após preencher
                ALTER TABLE {schema_name}.processes ALTER COLUMN title SET NOT NULL;
                ALTER TABLE {schema_name}.processes ALTER COLUMN priority SET NOT NULL;
                ALTER TABLE {schema_name}.processes ALTER COLUMN estimated_days SET NOT NULL;

                -- Atualizar status 'criado' para 'aguardando'
                UPDATE {schema_name}.processes SET status = 'aguardando' WHERE status = 'criado';
                ALTER TABLE {schema_name}.processes ALTER COLUMN status SET DEFAULT 'aguardando';

                -- Remover colunas antigas (opcional - comentar se quiser manter dados)
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS subtype;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS data;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS checklist;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS progress_percent;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS estimated_completion;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS canceled_at;
                -- ALTER TABLE {schema_name}.processes DROP COLUMN IF EXISTS extra_data;
            """))

            # Criar índice para process_type
            conn.execute(text(f"""
                CREATE INDEX IF NOT EXISTS ix_{schema_name}_processes_process_type
                    ON {schema_name}.processes(process_type);
            """))

            print(f"  ✅ Tabela processes migrada no schema {schema_name}")
        else:
            # Tabela não existe - criar nova
            print(f"  📦 Criando tabela processes no schema {schema_name}...")
            conn.execute(text(f"""
                CREATE TABLE {schema_name}.processes (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES {schema_name}.clients(id) ON DELETE CASCADE,
                    process_type VARCHAR(100) NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    priority VARCHAR(20) NOT NULL DEFAULT 'normal',
                    estimated_days INTEGER NOT NULL DEFAULT 30,
                    status VARCHAR(50) NOT NULL DEFAULT 'aguardando',
                    assigned_to INTEGER REFERENCES {schema_name}.users(id) ON DELETE SET NULL,
                    created_by INTEGER REFERENCES {schema_name}.users(id) ON DELETE SET NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                );

                -- Índices
                CREATE INDEX ix_{schema_name}_processes_client_id
                    ON {schema_name}.processes(client_id);
                CREATE INDEX ix_{schema_name}_processes_status
                    ON {schema_name}.processes(status);
                CREATE INDEX ix_{schema_name}_processes_process_type
                    ON {schema_name}.processes(process_type);
                CREATE INDEX ix_{schema_name}_processes_created_at
                    ON {schema_name}.processes(created_at DESC);

                -- Trigger para atualizar updated_at
                CREATE OR REPLACE FUNCTION {schema_name}.update_processes_updated_at()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;

                CREATE TRIGGER trigger_update_processes_updated_at
                    BEFORE UPDATE ON {schema_name}.processes
                    FOR EACH ROW
                    EXECUTE FUNCTION {schema_name}.update_processes_updated_at();
            """))

            print(f"  ✅ Tabela processes criada no schema {schema_name}")


def downgrade() -> None:
    """
    Remove tabela processes de todos os schemas de tenants
    """
    conn = op.get_bind()

    result = conn.execute(text("SELECT id FROM public.tenants"))
    tenant_ids = [row[0] for row in result]

    for tenant_id in tenant_ids:
        schema_name = f"tenant_{tenant_id}"
        conn.execute(text(f"DROP TABLE IF EXISTS {schema_name}.processes CASCADE"))
        print(f"✅ Tabela processes removida do schema {schema_name}")
