# 📝 CHANGELOG - LEGIA Platform
**Histórico de Mudanças do Projeto**

Todas as mudanças notáveis do projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [Não Lançado] - MVP 1.0 (72% concluído)

### Pendente
- Deploy do backend em produção
- Correção do fluxo de alteração contratual
- Integração CNPJ (ReceitaWS)
- Integração CEP (ViaCEP)
- Sistema de pagamentos Asaas
- WhatsApp Business API
- Upload de documentos
- Testes automatizados (>60% cobertura)

---

## [06/01/2026]

### Adicionado
- `CLAUDE.md` - Arquivo de memória completo (658 linhas)
- `BUGS.md` - Rastreamento de bugs conhecidos
- `CHANGELOG.md` - Este arquivo de histórico
- `SESSION_LOG.md` - Log de sessões de trabalho
- `FEATURES.md` - Status de features implementadas
- `DECISIONS.md` - Decisões técnicas importantes
- Documentação de versões utilizadas

### Mudado
- Nada nesta sessão

### Corrigido
- Nada nesta sessão

### Removido
- Nada nesta sessão (limpeza de arquivos antigos planejada)

---

## [21/12/2025]

### Corrigido
- CORS ao criar processo - Adicionado domínio Render (`87522ea`)
- Fluxo de automação sem etapas - Campos `current_stage` e `department` (`5f007bd`)
- Página de comunicações refatorada para "Acompanhamento de Protocolos"
- Modal único de alteração contratual em `/tenant/contracts`
- Build no Vercel (`ebf73b7`)
- Navegação entre páginas (`3d7e135`)

### Adicionado
- Campo `client_number` no model Client
- Sistema de etapas visuais em automação
- Integração do número do cliente em todo sistema
- Migrações automáticas no startup (`3072729`)

---

## [Dezembro 2025]

### Corrigido
- Import incorreto no endpoint WhatsApp (`fe1e07b`)
- Login detectando tipo de usuário automaticamente
- CORS para Vercel

### Adicionado
- Endpoint WhatsApp Business (parcial)
- Sistema de migração automática
- Documentação extensa (20+ arquivos .md)

---

## [Novembro 2025]

### Adicionado
- **9 Agentes de IA** (100% implementados, 27 testes passando):
  1. Orquestrador (300+ linhas)
  2. Agente Comercial (250+ linhas)
  3. Agente de Legalização (280+ linhas)
  4. Gestor de Contratos (200+ linhas)
  5. Monitor de Protocolos (220+ linhas)
  6. Agente de Protocolos (180+ linhas)
  7. Assistente ao Cliente (280+ linhas)
  8. Gestor de Comunicações (200+ linhas)
  9. Organizador de Documentos (180+ linhas)
- Total: ~2.500 linhas de código IA

### Adicionado - Backend
- Infraestrutura FastAPI completa
- PostgreSQL multi-tenant (schema por tenant)
- Sistema de autenticação JWT
- CRUD completo para Tenants, Clientes, Processos
- Sistema de seeds para dados de teste
- Alembic migrations
- Docker Compose

### Adicionado - Frontend
- Next.js 14 com App Router
- 13 páginas funcionais (admin + tenant)
- Dashboard completo
- Chat Widget IA flutuante
- Import Excel de clientes
- 15+ componentes UI (shadcn/ui)

### Adicionado - Banco de Dados
- Schema public (Legia/Super Admin):
  - legia_users, tenants, plans, subscriptions, payments
- Schema tenant (por escritório):
  - users, clients, processes, protocols, documents, quotes, communications, chat_messages

---

## [Outubro 2025]

### Adicionado
- Estrutura inicial do projeto
- Planejamento e PRD completo
- Definição de arquitetura multi-tenant
- Stack tecnológico definido

---

## Categorias de Mudanças

- **Adicionado** - Novas funcionalidades
- **Mudado** - Mudanças em funcionalidades existentes
- **Descontinuado** - Funcionalidades que serão removidas
- **Removido** - Funcionalidades removidas
- **Corrigido** - Correções de bugs
- **Segurança** - Correções de vulnerabilidades

---

## Formato de Versionamento

Quando lançar versões:
- **MAJOR** (1.0.0) - Mudanças incompatíveis na API
- **MINOR** (0.1.0) - Novas funcionalidades compatíveis
- **PATCH** (0.0.1) - Correções de bugs

**Versão atual:** MVP 0.72.0 (72% concluído)

---

**Última atualização:** 06/01/2026
