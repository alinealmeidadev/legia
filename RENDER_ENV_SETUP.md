# Configuração de Variáveis de Ambiente no Render.com

## ⚠️ ERRO ATUAL
```
FIRST_SUPERUSER_EMAIL: Field required
FIRST_SUPERUSER_PASSWORD: Field required
```

## 🔧 SOLUÇÃO: Adicionar Variáveis de Ambiente

### Passo a Passo

1. **Acesse o Dashboard do Render**
   - https://dashboard.render.com/
   - Encontre seu serviço "legia-backend"

2. **Vá em Environment**
   - No menu lateral, clique em "Environment"
   - Clique em "Add Environment Variable"

3. **Adicione TODAS as variáveis abaixo:**

---

## 📋 VARIÁVEIS OBRIGATÓRIAS

### Application Settings
```env
SECRET_KEY=legia_production_secret_key_2026_change_this_to_something_random_and_secure
JWT_SECRET_KEY=legia_jwt_production_secret_2026_also_change_this_to_random_secure_string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Database
```env
DATABASE_URL=postgresql://legia_backend_db_oavt_user:cFglV7fMlKvLLzPnpjAp6MFXqiRg94qR@dpg-cu35m5aj1k6c738soh3g-a.oregon-postgres.render.com/legia_backend_db_oavt
```
*(Sua URL do PostgreSQL no Render - verifique no dashboard do banco)*

### Redis
```env
REDIS_URL=redis://localhost:6379/0
```
*(Se tiver Redis configurado no Render, use a URL fornecida)*

### API Keys
```env
GEMINI_API_KEY=AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
ASAAS_API_KEY=$aact_hmlg_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZDJkYWNiLTZlMmMtNGJlMC04NDRkLTE3YmIwYzgzYzViZTo6JGFhY2hfNzA2NDcxZTYtZTJkMS00NjE1LWI4YWItMTRmZDEzYWNkMGJh
```

### Environment
```env
ENVIRONMENT=production
DEBUG=False
```

### CORS Origins
```env
CORS_ORIGINS=https://legia-git-main-aline-almeidas-projects.vercel.app,https://legia-aline-almeidas-projects.vercel.app,https://legia.vercel.app
```

### First Superuser (CRÍTICO - estava faltando!)
```env
FIRST_SUPERUSER_EMAIL=admin@legia.com.br
FIRST_SUPERUSER_PASSWORD=Admin@Legia2026!Seguro
FIRST_SUPERUSER_NAME=Admin Legia
```

---

## ⚡ ATENÇÃO DE SEGURANÇA

### ⚠️ Variáveis que DEVEM ser mudadas em produção:

1. **SECRET_KEY** - Gere uma chave aleatória de 64 caracteres
   ```bash
   # No terminal local:
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

2. **JWT_SECRET_KEY** - Gere outra chave aleatória
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

3. **FIRST_SUPERUSER_PASSWORD** - Use senha FORTE
   - Mínimo 12 caracteres
   - Letras maiúsculas, minúsculas, números e símbolos

---

## 📝 CHECKLIST

- [ ] Acessar Render Dashboard
- [ ] Ir em "legia-backend" → Environment
- [ ] Adicionar todas as 15 variáveis acima
- [ ] Verificar DATABASE_URL do seu PostgreSQL no Render
- [ ] Clicar em "Save Changes"
- [ ] Aguardar deploy automático (~2-3 minutos)
- [ ] Testar: https://legia-backend.onrender.com/health

---

## 🧪 TESTE APÓS CONFIGURAR

1. **Health Check:**
   ```bash
   curl https://legia-backend.onrender.com/health
   ```
   Esperado: `{"status":"healthy"}`

2. **Login do Super Admin:**
   ```bash
   curl -X POST https://legia-backend.onrender.com/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@legia.com.br",
       "password": "Admin@Legia2026!Seguro"
     }'
   ```
   Esperado: JSON com `access_token` e `refresh_token`

---

## ❌ SE CONTINUAR COM ERRO

### Erro: "relation 'tenants' does not exist"
**Solução:** Banco não inicializado. Execute seed:
```bash
curl -X POST https://legia-backend.onrender.com/api/v1/setup/init
curl -X POST https://legia-backend.onrender.com/api/v1/setup/seed
```

### Erro: "Could not connect to database"
**Solução:** Verificar DATABASE_URL no Render:
1. Ir em Dashboard → PostgreSQL
2. Copiar "External Database URL"
3. Colar em DATABASE_URL no Environment do backend

### Erro: "CORS policy"
**Solução:** Verificar CORS_ORIGINS inclui todas as URLs do Vercel

---

## 🚀 DEPOIS DE FUNCIONAR

1. **Atualizar Frontend (Vercel):**
   - Ir em Vercel → legia → Settings → Environment Variables
   - Garantir que `NEXT_PUBLIC_API_URL` aponta para Render:
     ```
     NEXT_PUBLIC_API_URL=https://legia-backend.onrender.com
     ```

2. **Redeploy Frontend:**
   - Vercel → Deployments → ⋯ → Redeploy

---

**Última atualização:** 07/01/2026
