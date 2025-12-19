-- LEGIA PLATFORM - Inicialização do Banco de Dados
-- PostgreSQL 15+

-- Criar extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Schema public já existe por padrão
-- Será usado para dados globais da Legia

-- Criar função para criar schemas de tenants automaticamente
CREATE OR REPLACE FUNCTION create_tenant_schema(tenant_id INTEGER)
RETURNS VOID AS $$
DECLARE
    schema_name TEXT;
BEGIN
    schema_name := 'tenant_' || tenant_id;

    -- Criar schema
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', schema_name);

    RAISE NOTICE 'Schema % criado com sucesso!', schema_name;
END;
$$ LANGUAGE plpgsql;

-- Criar trigger para criar schema automaticamente ao inserir tenant
CREATE OR REPLACE FUNCTION trigger_create_tenant_schema()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM create_tenant_schema(NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Mensagem de sucesso
DO $$
BEGIN
    RAISE NOTICE '✅ Banco de dados LEGIA PLATFORM inicializado com sucesso!';
    RAISE NOTICE '📦 Schema public criado';
    RAISE NOTICE '⚡ Extensões habilitadas: uuid-ossp, pgcrypto';
    RAISE NOTICE '🔧 Funções de multi-tenancy configuradas';
END $$;
