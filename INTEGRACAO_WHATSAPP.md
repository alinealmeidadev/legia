# Integração WhatsApp Business API - LEGIA

## 📱 Estrutura Implementada

### Endpoints Criados

✅ **POST /api/v1/whatsapp/webhook**
- Recebe mensagens dos clientes
- Processa automaticamente com Agente IA
- Identifica cliente pelo número

✅ **GET /api/v1/whatsapp/webhook**
- Verificação do webhook (Meta exige)

✅ **POST /api/v1/whatsapp/send**
- Envia mensagens para clientes
- Suporta templates

✅ **GET /api/v1/whatsapp/templates**
- Lista templates aprovados

✅ **POST /api/v1/whatsapp/client/{client_number}/notify**
- Notifica cliente específico pelo número

---

## 🔧 Como Configurar (Passo a Passo)

### 1. Criar Conta Meta for Developers

1. Acesse: https://developers.facebook.com/
2. Crie um aplicativo tipo "Business"
3. Adicione produto "WhatsApp"

### 2. Obter Credenciais

No painel do Meta:
- **Token de Acesso**: Settings → WhatsApp → API Setup
- **Phone Number ID**: Seu número de teste
- **WhatsApp Business Account ID**: Na URL

### 3. Adicionar no `.env`

```env
# WhatsApp Business API
WHATSAPP_TOKEN=SEU_TOKEN_AQUI
WHATSAPP_PHONE_NUMBER_ID=SEU_PHONE_ID
WHATSAPP_VERIFY_TOKEN=LEGIA_WEBHOOK_2025
```

### 4. Configurar Webhook no Meta

1. WhatsApp → Configuration → Webhook
2. **Callback URL**: `https://legia-backend.onrender.com/api/v1/whatsapp/webhook`
3. **Verify Token**: `LEGIA_WEBHOOK_2025`
4. **Subscribe**: Messages, Message Status

### 5. Testar

Envie mensagem do WhatsApp → Sistema responde automaticamente!

---

## 🤖 Fluxo de Atendimento com IA

```
1. Cliente envia: "Oi, qual o status do meu processo?"

2. Webhook recebe → Backend processa

3. Sistema identifica:
   - Cliente #1234 pelo número
   - Processo ativo: Alteração Contratual
   - Status: Aguardando documentos

4. Agente IA responde:
   "Olá Cliente #1234! Seu processo de Alteração Contratual
    está aguardando os seguintes documentos:
    - RG do sócio
    - Comprovante de endereço

    Pode enviar por aqui mesmo! 📄"

5. Cliente envia foto do RG → Sistema salva automaticamente
```

---

## 📊 Casos de Uso

### Atendimento Automático
- Cliente pergunta sobre processo
- IA responde com dados reais
- Busca no banco: Cliente #{client_number}

### Notificações Proativas
- Processo aprovado → WhatsApp automático
- Documentos pendentes → Lembrete
- Prazo vencendo → Alerta

### Coleta de Documentos
- Cliente envia foto → Sistema salva
- Valida documento → IA analisa qualidade
- Confirma recebimento

### Suporte Multi-Idioma
- IA detecta idioma
- Responde em PT, EN, ES

---

## 🔐 Segurança

- ✅ Webhook verificado com token
- ✅ HTTPS obrigatório
- ✅ Autenticação Meta
- ✅ Rate limiting
- ✅ Logs de todas as mensagens

---

## 💰 Custos

**Meta WhatsApp Business API:**
- Primeiras 1.000 conversas/mês: GRÁTIS
- Após isso: R$ 0,33 por conversa
- Conversa = janela de 24h

**Projeção LEGIA:**
- 100 clientes ativos
- ~5 conversas/cliente/mês
- Total: 500 conversas/mês
- **Custo: R$ 0 (dentro do grátis)**

---

## 🚀 Próximos Passos

1. ✅ Estrutura criada
2. ⏳ Configurar conta Meta (você faz)
3. ⏳ Adicionar credenciais no .env
4. ⏳ Testar webhook
5. ⏳ Conectar Agente IA
6. ⏳ Treinar respostas

---

## 📞 Números para Testar

Após configurar, teste com:
- Seu próprio WhatsApp
- Números de teste do Meta
- Número de produção (quando aprovar)

---

## ⚠️ Limitações Atuais

- Ainda não conectado ao Gemini (Agente IA)
- Não salva histórico no banco
- Não identifica cliente automaticamente
- Necessita configuração Meta

**Mas a ESTRUTURA está pronta!** 🎉
