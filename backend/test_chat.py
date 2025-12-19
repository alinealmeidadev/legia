"""
Script para testar os agentes via API
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_login():
    """Testa login e retorna token"""
    print("=" * 60)
    print("TESTANDO LOGIN")
    print("=" * 60)

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": "admin@xyz.com",
            "password": "admin123",
            "tenant_id": 2
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login bem-sucedido!")
        print(f"   Usuário: {data['user']['full_name']}")
        print(f"   Token recebido: {data['access_token'][:30]}...")
        return data['access_token']
    else:
        print(f"❌ Erro no login: {response.status_code}")
        print(f"   {response.text}")
        return None

def test_chat(token, message):
    """Testa envio de mensagem no chat"""
    print("\n" + "=" * 60)
    print(f"TESTANDO CHAT: '{message}'")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{BASE_URL}/agents/chat",
        headers=headers,
        json={
            "message": message,
            "context": {}
        }
    )

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Resposta recebida!")
        print(f"   Agente: {data.get('agent', 'N/A')}")
        print(f"   Resposta: {data.get('response', 'N/A')[:200]}...")
        return True
    else:
        print(f"❌ Erro no chat: {response.status_code}")
        print(f"   {response.text}")
        return False

# Executar testes
if __name__ == "__main__":
    # Teste 1: Login
    token = test_login()
    if not token:
        print("\n❌ Não foi possível continuar sem token")
        exit(1)

    # Teste 2: Saudação simples
    test_chat(token, "Olá!")

    # Teste 3: Pergunta comercial
    test_chat(token, "Quanto custa abrir uma empresa?")

    # Teste 4: Pergunta de FAQ
    test_chat(token, "O que é CNPJ?")

    # Teste 5: Pergunta sobre abertura de empresa
    test_chat(token, "Quero abrir uma empresa MEI")

    print("\n" + "=" * 60)
    print("TESTES CONCLUÍDOS")
    print("=" * 60)
