# 🎯 DECISÕES TÉCNICAS - LEGIA Platform
**Registro de Decisões Arquiteturais (ADR - Architecture Decision Records)**

---

## 📋 COMO USAR ESTE ARQUIVO

Sempre que tomar uma decisão técnica importante:
1. Documente o contexto
2. Liste as opções consideradas
3. Explique a decisão tomada
4. Justifique os motivos
5. Liste consequências (positivas e negativas)

---

## DECISÃO #1: Arquitetura Multi-Tenant

**Data:** Outubro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de arquitetura

### Contexto
Precisávamos definir como isolar dados de diferentes escritórios contábeis (tenants) no mesmo banco de dados.

### Opções Consideradas
1. **Banco separado por tenant** - Um banco PostgreSQL para cada escritório
2. **Schema separado por tenant** - Um schema PostgreSQL para cada escritório
3. **Coluna tenant_id em todas tabelas** - Tabelas compartilhadas com filtro por tenant_id

### Decisão
Escolhemos **Schema separado por tenant** (#2)

### Justificativa
**Prós:**
- ✅ Isolamento de dados forte (schema = namespace isolado)
- ✅ Mais barato que bancos separados
- ✅ Backup e restore por tenant
- ✅ Migrations independentes por tenant
- ✅ Melhor performance que tenant_id (sem filtros em todas queries)
- ✅ Escalável (centenas de tenants no mesmo PostgreSQL)

**Contras:**
- ❌ Mais complexo que tenant_id
- ❌ Precisa lógica para criar/deletar schemas dinamicamente
- ❌ Migrations precisam rodar em todos os schemas

### Consequências
- ✅ Implementado sistema automático de criação de schemas
- ✅ SQLAlchemy configurado para trocar schema dinamicamente
- ✅ Migrations Alembic aplicadas em todos schemas no startup
- ⚠️ Precisa gerenciar conexões por schema

### Arquivos Afetados
- `backend/app/db/base.py` - Configuração de schemas
- `backend/app/db/migrations.py` - Sistema de migrations
- `backend/app/core/deps.py` - Dependência para obter schema do tenant

---

## DECISÃO #2: Google Gemini como IA dos Agentes

**Data:** Novembro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de IA

### Contexto
Precisávamos escolher qual LLM usar para os 9 agentes de IA.

### Opções Consideradas
1. **OpenAI GPT-4** - Líder de mercado
2. **Google Gemini Pro** - Concorrente do Google
3. **Claude (Anthropic)** - Especializado em raciocínio
4. **LLaMA 2 (open source)** - Auto-hospedado

### Decisão
Escolhemos **Google Gemini Pro** (#2)

### Justificativa
**Prós:**
- ✅ Custo mais baixo que GPT-4
- ✅ Boa qualidade para caso de uso (assistente comercial)
- ✅ Generosa free tier para testes
- ✅ Latência aceitável
- ✅ Suporte a português BR nativo

**Contras:**
- ❌ Não tão bom quanto GPT-4 em raciocínio complexo
- ❌ Menos adoção no mercado
- ❌ API menos madura

### Consequências
- ✅ Economiza ~50% vs GPT-4
- ✅ 9 agentes implementados com sucesso
- ✅ 27 testes passando
- ⚠️ Pode precisar migrar para GPT-4 no futuro se qualidade não for suficiente

### Arquivos Afetados
- `backend/app/services/agents/` - Todos os 9 agentes
- `backend/app/core/config.py` - GOOGLE_API_KEY

### Custos (Estimativa)
- **Gemini Pro:** ~R$ 50-100/mês (1M tokens)
- **GPT-4:** ~R$ 100-200/mês (1M tokens)
- **Economia:** 50%

---

## DECISÃO #3: Next.js 14 com App Router (Frontend)

**Data:** Outubro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de frontend

### Contexto
Precisávamos escolher framework frontend para SaaS B2B.

### Opções Consideradas
1. **Next.js 14 (App Router)** - Framework React moderno
2. **Next.js 13 (Pages Router)** - Versão anterior mais estável
3. **Vite + React Router** - SPA puro
4. **Remix** - Alternativa ao Next.js

### Decisão
Escolhemos **Next.js 14 com App Router** (#1)

### Justificativa
**Prós:**
- ✅ SSR (Server-Side Rendering) para SEO
- ✅ App Router é o futuro do Next.js
- ✅ Server Components reduzem JS no cliente
- ✅ Streaming e suspense nativos
- ✅ Deploy fácil no Vercel (mesmos criadores)
- ✅ Grande comunidade

**Contras:**
- ❌ App Router ainda novo (bugs ocasionais)
- ❌ Curva de aprendizado (Server vs Client Components)
- ❌ Documentação ainda em evolução

### Consequências
- ✅ Deploy no Vercel funcionando perfeitamente
- ✅ Performance excelente (Server Components)
- ⚠️ Alguns bugs corrigidos (build, navegação)

### Arquivos Afetados
- `frontend/app/` - Toda estrutura App Router
- `frontend/next.config.js` - Configuração

---

## DECISÃO #4: shadcn/ui para Componentes UI

**Data:** Novembro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de frontend

### Contexto
Precisávamos de biblioteca de componentes UI profissional para SaaS B2B.

### Opções Consideradas
1. **shadcn/ui** - Componentes copiáveis (não biblioteca)
2. **Material UI** - Biblioteca consolidada
3. **Ant Design** - Popular no mercado
4. **Chakra UI** - Simples e acessível

### Decisão
Escolhemos **shadcn/ui** (#1)

### Justificativa
**Prós:**
- ✅ Componentes copiados no projeto (não dependência externa)
- ✅ Full controle sobre código
- ✅ Baseado em Radix UI (acessibilidade)
- ✅ TailwindCSS (consistência)
- ✅ Moderno e bonito
- ✅ Leve (sem biblioteca gigante)

**Contras:**
- ❌ Precisa copiar/atualizar componentes manualmente
- ❌ Menos componentes prontos que Material UI

### Consequências
- ✅ 15+ componentes implementados
- ✅ Consistência visual excelente
- ✅ Bundle size pequeno
- ⚠️ Atualizações manuais (mas raro precisar)

### Arquivos Afetados
- `frontend/components/ui/` - Componentes shadcn/ui
- `frontend/lib/utils.ts` - Utilitários (cn, etc)

---

## DECISÃO #5: FastAPI (Backend)

**Data:** Outubro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de backend

### Contexto
Precisávamos escolher framework backend Python.

### Opções Consideradas
1. **FastAPI** - Framework moderno assíncrono
2. **Django + DRF** - Framework completo
3. **Flask** - Microframework simples

### Decisão
Escolhemos **FastAPI** (#1)

### Justificativa
**Prós:**
- ✅ Performance (assíncrono)
- ✅ Tipagem forte (Pydantic)
- ✅ OpenAPI automático (Swagger)
- ✅ Validação automática
- ✅ Moderno e ativa comunidade
- ✅ Fácil integração com SQLAlchemy

**Contras:**
- ❌ Menos "batteries included" que Django
- ❌ Precisa configurar mais coisas manualmente

### Consequências
- ✅ API bem documentada (Swagger automático)
- ✅ Validação robusta (Pydantic schemas)
- ✅ Performance excelente
- ⚠️ Precisou configurar CORS, Auth, etc manualmente

### Arquivos Afetados
- `backend/app/main.py` - Aplicação FastAPI
- `backend/app/api/v1/` - Rotas
- `backend/app/schemas/` - Pydantic schemas

---

## DECISÃO #6: PostgreSQL (Banco de Dados)

**Data:** Outubro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de arquitetura

### Contexto
Precisávamos escolher banco de dados relacional.

### Opções Consideradas
1. **PostgreSQL** - Open source robusto
2. **MySQL** - Popular e simples
3. **SQLite** - Leve para desenvolvimento

### Decisão
Escolhemos **PostgreSQL** (#1)

### Justificativa
**Prós:**
- ✅ Suporte nativo a **schemas** (essencial para multi-tenant!)
- ✅ JSONB para dados semi-estruturados
- ✅ Full-text search nativo
- ✅ Extensível (postgis, timescale, etc)
- ✅ ACID compliant
- ✅ Open source e gratuito

**Contras:**
- ❌ Mais pesado que MySQL
- ❌ Curva de aprendizado (features avançadas)

### Consequências
- ✅ Schemas permitem isolamento perfeito por tenant
- ✅ Performance excelente
- ✅ JSONB usado em alguns campos (metadata, etc)

### Arquivos Afetados
- `docker-compose.yml` - PostgreSQL 15
- `backend/app/db/` - Configuração SQLAlchemy

---

## DECISÃO #7: Vercel (Deploy Frontend)

**Data:** Dezembro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de DevOps

### Contexto
Precisávamos fazer deploy do frontend Next.js.

### Opções Consideradas
1. **Vercel** - Criadores do Next.js
2. **Netlify** - Concorrente popular
3. **AWS Amplify** - Solução AWS
4. **Docker + VPS** - Auto-hospedado

### Decisão
Escolhemos **Vercel** (#1)

### Justificativa
**Prós:**
- ✅ Integração perfeita com Next.js
- ✅ Deploy automático via Git
- ✅ Preview deploys (cada PR)
- ✅ Edge functions gratuitas
- ✅ CDN global
- ✅ Plano gratuito generoso

**Contras:**
- ❌ Vendor lock-in
- ❌ Limites do plano gratuito (bandwidth)

### Consequências
- ✅ Frontend online: https://legia-git-main-aline-almeidas-projects.vercel.app
- ✅ Deploy em segundos
- ⚠️ Backend precisa CORS para Vercel

### URL
- **Produção:** https://legia-git-main-aline-almeidas-projects.vercel.app

---

## DECISÃO #8: Render.com (Deploy Backend - PENDENTE)

**Data:** Dezembro 2025
**Status:** ⚠️ NÃO IMPLEMENTADA (PENDENTE)
**Decisor:** Equipe de DevOps

### Contexto
Precisamos fazer deploy do backend FastAPI (atualmente só roda localmente).

### Opções Consideradas
1. **Render.com** - PaaS moderno
2. **Railway** - Similar ao Render
3. **Heroku** - PaaS tradicional
4. **AWS EC2** - VPS completo
5. **Fly.io** - Edge computing

### Decisão (Planejada)
Escolher **Render.com** (#1)

### Justificativa
**Prós:**
- ✅ Plano gratuito (750h/mês)
- ✅ PostgreSQL gratuito (1GB)
- ✅ Deploy automático via Git
- ✅ SSL grátis
- ✅ Logs e monitoramento
- ✅ Fácil configuração

**Contras:**
- ❌ Plano gratuito hiberna após inatividade (cold start de 30s)
- ❌ Limites do plano gratuito

### Consequências (Esperadas)
- ✅ Backend online em produção
- ✅ Sistema funcionando 100% online
- ⚠️ Pode ter cold start (aceito para MVP)

### Próximos Passos
1. Seguir `DEPLOY_GRATUITO.md`
2. Configurar variáveis de ambiente
3. Atualizar `NEXT_PUBLIC_API_URL` no Vercel
4. Testar integração completa

**Status:** ❌ BLOQUEADOR CRÍTICO - Precisa ser feito URGENTE

---

## DECISÃO #9: JWT para Autenticação

**Data:** Novembro 2025
**Status:** ✅ Implementada
**Decisor:** Equipe de segurança

### Contexto
Precisávamos escolher método de autenticação para API.

### Opções Consideradas
1. **JWT (JSON Web Tokens)** - Stateless
2. **Session cookies** - Stateful
3. **OAuth 2.0** - Padrão da indústria

### Decisão
Escolhemos **JWT** (#1)

### Justificativa
**Prós:**
- ✅ Stateless (não precisa armazenar sessões)
- ✅ Escalável (sem Redis/DB para sessões)
- ✅ Funciona bem com SPA/mobile
- ✅ Refresh token implementado
- ✅ Expiration automático

**Contras:**
- ❌ Não pode invalidar token antes de expirar (precisa blacklist)
- ❌ Payload visível (não colocar dados sensíveis)

### Consequências
- ✅ Access token: 30 minutos
- ✅ Refresh token: 7 dias
- ✅ Logout implementado (blacklist no Redis)

### Arquivos Afetados
- `backend/app/core/security.py` - Criação de tokens
- `backend/app/core/deps.py` - Validação de tokens

---

## DECISÃO #10: Não Usar Django

**Data:** Outubro 2025
**Status:** ✅ Confirmada
**Decisor:** Equipe de arquitetura

### Contexto
Django é o framework Python mais popular, mas escolhemos FastAPI.

### Por Que NÃO Django?
1. ❌ **Overhead desnecessário** - Django Admin, ORM próprio, templates
2. ❌ **Performance** - Síncrono por padrão
3. ❌ **Flexibilidade** - Muito opinionated
4. ❌ **API first** - Django é web-first, não API-first
5. ❌ **Peso** - 5MB+ vs FastAPI <1MB

### Por Que FastAPI Foi Melhor?
1. ✅ API-first (nosso caso de uso)
2. ✅ Assíncrono (melhor performance)
3. ✅ Leve e rápido
4. ✅ Validação automática (Pydantic)
5. ✅ OpenAPI/Swagger automático

### Consequências
- ✅ API rápida e leve
- ⚠️ Precisou construir mais coisas do zero (auth, admin, etc)

---

## 📊 RESUMO DE DECISÕES

| # | Decisão | Status | Impacto |
|---|---------|--------|---------|
| 1 | Multi-tenant (schemas) | ✅ | Alto |
| 2 | Google Gemini IA | ✅ | Alto |
| 3 | Next.js 14 App Router | ✅ | Alto |
| 4 | shadcn/ui | ✅ | Médio |
| 5 | FastAPI | ✅ | Alto |
| 6 | PostgreSQL | ✅ | Alto |
| 7 | Vercel (frontend) | ✅ | Médio |
| 8 | Render (backend) | ⚠️ PENDENTE | Alto |
| 9 | JWT | ✅ | Médio |
| 10 | Não usar Django | ✅ | Alto |

---

## 🎯 DECISÕES PENDENTES

### Para Decidir em Breve:

1. **WhatsApp Provider**
   - Digisac vs Twilio vs Evolution API
   - Custo: R$ 50-200/mês
   - Impacto: Médio

2. **Storage de Documentos**
   - AWS S3 vs Local vs MinIO
   - Custo: R$ 0-50/mês
   - Impacto: Alto

3. **Monitoring/Observability**
   - Sentry vs LogRocket vs DataDog
   - Custo: R$ 0-100/mês
   - Impacto: Médio

---

## 📝 TEMPLATE PARA NOVAS DECISÕES

```markdown
## DECISÃO #X: Título da Decisão

**Data:** DD/MM/YYYY
**Status:** ⚠️ Proposta / ✅ Implementada / ❌ Rejeitada
**Decisor:** Nome/Equipe

### Contexto
Explique o problema que precisa resolver.

### Opções Consideradas
1. Opção A
2. Opção B
3. Opção C

### Decisão
Escolhemos **Opção X**

### Justificativa
**Prós:**
- ✅ Pró 1
- ✅ Pró 2

**Contras:**
- ❌ Contra 1
- ❌ Contra 2

### Consequências
- Consequência positiva
- Consequência negativa

### Arquivos Afetados
- `caminho/arquivo.ext`
```

---

**Última atualização:** 06/01/2026
**Próxima revisão:** Após novas decisões técnicas importantes
