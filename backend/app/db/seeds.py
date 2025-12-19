"""
LEGIA PLATFORM - Seeds de Dados Iniciais
"""
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.public.plan import Plan
from app.models.public.tenant import Tenant
from app.models.public.legia_user import LegiaUser
from app.models.public.subscription import Subscription
from app.db.session import SessionLocal
from app.utils.tenant_schema import create_tenant_schema
from app.core.config import settings


def seed_plans(db: Session) -> None:
    """
    Cria os 3 planos padrão
    """
    print("\n📦 Criando planos...")

    plans_data = [
        {
            "name": "Básico",
            "slug": "basico",
            "description": "Ideal para escritórios pequenos iniciando",
            "price_monthly": 297.00,
            "price_yearly": 2970.00,
            "max_users": 3,
            "max_clients": 50,
            "max_storage_gb": 10,
            "features": ["leg_agents"],
            "color": "#3B82F6",
            "display_order": 1
        },
        {
            "name": "Pro",
            "slug": "pro",
            "description": "Para escritórios médios em crescimento",
            "price_monthly": 597.00,
            "price_yearly": 5970.00,
            "max_users": 10,
            "max_clients": 200,
            "max_storage_gb": 50,
            "features": ["leg_agents", "whatsapp_api", "email_marketing"],
            "color": "#8B5CF6",
            "display_order": 2
        },
        {
            "name": "Premium",
            "slug": "premium",
            "description": "Para escritórios grandes estabelecidos",
            "price_monthly": 997.00,
            "price_yearly": 9970.00,
            "max_users": None,  # Ilimitado
            "max_clients": None,  # Ilimitado
            "max_storage_gb": 200,
            "features": ["leg_agents", "whatsapp_api", "email_marketing", "api", "white_label"],
            "color": "#F59E0B",
            "display_order": 3
        }
    ]

    for plan_data in plans_data:
        # Verificar se já existe
        existing = db.query(Plan).filter(Plan.slug == plan_data["slug"]).first()
        if existing:
            print(f"  ⏭️  Plano '{plan_data['name']}' já existe")
            continue

        plan = Plan(**plan_data)
        db.add(plan)
        print(f"  ✅ Plano '{plan_data['name']}' criado")

    db.commit()
    print("✅ Planos criados com sucesso!\n")


def seed_superadmin(db: Session) -> None:
    """
    Cria o super admin padrão
    """
    print("👤 Criando super admin...")

    # Verificar se já existe
    existing = db.query(LegiaUser).filter(
        LegiaUser.email == settings.FIRST_SUPERUSER_EMAIL
    ).first()

    if existing:
        print("  ⏭️  Super admin já existe\n")
        return

    superadmin = LegiaUser(
        email=settings.FIRST_SUPERUSER_EMAIL,
        password_hash=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
        name=settings.FIRST_SUPERUSER_NAME,
        role="superadmin",
        is_active=True,
        is_verified=True
    )

    db.add(superadmin)
    db.commit()

    print(f"  ✅ Super admin criado: {settings.FIRST_SUPERUSER_EMAIL}")
    print(f"  🔑 Senha: {settings.FIRST_SUPERUSER_PASSWORD}")
    print("  ⚠️  IMPORTANTE: Altere a senha no primeiro login!\n")


def seed_tenants(db: Session) -> None:
    """
    Cria 2 tenants de exemplo
    """
    print("🏢 Criando tenants de exemplo...")

    # Buscar plano Pro
    plan_pro = db.query(Plan).filter(Plan.slug == "pro").first()
    if not plan_pro:
        print("  ❌ Plano Pro não encontrado! Execute seed_plans() primeiro.")
        return

    tenants_data = [
        {
            "name": "Escritório ABC Contabilidade",
            "subdomain": "abc",
            "cnpj": "12.345.678/0001-90",
            "crc": "CRC-SP 123456",
            "status": "active",
            "email": "contato@escritorioacbc.com.br",
            "phone": "(11) 3333-4444",
            "address_city": "São Paulo",
            "address_state": "SP"
        },
        {
            "name": "Escritório XYZ Assessoria",
            "subdomain": "xyz",
            "cnpj": "98.765.432/0001-10",
            "crc": "CRC-RJ 789012",
            "status": "trial",
            "email": "contato@escritorioxyz.com.br",
            "phone": "(21) 2222-3333",
            "address_city": "Rio de Janeiro",
            "address_state": "RJ"
        }
    ]

    for tenant_data in tenants_data:
        # Verificar se já existe
        existing = db.query(Tenant).filter(
            Tenant.subdomain == tenant_data["subdomain"]
        ).first()

        if existing:
            print(f"  ⏭️  Tenant '{tenant_data['name']}' já existe")
            continue

        # Criar tenant
        tenant = Tenant(**tenant_data, plan_id=plan_pro.id)
        db.add(tenant)
        db.flush()  # Para obter o ID

        # Criar schema do tenant
        print(f"  📦 Criando schema para '{tenant_data['name']}'...")
        create_tenant_schema(tenant.id, db)

        # Criar assinatura
        if tenant_data["status"] == "active":
            subscription = Subscription(
                tenant_id=tenant.id,
                plan_id=plan_pro.id,
                status="active",
                billing_cycle="monthly",
                current_period_start=datetime.now().date(),
                current_period_end=(datetime.now() + timedelta(days=30)).date(),
                amount=plan_pro.price_monthly
            )
            db.add(subscription)

        # Criar usuário admin do tenant no schema do tenant
        tenant_admin_password = "admin123"  # Senha padrão
        tenant_admin_email = f"admin@{tenant.subdomain}.com"
        db.execute(text(f"""
            INSERT INTO tenant_{tenant.id}.users (email, password_hash, name, role, is_active, is_verified)
            VALUES (
                '{tenant_admin_email}',
                '{get_password_hash(tenant_admin_password)}',
                'Admin {tenant.name}',
                'admin',
                TRUE,
                TRUE
            )
        """))

        print(f"  ✅ Tenant '{tenant_data['name']}' criado")
        print(f"     Subdomínio: {tenant.subdomain}")
        print(f"     Admin: {tenant_admin_email} / {tenant_admin_password}")

    db.commit()
    print("✅ Tenants criados com sucesso!\n")


def run_seeds():
    """
    Executa todos os seeds
    """
    print("=" * 60)
    print("🌱 LEGIA PLATFORM - Seeds de Dados Iniciais")
    print("=" * 60)

    db = SessionLocal()

    try:
        seed_plans(db)
        seed_superadmin(db)
        seed_tenants(db)

        print("=" * 60)
        print("🎉 Seeds concluídos com sucesso!")
        print("=" * 60)
        print("\n📝 RESUMO:")
        print(f"  Super Admin: {settings.FIRST_SUPERUSER_EMAIL} / {settings.FIRST_SUPERUSER_PASSWORD}")
        print(f"  Tenant ABC: admin@abc.com / admin123 (Tenant ID: 1)")
        print(f"  Tenant XYZ: admin@xyz.com / admin123 (Tenant ID: 2)")
        print("\n⚠️  IMPORTANTE: Altere todas as senhas padrão!\n")

    except Exception as e:
        print(f"\n❌ Erro ao executar seeds: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
