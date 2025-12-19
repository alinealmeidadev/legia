"""
LEGIA PLATFORM - Aplicação Principal FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings

# Criar aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Rota raiz - Health check"""
    return {
        "message": "🚀 LEGIA PLATFORM API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get(f"{settings.API_V1_PREFIX}/")
async def api_root():
    """Rota raiz da API v1"""
    return {
        "message": "LEGIA PLATFORM API v1",
        "docs": f"{settings.API_V1_PREFIX}/docs",
        "redoc": f"{settings.API_V1_PREFIX}/redoc",
    }


# Tratamento de erros global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handler global para exceções não tratadas"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "detail": str(exc) if settings.DEBUG else "Entre em contato com o suporte"
        }
    )


# Incluir rotas da API v1
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Executado ao iniciar a aplicação"""
    print("=" * 60)
    print(f"🚀 {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"📦 Ambiente: {settings.ENVIRONMENT}")
    print(f"🔗 Docs: http://localhost:8000{settings.API_V1_PREFIX}/docs")
    print(f"🔑 Autenticação: JWT Bearer Token")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao desligar a aplicação"""
    print("\n👋 LEGIA PLATFORM desligando...")
