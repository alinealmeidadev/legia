-- Migração: Adicionar coluna alteration_types na tabela processes
-- Data: 2025-12-19
-- Descrição: Suporta múltiplas alterações contratuais em um único processo

-- Para tenant_1 (ajuste o número do tenant conforme necessário)
ALTER TABLE tenant_1.processes
ADD COLUMN IF NOT EXISTS alteration_types JSON;

COMMENT ON COLUMN tenant_1.processes.alteration_types IS
'Lista de alterações solicitadas: ["endereco", "socios", "capital", "atividade"]';

-- Se tiver mais tenants, replicar para cada um:
-- ALTER TABLE tenant_2.processes ADD COLUMN IF NOT EXISTS alteration_types JSON;
-- ALTER TABLE tenant_3.processes ADD COLUMN IF NOT EXISTS alteration_types JSON;

-- Verificar se a coluna foi criada
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'tenant_1'
  AND table_name = 'processes'
  AND column_name = 'alteration_types';
