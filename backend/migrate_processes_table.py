"""
Script de Migração - Atualizar Tabela Processes
Este script atualiza a estrutura da tabela processes em todos os schemas de tenants
"""
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import text
from app.db.session import SessionLocal
from app.utils.tenant_schema import list_tenant_schemas, validate_schema_name


def migrate_processes_table():
    """Migrar tabela processes para nova estrutura"""
    db = SessionLocal()

    try:
        # Listar todos os schemas de tenants
        schemas = list_tenant_schemas(db)

        if not schemas:
            print("Nenhum schema de tenant encontrado")
            return

        print(f"Encontrados {len(schemas)} schemas de tenant")
        print()

        for schema_name in schemas:
            # Validar schema_name para prevenir SQL injection
            schema_name = validate_schema_name(schema_name)

            print(f"Migrando schema: {schema_name}")

            try:
                # Verificar se a tabela existe
                result = db.execute(text(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = '{schema_name}'
                        AND table_name = 'processes'
                    )
                """))

                table_exists = result.scalar()

                if not table_exists:
                    print(f"  ⏭️  Tabela processes não existe em {schema_name}")
                    continue

                # Verificar estrutura atual
                result = db.execute(text(f"""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_schema = '{schema_name}'
                    AND table_name = 'processes'
                """))

                columns = [row[0] for row in result.fetchall()]

                # Se já tem a coluna process_type, está na nova estrutura
                if 'process_type' in columns:
                    print(f"  ✅ Schema {schema_name} já está atualizado")
                    continue

                print(f"  🔄 Atualizando estrutura...")

                # Backup da tabela antiga
                db.execute(text(f"""
                    CREATE TABLE IF NOT EXISTS {schema_name}.processes_backup AS
                    SELECT * FROM {schema_name}.processes
                """))

                # Dropar tabela antiga
                db.execute(text(f"DROP TABLE {schema_name}.processes CASCADE"))

                # Criar nova tabela
                db.execute(text(f"""
                    CREATE TABLE {schema_name}.processes (
                        id SERIAL PRIMARY KEY,
                        client_id INTEGER NOT NULL REFERENCES {schema_name}.clients(id),
                        process_type VARCHAR(100) NOT NULL,
                        title VARCHAR(200) NOT NULL,
                        description TEXT,
                        priority VARCHAR(20) NOT NULL DEFAULT 'normal',
                        estimated_days INTEGER NOT NULL DEFAULT 30,
                        status VARCHAR(50) NOT NULL DEFAULT 'aguardando',
                        alteration_types JSONB,
                        assigned_to INTEGER REFERENCES {schema_name}.users(id),
                        created_by INTEGER REFERENCES {schema_name}.users(id),
                        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
                        started_at TIMESTAMP,
                        completed_at TIMESTAMP
                    )
                """))

                # Recriar índices
                db.execute(text(f"CREATE INDEX ix_{schema_name}_processes_client ON {schema_name}.processes(client_id)"))
                db.execute(text(f"CREATE INDEX ix_{schema_name}_processes_status ON {schema_name}.processes(status)"))

                db.commit()
                print(f"  ✅ Schema {schema_name} migrado com sucesso!")

            except Exception as e:
                db.rollback()
                print(f"  ❌ Erro ao migrar {schema_name}: {e}")

        print()
        print("✅ Migração concluída!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erro geral: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("MIGRAÇÃO - Atualizar Tabela Processes")
    print("=" * 60)
    print()

    response = input("Esta operação irá atualizar a estrutura da tabela processes.\nDeseja continuar? (sim/não): ")

    if response.lower() in ['sim', 's', 'yes', 'y']:
        migrate_processes_table()
    else:
        print("Operação cancelada")
