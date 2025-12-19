"""
LEGIA PLATFORM - Roteador Principal API v1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, tenants, clients, processes, agents, contracts, workflows


# Criar roteador principal
api_router = APIRouter()

# Incluir rotas de autenticação
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

# Incluir rotas de tenants (Super Admin)
api_router.include_router(
    tenants.router,
    prefix="/tenants",
    tags=["Tenants (Super Admin)"]
)

# Incluir rotas de clientes (Tenant)
api_router.include_router(
    clients.router,
    prefix="/clients",
    tags=["Clientes (Tenant)"]
)

# Incluir rotas de processos (Tenant)
api_router.include_router(
    processes.router,
    prefix="/processes",
    tags=["Processos (Tenant)"]
)

# Incluir rotas de agentes IA (Tenant)
api_router.include_router(
    agents.router,
    prefix="/agents",
    tags=["Agentes IA (Tenant)"]
)

# Incluir rotas de contratos (Tenant)
api_router.include_router(
    contracts.router,
    prefix="/contracts",
    tags=["Contratos (Tenant)"]
)

# Incluir rotas de workflows automatizados (Tenant)
api_router.include_router(
    workflows.router,
    prefix="/workflows",
    tags=["Workflows Automatizados (Tenant)"]
)

# TODO: Adicionar mais rotas
# - /plans (Super Admin)
# - /users (Ambos)
# - /processes (Tenant)
# - /documents (Tenant)
# - /quotes (Tenant)
# - /protocols (Tenant)
# - /communications (Tenant)
# - /dashboard (Ambos)
