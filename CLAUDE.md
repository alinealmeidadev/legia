# CLAUDE.md - Memória de Contexto do Projeto LEGIA
**Última atualização:** 06/01/2026
**Status do Projeto:** 72% Concluído (MVP avançado, mas incompleto para produção)

---

## 🔑 API KEYS E CREDENCIAIS

### Google Gemini (IA dos Agentes)
```
AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
```

### Asaas Sandbox (Pagamentos - NÃO IMPLEMENTADO AINDA)
```
$aact_hmlg_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZDJkYWNiLTZlMmMtNGJlMC04NDRkLTE3YmIwYzgzYzViZTo6JGFhY2hfNzA2NDcxZTYtZTJkMS00NjE1LWI4YWItMTRmZDEzYWNkMGJh
```

### Logins de Teste

**Super Admin (Legia):**
- Email: `admin@legia.com`
- Senha: `Admin@123`
- Tenant ID: (vazio)
- Acesso: Gestão de todos os tenants

**Tenant ABC Contabilidade:**
- Email: `admin@abc.com`
- Senha: `admin123`
- Tenant ID: 1
- Schema: `tenant_1`

**Tenant XYZ Contabilidade:**
- Email: `admin@xyz.com`
- Senha: `admin123`
- Tenant ID: 2
- Schema: `tenant_2`

---

## 🌐 URLs E DEPLOYS

**Frontend (Next.js):**
- URL: https://legia-git-main-aline-almeidas-projects.vercel.app
- Status: ✅ ONLINE no Vercel
- Deploy: Automático via Git push

**Backend (FastAPI):**
- URL Produção: ❌ NÃO DEPLOYADO (PROBLEMA CRÍTICO!)
- URL Local: http://localhost:8000
- Status: ⚠️ Só funciona localmente
- Problema: Frontend no Vercel tenta chamar localhost (não funciona)

**Banco de Dados:**
- PostgreSQL 15+ (local via Docker)
- Status: ⚠️ Docker não está rodando atualmente

**Redis:**
- Cache local via Docker
- Status: ⚠️ Docker não está rodando atualmente

---

## 📊 ESTADO ATUAL DO PROJETO

### O QUE JÁ ESTÁ 100% PRONTO E FUNCIONAL

#### 1. Infraestrutura Backend (95%)
- ✅ FastAPI estruturado com rotas organizadas
- ✅ PostgreSQL multi-tenant (schema por tenant)
- ✅ Redis configurado
- ✅ Docker Compose completo
- ✅ Alembic migrations automáticas
- ✅ Sistema de seeds (dados iniciais)
- ✅ JWT Authentication
- ✅ CORS configurado para Vercel
- ✅ Health checks
- ✅ Tratamento de erros padronizado
- ✅ Logging estruturado

#### 2. Agentes de IA (100% - TODOS IMPLEMENTADOS!)
**Status: 9/9 agentes criados e 27/27 testes passando**

1. **Orquestrador** (300+ linhas)
   - Analisa intenção do usuário
   - Roteia para agente correto
   - Gerencia contexto multi-turno
   - Sistema de delegação

2. **Agente Comercial** (250+ linhas)
   - Gera orçamentos automáticos (R$ 1.800 - R$ 5.800)
   - Tabela de preços completa
   - Breakdown detalhado de custos
   - Qualificação de leads

3. **Agente de Legalização** (280+ linhas)
   - Abertura de empresas
   - Alterações contratuais
   - Regularizações
   - Encerramento
   - Checklist automático

4. **Gestor de Contratos** (200+ linhas)
   - Geração de contratos sociais
   - Alterações contratuais
   - Atas de assembleia
   - Sistema de templates

5. **Monitor de Protocolos** (220+ linhas)
   - Acompanhamento de protocolos
   - Alertas de pendências
   - Cálculo de vencimentos
   - Atualização de status

6. **Agente de Protocolos** (180+ linhas)
   - Geração de protocolos
   - Validação de documentos
   - Cálculo de taxas

7. **Assistente ao Cliente** (280+ linhas)
   - Primeiro contato humanizado
   - FAQ integrada (50+ perguntas)
   - Tom 100% humano
   - Delegação para especialistas

8. **Gestor de Comunicações** (200+ linhas)
   - Ofícios para órgãos
   - Requerimentos administrativos
   - Notificações
   - Respostas a exigências

9. **Organizador de Documentos** (180+ linhas)
   - Estrutura de pastas padronizada
   - Indexação de documentos
   - Sistema de busca
   - Controle de vencimentos

