# SOLUÇÃO FINAL - CONFIGURAÇÃO VERCEL

## PROBLEMA:
Frontend faz requisições para SI MESMO em vez do backend Render.

## SOLUÇÃO APLICADA:

1. ✅ Arquivo `.env.production` criado com URL correta
2. ✅ Código do api.ts usa função dinâmica

## CONFIGURAÇÃO ADICIONAL NO VERCEL (VOCÊ PRECISA FAZER):

1. Acesse: https://vercel.com/dashboard
2. Seu projeto LEGIA
3. Settings → Environment Variables
4. Adicionar:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://legia-backend.onrender.com`
   - Environment: Production

5. Redeploy o projeto

## TESTE MANUAL:

Abra console (F12) e execute:
```javascript
console.log(api.defaults.baseURL)
```

Deve mostrar: `https://legia-backend.onrender.com/api/v1`

Se mostrar URL do Vercel, a variável de ambiente não foi configurada.
