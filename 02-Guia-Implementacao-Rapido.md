# LEGIA PLATFORM - Guia de Implementação Rápido

## 🎯 COMO USAR ESTE GUIA

Este guia mostra **EXATAMENTE** como implementar a LEGIA PLATFORM usando Claude Code.

**Pré-requisitos:**
- ✅ Claude Code instalado
- ✅ VS Code (opcional)
- ✅ Terminal
- ✅ PRD lido e compreendido

---

## 📋 PASSO A PASSO COMPLETO

### PASSO 1: Preparação do Ambiente

```bash
# Criar diretório do projeto
mkdir legia-platform
cd legia-platform

# Abrir VS Code (opcional)
code .

# Iniciar Claude Code
claude
```

### PASSO 2: Criar o PRD

Crie o arquivo `prd.md` com o conteúdo do PRD fornecido (documento 01-PRD-LEGIA-Platform.md).

**IMPORTANTE:** Copie TODO o conteúdo do PRD para este arquivo!

### PASSO 3: Inicializar Projeto

```bash
/init
```

Claude vai ler o PRD e criar `.claude/claude.md` (memória do projeto).

**Quando perguntar sobre permissões:**
- Primeira vez: Opção 2 (confiar após ler)
- Depois: Sempre confiar

### PASSO 4: Configurar MCPs (OBRIGATÓRIO!)

```bash
/mcp
cloud mcp add context7
```

**Context7 é ESSENCIAL!** Fornece documentação atualizada.

Opcionais (adicionar depois):
```bash
cloud mcp add github  # Se quiser integração Git
```

### PASSO 5: Configurar Memória

```bash
/memory
```

Adicione estas regras CRÍTICAS:

```markdown
# REGRAS FUNDAMENTAIS - LEGIA PLATFORM

## ARQUITETURA
- Multi-tenant: Schema por tenant (PostgreSQL)
- Isolamento TOTAL de dados entre escritórios
- Subdomínio identifica tenant: escritorio.legiaplatform.com.br

## STACK OBRIGATÓRIO
- Backend: Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic V2
- Frontend: Next.js 14+, TypeScript, TailwindCSS, shadcn/ui
- Database: PostgreSQL 15+
- Cache: Redis 7+
- IA: Google ADK + Gemini 3.0
- Pagamentos: Asaas API (brasileiro)

## ESTRUTURA DE SCHEMAS
```
legia_platform_db/
├── public/ (dados da Legia - global)
│   ├── tenants
│   ├── plans
│   ├── subscriptions
│   ├── payments
│   └── legia_users
├── tenant_001/ (Escritório 1)
│   ├── users
│   ├── clients
│   ├── processes
│   └── ... (LEG.Agents)
└── tenant_002/ (Escritório 2)
    └── ... (mesma estrutura)
```

## 3 NÍVEIS DE ACESSO
1. Super Admin (Legia) → Acessa tudo
2. Tenant Admin (Escritório) → Acessa só seu tenant
3. Funcionário → Acessa clientes atribuídos

## 8 AGENTES LEG.AGENTS
1. Orquestrador (coordena tudo)
2. Agente Comercial (orçamentos)
3. Agente Legalização (processos)
4. Monitor Protocolos (acompanhamento)
5. Gestor Contratos (documentos)
6. Gestor Comunicações (ofícios)
7. Organizador Documentos (gestão)
8. Assistente Cliente (atendimento)

## SEGURANÇA (NÃO NEGOCIÁVEL)
- OWASP Top 10 mandatório
- LGPD compliance total
- Bcrypt cost 12 (senhas)
- JWT + Refresh tokens
- TLS 1.3
- 2FA obrigatório para super admins
- Log de auditoria TUDO
- Backup diário automático

## TESTES
- Após CADA fase (não no final!)
- Coverage mínimo: 80%
- Testes unitários + integração
- E2E para fluxos críticos

## PRIORIDADES
1. Multi-tenancy funcionando PERFEITO
2. Segurança e isolamento
3. Painel Super Admin básico
4. Painel Tenant básico
5. LEG.Agents (agentes por ordem)

## PORTUGUÊS BRASILEIRO
- Toda interface em PT-BR
- Termos brasileiros (não Portugal)
- Formatação BR (dd/mm/aaaa, R$)
- Timezone: America/Sao_Paulo

## SE TIVER DÚVIDA
- SEMPRE pergunte antes de decidir
- NÃO invente soluções
- NÃO adicione features não pedidas
- Consulte PRD e memória
```

