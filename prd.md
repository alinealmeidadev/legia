# LEGIA PLATFORM - PRD (Documento de Requisitos do Produto)

**Versão:** 1.0.0  
**Data:** 17/12/2024  
**Empresa:** LEGIA  
**Produto:** LEGIA PLATFORM (SaaS Multi-tenant)  
**Módulo Inicial:** LEG.Agents (Agentes de Legalização)  

---

## 📋 ÍNDICE

1. [Visão Executiva](#visão-executiva)
2. [Modelo de Negócio](#modelo-de-negócio)
3. [Arquitetura da Plataforma](#arquitetura-da-plataforma)
4. [Níveis de Acesso](#níveis-de-acesso)
5. [Planos e Precificação](#planos-e-precificação)
6. [Sistema de Pagamentos](#sistema-de-pagamentos)
7. [LEG.Agents - 8 Agentes](#legagents---os-8-agentes)
8. [Segurança e Compliance](#segurança-e-compliance)
9. [Roadmap](#roadmap)
10. [Próximos Passos](#próximos-passos)

---

## 🎯 VISÃO EXECUTIVA

### O Que é a LEGIA PLATFORM?

**LEGIA PLATFORM** é uma plataforma SaaS B2B multi-tenant que fornece sistemas especializados baseados em IA para escritórios de contabilidade no Brasil.

**Produto Inicial:** LEG.Agents - Sistema de 8 agentes de IA que automatizam processos de legalização empresarial.

### Problema Que Resolve

**Dores dos Escritórios Contábeis:**
- ⏱️ Processos manuais demorados (abertura de empresa: 8-10 semanas)
- 📝 Documentação complexa e propensa a erros
- 📞 Atendimento reativo (cliente liga, escritório responde)
- 💰 Perda de oportunidades comerciais (orçamentos demoram dias)
- 📊 Falta de visibilidade gerencial

**Solução:**
- 🤖 Automação com 8 agentes de IA especializados
- ⚡ Redução de 90% no tempo de processos
- 💬 Atendimento proativo e humanizado 24/7
- 💰 Orçamentos automáticos em minutos
- 📊 Dashboard completo com métricas em tempo real

### Diferencial Competitivo

```
Concorrentes Tradicionais:
❌ Sistemas legados (interfaces antigas)
❌ Sem IA (tudo manual)
❌ Caros (R$ 500-2.000/mês)
❌ Complexos (curva de aprendizado alta)
❌ Suporte ruim

LEGIA PLATFORM:
✅ Interface moderna (Next.js + React)
✅ 8 agentes de IA especializados
✅ Preço competitivo (R$ 297-997/mês)
✅ Fácil de usar (onboarding em 5 minutos)
✅ Suporte dedicado brasileiro
✅ Trial grátis 14 dias
```

---

## 💼 MODELO DE NEGÓCIO

### Estrutura de 3 Camadas

```
┌────────────────────────────────────────┐
│  NÍVEL 1: LEGIA (Sua Empresa)         │
│  • Fornecedora da plataforma SaaS      │
│  • Cobra assinatura mensal             │
│  • Gerencia escritórios (tenants)      │
└────────────┬───────────────────────────┘
             │
             ↓ Vende para
┌────────────────────────────────────────┐
│  NÍVEL 2: ESCRITÓRIOS CONTÁBEIS        │
│  • Clientes B2B da Legia               │
│  • Pagam assinatura (R$ 297-997/mês)   │
│  • Usam LEG.Agents para atender        │
└────────────┬───────────────────────────┘
             │
             ↓ Atendem
┌────────────────────────────────────────┐
│  NÍVEL 3: EMPRESAS/EMPREENDEDORES      │
│  • Clientes finais dos escritórios     │
│  • Precisam abrir/alterar empresas     │
│  • São atendidos pelos agentes IA      │
└────────────────────────────────────────┘
```

### Fonte de Receita

**Receita Recorrente Mensal (MRR):**
```
Assinaturas mensais:
├─ Plano Básico: R$ 297/mês
├─ Plano Pro: R$ 597/mês  
└─ Plano Premium: R$ 997/mês

Receitas Adicionais:
├─ Usuários extras
├─ Armazenamento adicional
├─ White label (+R$ 200/mês)
└─ Integrações premium
```

**Projeção Ano 1:**
```
Mês 1-2:   10 escritórios (beta grátis)
Mês 3:     20 escritórios → R$ 6k/mês
Mês 6:     50 escritórios → R$ 20k/mês
Mês 12:   150 escritórios → R$ 67k/mês

ARR Ano 1: ~R$ 800.000
```

### Roadmap de Produtos

```
2025 Q1-Q2: LEG.Agents (Legalização)
2025 Q3-Q4: LEG.Fiscal (Tributário)
2026 Q1-Q2: LEG.Pessoal (RH/DP)
2026 Q3-Q4: LEG.Contábil (Contabilidade)
2027+:      LEG.Suite (Todos integrados)
```

---

## 🏗️ ARQUITETURA DA PLATAFORMA

### Multi-Tenancy (Multi-inquilino)

**Conceito:** Múltiplos clientes (escritórios) compartilham a mesma infraestrutura mas têm dados completamente isolados.

**Implementação Escolhida:** Schema por Tenant (PostgreSQL)

```sql
-- Banco de dados único
legia_platform_db

├── public (Dados globais da Legia)
│   ├── tenants (escritórios cadastrados)
│   ├── plans (planos disponíveis)
│   ├── subscriptions (assinaturas)
│   ├── payments (pagamentos)
│   └── legia_users (super admins)
│
├── tenant_001 (Escritório ABC)
│   ├── users (equipe do escritório)
│   ├── clients (clientes finais)
│   ├── processes (processos de legalização)
│   ├── documents (documentos)
│   └── ... (todas as tabelas do LEG.Agents)
│
├── tenant_002 (Escritório XYZ)
│   └── ... (mesma estrutura, dados isolados)
│
└── tenant_003 (Escritório 123)
    └── ... (mesma estrutura, dados isolados)
```

**Vantagens:**
- ✅ Isolamento total de dados
- ✅ Backup individual por tenant
- ✅ Fácil migração de clientes
- ✅ Performance otimizada
- ✅ Segurança reforçada

### Identificação de Tenant

**Por subdomínio:**
```
escritorio-abc.legiaplatform.com.br → tenant_001
escritorio-xyz.legiaplatform.com.br → tenant_002
```

**Middleware automático:**
```python
# Middleware identifica tenant e muda schema
host = request.headers["host"]
subdomain = host.split(".")[0]
tenant = get_tenant_by_subdomain(subdomain)

# Define schema para esta requisição
set_search_path(f"tenant_{tenant.id}")

# Todas as queries usam o schema correto
```

---

## 👥 NÍVEIS DE ACESSO

### 1. SUPER ADMIN (Legia - Você)

**Acesso:** Painel administrativo exclusivo

**Pode fazer:**
- ✅ Criar/editar/excluir escritórios (tenants)
- ✅ Gerenciar planos e preços
- ✅ Visualizar/processar pagamentos
- ✅ Acessar métricas globais
- ✅ Gerenciar super admins
- ✅ Configurar plataforma
- ✅ Suporte aos escritórios
- ✅ "Login como" qualquer escritório

**Dashboard:**
```
Métricas Principais:
├─ Escritórios ativos: 147
├─ MRR: R$ 87.450
├─ Crescimento mensal: +8.9%
├─ Churn rate: 3.2%
├─ Usuários ativos (hoje): 423
└─ Tickets suporte: 3 abertos
```

### 2. TENANT ADMIN (Dono do Escritório)

**Acesso:** Painel do escritório

**Pode fazer:**
- ✅ Gerenciar usuários da equipe
- ✅ Cadastrar clientes finais
- ✅ Usar LEG.Agents completo
- ✅ Configurar personalização (logo, cores)
- ✅ Ver relatórios do escritório
- ✅ Gerenciar assinatura e pagamento
- ❌ Não acessa dados de outros escritórios
- ❌ Não gerencia plataforma global

**Dashboard:**
```
Métricas do Escritório:
├─ Clientes ativos: 87
├─ Processos em andamento: 23
├─ Orçamentos enviados (mês): 34
├─ Taxa conversão: 47%
└─ Certidões vencendo: 3 (alerta)
```

### 3. FUNCIONÁRIO (Equipe do Escritório)

**Acesso:** Painel limitado

**Pode fazer:**
- ✅ Ver clientes atribuídos a ele
- ✅ Criar/editar processos
- ✅ Gerar orçamentos
- ✅ Usar os agentes IA
- ✅ Upload de documentos
- ❌ Não gerencia usuários
- ❌ Não acessa financeiro
- ❌ Não muda configurações

**Níveis de Função:**
```
Admin → Acesso total ao escritório
Contador → Processos + relatórios
Auxiliar → Apenas processos
Atendimento → Apenas chat/clientes
```

### 4. CLIENTE FINAL (Opcional - Futuro)

**Acesso:** Portal do cliente

**Pode fazer:**
- ✅ Ver seus processos
- ✅ Acompanhar status
- ✅ Fazer upload de documentos
- ✅ Receber notificações
- ❌ Apenas visualização (sem editar)

---

## 💰 PLANOS E PRECIFICAÇÃO

### Plano BÁSICO - R$ 297/mês

**Para:** Escritórios pequenos iniciando

```
Recursos:
✓ 3 usuários inclusos
✓ 50 clientes finais
✓ LEG.Agents completo (8 agentes IA)
✓ 10GB armazenamento
✓ Suporte email (48h)
✓ Relatórios básicos

✗ WhatsApp API
✗ Email marketing
✗ API integração
✗ White label

Usuários adicionais: +R$ 70/cada
```

### Plano PRO - R$ 597/mês

**Para:** Escritórios médios em crescimento

```
Recursos:
✓ 10 usuários inclusos
✓ 200 clientes finais
✓ LEG.Agents completo (8 agentes IA)
✓ 50GB armazenamento
✓ Suporte prioritário (12h)
✓ Relatórios avançados
✓ WhatsApp API integrado
✓ Email marketing (1k envios)

✗ API integração
✗ White label

Usuários adicionais: +R$ 50/cada
```

### Plano PREMIUM - R$ 997/mês

**Para:** Escritórios grandes estabelecidos

```
Recursos:
✓ Usuários ilimitados
✓ Clientes ilimitados
✓ LEG.Agents completo (8 agentes IA)
✓ 200GB armazenamento
✓ Suporte 24/7 dedicado
✓ Relatórios customizados
✓ WhatsApp + Telegram
✓ Email marketing ilimitado
✓ API de integração completa
✓ White label (+R$ 200 opcional)
✓ Gerente de conta dedicado
✓ SLA 99.9% uptime

Tudo ilimitado!
```

### Trial Gratuito

**14 dias grátis - Sem cartão**
- ✅ Acesso completo Plano Pro
- ✅ Sem compromisso
- ✅ Dados preservados após conversão

---

## 💳 SISTEMA DE PAGAMENTOS

### Gateway: Asaas (Brasileiro)

**Por quê:**
- ✅ Foco mercado brasileiro
- ✅ Boleto + PIX + Cartão
- ✅ Taxas competitivas
- ✅ Suporte português
- ✅ Compliance Brasil

**Formas de pagamento:**
```
Cartão Crédito (Recorrente):
├─ Cobrança automática mensal
├─ Retry 3x se falhar
└─ Aceita: Visa, Master, Elo, Amex

Boleto Bancário:
├─ Vencimento: Todo dia 25
├─ Validade: 3 dias úteis
└─ Juros: 2% + 1%am após vencimento

PIX:
├─ QR Code gerado
├─ Válido 24h
└─ Confirmação instantânea
```

### Gestão de Inadimplência

```
Vencimento + 0: Email "Processando"
Vencimento + 1: Email "Pagamento falhou"
Vencimento + 3: Email + WhatsApp "Regularize"
Vencimento + 7: SUSPENSÃO (modo leitura)
Vencimento + 15: Contato telefônico
Vencimento + 30: CANCELAMENTO (backup enviado)
```

**Reativação:**
- Pagar pendências → Acesso em 2h
- Sem taxa de reativação

---

## 🤖 LEG.AGENTS - OS 8 AGENTES

### Visão Geral

Sistema multi-agente que automatiza processos de legalização empresarial usando IA (Google Gemini 3.0).

```
Fluxo de Trabalho:
Usuario → Orquestrador → Agente Especializado → Execução → Resultado
```

### 1. 🎯 ORQUESTRADOR

**Função:** Maestro que coordena todos os outros agentes

**Responsabilidades:**
- Receber mensagens de humanos
- Analisar intenção
- Decidir qual agente acionar
- Gerenciar contexto e memória
- Consolidar respostas
- Atribuir processos a funcionários
- Cadastrar clientes no sistema

**Exemplo:**
```
Cliente: "Quanto custa abrir empresa?"
Orquestrador: [Analisa] → Intenção: orçamento
Orquestrador: [Aciona] → Agente Comercial
Comercial: [Trabalha] → Gera orçamento
Orquestrador: [Consolida] → Apresenta ao cliente
```

### 2. 💼 AGENTE COMERCIAL

**Função:** Geração de orçamentos e vendas

**Responsabilidades:**
- Gerar orçamentos automáticos
- Qualificar interessados (lead scoring)
- Negociar valores
- Gestão de funil de vendas
- Follow-up automático
- Upsell e cross-sell

**Tipos de orçamento:**
```
├─ Abertura de empresa (ME/LTDA/EIRELI/SA)
├─ Alterações societárias
├─ Regularizações (Alvará, licenças)
└─ Planos mensais (Básico/Pro/Premium)
```

**Cálculo automático:**
```python
# Exemplo simplificado
atividade = "Consultoria TI"
cidade = "São Paulo"
faturamento = 300_000  # R$/ano

cnae = "7490-1/04"
atendemos = check_cnae_atendido(cnae)  # True
junta = "JUCESP"
taxa_junta = 306.00

tipo_juridico = "ME"  # Faturamento < 360k
simples_viavel = True

custo_oficial = taxa_junta + certidoes + alvara
honorarios = tabela_precos["abertura_me"]

total = custo_oficial + honorarios
# R$ 2.250,00
```

### 3. 🤖 AGENTE DE LEGALIZAÇÃO

**Função:** Execução de processos de legalização

**Responsabilidades:**
- Abertura de empresas (completo)
- Alterações societárias
- Regularizações e licenças
- Encerramento de empresas
- Controle de execução
- Checklist automático

**Processo de abertura:**
```
1. Viabilidade de nome → Junta Comercial
2. Contrato Social → Contract Manager
3. Registro Junta → Protocolo + Monitor
4. CNPJ → Receita Federal
5. Inscrição Municipal → Prefeitura
6. Alvará → Prefeitura + Monitor
7. Licenças especiais → Se aplicável
8. Entrega final → Documentos completos
```

### 4. 📡 MONITOR DE PROTOCOLOS

**Função:** Acompanhamento de processos em órgãos

**Responsabilidades:**
- Consultar protocolos automaticamente
- Alertar sobre movimentações
- Download de documentos
- Controle de vencimentos
- Relatórios de status

**Órgãos monitorados:**
```
├─ Juntas Comerciais (27 estados)
├─ Receita Federal (e-CAC)
├─ Prefeituras (5.570 municípios)
├─ Secretarias Estaduais
└─ Tribunais (PJe, e-SAJ)
```

**Alertas automáticos:**
```
Certidão vence em 30 dias → Email lembrete
Certidão vence em 15 dias → Email + Sistema
Certidão vence em 7 dias → Email + WhatsApp (URGENTE)
Certidão vencida → Alerta crítico + Gerente
```

### 5. 📄 GESTOR DE CONTRATOS

**Função:** Elaboração de documentos jurídicos

**Responsabilidades:**
- Contratos sociais (LTDA, EIRELI, SA)
- Alterações contratuais
- Atas de assembleia/reunião
- Distratos (encerramento)
- Contratos comerciais
- Templates customizados

**Sistema de merge:**
```python
template = load_template("contrato_social_ltda.docx")

dados = {
    "nome_empresa": "Silva Consultoria LTDA",
    "socio1_nome": "João da Silva",
    "socio1_cpf": "123.456.789-00",
    "capital_social": "R$ 10.000,00",
    # ... mais dados
}

contrato_final = template.merge(dados)
# Gera DOCX formatado e pronto
```

### 6. 📧 GESTOR DE COMUNICAÇÕES

**Função:** Comunicações oficiais com órgãos

**Responsabilidades:**
- Ofícios (Receita, Junta, Prefeitura)
- Requerimentos administrativos
- Notificações
- Respostas a exigências
- Recursos administrativos

**Exemplo:**
```
Junta emite exigência:
"Falta CEP completo no endereço"

Monitor detecta → Comunicações elabora resposta

RESPOSTA À EXIGÊNCIA
Processo: 2024/123456
[Texto formal com anexos]

Comunicações → Protocola → Monitor acompanha
```

### 7. 📁 ORGANIZADOR DE DOCUMENTOS

**Função:** Gestão documental completa

**Responsabilidades:**
- Estrutura de pastas padronizada
- Upload e indexação
- Sistema de busca avançada
- Controle de versões
- Relatórios gerenciais
- Alertas de vencimentos

**Estrutura de pastas:**
```
/cliente_cnpj/
├── societario/ (contratos, atas, certidões)
├── tributario/ (CNPJ, inscrições, certidões)
├── licencas/ (alvarás, licenças)
├── contratos/ (comerciais, serviços)
├── processos/ (por órgão)
├── comunicacoes/ (ofícios, notificações)
└── diversos/ (procurações, identificações)
```

### 8. 🙋 ASSISTENTE AO CLIENTE

**Função:** Atendimento humanizado

**Responsabilidades:**
- Primeiro contato (triagem)
- Responder dúvidas gerais
- Orientar procedimentos
- Consultar base de conhecimento
- Follow-up proativo
- TOM 100% HUMANO (sem parecer IA)

**Tom de voz:**
```
❌ EVITAR:
"Como IA, posso processar..."
"Meu algoritmo indica..."

✅ USAR:
"Claro! Deixa eu te ajudar..."
"Vou verificar aqui rapidinho..."
"Pela minha experiência, o ideal é..."
```

---

## 🔐 SEGURANÇA E COMPLIANCE

### Segurança de Dados

**Criptografia:**
- ✅ TLS 1.3 (transporte)
- ✅ AES-256 (armazenamento)
- ✅ Bcrypt cost 12 (senhas)
- ✅ JWT + Refresh tokens

**Isolamento Multi-tenant:**
- ✅ Schema separado por tenant
- ✅ Impossível acessar dados de outros
- ✅ Backup individual por tenant

**Autenticação:**
- ✅ Email + senha (obrigatório)
- ✅ 2FA (opcional usuários, obrigatório super admin)
- ✅ Sessões com timeout (2h inatividade)

### LGPD Compliance

**Atendimento completo:**
- ✅ Consentimento explícito
- ✅ Direito de acesso
- ✅ Direito de retificação
- ✅ Direito de exclusão
- ✅ Portabilidade de dados
- ✅ Encarregado designado
- ✅ Política de privacidade

**Retenção:**
- Dados ativos: Enquanto conta ativa
- Dados inativos: 30 dias após cancelamento
- Backups: 90 dias
- Logs: 5 anos (obrigação legal)

### Backup

**Estratégia:**
```
Diário: 03:00 AM, retenção 30 dias
Semanal: Domingo 02:00 AM, retenção 90 dias
Mensal: 1º domingo, retenção 1 ano

Storage: AWS S3 multi-região
Teste: Semanal (restore)
```

**Disaster Recovery:**
- RTO: 4 horas
- RPO: 24 horas

---

## 📊 ROADMAP

### Fase 1: MVP (0-4 meses) - EM DESENVOLVIMENTO

```
✓ LEG.Agents completo (8 agentes)
✓ Multi-tenancy funcional
✓ Painel Super Admin
✓ Painel Escritório
✓ Pagamentos (Asaas)
✓ Trial 14 dias
✓ 3 planos
✓ Onboarding
```

### Fase 2: Crescimento (4-12 meses)

```
├─ WhatsApp API integrado
├─ Email marketing
├─ OCR de documentos
├─ Assinatura digital (ICP-Brasil)
├─ Portal cliente final
├─ App mobile
├─ API REST + Webhooks
└─ White label
```

### Fase 3: Expansão (12-24 meses)

```
LEG.Fiscal (Novo Módulo):
├─ Apuração automática impostos
├─ SPED Fiscal
├─ Planejamento tributário
└─ Alertas de obrigações

LEG.Pessoal (Novo Módulo):
├─ Folha de pagamento
├─ eSocial
├─ Férias e rescisões
└─ Ponto eletrônico
```

### Fase 4: Consolidação (24-36 meses)

```
LEG.Contábil (Novo Módulo):
├─ Escrituração contábil
├─ Conciliação bancária
├─ Demonstrativos
└─ Indicadores

LEG.Suite:
└─ Todos os módulos integrados
```

---

## 🚀 PRÓXIMOS PASSOS

### Para Desenvolvimento (Claude Code)

**Sequência de Implementação:**

```
Sprint 1-2: Fundação
├─ Setup FastAPI + PostgreSQL
├─ Multi-tenancy (schema por tenant)
├─ Autenticação (JWT)
└─ CRUD básico

Sprint 3-4: Super Admin
├─ Dashboard Legia
├─ Gestão de escritórios
├─ Gestão de planos
└─ Integração Asaas

Sprint 5-6: Tenant Admin
├─ Dashboard escritório
├─ Gestão de usuários
├─ CRUD clientes
└─ Personalização

Sprint 7-10: LEG.Agents Core
├─ Orquestrador
├─ Agente Comercial
├─ Agente Legalização
└─ Monitor Protocolos

Sprint 11-12: LEG.Agents Completo
├─ Gestor Contratos
├─ Gestor Comunicações
├─ Organizador Documentos
└─ Assistente Cliente

Sprint 13-14: Polimento
├─ Testes E2E
├─ Performance
├─ Bugs
└─ Documentação

Sprint 15-16: Launch
├─ Deploy produção
├─ Beta (10 escritórios)
└─ Feedback
```

**Prazo MVP:** 4 meses (16 semanas)

### Stack Tecnológico

**Frontend:**
```
Next.js 14+ (App Router)
TypeScript
TailwindCSS + shadcn/ui
Zustand (state)
TanStack Query (data fetching)
```

**Backend:**
```
FastAPI (Python 3.11+)
SQLAlchemy 2.0 (ORM)
Pydantic V2 (validation)
PostgreSQL 15+
Redis 7+ (cache)
Celery (queue)
```

**IA:**
```
Google ADK (Agentic Development Kit)
Google Gemini 3.0 Flash/Pro
```

**Infraestrutura:**
```
Docker + Docker Compose
AWS / Google Cloud
GitHub Actions (CI/CD)
```

---

## 📄 CONCLUSÃO

Este PRD define o **MVP da LEGIA PLATFORM** - uma plataforma SaaS multi-tenant B2B para escritórios de contabilidade.

**O produto inicial (LEG.Agents)** automatiza processos de legalização empresarial usando 8 agentes de IA especializados.

**Próximos documentos:**
1. ✅ PRD-LEGIA-Platform.md (este documento)
2. 📝 Guia-Implementacao.md (passo a passo técnico)
3. 📝 Checklist-Adaptacoes.md (o que adaptar)
4. 📝 Database-Schema.md (estrutura completa)

**Pronto para desenvolvimento com Claude Code!** 🚀

---

**Aprovado por:** [Você - Proprietária da Legia]  
**Data de Aprovação:** 17/12/2025  
**Versão:** 1.0.0 - MVP