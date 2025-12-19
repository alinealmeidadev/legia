"""
Script temporário para resetar senha do usuário tenant
"""
import sys
sys.path.insert(0, '/app')

from app.core.security import get_password_hash
from sqlalchemy import create_engine, text
from app.core.config import settings

# Conectar ao banco
engine = create_engine(settings.DATABASE_URL)

# Hash da senha
new_password_hash = get_password_hash("admin123")

print(f"Novo hash: {new_password_hash}")

# Atualizar senha no tenant_2
with engine.connect() as conn:
    result = conn.execute(
        text("UPDATE tenant_2.users SET password_hash = :hash WHERE email = 'admin@xyz.local'"),
        {"hash": new_password_hash}
    )
    conn.commit()
    print(f"Senha atualizada! Linhas afetadas: {result.rowcount}")

print("✅ Senha resetada para: admin123")
print("Email: admin@xyz.local")
print("Tenant ID: 2")
