# LEGIA PLATFORM - Database Schema Completo

## 📊 VISÃO GERAL

Database PostgreSQL 15+ com arquitetura multi-schema:
- **Schema `public`**: Dados globais da Legia
- **Schema `tenant_XXX`**: Dados de cada escritório (isolados)

---

## 🗄️ SCHEMA PUBLIC (Dados da Legia)

### Tabela: tenants
```sql
CREATE TABLE public.tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(100) UNIQUE NOT NULL,
    cnpj VARCHAR(18) UNIQUE NOT NULL,
    crc VARCHAR(50),  -- CRC do escritório
    status VARCHAR(50) NOT NULL DEFAULT 'trial',
    -- Status: trial, active, suspended, canceled
    
    plan_id INTEGER REFERENCES public.plans(id),
    
    -- Datas
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    trial_ends_at TIMESTAMP,
    activated_at TIMESTAMP,
    suspended_at TIMESTAMP,
    canceled_at TIMESTAMP,
    
    -- Personalização
    logo_url VARCHAR(500),
    primary_color VARCHAR(7) DEFAULT '#004E89',
    secondary_color VARCHAR(7) DEFAULT '#FF6B35',
    
    -- Contato
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    website VARCHAR(255),
    
    -- Endereço
    address_street VARCHAR(255),
    address_number VARCHAR(20),
    address_complement VARCHAR(100),
    address_neighborhood VARCHAR(100),
    address_city VARCHAR(100),
    address_state VARCHAR(2),
    address_zipcode VARCHAR(10),
    
    -- Domínio customizado (futuro)
    custom_domain VARCHAR(255),
    custom_domain_verified BOOLEAN DEFAULT false,
    
    -- Configurações
    settings JSONB DEFAULT '{}',
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_tenants_subdomain ON public.tenants(subdomain);
CREATE INDEX idx_tenants_status ON public.tenants(status);
CREATE INDEX idx_tenants_cnpj ON public.tenants(cnpj);
```

### Tabela: plans
```sql
CREATE TABLE public.plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    
    -- Precificação
    price_monthly DECIMAL(10,2) NOT NULL,
    price_yearly DECIMAL(10,2),  -- Desconto anual
    
    -- Limites
    max_users INTEGER,  -- NULL = ilimitado
    max_clients INTEGER,
    max_storage_gb INTEGER,
    max_processes_month INTEGER,
    
    -- Features (JSON com lista)
    features JSONB NOT NULL DEFAULT '[]',
    -- Exemplo: ["leg_agents", "whatsapp_api", "email_marketing"]
    
    -- UI
    color VARCHAR(7),
    icon VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    
    -- Visibilidade
    is_public BOOLEAN DEFAULT true,
    is_active BOOLEAN DEFAULT true,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Dados padrão
INSERT INTO public.plans (name, slug, price_monthly, price_yearly, max_users, max_clients, features) VALUES
('Básico', 'basico', 297.00, 2970.00, 3, 50, '["leg_agents"]'),
('Pro', 'pro', 597.00, 5970.00, 10, 200, '["leg_agents", "whatsapp_api", "email_marketing"]'),
('Premium', 'premium', 997.00, 9970.00, NULL, NULL, '["leg_agents", "whatsapp_api", "email_marketing", "api", "white_label"]');
```

### Tabela: subscriptions
```sql
CREATE TABLE public.subscriptions (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenants(id) ON DELETE CASCADE,
    plan_id INTEGER NOT NULL REFERENCES public.plans(id),
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    -- Status: active, past_due, canceled, expired
    
    -- Período
    billing_cycle VARCHAR(20) NOT NULL DEFAULT 'monthly',
    -- Billing: monthly, yearly
    
    current_period_start DATE NOT NULL,
    current_period_end DATE NOT NULL,
    
    -- Cancelamento
    cancel_at_period_end BOOLEAN DEFAULT false,
    canceled_at TIMESTAMP,
    cancellation_reason TEXT,
    
    -- Valores
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BRL',
    
    -- Usuários extras
    extra_users INTEGER DEFAULT 0,
    extra_users_price DECIMAL(10,2) DEFAULT 0,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_subscriptions_tenant ON public.subscriptions(tenant_id);
CREATE INDEX idx_subscriptions_status ON public.subscriptions(status);
```

