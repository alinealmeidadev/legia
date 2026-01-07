# 📦 VERSÕES - LEGIA Platform
**Controle de Versões de Tecnologias Utilizadas**

---

## 🐍 BACKEND (Python)

### Runtime
| Tecnologia | Versão | Notas |
|------------|--------|-------|
| **Python** | 3.13.7 | Ambiente local |
| **Python (recomendado)** | 3.11+ | Para produção |

### Framework e Servidor
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **FastAPI** | 0.109.0 | Framework web API-first |
| **Uvicorn** | 0.27.0 | Servidor ASGI (com `[standard]`) |
| **Python-multipart** | 0.0.6 | Upload de arquivos |

### Banco de Dados
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **SQLAlchemy** | 2.0.25 | ORM moderno |
| **Alembic** | 1.13.1 | Migrations |
| **psycopg2-binary** | 2.9.9 | Driver PostgreSQL (sync) |
| **asyncpg** | 0.29.0 | Driver PostgreSQL (async) |
| **PostgreSQL** | 15+ | Banco de dados (via Docker) |

### Validação
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Pydantic** | 2.5.3 | Validação e serialização |
| **Pydantic Settings** | 2.1.0 | Configurações |
| **Email Validator** | 2.1.0 | Validação de emails |

### Autenticação e Segurança
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **python-jose** | 3.3.0 | JWT (com `[cryptography]`) |
| **passlib** | 1.7.4 | Hashing de senhas (com `[bcrypt]`) |
| **bcrypt** | 4.1.2 | Algoritmo de hash |
| **pyotp** | 2.9.0 | 2FA/TOTP (não usado ainda) |

### Cache e Filas
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Redis** | 5.0.1 | Cliente Python |
| **Redis (servidor)** | 7.x | Cache (via Docker) |
| **Celery** | 5.3.6 | Filas de tarefas (não usado ainda) |

### HTTP Client
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **httpx** | 0.26.0 | Cliente HTTP async |
| **aiohttp** | 3.9.1 | Cliente HTTP async alternativo |

### IA / Machine Learning
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **google-generativeai** | ≥0.8.0 | Google Gemini API |
| **Gemini Model** | gemini-1.5-pro | Modelo usado pelos 9 agentes |

**API Key:** Configurada em `GOOGLE_API_KEY` (.env)

### Utilidades
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **python-dotenv** | 1.0.0 | Variáveis de ambiente |
| **python-dateutil** | 2.8.2 | Manipulação de datas |
| **pytz** | 2023.3 | Timezones |
| **loguru** | 0.7.2 | Logging estruturado |

### Arquivos e Dados
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **python-magic** | 0.4.27 | Detecção de tipo de arquivo |
| **Pillow** | 10.2.0 | Processamento de imagens |
| **openpyxl** | 3.1.5 | Leitura/escrita Excel |
| **pandas** | 2.3.2 | Manipulação de dados |

### Testes
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **pytest** | 7.4.4 | Framework de testes |
| **pytest-asyncio** | 0.23.3 | Suporte async |
| **pytest-cov** | 4.1.0 | Cobertura de código |
| **Faker** | 22.0.0 | Dados fake para testes |

---

## ⚛️ FRONTEND (Next.js)

### Runtime e Framework
| Tecnologia | Versão | Notas |
|------------|--------|-------|
| **Node.js** | 20.x | Recomendado (LTS) |
| **Next.js** | 14.0.4 | Framework React |
| **React** | 18.2.0 | Biblioteca UI |
| **React DOM** | 18.2.0 | Renderização DOM |
| **TypeScript** | 5.3.3 | Tipagem forte |

### Estilização
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **TailwindCSS** | 3.4.0 | CSS utilitário |
| **PostCSS** | 8.4.32 | Processador CSS |
| **Autoprefixer** | 10.4.16 | Prefixos CSS |
| **tailwind-merge** | 2.2.0 | Merge de classes Tailwind |
| **tailwindcss-animate** | 1.0.7 | Animações Tailwind |
| **class-variance-authority** | 0.7.0 | Variantes de componentes |
| **clsx** | 2.1.0 | Construção de classes CSS |

### Componentes UI (Radix UI / shadcn/ui)
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **@radix-ui/react-checkbox** | 1.3.3 | Checkbox acessível |
| **@radix-ui/react-dialog** | 1.0.5 | Modais/Dialogs |
| **@radix-ui/react-dropdown-menu** | 2.0.6 | Dropdowns |
| **@radix-ui/react-label** | 2.0.2 | Labels |
| **@radix-ui/react-select** | 2.0.0 | Selects |
| **@radix-ui/react-slot** | 1.0.2 | Slot composition |
| **@radix-ui/react-toast** | 1.1.5 | Notificações toast |
| **lucide-react** | 0.302.0 | Ícones |

### Estado e Dados
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Zustand** | 4.4.7 | State management |
| **@tanstack/react-query** | 5.17.9 | Cache e fetch de dados |
| **Axios** | 1.6.5 | Cliente HTTP |

### Formulários
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **react-hook-form** | 7.49.2 | Gerenciamento de forms |
| **@hookform/resolvers** | 3.3.4 | Resolvers para validação |
| **Zod** | 3.22.4 | Schema validation |

### Linting
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **ESLint** | 8.56.0 | Linter JavaScript/TypeScript |
| **eslint-config-next** | 14.0.4 | Config ESLint para Next.js |

---

## 🐳 INFRAESTRUTURA E DEVOPS

### Containerização
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Docker** | 20.x+ | Containerização |
| **Docker Compose** | 2.x+ | Orquestração multi-container |

