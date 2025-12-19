# LEGIA PLATFORM - Checklist de Adaptações

## 🎯 PROPÓSITO DESTE DOCUMENTO

Este checklist mostra **EXATAMENTE O QUE ADAPTAR** ao usar o guia original do LEG.Agents para criar a LEGIA PLATFORM multi-tenant.

**Use quando:** Claude gerar código baseado em exemplos simples mas você precisa da versão multi-tenant.

---

## 📋 ADAPT

AÇÕES PRIORITÁRIAS

### ⚠️ ADAPTAÇÃO CRÍTICA 1: Database Multi-Schema

**O QUE MUDAR:**
- ❌ Database único com todas as tabelas
- ✅ Database com múltiplos schemas (um por tenant)

**ONDE MUDAR:**
```
Arquivo: backend/app/core/database.py
```

**ANTES (Simples):**
```python
DATABASE_URL = "postgresql://user:pass@localhost/legagents"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
```

**DEPOIS (Multi-tenant):**
```python
DATABASE_URL = "postgresql://user:pass@localhost/legia_platform_db"

engine = create_engine(DATABASE_URL)

# Criar session com schema dinâmico
def get_db(schema: str = "public"):
    db = SessionLocal()
    # Define schema para esta sessão
    db.execute(text(f"SET search_path TO {schema}"))
    try:
        yield db
    finally:
        db.close()
```

---

### ⚠️ ADAPTAÇÃO CRÍTICA 2: Middleware de Tenant

**O QUE ADICIONAR:**
Middleware que identifica qual tenant está fazendo a requisição.

**CRIAR ARQUIVO:**
```
backend/app/middleware/tenant.py
```

**CÓDIGO:**
```python
from fastapi import Request
from app.models.tenant import Tenant

class TenantMiddleware:
    async def __call__(self, request: Request, call_next):
        # Extrair subdomain
        host = request.headers.get("host", "")
        subdomain = host.split(".")[0]
        
        # Buscar tenant (usa schema public)
        tenant = await Tenant.get_by_subdomain(subdomain)
        
        if not tenant:
            return {"error": "Tenant not found"}, 404
        
        # Armazenar no request
        request.state.tenant_id = tenant.id
        request.state.tenant_schema = f"tenant_{tenant.id}"
        
        # Processar request
        response = await call_next(request)
        return response
```

**REGISTRAR NO MAIN:**
```python
# backend/app/main.py
from app.middleware.tenant import TenantMiddleware

app = FastAPI()
app.add_middleware(TenantMiddleware)
```

---

### ⚠️ ADAPTAÇÃO CRÍTICA 3: Modelos com Schema Dinâmico

**O QUE MUDAR:**
Modelos devem usar o schema correto automaticamente.

**ANTES (Simples):**
```python
# backend/app/models/client.py
class Client(Base):
    __tablename__ = "clients"
    # ...
```

**DEPOIS (Multi-tenant):**
```python
# backend/app/models/client.py
from app.core.database import get_current_schema

class Client(Base):
    __tablename__ = "clients"
    __table_args__ = {
        'schema': get_current_schema()  # Schema dinâmico!
    }
    # ...
```

---

### ⚠️ ADAPTAÇÃO CRÍTICA 4: Rotas com Tenant Context

**O QUE MUDAR:**
Todas as rotas de tenant devem usar o schema correto.

**ANTES (Simples):**
```python
@router.get("/clients")
async def list_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients
```

**DEPOIS (Multi-tenant):**
```python
@router.get("/clients")
async def list_clients(
    request: Request,
    db: Session = Depends(get_db)
):
    # Usar schema do tenant
    schema = request.state.tenant_schema
    db.execute(text(f"SET search_path TO {schema}"))
    
    clients = db.query(Client).all()
    return clients
```

---

## 📝 LISTA COMPLETA DE ADAPTAÇÕES

### BACKEND

#### Arquivo: `backend/app/core/config.py`
```python
# ADICIONAR:
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Multi-tenancy
    TENANT_SCHEMA_PREFIX: str = "tenant_"
    DEFAULT_SCHEMA: str = "public"
    
    # Subdomains
    BASE_DOMAIN: str = "legiaplatform.com.br"
    ALLOW_LOCALHOST: bool = True  # Para desenvolvimento
```

#### Arquivo: `backend/app/models/__init__.py`
```python
# ORGANIZAR EM 2 GRUPOS:

# Modelos GLOBAIS (schema public):
from app.models.tenant import Tenant
from app.models.plan import Plan
from app.models.subscription import Subscription
from app.models.payment import Payment
from app.models.legia_user import LegiaUser

# Modelos POR TENANT (schema tenant_XXX):
from app.models.user import User
from app.models.client import Client
from app.models.process import Process
from app.models.document import Document
# ... todos os outros
```

#### Arquivo: `backend/app/api/deps.py`
```python
# ADICIONAR:
from fastapi import Request, HTTPException

def get_current_tenant(request: Request) -> int:
    """Retorna ID do tenant atual"""
    if not hasattr(request.state, "tenant_id"):
        raise HTTPException(status_code=400, detail="Tenant not found")
    return request.state.tenant_id

def get_tenant_schema(request: Request) -> str:
    """Retorna schema do tenant atual"""
    if not hasattr(request.state, "tenant_schema"):
        raise HTTPException(status_code=400, detail="Tenant schema not found")
    return request.state.tenant_schema
```