### Tabela: payments
```sql
CREATE TABLE public.payments (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL REFERENCES public.tenants(id),
    subscription_id INTEGER REFERENCES public.subscriptions(id),
    
    -- Valores
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'BRL',
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    -- Status: pending, paid, failed, refunded, canceled
    
    -- Método
    payment_method VARCHAR(50) NOT NULL,
    -- Método: credit_card, boleto, pix
    
    -- Datas
    due_date DATE NOT NULL,
    paid_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Gateway (Asaas)
    gateway_id VARCHAR(255),  -- ID no Asaas
    gateway_status VARCHAR(100),
    invoice_url VARCHAR(500),
    boleto_url VARCHAR(500),
    pix_qrcode TEXT,
    
    -- Detalhes do cartão (últimos 4 dígitos)
    card_last4 VARCHAR(4),
    card_brand VARCHAR(20),
    
    -- Falhas
    failure_code VARCHAR(50),
    failure_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_payments_tenant ON public.payments(tenant_id);
CREATE INDEX idx_payments_status ON public.payments(status);
CREATE INDEX idx_payments_gateway_id ON public.payments(gateway_id);
```

### Tabela: legia_users
```sql
CREATE TABLE public.legia_users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    
    -- Função
    role VARCHAR(50) NOT NULL DEFAULT 'support',
    -- Roles: superadmin, support, financial, technical
    
    -- 2FA
    two_factor_enabled BOOLEAN DEFAULT false,
    two_factor_secret VARCHAR(255),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    
    -- Datas
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMP,
    
    -- Metadata
    permissions JSONB DEFAULT '{}'
);

-- Super admin padrão
INSERT INTO public.legia_users (email, password_hash, name, role) VALUES
('admin@legia.com.br', '$2b$12$...', 'Admin Legia', 'superadmin');
```

---

## 🏢 SCHEMA TENANT_XXX (Dados do Escritório)

**Nota:** Esta estrutura é REPLICADA para cada tenant.

### Tabela: users
```sql
CREATE TABLE tenant_XXX.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    
    -- Função no escritório
    role VARCHAR(50) NOT NULL DEFAULT 'contador',
    -- Roles: admin, contador, auxiliar, atendimento
    
    -- Permissões granulares
    permissions JSONB DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    
    -- 2FA
    two_factor_enabled BOOLEAN DEFAULT false,
    two_factor_secret VARCHAR(255),
    
    -- Contato
    phone VARCHAR(20),
    
    -- Datas
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_login_at TIMESTAMP,
    invited_at TIMESTAMP,
    invited_by INTEGER REFERENCES tenant_XXX.users(id),
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);
```

### Tabela: clients
```sql
CREATE TABLE tenant_XXX.clients (
    id SERIAL PRIMARY KEY,
    
    -- Tipo
    type VARCHAR(10) NOT NULL,
    -- Type: pf (pessoa física), pj (pessoa jurídica)
    
    -- Identificação
    name VARCHAR(255) NOT NULL,
    document VARCHAR(18) NOT NULL,  -- CPF ou CNPJ
    
    -- Dados PJ
    company_name VARCHAR(255),  -- Razão social
    trade_name VARCHAR(255),  -- Nome fantasia
    cnae_primary VARCHAR(20),
    cnae_secondary TEXT[],
    state_registration VARCHAR(50),
    municipal_registration VARCHAR(50),
    
    -- Contato
    email VARCHAR(255),
    phone VARCHAR(20),
    mobile VARCHAR(20),
    
    -- Endereço
    address_street VARCHAR(255),
    address_number VARCHAR(20),
    address_complement VARCHAR(100),
    address_neighborhood VARCHAR(100),
    address_city VARCHAR(100),
    address_state VARCHAR(2),
    address_zipcode VARCHAR(10),
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'lead',
    -- Status: lead, active, inactive, suspended
    
    -- Relacionamento
    assigned_to INTEGER REFERENCES tenant_XXX.users(id),
    
    -- Datas
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    activated_at TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_clients_document ON tenant_XXX.clients(document);
CREATE INDEX idx_clients_status ON tenant_XXX.clients(status);
CREATE INDEX idx_clients_assigned ON tenant_XXX.clients(assigned_to);
```

### Tabela: processes
```sql
CREATE TABLE tenant_XXX.processes (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES tenant_XXX.clients(id),
    
    -- Tipo
    type VARCHAR(100) NOT NULL,
    -- Type: abertura, alteracao, regularizacao, encerramento
    
    -- Subtipo
    subtype VARCHAR(100),
    -- Abertura: me, ltda, eireli, sa
    -- Alteracao: endereco, socio, capital, cnae
    -- Regularizacao: alvara, licenca, inscricao
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'criado',
    -- Status: criado, aguardando_docs, em_andamento, 
    --         protocolado, concluido, cancelado
    
    -- Atribuição
    assigned_to INTEGER REFERENCES tenant_XXX.users(id),
    created_by INTEGER REFERENCES tenant_XXX.users(id),
    
    -- Dados específicos do processo (JSON)
    data JSONB DEFAULT '{}',
    
    -- Progresso
    checklist JSONB DEFAULT '[]',
    progress_percent INTEGER DEFAULT 0,
    
    -- Prazos
    estimated_completion DATE,
    
    -- Datas
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    canceled_at TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_processes_client ON tenant_XXX.processes(client_id);
CREATE INDEX idx_processes_status ON tenant_XXX.processes(status);
CREATE INDEX idx_processes_assigned ON tenant_XXX.processes(assigned_to);
```

