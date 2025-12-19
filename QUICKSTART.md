# ⚡ LEGIA PLATFORM - GUIA RÁPIDO

## 🚀 Como Rodar TUDO em 3 Comandos

```bash
# 1. Ir para a pasta do projeto
cd C:\Users\aline\OneDrive\Desktop\LEGIA

# 2. Subir todos os containers (backend + frontend + banco + redis)
docker-compose up -d

# 3. Aguardar ~30 segundos e acessar
```

**Pronto!** Sua aplicação está rodando:
- 🌐 **Frontend:** http://localhost:3000
- 🔌 **Backend API:** http://localhost:8000
- 📚 **Documentação:** http://localhost:8000/api/v1/docs

## 🔐 Login Rápido

### Super Admin (Gestão da Plataforma)
```
URL: http://localhost:3000
Email: admin@legia.com.br
Senha: admin123
Tenant ID: deixe vazio
```

### Tenant - Escritório XYZ (Uso Normal)
```
URL: http://localhost:3000
Email: admin@xyz.com
Senha: admin123
Tenant ID: 2
```

## 📋 O Que Você Pode Fazer

### Como Super Admin
✅ Ver dashboard com métricas
✅ Listar todos os tenants
✅ **NOVO: Criar e editar tenants com formulário completo**
✅ Ver detalhes de cada escritório
✅ Gerenciar planos e usuários

### Como Usuário de Tenant
✅ Ver dashboard do escritório
✅ Listar clientes
✅ **NOVO: Criar e editar clientes (PF e PJ)**
✅ **NOVO: Página de processos (estrutura pronta)**
✅ Upload de documentos (estrutura pronta)

## 🛠️ Comandos Úteis

```bash
# Ver logs do backend
docker-compose logs -f backend

# Ver logs do frontend
docker-compose logs -f frontend

# Reiniciar tudo
docker-compose restart

# Parar tudo
docker-compose down

# Limpar e recriar do zero
docker-compose down -v
docker-compose up -d --build
```

## 🐛 Problemas Comuns

### Frontend não carrega
```bash
# Reconstruir container
docker-compose up -d --build frontend
```

### Backend com erro
```bash
# Ver logs
docker-compose logs backend

# Reiniciar
docker-compose restart backend
```

### Banco de dados vazio
```bash
# Entrar no container e rodar seeds
docker-compose exec backend python -m app.db.seeds
```

## 📊 Status Atual do Projeto

### ✅ 100% Funcional
- Backend API REST completo
- Autenticação JWT (login/logout/refresh)
- Multi-tenancy (schemas separados)
- Banco de dados PostgreSQL + Redis
- Frontend Next.js moderno
- Login funcionando
- 2 Dashboards (Admin + Tenant)
- **Listagem e CRUD de Tenants (criar/editar)**
- **Listagem e CRUD de Clientes (criar/editar PF/PJ)**
- **Sistema de notificações Toast**
- **Página de Processos (estrutura pronta)**

### 🔨 Estrutura Pronta (Pode Expandir)
- Mais páginas CRUD (Processos, Documentos)
- Upload de arquivos
- Gráficos e relatórios
- Dark mode
- Filtros e busca avançada

### 📅 Para o Futuro (Sprint 7-12)
- 8 Agentes IA com Google Gemini
- Integração Asaas (pagamentos)
- WhatsApp API
- Email marketing
- Sistema de backup
- Monitoramento

## 💰 Custo Até Agora

**Sprint 1-6:** ~$2.00 USD
**Sprint 7-8:** ~$1.50 USD
**Total gasto:** ~$3.50 USD (de $4.78 disponível)
**Tokens usados:** ~75.000 / 200.000

## 🎯 Próximos Passos

1. **Testar tudo funcionando**
   - Criar tenant pelo formulário
   - Criar clientes (PF e PJ)
   - Editar registros
   - Verificar notificações toast

2. **Sprint 9-10 (se adicionar mais crédito):**
   - Backend de Processos completo
   - Upload de documentos
   - Gráficos no dashboard
   - Mais filtros e buscas

3. **Sprint 11-12 (Futuro):**
   - 8 Agentes IA com Google Gemini
   - Integração Asaas (pagamentos)
   - WhatsApp API
   - Email marketing

---

**Dúvidas?** Verifique os arquivos:
- `README.md` - Documentação completa do projeto
- `FRONTEND_README.md` - Detalhes do frontend
- `backend/README.md` - Detalhes do backend (se existir)
