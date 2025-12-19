# 🚀 DEPLOY GRATUITO - LEGIA PLATFORM

## ✅ Plano: 100% Gratuito por 30 Dias

```
Frontend (Site): Vercel → GRÁTIS SEMPRE
Backend (IA): Render → GRÁTIS 90 DIAS
Banco PostgreSQL: Render → GRÁTIS 90 DIAS
Redis: Render → GRÁTIS 25MB
```

---

## 📋 PASSO 1: Criar Contas (5 minutos)

### 1.1 Criar Conta no Render
1. Acesse: https://render.com
2. Clique em **"Get Started"**
3. Escolha **"Sign up with GitHub"** (mais fácil)
4. Autorize o Render a acessar seu repositório

### 1.2 Criar Conta no Vercel
1. Acesse: https://vercel.com
2. Clique em **"Sign Up"**
3. Escolha **"Continue with GitHub"**
4. Autorize o Vercel

---

## 🎯 PASSO 2: Deploy do Backend (Render)

### 2.1 No Render Dashboard:

1. Clique em **"New +"** → **"Blueprint"**
2. Conecte seu repositório GitHub: `alinealmeidadev/legia`
3. O Render vai detectar o arquivo `render.yaml` automaticamente
4. Clique em **"Apply"**

### 2.2 Configurar Variáveis de Ambiente:

No painel do Render, adicione:

```
GEMINI_API_KEY = AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o
ASAAS_API_KEY = $aact_hmlg_000MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmFkZDJkYWNiLTZlMmMtNGJlMC04NDRkLTE3YmIwYzgzYzViZTo6JGFhY2hfNzA2NDcxZTYtZTJkMS00NjE1LWI4YWItMTRmZDEzYWNkMGJh
```

As outras variáveis (SECRET_KEY, JWT_SECRET_KEY, DATABASE_URL, REDIS_URL) são geradas automaticamente!

### 2.3 Aguarde o Deploy (5-10 minutos)

Você vai receber uma URL tipo:
```
https://legia-backend.onrender.com
```

✅ **Teste**: Abra a URL no navegador. Deve aparecer: `"🚀 LEGIA PLATFORM API"`

---

## 🎨 PASSO 3: Deploy do Frontend (Vercel)

### 3.1 No Vercel Dashboard:

1. Clique em **"Add New..."** → **"Project"**
2. Importe o repositório: `alinealmeidadev/legia`
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### 3.2 Adicionar Variável de Ambiente:

```
NEXT_PUBLIC_API_URL = https://legia-backend.onrender.com
```

(Use a URL que você recebeu no Passo 2.3)

### 3.3 Deploy! (3-5 minutos)

Clique em **"Deploy"** e aguarde.

Você vai receber uma URL tipo:
```
https://legia-platform.vercel.app
```

✅ **Pronto!** Seu sistema está no ar!

---

## 🔗 URLs Finais

Depois do deploy, você terá:

```
Frontend (Site): https://legia-platform.vercel.app
Backend (API): https://legia-backend.onrender.com
Documentação: https://legia-backend.onrender.com/api/v1/docs
```

---

## ⚡ POR QUE ESTAVA LENTO LOCALMENTE?

### Motivos da Lentidão Local:

1. **Modo Desenvolvimento** (Next.js `npm run dev`)
   - Recompila a cada mudança
   - Não tem otimizações de produção
   - Hot reload consome recursos

2. **Backend sem Cache**
   - Redis não estava configurado
   - Banco de dados SQLite (mais lento)

3. **Sem CDN**
   - Imagens e assets não otimizados
   - Sem compressão

### ✅ Na Nuvem Será MUITO MAIS RÁPIDO:

- **Vercel**: CDN global (seus arquivos ficam em vários países)
- **Render**: Servidor otimizado com cache
- **PostgreSQL**: Banco de dados profissional
- **Redis**: Cache de alta velocidade

**Espere:** 10x a 50x mais rápido! 🚀

---

## ⏰ Renovação Gratuita

### Render (90 dias grátis):
- PostgreSQL expira em **90 dias**
- Antes de expirar, você pode:
  - **Opção A**: Exportar dados e criar novo banco grátis
  - **Opção B**: Migrar para Neon (grátis sempre, 0.5GB)
  - **Opção C**: Pagar ~R$7/mês pelo Render

### Vercel (grátis sempre):
- Frontend continua grátis para sempre!
- 100GB bandwidth/mês (suficiente para 100k visitantes)

---

## 🆘 Se Der Erro

### Backend não sobe:
1. Verifique logs no Render Dashboard
2. Confirme que variáveis de ambiente estão corretas
3. Aguarde 5-10 minutos (primeira vez demora)

### Frontend não conecta ao backend:
1. Verifique se `NEXT_PUBLIC_API_URL` está correta
2. Teste a URL do backend no navegador
3. Limpe cache do Vercel e faça redeploy

### Banco de dados não conecta:
1. Aguarde criação do banco (pode demorar)
2. Verifique que `DATABASE_URL` foi gerada automaticamente
3. Veja logs de migração no Render

---

## 📞 Próximos Passos

Depois do deploy funcionando:

1. ✅ **Testar sistema completo na web**
2. ✅ **Integrar WhatsApp (Digisac)**
3. ✅ **Corrigir processos errados**
4. ✅ **Adicionar domínio customizado** (opcional)

---

## 🎁 Bônus: Deploy Automático

Depois do primeiro deploy, é **automático**:

```
Você faz mudança no código
    ↓
Dá git push no GitHub
    ↓
Vercel e Render detectam automaticamente
    ↓
Fazem deploy sozinhos em 2-5 minutos!
    ↓
Seu site atualiza automaticamente! 🎉
```

**Nunca mais precisa fazer deploy manual!**
