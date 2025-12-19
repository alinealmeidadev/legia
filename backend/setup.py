#!/usr/bin/env python
"""
LEGIA PLATFORM - Script de Setup Inicial

Este script executa todas as etapas necessárias para configurar o projeto:
1. Cria o banco de dados
2. Executa migrations (cria tabelas schema public)
3. Executa seeds (popula dados iniciais)
"""
import sys
import time
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from app.core.config import settings
from app.db.seeds import run_seeds


def wait_for_db(max_retries=30):
    """
    Aguarda o banco de dados estar disponível
    """
    print("🔌 Aguardando conexão com o banco de dados...")

    for i in range(max_retries):
        try:
            engine = create_engine(settings.DATABASE_URL)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Banco de dados conectado!\n")
            return True
        except Exception as e:
            print(f"  Tentativa {i+1}/{max_retries}... {str(e)[:50]}")
            time.sleep(2)

    print("❌ Não foi possível conectar ao banco de dados!")
    return False


def run_migrations():
    """
    Executa as migrations do Alembic
    """
    print("🔧 Executando migrations...")
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("✅ Migrations executadas com sucesso!\n")
        return True
    except Exception as e:
        print(f"❌ Erro ao executar migrations: {e}\n")
        return False


def main():
    """
    Função principal do setup
    """
    print("=" * 60)
    print("🚀 LEGIA PLATFORM - Setup Inicial")
    print("=" * 60)
    print()

    # Passo 1: Aguardar banco de dados
    if not wait_for_db():
        sys.exit(1)

    # Passo 2: Executar migrations
    if not run_migrations():
        print("⚠️  Migrations falharam, mas continuando para seeds...")

    # Passo 3: Executar seeds
    try:
        run_seeds()
    except Exception as e:
        print(f"❌ Erro ao executar seeds: {e}")
        sys.exit(1)

    print("=" * 60)
    print("✨ Setup concluído com sucesso!")
    print("=" * 60)
    print()
    print("📌 Próximos passos:")
    print("  1. Inicie o servidor: uvicorn app.main:app --reload")
    print("  2. Acesse a API: http://localhost:8000")
    print("  3. Documentação: http://localhost:8000/api/v1/docs")
    print()
    print("🔐 Credenciais padrão:")
    print(f"  Super Admin: {settings.FIRST_SUPERUSER_EMAIL} / {settings.FIRST_SUPERUSER_PASSWORD}")
    print("  Tenant ABC: admin@abc.local / admin123")
    print("  Tenant XYZ: admin@xyz.local / admin123")
    print()


if __name__ == "__main__":
    main()
