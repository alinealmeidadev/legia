# 🧪 GUIA DE TESTES - LEGIA PLATFORM

**Data:** 18/12/2025
**Versão:** Sprint 9-10 Concluída

---

## 🚀 Como Rodar a Aplicação

### 1. Instalar Dependências do Backend

```bash
cd backend
pip install -r requirements.txt
```

**IMPORTANTE:** A nova dependência `google-generativeai` foi adicionada para os agentes IA.

### 2. Subir os Containers

```bash
# Na raiz do projeto
docker-compose up -d
```

Isso irá iniciar:
- PostgreSQL (porta 5432)
- Redis (porta 6379)
- Backend FastAPI (porta 8000)
- Frontend Next.js (porta 3000)

### 3. Acessar a Aplicação

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Documentação API:** http://localhost:8000/api/v1/docs

---

## 🔐 Credenciais de Teste

### Super Admin
```
Email: admin@legia.com.br
Senha: admin123
Tenant ID: (deixe vazio)
```

### Tenant - Escritório XYZ
```
Email: admin@xyz.com
Senha: admin123
Tenant ID: 2
```

---

## ✅ TESTES - SISTEMA DE PROCESSOS

### Teste 1: Criar Processo

1. Faça login como tenant (admin@xyz.com)
2. Navegue para "Processos" no menu
3. Clique em "Novo Processo"
4. Preencha:
   - Cliente: Selecione um cliente existente
   - Tipo: Abertura de Empresa
   - Título: "Abertura de LTDA - Consultoria TI"
   - Descrição: "Processo de abertura para cliente novo"
   - Prioridade: Normal
   - Prazo: 30 dias
5. Clique em "Criar Processo"

**Resultado Esperado:**
- Toast de sucesso aparece
- Processo aparece na lista
- Estatísticas são atualizadas

### Teste 2: Visualizar Processos

1. Na página de Processos
2. Observe os cards de estatísticas (Total, Aguardando, Em Andamento, Concluído)
3. Visualize a lista de processos com:
   - Título do processo
   - Status com badge colorido
   - Nome do cliente
   - Tipo de processo
   - Prioridade
   - Data de criação

**Resultado Esperado:**
- Todos os processos são exibidos corretamente
- Cores dos badges correspondem aos status
- Informações do cliente aparecem

### Teste 3: Estatísticas

1. Crie vários processos com diferentes status
2. Observe as estatísticas no topo da página
3. Verifique se os números são atualizados automaticamente

**Resultado Esperado:**
- Contadores refletem o número real de processos
- Estatísticas são calculadas corretamente

---

## 🤖 TESTES - ORQUESTRADOR (Agente IA)

### Teste 4: Verificar Status dos Agentes

**Via API (Swagger):**

1. Acesse: http://localhost:8000/api/v1/docs
2. Faça login (Authorize) com token de tenant
3. Teste o endpoint: `GET /api/v1/agents/agents/status`

**Resultado Esperado:**
```json
{
  "orchestrator": {
    "name": "Orquestrador",
    "role": "coordenador de agentes especializados em legalização empresarial",
    "status": "online"
  },
  "available_agents": [
    "comercial",
    "legalizacao",
    "monitor",
    "contratos",
    "comunicacoes",
    "documentos",
    "assistente"
  ],
  "status": "operational"
}
```

### Teste 5: Chat com Orquestrador

**Via API (Swagger):**

1. Acesse: http://localhost:8000/api/v1/docs
2. Faça login (Authorize)
3. Teste o endpoint: `POST /api/v1/agents/chat`
4. Envie:

**Teste 5.1 - Orçamento:**
```json
{
  "message": "Quanto custa para abrir uma empresa?",
  "context": {}
}
```

**Resultado Esperado:**
- `intent`: "orcamento"
- `agent`: "comercial"
- `response`: Resposta humanizada sobre orçamentos

**Teste 5.2 - Abertura:**
```json
{
  "message": "Quero abrir uma LTDA",
  "context": {}
}
```

**Resultado Esperado:**
- `intent`: "abertura"
- `agent`: "legalizacao"
- `response`: Resposta sobre processo de abertura

**Teste 5.3 - Consulta:**
```json
{
  "message": "Qual o status do meu protocolo?",
  "context": {}
}
```

**Resultado Esperado:**
- `intent`: "consulta"
- `agent`: "monitor"
- `response`: Resposta sobre consulta de status