---

### FRONTEND

#### Arquivo: `frontend/next.config.js`
```javascript
// ADICIONAR suporte a subdomínios
module.exports = {
  async rewrites() {
    return [
      {
        source: '/:path*',
        has: [
          {
            type: 'host',
            value: ':subdomain.legiaplatform.com.br',
          },
        ],
        destination: '/tenant/:path*',
      },
    ]
  },
}
```

#### Arquivo: `frontend/lib/api.ts`
```typescript
// ADICIONAR:
export function getTenantFromHost(): string {
  if (typeof window === 'undefined') return '';
  
  const host = window.location.host;
  const subdomain = host.split('.')[0];
  
  // Localhost: tenant-001.localhost:3000
  // Produção: escritorio-abc.legiaplatform.com.br
  return subdomain;
}

export async function apiCall(endpoint: string, options: RequestInit = {}) {
  const tenant = getTenantFromHost();
  
  const headers = {
    ...options.headers,
    'X-Tenant': tenant,  // Envia tenant no header
  };
  
  return fetch(`/api${endpoint}`, { ...options, headers });
}
```

---

### MIGRATIONS

#### Criar schemas de tenants:
```sql
-- migrations/001_create_schemas.sql

-- Schema global (Legia)
CREATE SCHEMA IF NOT EXISTS public;

-- Schemas de exemplo para tenants
CREATE SCHEMA IF NOT EXISTS tenant_001;
CREATE SCHEMA IF NOT EXISTS tenant_002;

-- Function para criar novo tenant
CREATE OR REPLACE FUNCTION create_tenant_schema(tenant_id INTEGER)
RETURNS VOID AS $$
BEGIN
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS tenant_%s', tenant_id);
END;
$$ LANGUAGE plpgsql;
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

### Multi-tenancy Básico
- [ ] Middleware de tenant criado
- [ ] Schemas separados (public + tenant_XXX)
- [ ] Subdomain identifica tenant
- [ ] Session usa schema correto
- [ ] Modelos isolados por schema

### Testes de Isolamento
- [ ] Criar dado em tenant_001
- [ ] Verificar que tenant_002 NÃO vê
- [ ] Login em tenant_001 funciona
- [ ] Login em tenant_002 funciona
- [ ] Dados não vazam entre tenants

### Painel Super Admin
- [ ] Acessa schema public (não tenant)
- [ ] Lista todos os tenants
- [ ] Cria novos tenants
- [ ] "Login como" funciona
- [ ] Métricas globais corretas

### Painel Tenant
- [ ] Acessa apenas seu schema
- [ ] Não vê outros tenants
- [ ] CRUD de clientes funciona
- [ ] CRUD de processos funciona
- [ ] Documentos isolados

### Segurança
- [ ] Token JWT contém tenant_id
- [ ] Middleware valida tenant
- [ ] Queries forçam schema correto
- [ ] Impossível acessar outro tenant via API
- [ ] Log de auditoria por tenant

---

## 🚨 ERROS COMUNS E SOLUÇÕES

### Erro: "relation does not exist"
**Causa:** Schema não está sendo definido corretamente

**Solução:**
```python
# Sempre definir schema antes de query
db.execute(text(f"SET search_path TO {schema}"))
```

### Erro: "Tenant not found"
**Causa:** Subdomain não está sendo extraído corretamente

**Solução:**
```python
# Verificar formato do host
# Desenvolvimento: tenant-001.localhost:3000
# Produção: escritorio-abc.legiaplatform.com.br

# Extrair subdomain corretamente
parts = host.split(".")
subdomain = parts[0] if len(parts) > 1 else "default"
```

### Erro: "Dados vazando entre tenants"
**Causa:** Esqueceu de definir schema em alguma query

**Solução:**
```python
# SEMPRE usar middleware ou dependency
def get_db(request: Request):
    schema = request.state.tenant_schema
    db = SessionLocal()
    db.execute(text(f"SET search_path TO {schema}"))
    # ...
```

---

## 📊 ORDEM DE IMPLEMENTAÇÃO

### Prioridade ALTA (fazer primeiro)
1. ✅ Setup database multi-schema
2. ✅ Middleware de tenant
3. ✅ Modelos global vs tenant
4. ✅ Rotas com context correto
5. ✅ Testes de isolamento

### Prioridade MÉDIA (depois do básico)
6. ✅ Painel Super Admin
7. ✅ Painel Tenant
8. ✅ Sistema de pagamentos
9. ✅ Onboarding de tenants

### Prioridade BAIXA (features extras)
10. ✅ White label por tenant
11. ✅ Domínio customizado
12. ✅ Métricas avançadas

---

## 🎯 RESUMO EXECUTIVO

**O que muda do modelo simples para multi-tenant:**

1. **Database:** Schema único → Múltiplos schemas
2. **Identificação:** - → Subdomain define tenant
3. **Middleware:** - → Extrai e valida tenant
4. **Queries:** Diretas → Com schema prefix
5. **Isolamento:** - → Total por tenant
6. **Painéis:** 1 → 2 (Super Admin + Tenant)

**Complexidade adicional:** +30% de código  
**Benefício:** Plataforma SaaS completa e escalável!

---

**Versão:** 1.0.0  
**Data:** 17/12/2024  
**Próximo documento:** 04-Database-Schema.md