**Total: ~2.500 linhas de código IA**
**Localização:** `backend/app/services/agents/`

#### 3. API Endpoints Backend (85%)

**Autenticação (100%):**
- POST `/api/v1/auth/login` - Login com JWT
- POST `/api/v1/auth/refresh` - Renovar token
- POST `/api/v1/auth/logout` - Logout
- GET `/api/v1/auth/me` - Dados do usuário logado

**Tenants - Super Admin (100%):**
- GET `/api/v1/tenants/` - Listar todos
- POST `/api/v1/tenants/` - Criar novo tenant
- GET `/api/v1/tenants/{id}` - Detalhes
- PUT `/api/v1/tenants/{id}` - Atualizar
- DELETE `/api/v1/tenants/{id}` - Deletar
- GET `/api/v1/tenants/stats` - Estatísticas

**Clientes (100%):**
- GET `/api/v1/clients/` - Listar (com paginação)
- POST `/api/v1/clients/` - Criar cliente PF/PJ
- GET `/api/v1/clients/{id}` - Detalhes
- PUT `/api/v1/clients/{id}` - Atualizar
- DELETE `/api/v1/clients/{id}` - Deletar
- POST `/api/v1/clients/import` - Importar Excel

**Processos (100%):**
- GET `/api/v1/processes/` - Listar
- POST `/api/v1/processes/` - Criar processo
- GET `/api/v1/processes/{id}` - Detalhes
- PUT `/api/v1/processes/{id}` - Atualizar
- DELETE `/api/v1/processes/{id}` - Deletar
- GET `/api/v1/processes/stats` - Estatísticas
- GET `/api/v1/processes/{id}/timeline` - Histórico

**Agentes IA (100%):**
- POST `/api/v1/agents/chat` - Conversar com IA
- GET `/api/v1/agents/agents/status` - Status dos agentes

**Setup (100%):**
- POST `/api/v1/setup/init` - Inicializar banco
- POST `/api/v1/setup/seed` - Popular dados de teste

**Workflows (50% - PARCIAL):**
- POST `/api/v1/workflows/abertura` - Abertura (parcial)
- POST `/api/v1/workflows/alteracao` - Alteração (parcial)
- POST `/api/v1/workflows/baixa` - Encerramento (parcial)

#### 4. Frontend (90%)

**Páginas Super Admin (100%):**
- `/admin` - Dashboard
- `/admin/tenants` - Gestão de tenants (CRUD completo)
- `/admin/plans` - Gestão de planos
- `/admin/users` - Gestão de super admins
- `/admin/settings` - Configurações
- `/admin/support` - Suporte

**Páginas Tenant (90%):**
- `/tenant` - Dashboard
- `/tenant/clients` - Gestão de clientes (CRUD completo)
- `/tenant/processes` - Gestão de processos
- `/tenant/automation` - Automação de processos
- `/tenant/contracts` - Contratos (50% implementado)
- `/tenant/communications` - Comunicações (50% implementado)
- `/tenant/documents` - Documentos (50% implementado)
- `/tenant/settings` - Configurações

**Componentes Especiais:**
- Chat Widget IA (280 linhas) - Flutuante em todas as páginas
- 15+ componentes UI (shadcn/ui)
- Import Excel Dialog
- Client/Tenant/Process Form Dialogs
- Filtros e paginação

#### 5. Banco de Dados (100%)

**Schema Public (Legia/Super Admin):**
- `legia_users` - Super admins
- `tenants` - Escritórios contratantes
- `plans` - Planos de assinatura
- `subscriptions` - Assinaturas ativas
- `payments` - Pagamentos

**Schema Tenant (Por Escritório):**
- `users` - Usuários do escritório
- `clients` - Clientes finais PF/PJ
- `processes` - Processos de legalização
- `protocols` - Protocolos em órgãos
- `documents` - Documentos
- `quotes` - Orçamentos
- `communications` - Comunicações oficiais
- `chat_messages` - Histórico de conversas IA

**Migrations:**
- ✅ Sistema Alembic configurado
- ✅ Auto-criação de schemas por tenant
- ✅ Migrations automáticas no startup

---

## ⚠️ PROBLEMAS CRÍTICOS CONHECIDOS

### 🔴 PROBLEMA #1: Backend Não Deployado (BLOQUEADOR)
**Descrição:**
- Frontend está no Vercel mas backend só roda localmente
- Frontend tenta chamar `http://localhost:8000` (não funciona online)
- Sistema completamente inutilizável em produção

**Impacto:** Sistema não pode ser usado por ninguém além de você localmente