### PASSO 6: Planejamento Detalhado

Ative o Plan Mode:
```
Shift + Tab
```

Envie este prompt:

```
Vamos planejar a implementação da LEGIA PLATFORM usando @prd.md

INSTRUÇÕES IMPORTANTES:

1. Usar @plan mode (OBRIGATÓRIO)

2. Planejamento DETALHADO em FASES
   - Fase 1: Fundação e Multi-tenancy
   - Fase 2: Painel Super Admin
   - Fase 3: Painel Tenant
   - Fase 4: LEG.Agents (agentes)
   - Fase 5: Integrações e Polimento

3. ARQUITETURA:
   - Multi-tenant com schema por tenant
   - 3 níveis de acesso
   - Isolamento total de dados

4. STACK (usar exatamente):
   - Backend: FastAPI + SQLAlchemy + Pydantic
   - Frontend: Next.js + TailwindCSS + shadcn/ui
   - Database: PostgreSQL (multi-schema)
   - IA: Google ADK + Gemini 3.0
   - Pagamentos: Asaas

5. SEGURANÇA:
   - OWASP Top 10 mandatório
   - LGPD compliance
   - Tudo em português brasileiro

6. PERGUNTAS:
   - Se tiver QUALQUER dúvida arquitetural, PERGUNTE
   - NÃO tome decisões sem confirmar
   - Verifique se entendeu TUDO do PRD

7. TESTES:
   - Após CADA fase (não no final)
   - Coverage > 80%

8. Documentar progresso em claude.md

Entendeu o escopo? Confirme ANTES de planejar!
```

### PASSO 7: Responder Perguntas do Claude

Claude vai fazer ~10-15 perguntas. Exemplos de respostas:

**Q: "Confirma multi-tenant com schema por tenant?"**
```
R: SIM! Schema separado por tenant no PostgreSQL.
Cada escritório = um schema (tenant_001, tenant_002, etc).
Isolamento TOTAL de dados.
```

**Q: "Qual LLM usar para os agentes?"**
```
R: Google Gemini 3.0
- Flash para operações rápidas (Comercial, Assistente)
- Pro para operações complexas (Legalização, Orquestrador)
```

**Q: "Gateway de pagamento?"**
```
R: Asaas (brasileiro)
- Boleto + PIX + Cartão
- Cobrança recorrente mensal
- Webhook para atualizar status
```

**Q: "Como identificar o tenant?"**
```
R: Por subdomínio
escritorio-abc.legiaplatform.com.br → tenant_001
escritorio-xyz.legiaplatform.com.br → tenant_002

Middleware extrai subdomain e define schema.
```

**Q: "Começar com dados de exemplo?"**
```
R: SIM!
- 1 super admin (você)
- 2 tenants de exemplo
- Cada tenant com 1 admin + 2 usuários + 5 clientes
```

### PASSO 8: Revisar e Aprovar Plano

Claude vai gerar um plano detalhado. REVISE TUDO:

```
Checklist de Revisão:
[ ] Multi-tenancy está correto?
[ ] 3 níveis de acesso definidos?
[ ] 8 agentes listados?
[ ] Stack correto (FastAPI, Next.js, PostgreSQL)?
[ ] Segurança incluída?
[ ] Testes após cada fase?
[ ] Fases bem divididas?
```

Se estiver OK:
```
y  # Aprovar e começar
```

Se tiver problemas:
```
n  # Recusar e ajustar
```

### PASSO 9: Acompanhar Implementação

Claude vai implementar fase por fase.

**Durante a execução:**
- Monitore o progresso
- Responda se Claude perguntar algo
- Teste após cada fase
- NÃO interrompa no meio (deixe terminar a fase)

**Se precisar pausar:**
```
ESC ESC  # Pausa
```

