"""
LEGIA PLATFORM - Setup Inicial (TEMPORÁRIO)
Este endpoint deve ser REMOVIDO após criar o primeiro admin!
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.db.base import Base
from app.db.session import engine
from app.models.public.legia_user import LegiaUser
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/init")
def initialize_platform(db: Session = Depends(get_db)):
    """
    🚨 ENDPOINT TEMPORÁRIO DE SETUP

    Cria:
    1. Todas as tabelas no banco
    2. Usuário admin inicial
    3. Planos e tenants de exemplo (se run_seeds=true)

    ⚠️ Este endpoint deve ser REMOVIDO após uso!
    """
    from app.db.seeds import seed_plans, seed_tenants

    try:
        # Criar tabelas
        Base.metadata.create_all(bind=engine)

        # Verificar se admin já existe
        existing_admin = db.query(LegiaUser).filter(
            LegiaUser.email == "admin@legia.com"
        ).first()

        seeds_executed = False
        if not existing_admin:
            # Criar admin
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
            db.refresh(admin)

            # Executar seeds automaticamente
            try:
                seed_plans(db)
                seed_tenants(db)
                seeds_executed = True
            except Exception as seed_error:
                print(f"Aviso: Erro ao executar seeds: {seed_error}")

            return {
                "status": "success",
                "message": "Plataforma inicializada com sucesso!",
                "admin": {
                    "email": "admin@legia.com",
                    "password": "Admin@123"
                },
                "seeds_executed": seeds_executed,
                "tenants": [
                    {"email": "admin@abc.com", "password": "admin123", "tenant_id": 1},
                    {"email": "admin@xyz.com", "password": "admin123", "tenant_id": 2}
                ] if seeds_executed else [],
                "warning": "⚠️ TROQUE TODAS AS SENHAS APÓS O LOGIN!"
            }
        else:
            # Tentar executar seeds mesmo se admin já existe
            try:
                seed_plans(db)
                seed_tenants(db)
                seeds_executed = True
            except Exception as seed_error:
                print(f"Aviso: Erro ao executar seeds: {seed_error}")

            return {
                "status": "already_initialized",
                "message": "Plataforma já está inicializada. Seeds executados.",
                "admin_email": "admin@legia.com",
                "seeds_executed": seeds_executed,
                "tenants": [
                    {"email": "admin@abc.com", "password": "admin123", "tenant_id": 1},
                    {"email": "admin@xyz.com", "password": "admin123", "tenant_id": 2}
                ] if seeds_executed else []
            }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao inicializar: {str(e)}")


@router.get("/status")
def check_setup_status(db: Session = Depends(get_db)):
    """
    Verifica se a plataforma já foi inicializada
    """
    try:
        admin_exists = db.query(LegiaUser).filter(
            LegiaUser.email == "admin@legia.com"
        ).first() is not None

        return {
            "initialized": admin_exists,
            "admin_email": "admin@legia.com" if admin_exists else None
        }
    except Exception as e:
        return {
            "initialized": False,
            "error": "Banco de dados ainda não inicializado",
            "detail": str(e)
        }


@router.post("/run-seeds")
def run_seeds_endpoint(db: Session = Depends(get_db)):
    """
    🚨 ENDPOINT TEMPORÁRIO - Executa seeds de dados iniciais
    Cria planos, tenants e usuários de exemplo
    """
    from app.db.seeds import seed_plans, seed_tenants

    try:
        seed_plans(db)
        seed_tenants(db)

        return {
            "status": "success",
            "message": "Seeds executados com sucesso!",
            "tenants": [
                {
                    "name": "Escritório ABC Contabilidade",
                    "tenant_id": 1,
                    "email": "admin@abc.com",
                    "password": "admin123"
                },
                {
                    "name": "Escritório XYZ Assessoria",
                    "tenant_id": 2,
                    "email": "admin@xyz.com",
                    "password": "admin123"
                }
            ]
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao executar seeds: {str(e)}")