**Solução:**
- Fazer deploy do backend no Render.com (plano gratuito)
- Seguir instruções em `DEPLOY_GRATUITO.md`
- Atualizar variáveis de ambiente no Vercel
- Tempo estimado: 30 minutos

**Status:** ❌ NÃO RESOLVIDO

---

### 🔴 PROBLEMA #2: Fluxo de Alteração Contratual Incorreto (CRÍTICO)
**Descrição:**
O sistema atual trata cada tipo de alteração como um processo separado:
- `/tenant/automation/alteracao-endereco`
- `/tenant/automation/alteracao-socios`
- `/tenant/automation/alteracao-capital`
- `/tenant/automation/alteracao-atividade`

**Problema:**
Na vida real, um cliente pode querer fazer VÁRIAS alterações de uma vez:
- Mudar endereço + Adicionar sócio + Aumentar capital = 1 processo único
- Atualmente o sistema força a criar 3 processos separados (ERRADO!)

**Solução Correta:**
- UMA página `/tenant/automation/alteracao-contratual`
- Checkboxes de múltipla escolha:
  - [ ] Alteração de Endereço
  - [ ] Alteração de Sócios
  - [ ] Alteração de Capital Social
  - [ ] Alteração de Atividade
  - [ ] Alteração de Nome Empresarial
  - [ ] Alteração de Objeto Social
- Cliente marca TODAS as alterações que quer
- Sistema cria UM processo único com múltiplas alterações

**Detalhes completos:** `BRIEFING-MELHORIAS.md` - FASE 1

**Impacto:** Usabilidade ruim, não reflete processo real

**Status:** ❌ NÃO RESOLVIDO

---

### 🟡 PROBLEMA #3: Docker Não Está Rodando
**Descrição:**
- Docker Desktop não está ativo no ambiente
- Backend e banco de dados locais não estão acessíveis

**Impacto:** Não consegue testar localmente

**Solução:** Iniciar Docker Desktop e rodar `docker-compose up -d`

**Status:** ⚠️ PENDENTE

---

## 🚧 O QUE FALTA IMPLEMENTAR

### URGENTE (Bloqueadores de Produção)

#### 1. Deploy do Backend (30 minutos)
- ❌ Backend no Render.com
- ❌ Configurar variáveis de ambiente
- ❌ Conectar ao PostgreSQL (ElephantSQL ou Render)
- ❌ Atualizar frontend para usar URL de produção
- **Guia:** `DEPLOY_GRATUITO.md`

#### 2. Corrigir Fluxo de Alteração (3-4 horas)
- ❌ Criar página única de alteração contratual
- ❌ Sistema de checkboxes múltiplos
- ❌ Backend aceitar array de tipos de alteração
- ❌ Remover páginas separadas antigas
- **Detalhes:** `BRIEFING-MELHORIAS.md` - FASE 1

---

### IMPORTANTE (Funcionalidades Essenciais)

#### 3. Consulta CNPJ Automática (1-2 horas)
- ❌ API ReceitaWS (gratuita, 3 req/min)
- ❌ Auto-preenchimento de dados da empresa
- ❌ Validação de CNPJ
- **Código pronto em:** `BRIEFING-MELHORIAS.md` - FASE 2
- **Custo:** R$ 0

#### 4. Consulta CEP Automática (30 minutos)
- ❌ API ViaCEP (gratuita, ilimitada)
- ❌ Auto-preenchimento de endereço
- **Código pronto em:** `BRIEFING-MELHORIAS.md` - FASE 2
- **Custo:** R$ 0

#### 5. Sistema de Pagamentos Asaas (6-8 horas)
- ❌ Integração com API Asaas
- ❌ Geração de cobranças
- ❌ Webhooks de pagamento
- ❌ Controle de inadimplência
- **Chave sandbox já disponível acima**
- **Custo:** R$ 0 (sandbox), produção 1.49% + R$0.49/transação

#### 6. WhatsApp Business API (4-6 horas)
- ❌ Escolher provider (Digisac / Twilio / Evolution API)
- ❌ Envio de notificações
- ❌ Atendimento automatizado
- ❌ Integração com agentes IA
- **Custo:** R$ 50-200/mês

#### 7. Upload e Gestão de Documentos (4-6 horas)
- ❌ Upload drag & drop
- ❌ Storage (AWS S3 ou local)
- ❌ Preview de PDFs
- ❌ Download
- ❌ Versionamento
- ❌ Controle de acesso

---

### MÉDIO PRAZO (Polimento e Qualidade)

