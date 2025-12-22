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
    allow_origins=[
        "http://localhost:3000",
        "https://legia-git-main-aline-almeidas-projects.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
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

    # Auto-inicialização do banco de dados (primeira vez)
    try:
        from app.db.base import Base
        from app.db.session import engine, SessionLocal
        from app.models.public.legia_user import LegiaUser
        from app.core.security import get_password_hash
        from sqlalchemy import inspect

        print("\n🔍 Verificando banco de dados...")

        # Verificar se tabelas existem
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        if not tables or 'legia_users' not in tables:
            print("📦 Criando tabelas do banco de dados...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tabelas criadas com sucesso!")
        else:
            print("✅ Tabelas já existem")

        # Verificar se existe admin
        db = SessionLocal()
        try:
            admin_exists = db.query(LegiaUser).filter(
                LegiaUser.email == "admin@legia.com"
            ).first()

            if not admin_exists:
                print("👤 Criando usuário administrador...")
                admin = LegiaUser(
                    email="admin@legia.com",
                    name="Administrador LEGIA",
                    password_hash=get_password_hash("Admin@123"),
                    role="superadmin",
                    is_active=True,
                    is_verified=True
                )
                db.add(admin)
                db.commit()
                print("✅ Admin criado: admin@legia.com / Admin@123")
                print("⚠️  IMPORTANTE: Troque a senha após o primeiro login!")
            else:
                print("✅ Usuário admin já existe")
        finally:
            db.close()

        # Executar migrações automáticas
        print("\n🔄 Executando migrações automáticas...")
        try:
            from app.models.public.tenant import Tenant
            from sqlalchemy import text

            tenants = db.query(Tenant).all()
            print(f"📦 Encontrados {len(tenants)} tenants")

            for tenant in tenants:
                schema_name = f"tenant_{tenant.id}"
                try:
                    # Adicionar client_number se não existir
                    db.execute(text(f"""
                        ALTER TABLE {schema_name}.clients
                        ADD COLUMN IF NOT EXISTS client_number INTEGER UNIQUE
                    """))

                    # Criar index
                    db.execute(text(f"""
                        CREATE INDEX IF NOT EXISTS idx_clients_number
                        ON {schema_name}.clients(client_number)
                    """))

                    # Preencher client_number
                    db.execute(text(f"""
                        UPDATE {schema_name}.clients
                        SET client_number = id
                        WHERE client_number IS NULL
                    """))

                    # Adicionar current_stage
                    db.execute(text(f"""
                        ALTER TABLE {schema_name}.processes
                        ADD COLUMN IF NOT EXISTS current_stage VARCHAR(100)
                    """))

                    # Adicionar department
                    db.execute(text(f"""
                        ALTER TABLE {schema_name}.processes
                        ADD COLUMN IF NOT EXISTS department VARCHAR(100)
                    """))

                    db.commit()
                    print(f"  ✅ Schema {schema_name} migrado")

                except Exception as migration_error:
                    print(f"  ⚠️  {schema_name}: {migration_error}")
                    db.rollback()

            print("✅ Migrações concluídas!")
        except Exception as migration_error:
            print(f"⚠️  Erro nas migrações: {migration_error}")

        print("🎉 Sistema inicializado e pronto para uso!\n")

    except Exception as e:
        print(f"⚠️  Erro na inicialização automática: {e}")
        print("💡 O sistema vai continuar, mas pode precisar de setup manual")


@app.on_event("shutdown")
async def shutdown_event():
    """Executado ao desligar a aplicação"""
    print("\n👋 LEGIA PLATFORM desligando...")