**Teste 5.4 - Saudação:**
```json
{
  "message": "Olá, bom dia!",
  "context": {}
}
```

**Resultado Esperado:**
- `intent`: "saudacao"
- `agent`: "assistente"
- `response`: Saudação profissional e humanizada

### Teste 6: Verificar Tom de Voz

Envie várias mensagens e verifique se o Orquestrador:
- ✅ Responde de forma humanizada (não robótica)
- ✅ NUNCA menciona que é uma IA
- ✅ Usa linguagem natural e acolhedora
- ✅ É profissional mas amigável

---

## 🐛 PROBLEMAS CONHECIDOS

### Backend

1. **Timeline de Processos:**
   - Tabela `process_timeline` ainda não existe no banco
   - Endpoints de timeline retornam dados mockados
   - Para implementar: criar migration para a tabela

2. **Agentes Especializados:**
   - Apenas o Orquestrador está implementado
   - Outros 7 agentes ainda não foram criados
   - Delegação de tarefas está mockada

### Frontend

1. **Detalhes do Processo:**
   - Botão "Ver Detalhes" ainda não tem funcionalidade
   - Precisa criar página de detalhes do processo

2. **Edição de Processos:**
   - Não há modal de edição implementado
   - Próxima feature a ser desenvolvida

---

## 📊 O QUE FOI IMPLEMENTADO NESTA SPRINT

### Backend ✅
- [x] `process_service.py` - Service completo de processos
- [x] `app/api/v1/endpoints/processes.py` - Endpoints REST completos
- [x] Schemas de processos atualizados
- [x] Router integrado
- [x] Estrutura base de agentes (`BaseAgent`)
- [x] `OrchestratorAgent` completo com Gemini
- [x] Endpoint de chat com orquestrador
- [x] Análise de intenção por palavras-chave
- [x] Roteamento inteligente para agentes

### Frontend ✅
- [x] `process-form-dialog.tsx` - Formulário de criação
- [x] Página de processos atualizada com dados reais
- [x] Cards de estatísticas
- [x] Lista de processos com badges
- [x] Integração com API
- [x] Componente Badge criado
- [x] Notificações toast

### Dependências ✅
- [x] `google-generativeai` adicionado ao requirements.txt
- [x] Configuração do Gemini no BaseAgent

---

## 🎯 PRÓXIMOS PASSOS

### Para Completar MVP:

1. **Agentes Especializados (Sprint 11-12):**
   - Implementar Agente Comercial
   - Implementar Agente de Legalização
   - Implementar Agente Monitor
   - Implementar Agente de Contratos
   - Implementar Agente de Comunicações
   - Implementar Agente Organizador
   - Implementar Agente Assistente

2. **Timeline de Processos:**
   - Criar tabela `process_timeline`
   - Implementar endpoints reais

3. **Frontend de Chat:**
   - Criar componente de chat para interagir com Orquestrador
   - Adicionar interface conversacional
   - Histórico de conversas

4. **Melhorias:**
   - Página de detalhes do processo
   - Modal de edição de processos
   - Filtros avançados
   - Paginação real

---

## 💰 CUSTO DESTA SPRINT

**Tokens Usados:** ~85.000 / 200.000
**Tempo Estimado:** ~2 horas
**Custo Aproximado:** $2.00 USD

**Saldo Restante:** ~$4.00 USD

---

## 📝 NOTAS IMPORTANTES

1. **Google Gemini API Key:**
   - Certifique-se de que `GEMINI_API_KEY` está configurada no `.env`
   - A chave fornecida: `AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o`

2. **Reiniciar Backend:**
   - Após adicionar `google-generativeai`, é necessário reinstalar dependências
   - Execute: `docker-compose down && docker-compose up -d --build backend`

3. **Testes do Orquestrador:**
   - Funciona melhor com mensagens em português
   - Suporta variações de escrita
   - Aprende com contexto da conversa

---

## ✨ PRÓXIMA SESSÃO

**Recomendado:**
1. Testar todos os endpoints criados
2. Criar mais processos para popular o sistema
3. Testar o Orquestrador com diferentes tipos de mensagens
4. Reportar bugs encontrados

Se houver crédito disponível:
5. Implementar mais agentes especializados
6. Criar interface de chat no frontend
7. Adicionar timeline de processos

---

**🚀 Pronto para testes!**
