# CONFIGURAR VARIÁVEL NO VERCEL - URGENTE

## PROBLEMA IDENTIFICADO
A variável `NEXT_PUBLIC_API_URL` não está configurada no Vercel, fazendo o frontend usar `http://localhost:8000` em produção.

## SOLUÇÃO IMEDIATA

### Opção 1: Via Interface do Vercel (RECOMENDADO)
1. Acesse: https://vercel.com/aline-almeidas-projects/legia
2. Vá em **Settings** > **Environment Variables**
3. Adicione a variável:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://legia-backend.onrender.com`
   - **Environment**: Production, Preview, Development (marque todos)
4. Clique em **Save**
5. Vá em **Deployments** e clique em **Redeploy** no último deploy

### Opção 2: Via Vercel CLI
```bash
# Instalar Vercel CLI (se não tiver)
npm install -g vercel

# Fazer login
vercel login

# Adicionar variável
vercel env add NEXT_PUBLIC_API_URL production
# Quando pedir o valor, cole: https://legia-backend.onrender.com

# Repetir para preview e development
vercel env add NEXT_PUBLIC_API_URL preview
vercel env add NEXT_PUBLIC_API_URL development

# Forçar novo deploy
vercel --prod
```

## VERIFICAÇÃO
Após configurar e fazer redeploy:
1. Acesse: https://legia-git-main-aline-almeidas-projects.vercel.app/login
2. Tente fazer login com: admin@legia.com / Admin@123
3. Abra o Console do navegador (F12) e veja se o erro mudou

## STATUS ATUAL
- Backend: FUNCIONANDO (https://legia-backend.onrender.com)
- Frontend: DEPLOYADO mas usando URL errada
- Login API: TESTADO e funcionando
- Credenciais: CORRETAS

**AÇÃO NECESSÁRIA**: Configurar a variável no Vercel conforme instruções acima.
