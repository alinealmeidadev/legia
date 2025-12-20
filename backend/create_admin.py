"""
Script para criar primeiro usuário admin da plataforma LEGIA
Execute: python create_admin.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.database import Base, engine, SessionLocal
from app.models.user import LegiaUser
from app.core.security import get_password_hash
from sqlalchemy.exc import IntegrityError

def create_tables():
    """Cria todas as tabelas no banco"""
    print("🔧 Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

def create_admin_user():
    """Cria usuário admin inicial"""
    db = SessionLocal()

    try:
        # Verificar se já existe admin
        existing = db.query(LegiaUser).filter(LegiaUser.email == "admin@legia.com").first()
        if existing:
            print("⚠️  Usuário admin já existe!")
            print(f"📧 Email: admin@legia.com")
            return

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

        print("✅ Usuário admin criado com sucesso!")
        print(f"📧 Email: admin@legia.com")
        print(f"🔑 Senha: Admin@123")
        print("\n⚠️  IMPORTANTE: Troque a senha após o primeiro login!")

    except IntegrityError:
        print("⚠️  Usuário admin já existe!")
        db.rollback()
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 LEGIA PLATFORM - Setup Inicial\n")
    print("=" * 50)

    # Criar tabelas
    create_tables()
    print()

    # Criar admin
    create_admin_user()
    print()
    print("=" * 50)
    print("✅ Setup concluído! Você já pode fazer login no site.")
