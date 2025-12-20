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

    ⚠️ Este endpoint deve ser REMOVIDO após uso!
    """
    try:
        # Criar tabelas
        Base.metadata.create_all(bind=engine)

        # Verificar se admin já existe
        existing_admin = db.query(LegiaUser).filter(
            LegiaUser.email == "admin@legia.com"
        ).first()

        if existing_admin:
            return {
                "status": "already_initialized",
                "message": "Plataforma já está inicializada",
                "admin_email": "admin@legia.com"
            }

        # Criar admin
        admin = LegiaUser(
            email="admin@legia.com",
            full_name="Administrador LEGIA",
            hashed_password=get_password_hash("Admin@123"),
            role="platform_admin",
            is_active=True,
            is_verified=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        return {
            "status": "success",
            "message": "Plataforma inicializada com sucesso!",
            "admin": {
                "email": "admin@legia.com",
                "password": "Admin@123",
                "warning": "⚠️ TROQUE A SENHA APÓS O PRIMEIRO LOGIN!"
            }
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
