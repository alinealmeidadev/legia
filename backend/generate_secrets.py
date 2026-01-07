#!/usr/bin/env python3
"""
Script para gerar SECRET_KEY e JWT_SECRET_KEY seguros

Execute: python backend/generate_secrets.py
"""
import secrets

print("=" * 60)
print("GERADOR DE CHAVES SEGURAS PARA PRODUÇÃO")
print("=" * 60)
print()
print("Use estas chaves nas variáveis de ambiente do Render:")
print()
print("SECRET_KEY:")
print(secrets.token_urlsafe(64))
print()
print("JWT_SECRET_KEY:")
print(secrets.token_urlsafe(64))
print()
print("=" * 60)
print("⚠️  NUNCA compartilhe estas chaves publicamente!")
print("=" * 60)