### Tabela: documents
```sql
CREATE TABLE tenant_XXX.documents (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES tenant_XXX.clients(id),
    process_id INTEGER REFERENCES tenant_XXX.processes(id),
    
    -- Arquivo
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    -- Type: contrato, certidao, alvara, rg, cpf, comprovante, etc
    
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,  -- Bytes
    mime_type VARCHAR(100),
    
    -- Categorização
    category VARCHAR(100),
    -- Category: societario, tributario, licencas, etc
    
    tags TEXT[],
    
    -- Validade (para certidões, etc)
    issue_date DATE,
    expiry_date DATE,
    
    -- Upload
    uploaded_by INTEGER REFERENCES tenant_XXX.users(id),
    uploaded_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Versioning
    version INTEGER DEFAULT 1,
    replaces INTEGER REFERENCES tenant_XXX.documents(id),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_documents_client ON tenant_XXX.documents(client_id);
CREATE INDEX idx_documents_process ON tenant_XXX.documents(process_id);
CREATE INDEX idx_documents_type ON tenant_XXX.documents(type);
CREATE INDEX idx_documents_expiry ON tenant_XXX.documents(expiry_date);
```

### Tabela: quotes (Orçamentos)
```sql
CREATE TABLE tenant_XXX.quotes (
    id SERIAL PRIMARY KEY,
    client_id INTEGER REFERENCES tenant_XXX.clients(id),
    
    -- Tipo de serviço
    service_type VARCHAR(100) NOT NULL,
    -- Type: abertura, alteracao, regularizacao, etc
    
    service_details JSONB NOT NULL,
    
    -- Valores
    amount DECIMAL(10,2) NOT NULL,
    discount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL,
    
    -- Breakdown de custos
    breakdown JSONB DEFAULT '{}',
    -- {
    --   "custos_oficiais": 513.00,
    --   "honorarios": 1737.00
    -- }
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    -- Status: draft, sent, viewed, approved, rejected, expired
    
    -- Validade
    valid_until DATE,
    
    -- Criação
    created_by INTEGER REFERENCES tenant_XXX.users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Interações
    sent_at TIMESTAMP,
    viewed_at TIMESTAMP,
    approved_at TIMESTAMP,
    rejected_at TIMESTAMP,
    rejection_reason TEXT,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_quotes_client ON tenant_XXX.quotes(client_id);
CREATE INDEX idx_quotes_status ON tenant_XXX.quotes(status);
```

### Tabela: protocols
```sql
CREATE TABLE tenant_XXX.protocols (
    id SERIAL PRIMARY KEY,
    process_id INTEGER NOT NULL REFERENCES tenant_XXX.processes(id),
    
    -- Protocolo
    protocol_number VARCHAR(255) NOT NULL,
    organ VARCHAR(100) NOT NULL,
    -- Organ: junta, receita, prefeitura, estado, tribunal
    
    organ_details VARCHAR(255),
    -- Ex: "JUCESP", "Receita Federal", "Prefeitura SP"
    
    -- Status
    status VARCHAR(100),
    -- Status varia por órgão: protocolado, em_analise, 
    --         deferido, indeferido, exigencia, etc
    
    -- Datas
    protocol_date DATE NOT NULL,
    last_check TIMESTAMP,
    last_update TIMESTAMP,
    
    -- Detalhes
    data JSONB DEFAULT '{}',
    
    -- Documentos disponíveis
    documents_available TEXT[],
    
    -- Alertas
    has_alert BOOLEAN DEFAULT false,
    alert_type VARCHAR(50),
    alert_message TEXT,
    
    -- Metadata
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_protocols_process ON tenant_XXX.protocols(process_id);
CREATE INDEX idx_protocols_organ ON tenant_XXX.protocols(organ);
```

