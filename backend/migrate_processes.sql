-- Migração da tabela processes para nova estrutura
-- Execute este script manualmente no seu banco de dados PostgreSQL

-- Para cada schema de tenant (substitua X pelo ID do tenant)
-- Exemplo para tenant_1:

DO $$
DECLARE
    schema_record RECORD;
BEGIN
    FOR schema_record IN
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name LIKE 'tenant_%'
    LOOP
        -- Verificar se a coluna process_type já existe
        IF NOT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_schema = schema_record.schema_name
            AND table_name = 'processes'
            AND column_name = 'process_type'
        ) THEN
            RAISE NOTICE 'Migrando schema: %', schema_record.schema_name;

            -- Backup da tabela antiga
            EXECUTE format('CREATE TABLE IF NOT EXISTS %I.processes_backup AS SELECT * FROM %I.processes',
                          schema_record.schema_name, schema_record.schema_name);

            -- Dropar tabela antiga
            EXECUTE format('DROP TABLE %I.processes CASCADE', schema_record.schema_name);

            -- Criar nova tabela
            EXECUTE format('
                CREATE TABLE %I.processes (
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES %I.clients(id),
                    process_type VARCHAR(100) NOT NULL,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    priority VARCHAR(20) NOT NULL DEFAULT ''normal'',
                    estimated_days INTEGER NOT NULL DEFAULT 30,
                    status VARCHAR(50) NOT NULL DEFAULT ''aguardando'',
                    alteration_types JSONB,
                    assigned_to INTEGER REFERENCES %I.users(id),
                    created_by INTEGER REFERENCES %I.users(id),
                    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                    started_at TIMESTAMP,
                    completed_at TIMESTAMP
                )',
                schema_record.schema_name,
                schema_record.schema_name,
                schema_record.schema_name,
                schema_record.schema_name
            );

            -- Recriar índices
            EXECUTE format('CREATE INDEX ix_%I_processes_client ON %I.processes(client_id)',
                          schema_record.schema_name, schema_record.schema_name);
            EXECUTE format('CREATE INDEX ix_%I_processes_status ON %I.processes(status)',
                          schema_record.schema_name, schema_record.schema_name);

            RAISE NOTICE 'Schema % migrado com sucesso!', schema_record.schema_name;
        ELSE
            RAISE NOTICE 'Schema % já está atualizado', schema_record.schema_name;
        END IF;
    END LOOP;
END $$;