#### 8. Workflows Completos (10-15 horas)
- ❌ Fluxo completo de abertura
- ❌ Fluxo completo de alteração (após corrigir)
- ❌ Fluxo completo de encerramento
- ❌ Validações e regras de negócio
- ❌ Estados intermediários

#### 9. Dashboard Avançado (3-4 horas)
- ❌ Gráficos (Chart.js ou Recharts)
- ❌ KPIs em tempo real
- ❌ Filtros avançados
- ❌ Relatórios exportáveis (PDF, Excel)

#### 10. Testes Automatizados (8-10 horas)
- ❌ Testes unitários (pytest)
- ❌ Testes de integração
- ❌ Testes E2E (Playwright)
- ❌ Cobertura >80%
- ❌ CI/CD (GitHub Actions)

---

## 📈 PROGRESSO E MÉTRICAS

**Funcionalidades Core:**
- Infraestrutura: 95% ✅
- Agentes IA: 100% ✅
- API Backend: 85% 🟡
- Frontend: 90% ✅
- Banco de Dados: 100% ✅
- Integrações: 10% ❌
- Testes: 30% ❌
- Deploy: 50% 🟡 (frontend sim, backend não)

**Geral:** 72% concluído

**Tempo já investido:** ~100-120 horas

**Tempo estimado para MVP 100%:** 44-64 horas
- Para MVP mínimo funcional: 15-20 horas
- Trabalhando 4h/dia: 4-5 dias úteis

---

## 🎯 PRÓXIMOS PASSOS RECOMENDADOS

### Opção 1: MVP Mínimo Funcional (15-20 horas)
1. ✅ Deploy backend (30 min) - CRÍTICO
2. ✅ CNPJ + CEP (2-3h) - Alto impacto
3. ✅ Corrigir alteração (3-4h) - Usabilidade
4. ✅ Asaas pagamentos (6-8h) - Monetização
5. ✅ Ajustes finais (2-3h)

### Opção 2: MVP Completo (40-50 horas)
- MVP Mínimo +
- WhatsApp (4-6h)
- Upload docs (4-6h)
- Workflows completos (10-15h)
- Testes (8-10h)

---

## 📚 ARQUIVOS DE DOCUMENTAÇÃO IMPORTANTES

**Status e Análise:**
- `PROJECT_STATUS.md` - Status geral
- `STATUS_PROJETO_COMPLETO.md` - Análise detalhada (72%)
- `STATUS_LOGIN_CONSERTADO.md` - Correção do login
- `CAPACIDADES_REAIS_VS_LIMITACOES.md` - O que funciona vs não funciona

**Guias e Instruções:**
- `README.md` - Documentação geral
- `QUICKSTART.md` - Guia rápido de inicialização
- `DEPLOY_GRATUITO.md` - Como fazer deploy gratuito
- `BRIEFING-MELHORIAS.md` - Melhorias prioritárias com código

**Técnicos:**
- `01-PRD-LEGIA-Platform.md` - Product Requirements Document
- `04-Database-Schema.md` - Schema completo do banco
- `FAQ_TECNICA_AGENTES.md` - FAQ sobre agentes IA

**Planejamento:**
- `PROXIMOS_PASSOS.md` - Próximas ações
- `VERSIONS.md` - Versões completas de todas tecnologias

---

## 💡 INFORMAÇÕES TÉCNICAS IMPORTANTES

### Stack Tecnológica
**Backend:**
- Python 3.13.7 (local) / 3.11+ (recomendado produção)
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Alembic 1.13.1
- PostgreSQL 15+
- Redis 5.0.1 (Python client) / 7.x (servidor)
- Google Gemini API (gemini-1.5-pro)
- JWT - python-jose 3.3.0

**Frontend:**
- Next.js 14.0.4 (App Router)
- React 18.2.0
- TypeScript 5.3.3
- TailwindCSS 3.4.0
- shadcn/ui (Radix UI)
- React Query 5.17.9
- Zustand 4.4.7

**Desenvolvimento:**
- Claude Code (Claude Sonnet 4.5 - claude-sonnet-4-5-20250929)
- Docker 20.x+ / Docker Compose 2.x+

**Versões completas:** Ver arquivo `VERSIONS.md`

### Estrutura de Pastas
```
LEGIA/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # Rotas
│   │   ├── core/           # Config
│   │   ├── db/             # Database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Lógica de negócio
│   │   │   └── agents/     # 9 agentes IA
│   │   └── utils/          # Utilidades
│   ├── alembic/            # Migrations
│   └── tests/              # Testes
├── frontend/
│   ├── app/                # Next.js App Router
│   │   ├── admin/          # Super admin
│   │   └── tenant/         # Tenant
│   ├── components/         # Componentes React
│   └── lib/                # Utilidades
└── docker-compose.yml
```

