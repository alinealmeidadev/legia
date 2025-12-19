# 🚀 LEGIA PLATFORM

Plataforma SaaS B2B multi-tenant para escritórios de contabilidade no Brasil.

**Versão:** 1.0.0 (MVP - Sprint 1-2 Fundação)
**Status:** 🟢 Em Desenvolvimento

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Rodar](#-como-rodar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Endpoints](#-api-endpoints)
- [Multi-Tenancy](#-multi-tenancy)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)

---

## 🎯 Visão Geral

LEGIA PLATFORM é uma plataforma SaaS que fornece sistemas especializados baseados em IA para escritórios de contabilidade.

**Produto Inicial:** LEG.Agents - Sistema de 8 agentes de IA que automatizam processos de legalização empresarial.

### Arquitetura Multi-Tenant

- **Schema por Tenant**: Cada escritório tem um schema PostgreSQL isolado
- **3 Níveis de Acesso**: Super Admin (Legia) → Tenant Admin (Escritório) → Funcionário
- **Isolamento Total**: Dados completamente separados entre tenants

---

## 🛠️ Tecnologias

### Backend
- **Python 3.11+**
- **FastAPI** - Framework web
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL 15+** - Banco de dados (multi-schema)
- **Redis 7+** - Cache e filas
- **Alembic** - Migrations
- **Pydantic V2** - Validação

### IA
- **Google Gemini 3.0** - LLM para agentes
- **Google ADK** - Agentic Development Kit

### Pagamentos
- **Asaas** - Gateway de pagamentos brasileiro

### DevOps
- **Docker & Docker Compose**
- **GitHub Actions** (futuro)

---

## ✅ Pré-requisitos

- **Docker Desktop** instalado e rodando
- **Git** para clonar o repositório
- **Chaves API**:
  - Google Gemini API Key
  - Asaas Sandbox API Key

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone <repo-url>
cd LEGIA
```

### 2. Configure as variáveis de ambiente

O arquivo `.env` já está configurado com as chaves fornecidas. Verifique se as informações estão corretas:

```bash
# Verificar .env
cat .env
```

**Principais variáveis:**
- `DATABASE_URL`: URL do PostgreSQL
- `REDIS_URL`: URL do Redis
- `GEMINI_API_KEY`: Sua chave do Google Gemini
- `ASAAS_API_KEY`: Sua chave do Asaas (Sandbox)

### 3. Suba os containers Docker

```bash
docker-compose up -d
```

Isso vai iniciar:
- PostgreSQL (porta 5432)
- Redis (porta 6379)
- Backend FastAPI (porta 8000)

### 4. Execute o setup inicial

Entre no container do backend:

```bash
docker-compose exec backend bash
```

Execute o script de setup:

```bash
python setup.py
```

Isso vai:
1. Aguardar o banco estar pronto
2. Executar migrations (criar tabelas)
3. Executar seeds (dados iniciais)

---

## 🎮 Como Rodar

### Desenvolvimento (com Docker)

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Parar serviços
docker-compose down
```

### Acessos

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **API** | http://localhost:8000 | - |
| **Documentação** | http://localhost:8000/api/v1/docs | - |
| **Super Admin** | - | admin@legia.com.br / admin123 |
| **Tenant ABC** | http://abc.localhost:8000 | admin@abc.local / admin123 |
| **Tenant XYZ** | http://xyz.localhost:8000 | admin@xyz.local / admin123 |

⚠️ **IMPORTANTE**: Altere todas as senhas padrão após o primeiro login!

---

## 📁 Estrutura do Projeto

```
LEGIA/
├── backend/                    # Backend FastAPI
│   ├── app/
│   │   ├── api/                # Rotas da API
│   │   ├── core/               # Configurações, segurança
│   │   ├── db/                 # Database, sessions, seeds
│   │   ├── models/             # Modelos SQLAlchemy
│   │   │   ├── public/         # Schema public (Legia)
│   │   │   └── tenant/         # Schema tenant (Escritórios)
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Lógica de negócio
│   │   ├── middleware/         # Middlewares
│   │   ├── utils/              # Utilitários
│   │   └── main.py             # Aplicação principal
│   ├── migrations/             # Alembic migrations
│   ├── tests/                  # Testes
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile              # Imagem Docker
│   └── setup.py                # Script de setup
├── frontend/                   # Frontend Next.js (futuro)
├── docker/                     # Arquivos Docker
│   └── init-db.sql             # Inicialização do banco
├── docker-compose.yml          # Orquestração Docker
├── .env                        # Variáveis de ambiente
├── .env.example                # Exemplo de .env
├── prd.md                      # Documento de requisitos
└── README.md                   # Este arquivo
```

---

## 🔌 API Endpoints

### Health Check

```http
GET /
GET /health
```

### API v1

```http
GET /api/v1/
```

**Documentação interativa:**
- Swagger UI: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## 🏢 Multi-Tenancy

### Como Funciona

1. **Schema Separado**: Cada escritório (tenant) tem seu próprio schema PostgreSQL
   - `public`: Dados globais da Legia (tenants, planos, pagamentos)
   - `tenant_001`: Dados do Escritório ABC
   - `tenant_002`: Dados do Escritório XYZ

2. **Identificação**: Por subdomínio
   - `abc.legiaplatform.com.br` → tenant_001
   - `xyz.legiaplatform.com.br` → tenant_002

3. **Isolamento**: Impossível acessar dados de outros tenants
   - Middleware define o schema por requisição
   - Queries só veem dados do schema ativo

### Criando Novo Tenant

```python
from app.models.public.tenant import Tenant
from app.utils.tenant_schema import create_tenant_schema

# 1. Criar registro do tenant
tenant = Tenant(
    name="Escritório Novo",
    subdomain="novo",
    cnpj="11.222.333/0001-44",
    email="contato@novo.com.br"
)
db.add(tenant)
db.flush()

# 2. Criar schema do tenant
create_tenant_schema(tenant.id, db)
```

---

## 💻 Desenvolvimento

### Executar migrations

```bash
# No container
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1

# Criar nova migration
docker-compose exec backend alembic revision --autogenerate -m "descricao"
```

### Executar seeds

```bash
docker-compose exec backend python app/db/seeds.py
```

### Acessar banco de dados

```bash
docker-compose exec postgres psql -U postgres -d legia_platform_db
```

```sql
-- Listar schemas
\dn

-- Ver tabelas do schema public
\dt public.*

-- Ver tabelas do tenant_001
\dt tenant_001.*

-- Testar isolamento
SET search_path TO tenant_001;
SELECT * FROM clients;
```

---

## 🧪 Testes

```bash
# Rodar todos os testes
docker-compose exec backend pytest

# Com coverage
docker-compose exec backend pytest --cov=app --cov-report=html

# Teste específico
docker-compose exec backend pytest tests/test_tenant.py -v
```

---

## 📊 Status Atual (Sprint 1-2)

### ✅ Completo

- [x] Estrutura do projeto
- [x] Docker Compose configurado
- [x] FastAPI estruturado
- [x] Multi-tenancy implementado
- [x] Modelos SQLAlchemy (public + tenant)
- [x] Migrations com Alembic
- [x] Seeds de dados iniciais
- [x] Sistema de segurança (JWT, bcrypt)
- [x] Variáveis de ambiente

### 🔄 Em Progresso

- [ ] Sistema de autenticação completo
- [ ] Middleware de identificação de tenant
- [ ] CRUD básico Super Admin
- [ ] CRUD básico Tenant Admin

### 📋 Próximas Sprints

- Sprint 3-4: Painel Super Admin
- Sprint 5-6: Painel Tenant Admin
- Sprint 7-10: LEG.Agents Core (Orquestrador + Agentes)
- Sprint 11-12: LEG.Agents Completo (8 agentes)

---

## 🔐 Segurança

- ✅ Senhas com bcrypt (cost 12)
- ✅ JWT para autenticação
- ✅ 2FA disponível (TOTP)
- ✅ Isolamento total de dados (multi-tenant)
- ✅ HTTPS/TLS 1.3 (produção)
- ✅ CORS configurado
- ✅ SQL Injection protegido (SQLAlchemy)

---

## 🤝 Contribuindo

Este é um projeto em desenvolvimento inicial. Guidelines de contribuição serão adicionados em breve.

---

## 📄 Licença

Propriedade da LEGIA. Todos os direitos reservados.

---

## 📞 Suporte

Para dúvidas ou problemas:
- Email: suporte@legia.com.br
- Documentação: Ver arquivos `prd.md` e guias na pasta raiz

---

**Desenvolvido com ❤️ para escritórios de contabilidade brasileiros.**