### Tabela: communications
```sql
CREATE TABLE tenant_XXX.communications (
    id SERIAL PRIMARY KEY,
    process_id INTEGER REFERENCES tenant_XXX.processes(id),
    
    -- Tipo
    type VARCHAR(100) NOT NULL,
    -- Type: oficio, requerimento, notificacao, resposta
    
    -- Destinatário
    recipient_organ VARCHAR(100),
    recipient_name VARCHAR(255),
    recipient_email VARCHAR(255),
    
    -- Conteúdo
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    
    -- Arquivos anexos
    attachments JSONB DEFAULT '[]',
    
    -- Protocolo (se protocolado)
    protocol_number VARCHAR(255),
    protocol_date DATE,
    
    -- Status
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    -- Status: draft, sent, delivered, read, responded
    
    -- Criação e envio
    created_by INTEGER REFERENCES tenant_XXX.users(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    sent_at TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);
```

### Tabela: chat_messages
```sql
CREATE TABLE tenant_XXX.chat_messages (
    id SERIAL PRIMARY KEY,
    
    -- Conversa
    conversation_id UUID NOT NULL,
    
    -- Participantes
    sender_type VARCHAR(20) NOT NULL,
    -- Type: user, agent, client
    
    sender_id INTEGER,
    sender_name VARCHAR(255),
    
    -- Mensagem
    message TEXT NOT NULL,
    
    -- Agente IA (se aplicável)
    agent_name VARCHAR(100),
    -- Ex: "Orquestrador", "Agente Comercial"
    
    -- Dados estruturados (se houver)
    data JSONB DEFAULT '{}',
    
    -- Timestamp
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    
    -- Metadata
    metadata JSONB DEFAULT '{}'
);

-- Índices
CREATE INDEX idx_chat_conversation ON tenant_XXX.chat_messages(conversation_id);
CREATE INDEX idx_chat_created ON tenant_XXX.chat_messages(created_at);
```

---

## 🔐 FUNÇÕES E TRIGGERS

### Criar novo tenant automaticamente
```sql
CREATE OR REPLACE FUNCTION create_tenant_schema(tenant_id INTEGER)
RETURNS VOID AS $$
DECLARE
    schema_name TEXT;
BEGIN
    schema_name := 'tenant_' || tenant_id;
    
    -- Criar schema
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', schema_name);
    
    -- Criar todas as tabelas
    -- (SQL completo das tabelas acima, mas com schema dinâmico)
    EXECUTE format('CREATE TABLE %I.users (...)', schema_name);
    EXECUTE format('CREATE TABLE %I.clients (...)', schema_name);
    -- ... todas as outras tabelas
    
    -- Criar admin padrão
    EXECUTE format('
        INSERT INTO %I.users (email, password_hash, name, role)
        VALUES ($1, $2, $3, $4)
    ', schema_name)
    USING 'admin@tenant.local', '$2b$12$...', 'Admin', 'admin';
END;
$$ LANGUAGE plpgsql;
```

### Trigger: Criar schema após criar tenant
```sql
CREATE OR REPLACE FUNCTION trigger_create_tenant_schema()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM create_tenant_schema(NEW.id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_tenant_insert
    AFTER INSERT ON public.tenants
    FOR EACH ROW
    EXECUTE FUNCTION trigger_create_tenant_schema();
```

---

## 📊 MIGRATIONS (Exemplo Alembic)

```python
# migrations/versions/001_initial.py
def upgrade():
    # Schema public
    op.execute("CREATE SCHEMA IF NOT EXISTS public")
    
    # Criar tabelas public
    op.create_table(
        'tenants',
        schema='public',
        # ... colunas
    )
    
    # Criar tenants de exemplo
    op.execute("""
        INSERT INTO public.tenants (name, subdomain, cnpj, status)
        VALUES 
            ('Escritório ABC', 'abc', '12.345.678/0001-90', 'active'),
            ('Escritório XYZ', 'xyz', '98.765.432/0001-10', 'active')
    """)
    
    # Criar schemas dos tenants
    op.execute("SELECT create_tenant_schema(1)")
    op.execute("SELECT create_tenant_schema(2)")

def downgrade():
    op.drop_schema('tenant_2', cascade=True)
    op.drop_schema('tenant_1', cascade=True)
    op.drop_table('tenants', schema='public')
```

---

## ✅ VERIFICAÇÕES

### Testar isolamento:
```sql
-- Inserir em tenant_001
SET search_path TO tenant_001;
INSERT INTO clients (name, type, document) 
VALUES ('Silva LTDA', 'pj', '12.345.678/0001-90');

-- Tentar acessar de tenant_002
SET search_path TO tenant_002;
SELECT * FROM clients WHERE document = '12.345.678/0001-90';
-- Deve retornar 0 resultados! ✅
```

---

**Versão:** 1.0.0  
**Data:** 17/12/2024  
**Schema PostgreSQL 15+**