### Variáveis de Ambiente Críticas

**Backend (.env):**
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/legia
REDIS_URL=redis://localhost:6379
GOOGLE_API_KEY=AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
SECRET_KEY=sua-chave-secreta-jwt
ASAAS_API_KEY=$aact_hmlg_...
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🔄 ÚLTIMAS ALTERAÇÕES (Git Log)

**Commits Recentes:**
- `87522ea` - Fix: CORS completo
- `3861d2e` - Fix: CORS completo
- `5f007bd` - correção automação e cord
- `ebf73b7` - fix: correções cirúrgicas - modal único e build corrigido
- `3d7e135` - correção processo -> workflow e navegação

**Foco recente:**
- Correções de CORS para Vercel-Backend
- Ajustes no fluxo de login
- Correções em automação de processos
- Build no Vercel
- Navegação entre páginas

---

## ⚡ COMANDOS ÚTEIS

### Backend
```bash
# Iniciar com Docker
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f backend

# Criar migration
docker-compose exec backend alembic revision --autogenerate -m "descricao"

# Aplicar migrations
docker-compose exec backend alembic upgrade head

# Seeds
curl -X POST http://localhost:8000/api/v1/setup/seed
```

### Frontend
```bash
# Instalar dependências
npm install

# Rodar localmente
npm run dev

# Build
npm run build

# Deploy Vercel
git push  # Deploy automático
```

---

## 🎨 CAPACIDADES REAIS vs LIMITAÇÕES

### O Sistema FAZ (100% Automático):
✅ Gera orçamentos automáticos
✅ Cria contratos sociais
✅ Organiza documentos
✅ Envia notificações
✅ Mantém histórico
✅ Calcula prazos e valores
✅ Chat IA 24/7
✅ Multi-tenant completo

### O Sistema PREPARA (Humano Valida):
🟡 Documentos contratuais (IA gera, humano revisa)
🟡 Protocolos (IA prepara, humano protocola)
🟡 Análise de viabilidade
🟡 Comunicações oficiais
🟡 Decisões comerciais

### O Sistema ORIENTA (Apenas Consultivo):
🔵 Login em portais governamentais
🔵 Resolução de CAPTCHA
🔵 Submissão real de protocolos
🔵 Pagamento de taxas
🔵 Assinatura digital
🔵 Upload em sistemas externos

### Limitações Técnicas/Legais:
❌ NÃO pode fazer login automático em Gov.br/Jucesp (CAPTCHA + termos de uso)
❌ NÃO pode consultar status em tempo real sem API
❌ NÃO pode fazer scraping (viola termos)
❌ NÃO pode assinar documentos (certificado digital necessário)
❌ NÃO pode pagar taxas automaticamente (integração bancária restrita)

---

## 📞 SUPORTE E RECURSOS

**Documentação Google Gemini:**
- https://ai.google.dev/

**Documentação Asaas:**
- https://docs.asaas.com/

**Issues conhecidos:**
- Ver `BRIEFING-MELHORIAS.md`
- Ver `CAPACIDADES_REAIS_VS_LIMITACOES.md`

---

## 🏁 CRITÉRIOS DE CONCLUSÃO DO MVP

**MVP será considerado 100% quando:**
1. ✅ Backend deployado e acessível online
2. ✅ Frontend conectando ao backend de produção
3. ✅ Fluxo de alteração contratual corrigido
4. ✅ Consultas CNPJ e CEP funcionando
5. ✅ Sistema de pagamentos Asaas integrado
6. ✅ Upload de documentos funcionando
7. ✅ Todos os workflows core completos
8. ✅ Testes automatizados básicos (>60% cobertura)
9. ✅ Sem erros críticos conhecidos
10. ✅ Documentação de uso atualizada

**Estimativa:** 2-3 semanas de trabalho focado (4h/dia)

---

## 🎯 FOCO ATUAL (Atualizar a cada sessão)

**Última sessão:** 06/01/2026
**Trabalhando em:** Atualização deste arquivo de memória
**Próximo passo:** Aguardando definição do usuário

**Opções sugeridas:**
1. 🚀 Deploy do backend (resolver bloqueador)
2. 🔧 Corrigir fluxo de alteração contratual
3. 🔌 Integrar CNPJ + CEP
4. 📊 Outra tarefa específica

---

**FIM DO ARQUIVO DE CONTEXTO**
