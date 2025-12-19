# 🎨 LEGIA PLATFORM - FRONTEND

Frontend Next.js 14 com TypeScript e Tailwind CSS.

## 📦 Stack Tecnológico

- **Next.js 14** - App Router
- **TypeScript** - Tipagem forte
- **Tailwind CSS** - Estilização moderna
- **Shadcn/ui** - Componentes UI
- **Axios** - Cliente HTTP
- **React Hook Form** - Formulários
- **Zod** - Validação

## 🚀 Rodar o Frontend

### Com Docker (Recomendado)

```bash
# Na raiz do projeto LEGIA
docker-compose up frontend
```

O frontend estará disponível em: **http://localhost:3000**

### Sem Docker (Desenvolvimento Local)

```bash
cd frontend

# Instalar dependências
npm install

# Rodar em modo dev
npm run dev
```

## 🔐 Credenciais de Teste

### Super Admin (Legia)
- **Email:** admin@legia.com.br
- **Senha:** admin123
- **Tenant ID:** deixe vazio

### Tenant (Escritório XYZ)
- **Email:** admin@xyz.com
- **Senha:** admin123
- **Tenant ID:** 2

## 📁 Estrutura do Código

```
frontend/
├── app/                          # Páginas Next.js (App Router)
│   ├── globals.css               # Estilos globais
│   ├── layout.tsx                # Layout raiz
│   ├── page.tsx                  # Página inicial (redirect)
│   ├── login/                    # Página de login
│   ├── admin/                    # Páginas Super Admin
│   │   ├── layout.tsx            # Layout com sidebar
│   │   ├── page.tsx              # Dashboard
│   │   └── tenants/              # CRUD de tenants
│   └── tenant/                   # Páginas Tenant
│       ├── layout.tsx            # Layout com sidebar
│       ├── page.tsx              # Dashboard
│       └── clients/              # CRUD de clientes
├── components/                   # Componentes React
│   ├── ui/                       # Componentes base (Shadcn)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── label.tsx
│   │   └── card.tsx
│   └── sidebar.tsx               # Sidebar de navegação
├── lib/                          # Utilitários
│   ├── utils.ts                  # Funções auxiliares
│   ├── api.ts                    # Cliente Axios
│   └── auth.ts                   # Serviço de autenticação
└── package.json                  # Dependências

```

## 🎨 Páginas Implementadas

### ✅ Autenticação
- [x] **Login** - `/login`
  - Login Super Admin
  - Login Tenant User
  - Suporte a 2FA (preparado)

### ✅ Super Admin (Legia)
- [x] **Dashboard** - `/admin`
  - Métricas principais
  - Tenants recentes
- [x] **Tenants** - `/admin/tenants`
  - Lista de tenants
  - **NOVO: Criar tenant (formulário completo)**
  - **NOVO: Editar tenant (modal)**
  - Status e informações

### ✅ Tenant (Escritório)
- [x] **Dashboard** - `/tenant`
  - Métricas do escritório
  - Ações rápidas
- [x] **Clientes** - `/tenant/clients`
  - Lista de clientes
  - **NOVO: Criar cliente PF/PJ (formulário completo)**
  - **NOVO: Editar cliente (modal)**
  - Filtros e busca (preparado)
- [x] **Processos** - `/tenant/processes`
  - **NOVO: Página estruturada**
  - Lista de processos (estrutura pronta)
  - Aguardando backend endpoint

## 🔌 Integração com Backend

O frontend consome a API REST do backend:

- **Base URL:** `http://localhost:8000/api/v1`
- **Autenticação:** JWT Bearer Token
- **Refresh Token:** Automático via interceptor

### Exemplo de Requisição

```typescript
import api from '@/lib/api'

// O token é adicionado automaticamente
const response = await api.get('/tenants/')
console.log(response.data)
```

## 🎯 Funcionalidades Principais

### ✅ Sistema de Autenticação
- Login com JWT
- Refresh token automático
- Proteção de rotas
- Logout

### ✅ Layouts Responsivos
- Sidebar com navegação
- Dashboards com métricas
- Cards e componentes reutilizáveis

### ✅ Páginas CRUD Completas
- **Listagem com paginação (preparado)**
- **Formulários de criação (Tenant e Cliente)**
- **Modais de edição (Tenant e Cliente)**
- **Notificações Toast (sucesso/erro)**
- **Validação de campos (CPF, CNPJ, CEP)**
- Filtros e busca (preparado)

## 🎨 Temas e Estilos

### Cores Principais
- **Primary:** `#004E89` (Azul LEGIA)
- **Secondary:** `#FF6B35` (Laranja destaque)
- **Background:** Branco / Cinza claro

### Componentes UI
Todos os componentes seguem o padrão **Shadcn/ui**:
- Button
- Input
- Label
- Card
- **Dialog** (modais)
- **Select** (dropdowns)
- **Toast** (notificações)
- e mais...

## 🔧 Próximos Passos (Para Continuar)

### ✅ Sprint 7-8: CRUD Completo (CONCLUÍDO)
- [x] Formulários de criação (Tenant e Cliente)
- [x] Modais de edição (Tenant e Cliente)
- [x] Sistema de notificações Toast
- [x] Página de Processos (estrutura)
- [x] Validações e formatações

### Sprint 9-10: Features Avançadas
- [ ] Backend de Processos (criar/editar)
- [ ] Página de Documentos (upload)
- [ ] Gráficos nos dashboards (Recharts)
- [ ] Filtros e busca funcionais
- [ ] Paginação real

### Sprint 11-12: IA e Integrações
- [ ] Chat com agentes IA
- [ ] Integração Asaas (pagamentos)
- [ ] WhatsApp API
- [ ] Dark mode
- [ ] Tema customizado por tenant

## 📝 Notas Importantes

1. **CRUD Completo:** Formulários de criação e edição funcionais para Tenants e Clientes.

2. **API Integration:** Todas as chamadas de API estão prontas e funcionando.

3. **Responsivo:** Todos os layouts são responsivos e funcionam em mobile/tablet.

4. **TypeScript:** Todo código está tipado corretamente.

5. **Performance:** Next.js 14 com Server Components onde possível.

6. **Validações:** CPF, CNPJ e CEP com formatação automática.

## 🐛 Troubleshooting

### Erro de conexão com backend
```bash
# Verificar se backend está rodando
curl http://localhost:8000/health

# Reiniciar containers
docker-compose restart backend frontend
```

### Erro ao instalar dependências
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Frontend não atualiza
```bash
# Limpar cache do Next.js
cd frontend
rm -rf .next
npm run dev
```

---

**Frontend desenvolvido com ❤️ para a LEGIA PLATFORM**
