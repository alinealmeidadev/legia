# ⚠️ SOLUÇÃO RÁPIDA - Erro no Render

## 🔴 PROBLEMA
```
FIRST_SUPERUSER_EMAIL: Field required
FIRST_SUPERUSER_PASSWORD: Field required
```

## ✅ SOLUÇÃO EM 3 PASSOS

### PASSO 1: Acesse o Render
1. Vá em https://dashboard.render.com/
2. Clique no seu serviço "legia-backend"
3. Vá na aba **Environment**

### PASSO 2: Cole estas variáveis

Clique em "Add Environment Variable" e adicione **TODAS** estas:

```env
# === CRÍTICO - ESTAVA FALTANDO ===
FIRST_SUPERUSER_EMAIL=admin@legia.com.br
FIRST_SUPERUSER_PASSWORD=Admin@Legia2026!Seguro
FIRST_SUPERUSER_NAME=Admin Legia

# === SEGURANÇA ===
SECRET_KEY=aK8Pk4o0NcNdzciI38Gos3OFFQGgatUQFKQZXSa6RR25f_K_q98tEP8H8UEmBupDJf2eiJwV9CDZ7H89vSrw5g
JWT_SECRET_KEY=6VZ8z5N5o34yCBSIDZnbqISsLeiMQHsvtFK4PUFoFMpRXEbvcJV0gbGconjN_KGqGDQdKC8x8eII4XjBogY_Kw
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# === BANCO DE DADOS ===
DATABASE_URL=postgresql://legia_backend_db_oavt_user:cFglV7fMlKvLLzPnpjAp6MFXqiRg94qR@dpg-cu35m5aj1k6c738soh3g-a.oregon-postgres.render.com/legia_backend_db_oavt

# === REDIS ===
REDIS_URL=redis://localhost:6379/0

# === API KEYS ===
GEMINI_API_KEY=AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
ASAAS_API_KEY=$aact_hmlg_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZDJkYWNiLTZlMmMtNGJlMC04NDRkLTE3YmIwYzgzYzViZTo6JGFhY2hfNzA2NDcxZTYtZTJkMS00NjE1LWI4YWItMTRmZDEzYWNkMGJh

# === AMBIENTE ===
ENVIRONMENT=production
DEBUG=False

# === CORS ===
CORS_ORIGINS=https://legia-git-main-aline-almeidas-projects.vercel.app,https://legia-aline-almeidas-projects.vercel.app,https://legia.vercel.app
```

**IMPORTANTE:**
- Se sua DATABASE_URL do PostgreSQL for diferente, use a URL que aparece no seu dashboard do banco de dados do Render
- Para encontrar: Dashboard → PostgreSQL → External Database URL

### PASSO 3: Salvar e Aguardar

1. Clique em **"Save Changes"** no Render
2. Aguarde o deploy automático (2-3 minutos)
3. Verifique os logs em "Logs"

---

## 🧪 TESTE SE FUNCIONOU

Abra o terminal e execute:

```bash
curl https://legia-backend.onrender.com/health
```

**Esperado:**
```json
{"status":"healthy"}
```

Se der erro, verifique os logs no Render: Dashboard → legia-backend → Logs

---

## 📝 DEPOIS QUE FUNCIONAR

### Inicializar Banco de Dados (só uma vez)

```bash
curl -X POST https://legia-backend.onrender.com/api/v1/setup/init
curl -X POST https://legia-backend.onrender.com/api/v1/setup/seed
```

### Testar Login

```bash
curl -X POST https://legia-backend.onrender.com/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@legia.com.br","password":"Admin@Legia2026!Seguro"}'
```

Deve retornar um JSON com `access_token` e `refresh_token`.

---

## 🎯 PRÓXIMO PASSO

Depois que o backend estiver funcionando, atualize o frontend:

1. **Vercel Dashboard** → legia → Settings → Environment Variables
2. Adicione/Atualize:
   ```
   NEXT_PUBLIC_API_URL=https://legia-backend.onrender.com
   ```
3. Faça redeploy do frontend

---

## 📚 MAIS DETALHES

Se precisar de mais informações, veja:
- `RENDER_ENV_SETUP.md` - Guia completo
- `backend/generate_secrets.py` - Script para gerar novas chaves

---

**Última atualização:** 07/01/2026
**Status:** Backend no Render está PARADO aguardando variáveis de ambiente
