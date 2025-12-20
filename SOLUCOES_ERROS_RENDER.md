# 🛠️ SOLUÇÕES RÁPIDAS - ERROS RENDER

## 🔴 ERRO MAIS PROVÁVEL: Pacotes Pesados Demais

### **Sintoma nos Logs:**
```
ERROR: Failed building wheel for [nome-pacote]
gcc: error trying to exec 'cc1plus': execvp: No such file or directory
Command "python setup.py egg_info" failed with error code 1
Exited with status 1
```

### **Causa:**
Alguns pacotes do `requirements.txt` precisam compilar código C, mas o plano FREE do Render não tem as ferramentas necessárias.

**Pacotes problemáticos:**
- ❌ `aiohttp` (compilação C++)
- ❌ `python-magic` (precisa de libmagic do sistema)
- ❌ `Pillow` (compilação pesada de imagens)

### **✅ SOLUÇÃO:**

Trocar o arquivo `requirements.txt` por uma versão simplificada:

1. Deletar `backend/requirements.txt`
2. Renomear `backend/requirements-render.txt` → `backend/requirements.txt`
3. Commit e push no GitHub
4. Render vai detectar automaticamente e refazer deploy

---

## 🔴 ERRO 2: Módulo Não Encontrado

### **Sintoma nos Logs:**
```
ModuleNotFoundError: No module named 'app'
ImportError: cannot import name 'app'
```

### **Causa:**
O comando está rodando no diretório errado.

### **✅ SOLUÇÃO:**

**No painel do Render:**
1. Clique no serviço `legia-backend`
2. **Settings** (menu lateral)
3. Procure **"Root Directory"**
4. Se estiver vazio, coloque: `backend`
5. Clique em **"Save Changes"**
6. Deploy vai rodar automaticamente

---

## 🔴 ERRO 3: Variáveis de Ambiente Faltando

### **Sintoma nos Logs:**
```
pydantic_core._pydantic_core.ValidationError: 6 validation errors for Settings
Field required [type=missing, input_value={}, input_type=dict]
KeyError: 'DATABASE_URL'
```

### **Causa:**
Variáveis de ambiente não foram configuradas.

### **✅ SOLUÇÃO:**

**No painel do Render:**
1. Serviço `legia-backend` → **Environment** (menu lateral)
2. Clique em **"Add Environment Variable"**
3. Adicione TODAS essas:

```
PYTHON_VERSION = 3.11.0
ENVIRONMENT = production
GEMINI_API_KEY = AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
ASAAS_API_KEY = $aact_hmlg_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZDJkYWNiLTZlMmMtNGJlMC04NDRkLTE3YmIwYzgzYzViZTo6JGFhY2hfNzA2NDcxZTYtZTJkMS00NjE1LWI4YWItMTRmZDEzYWNkMGJh
```

4. Para DATABASE_URL e REDIS_URL:
   - Clique em **"Add from Database"**
   - Escolha o banco correspondente
   - Property: "Internal Connection String"

5. Para SECRET_KEY e JWT_SECRET_KEY:
   - Clique em **"Generate"** ao lado

6. **Save Changes**

---

## 🔴 ERRO 4: Porta Incorreta

### **Sintoma nos Logs:**
```
Failed to bind to port
Address already in use
```

### **Causa:**
Comando de start não está usando a variável `$PORT` do Render.

### **✅ SOLUÇÃO:**

**No painel do Render:**
1. Settings → **Build & Deploy**
2. **Start Command** deve ser:
```
cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
(⚠️ Importante: `$PORT` não `8000`)

3. **Save Changes**

---

## 🔴 ERRO 5: Python Version

### **Sintoma nos Logs:**
```
Python 3.7 is no longer supported
requires-python >=3.8
```

### **Causa:**
Render está usando Python 3.7 por padrão.

### **✅ SOLUÇÃO:**

Adicionar variável de ambiente:
```
PYTHON_VERSION = 3.11.0
```

---

## 📋 CHECKLIST COMPLETO

Antes de tentar novamente, confirme:

- [ ] Root Directory: `backend`
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Python Version: `3.11.0` (variável de ambiente)
- [ ] Todas as variáveis de ambiente configuradas
- [ ] DATABASE_URL conectado ao PostgreSQL
- [ ] REDIS_URL conectado ao Redis
- [ ] requirements.txt sem pacotes problemáticos

---

## 🆘 Se Nada Funcionar

**Me mande:**
1. Últimas 50 linhas dos logs
2. Screenshot das configurações (Settings)
3. Lista de variáveis de ambiente que você configurou

**Vou corrigir na hora!** 🚀
