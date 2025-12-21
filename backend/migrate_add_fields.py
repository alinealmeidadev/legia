"""
Migração: Adicionar campos client_number, current_stage e department
"""
from sqlalchemy import text
from app.db.session import SessionLocal, engine
from app.models.public.tenant import Tenant

def migrate():
    db = SessionLocal()
    try:
        # Buscar todos os tenants
        tenants = db.query(Tenant).all()

        print(f"📦 Encontrados {len(tenants)} tenants")

        for tenant in tenants:
            schema_name = f"tenant_{tenant.id}"
            print(f"\n🔄 Migrando schema: {schema_name}")

            try:
                # Adicionar client_number na tabela clients
                db.execute(text(f"""
                    ALTER TABLE {schema_name}.clients
                    ADD COLUMN IF NOT EXISTS client_number INTEGER UNIQUE
                """))
                print("  ✅ Campo client_number adicionado em clients")

                # Criar index
                db.execute(text(f"""
                    CREATE INDEX IF NOT EXISTS idx_clients_number
                    ON {schema_name}.clients(client_number)
                """))

                # Preencher client_number com IDs existentes
                db.execute(text(f"""
                    UPDATE {schema_name}.clients
                    SET client_number = id
                    WHERE client_number IS NULL
                """))
                print("  ✅ client_number preenchido para registros existentes")

                # Adicionar current_stage na tabela processes
                db.execute(text(f"""
                    ALTER TABLE {schema_name}.processes
                    ADD COLUMN IF NOT EXISTS current_stage VARCHAR(100)
                """))
                print("  ✅ Campo current_stage adicionado em processes")

                # Adicionar department na tabela processes
                db.execute(text(f"""
                    ALTER TABLE {schema_name}.processes
                    ADD COLUMN IF NOT EXISTS department VARCHAR(100)
                """))
                print("  ✅ Campo department adicionado em processes")

                db.commit()
                print(f"  🎉 Schema {schema_name} migrado com sucesso!")

            except Exception as e:
                print(f"  ⚠️  Erro ao migrar {schema_name}: {e}")
                db.rollback()

        print("\n✅ Migração concluída!")

    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Iniciando migração...")
    migrate()