**Se der erro:**
- Claude vai tentar corrigir automaticamente
- Se persistir, compartilhe o erro completo

### PASSO 10: Testar Cada Fase

**Fase 1 concluída?**
```bash
# Testar multi-tenancy
python -m pytest backend/tests/

# Testar se schemas foram criados
psql -h localhost -U postgres -d legia_platform_db -c "\dn"

# Deve mostrar:
# public
# tenant_001
# tenant_002
```

**Fase 2 concluída?**
```bash
# Rodar backend
cd backend
uvicorn app.main:app --reload

# Acessar super admin
http://localhost:8000/admin/login
```

**Fase 3 concluída?**
```bash
# Rodar frontend
cd frontend
npm run dev

# Acessar tenant
http://escritorio-001.localhost:3000
```

---

## 🐛 TROUBLESHOOTING

### Problema: Claude não lê o PRD completo

**Solução:**
```
"Por favor, leia COMPLETAMENTE o arquivo @prd.md antes de planejar.
Confirme que entendeu:
- Multi-tenancy com schemas
- 3 níveis de acesso
- 8 agentes
- Planos e pagamentos"
```

### Problema: Contexto cheio

**Sintoma:** "Compactando conversação..."

**Solução:** Deixe compactar. Se piorar:
```bash
/clean
/memory  # Recarregar memória
```

### Problema: Dependências desatualizadas

**Após implementação:**
```
"Atualize TODAS as dependências para versões mais recentes:
- backend/requirements.txt
- frontend/package.json
Use versões stable (não beta)."
```

### Problema: Testes falhando

**Solução:**
```
"Analise TODOS os testes que falharam.
Corrija cada um.
Re-execute TODOS os testes.
Só continue após 100% passing."
```

### Problema: Multi-tenancy não funciona

**Verificar:**
```python
# Middleware está configurado?
# app/middleware/tenant.py

# Schema é definido por request?
request.state.schema = f"tenant_{tenant_id}"

# Queries usam o schema?
set_search_path(request.state.schema)
```

---

## ✅ CHECKLIST COMPLETO

### Antes de Começar
- [ ] Claude Code instalado
- [ ] PRD criado (prd.md)
- [ ] Entendeu o conceito multi-tenant
- [ ] Entendeu os 3 níveis de acesso
- [ ] Entendeu os 8 agentes

### Setup Inicial
- [ ] Diretório criado
- [ ] Claude iniciado
- [ ] PRD criado
- [ ] /init executado
- [ ] MCPs configurados (Context7)
- [ ] Memória configurada

### Planejamento
- [ ] Plan Mode ativado
- [ ] Prompt detalhado enviado
- [ ] Perguntas respondidas
- [ ] Plano revisado
- [ ] Plano aprovado

### Implementação
- [ ] Fase 1: Fundação ✓
- [ ] Fase 2: Super Admin ✓
- [ ] Fase 3: Tenant Admin ✓
- [ ] Fase 4: LEG.Agents ✓
- [ ] Fase 5: Integrações ✓

### Testes
- [ ] Testes unitários > 80%
- [ ] Multi-tenancy funcionando
- [ ] 3 níveis de acesso OK
- [ ] Isolamento de dados OK
- [ ] Agentes respondendo

### Finalização
- [ ] Documentação completa
- [ ] README atualizado
- [ ] .env.example criado
- [ ] Docker funcionando
- [ ] Pronto para deploy

---

## 🚀 PRÓXIMOS PASSOS APÓS MVP

1. Deploy em staging
2. Beta com 5-10 escritórios
3. Coletar feedback
4. Ajustar baseado em uso real
5. Deploy em produção
6. Marketing e vendas
7. Crescimento! 📈

---

## 📞 DÚVIDAS?

Se travar em algum passo:
1. Revise este guia
2. Consulte o PRD
3. Verifique a memória (.claude/claude.md)
4. Pause (ESC ESC) e analise
5. Pergunte ao Claude especificamente

**Boa sorte! Você vai criar algo incrível! 🎉**

---

**Versão:** 1.0.0  
**Data:** 17/12/2024  
**Próximo documento:** 03-Checklist-Adaptacoes.md