### Banco de Dados (Produção)
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **PostgreSQL** | 15+ | Banco relacional |
| **Redis** | 7.x | Cache e sessions |

### Deploy
| Plataforma | Custo | Status | URL |
|------------|-------|--------|-----|
| **Vercel** (Frontend) | R$ 0 (plano gratuito) | ✅ ONLINE | https://legia-git-main-aline-almeidas-projects.vercel.app |
| **Render.com** (Backend) | R$ 0 (plano gratuito) | ❌ PENDENTE | N/A |

---

## 🤖 INTELIGÊNCIA ARTIFICIAL

### Claude Code (Desenvolvimento)
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Claude Code** | Latest | CLI de desenvolvimento |
| **Modelo** | Claude Sonnet 4.5 | `claude-sonnet-4-5-20250929` |
| **Cutoff de conhecimento** | Janeiro 2025 | Data limite |
| **Contexto máximo** | 200.000 tokens | Limite de conversa |

### Google Gemini (Agentes IA)
| Tecnologia | Versão/Modelo | Propósito |
|------------|---------------|-----------|
| **google-generativeai** | ≥0.8.0 | SDK Python |
| **Modelo** | gemini-1.5-pro | LLM para os 9 agentes |
| **Contexto** | 1M tokens | Janela de contexto |
| **Custo** | ~R$ 0.50/1M input tokens | Preço estimado |

**Agentes implementados:** 9/9 (100%)
**Testes passando:** 27/27 (100%)

---

## 🔧 FERRAMENTAS DE DESENVOLVIMENTO

### Editores e IDEs
| Ferramenta | Recomendado |
|------------|-------------|
| **VS Code** | ✅ Recomendado |
| **PyCharm** | Alternativa |

### Extensões VS Code Recomendadas
- Python
- Pylance
- Black Formatter
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- GitHub Copilot (opcional)

---

## 📊 COMPATIBILIDADE

### Python
- **Mínimo:** Python 3.11
- **Recomendado:** Python 3.11 - 3.12
- **Testado:** Python 3.13.7 (funciona mas não recomendado para produção)
- **Não suportado:** Python 3.10 ou inferior

### Node.js
- **Mínimo:** Node.js 18.x (LTS)
- **Recomendado:** Node.js 20.x (LTS)
- **Testado:** Node.js 20.x

### Navegadores (Frontend)
- **Chrome/Edge:** 100+
- **Firefox:** 100+
- **Safari:** 15+
- **Mobile:** iOS 15+, Android Chrome

---

## 🔄 ATUALIZAÇÕES RECENTES

### Backend
- **FastAPI 0.109.0** - Atualizado em Dezembro 2025
- **SQLAlchemy 2.0.25** - SQLAlchemy 2.0 (nova API)
- **Pydantic 2.5.3** - Pydantic v2 (breaking changes)

### Frontend
- **Next.js 14.0.4** - App Router (nova arquitetura)
- **React 18.2.0** - Server Components
- **TypeScript 5.3.3** - Decorators, satisfies operator

---

## ⚠️ BREAKING CHANGES CONHECIDOS

### SQLAlchemy 2.0
- Nova sintaxe de queries (mais explícita)
- Método `execute()` retorna `Result` ao invés de cursor
- Migrations Alembic precisam ser adaptadas

### Pydantic v2
- `validator` → `field_validator`
- `Config` → `model_config`
- Performance muito melhor (até 10x)

### Next.js 14 App Router
- `pages/` → `app/` (nova estrutura)
- Server Components por padrão
- `getServerSideProps` → Server Components
- Layouts aninhados

---

## 📝 GERENCIAMENTO DE DEPENDÊNCIAS

### Backend
**Arquivo:** `backend/requirements.txt`

**Instalar:**
```bash
pip install -r requirements.txt
```

**Atualizar:**
```bash
pip list --outdated
pip install --upgrade <pacote>
pip freeze > requirements.txt
```

### Frontend
**Arquivo:** `frontend/package.json`

**Instalar:**
```bash
npm install
```

**Atualizar:**
```bash
npm outdated
npm update <pacote>
```

---

## 🔐 SEGURANÇA

### Versões com Vulnerabilidades Conhecidas
**Nenhuma no momento** (última verificação: 06/01/2026)

**Verificar vulnerabilidades:**
```bash
# Backend
pip-audit

# Frontend
npm audit
```

---

## 🎯 PRÓXIMAS ATUALIZAÇÕES PLANEJADAS

### Backend
- ⏳ FastAPI 0.110+ (quando lançar)
- ⏳ SQLAlchemy 2.1+ (quando lançar)

### Frontend
- ⏳ Next.js 15 (quando estável)
- ⏳ React 19 (quando lançar)

---

## 📚 DOCUMENTAÇÃO DAS TECNOLOGIAS

### Backend
- **FastAPI:** https://fastapi.tiangolo.com/
- **SQLAlchemy:** https://docs.sqlalchemy.org/en/20/
- **Pydantic:** https://docs.pydantic.dev/latest/
- **Alembic:** https://alembic.sqlalchemy.org/

### Frontend
- **Next.js:** https://nextjs.org/docs
- **React:** https://react.dev/
- **TailwindCSS:** https://tailwindcss.com/docs
- **shadcn/ui:** https://ui.shadcn.com/

### IA
- **Google Gemini:** https://ai.google.dev/
- **Claude API:** https://docs.anthropic.com/

---

**Última atualização:** 06/01/2026
**Próxima revisão:** Mensal ou quando atualizar versões importantes
