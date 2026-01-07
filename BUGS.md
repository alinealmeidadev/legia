# 🐛 BUGS CONHECIDOS - LEGIA Platform
**Última atualização:** 06/01/2026

---

## 🔴 CRÍTICOS (Bloqueadores de Produção)

### BUG #1: Backend Não Deployado
**Status:** ❌ ATIVO
**Descoberto em:** Dezembro 2025
**Impacto:** Sistema completamente inutilizável em produção
**Descrição:**
- Frontend está no Vercel (online)
- Backend roda apenas localmente
- Frontend tenta chamar `http://localhost:8000` (não funciona online)
- Ninguém além de você consegue usar o sistema

**Solução:**
- Fazer deploy do backend no Render.com (plano gratuito)
- Seguir instruções em `DEPLOY_GRATUITO.md`
- Atualizar `NEXT_PUBLIC_API_URL` no Vercel para URL do Render
- Tempo estimado: 30 minutos

**Arquivo:** `DEPLOY_GRATUITO.md`
**Prioridade:** 🔥 URGENTE

---

### BUG #2: Fluxo de Alteração Contratual Incorreto
**Status:** ❌ ATIVO
**Descoberto em:** Desenvolvimento inicial
**Impacto:** Usabilidade ruim, não reflete processo real
**Descrição:**
- Sistema tem páginas SEPARADAS para cada tipo de alteração em `/tenant/automation`:
  - `/tenant/automation/alteracao-endereco`
  - `/tenant/automation/alteracao-socios`
  - `/tenant/automation/alteracao-capital`
  - `/tenant/automation/alteracao-atividade`
- Cliente precisa criar MÚLTIPLOS processos para fazer várias alterações
- Na vida real: Empresas fazem múltiplas alterações de uma vez (ex: mudar endereço + adicionar sócio + aumentar capital = 1 processo único)
- Sistema força a criar 3 processos separados (ERRADO!)

**Nota:** A página `/tenant/contracts` já tem o modal correto com múltiplas escolhas! O problema é na `/tenant/automation`

**Solução:**
- Criar UMA página `/tenant/automation/alteracao-contratual`
- Modal com checkboxes de múltipla escolha (igual `/tenant/contracts`)
- Backend aceitar array de tipos de alteração
- Remover páginas separadas antigas
- Tempo estimado: 3-4 horas

**Arquivo:** `BRIEFING-MELHORIAS.md` - FASE 1
**Prioridade:** 🔥 ALTA

---

## 🟡 MÉDIOS (Usabilidade/Performance)

### BUG #3: Docker Não Está Rodando
**Status:** ⚠️ ATIVO
**Descoberto em:** 06/01/2026
**Impacto:** Não consegue testar localmente
**Descrição:**
- Docker Desktop não está ativo
- Backend e PostgreSQL locais não acessíveis
- Redis não disponível

**Solução:**
- Iniciar Docker Desktop
- Executar: `docker-compose up -d`
- Tempo estimado: 2 minutos

**Prioridade:** 🟡 MÉDIA

---

## 🟢 BUGS RESOLVIDOS (Últimas 4 semanas)

### ✅ BUG: CORS ao Criar Processo
**Resolvido em:** 21/12/2025
**Commit:** `87522ea - Fix: CORS completo`
**Sintoma:**
- Ao clicar "Criar Processo" dava erro de CORS
- Backend 500 Internal Server Error

**Causa:**
- Backend no Render não estava nos domínios permitidos do CORS

**Solução aplicada:**
- Adicionado `https://legia-backend.onrender.com` em `backend/app/core/config.py:41`

---

### ✅ BUG: Automação Sem Fluxo de Etapas
**Resolvido em:** 21/12/2025
**Commit:** `5f007bd - correção automação e cord`
**Sintoma:**
- Depois de criar automação, não tinha próximos passos
- Sistema não mostrava progresso

**Solução aplicada:**
- Adicionados campos `current_stage` e `department` no model Process
- Interface visual de etapas no frontend
- 5 etapas: Comercial → Documentos → Contratos → Protocolos → Monitoramento
- Arquivo: `backend/app/models/tenant/process.py:44-47`

---

### ✅ BUG: Página Comunicações Confusa
**Resolvido em:** 21/12/2025
**Sintoma:**
- Não ficava claro se era para falar com super admin ou acompanhar protocolos

**Solução aplicada:**
- Página refatorada para "Acompanhamento de Protocolos"
- Monitora protocolos em órgãos públicos (Junta Comercial, Receita, Prefeitura)
- Mostra: status, prazos, número do protocolo
- Arquivo: `frontend/app/tenant/communications/page.tsx` (264 linhas)

---

### ✅ BUG: Erro de Import no WhatsApp Endpoint
**Resolvido em:** Dezembro 2025
**Commit:** `fe1e07b - fix: corrigir import no endpoint whatsapp`
**Sintoma:**
- `ModuleNotFoundError: No module named 'app.core.auth'`

**Causa:**
- Import incorreto: `from app.core.auth import get_current_user`
- Deveria ser: `from app.core.deps import get_current_tenant_user`

**Solução aplicada:**
- Corrigido import em 4 lugares no `backend/app/api/v1/endpoints/whatsapp.py`

---

### ✅ BUG: Login Detectando Tipo de Usuário
**Resolvido em:** Dezembro 2025
**Commit:** `3d7e135 - correção processo -> workflow e navegação`
**Sintoma:**
- Sistema não detectava automaticamente se era super admin ou tenant

**Solução aplicada:**
- Lógica de detecção automática no login
- Redireciona para `/admin` ou `/tenant` conforme tipo de usuário

---

## 📋 COMO REPORTAR UM BUG

Ao encontrar um bug, adicione aqui com:

```markdown
### BUG #X: Título Descritivo
**Status:** ❌ ATIVO / ⚠️ EM ANÁLISE / ✅ RESOLVIDO
**Descoberto em:** DD/MM/YYYY
**Impacto:** Descrição do impacto
**Descrição:**
- Como reproduzir
- O que acontece
- O que deveria acontecer

**Solução (se conhecida):**
- Passos para resolver

**Arquivo(s) afetado(s):** `caminho/arquivo.ext:linha`
**Prioridade:** 🔥 URGENTE / 🟡 MÉDIA / 🟢 BAIXA
```

---

## 🎯 ESTATÍSTICAS

**Total de bugs ativos:** 3 (2 críticos, 1 médio)
**Total resolvidos (30 dias):** 4
**Taxa de resolução:** 57% (4 de 7)
**Bug mais antigo ativo:** #2 - Alteração Contratual (desde desenvolvimento inicial)

---

**Última revisão:** 06/01/2026
**Próxima revisão:** Após cada correção de bug
