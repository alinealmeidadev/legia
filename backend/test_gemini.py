"""
Script para testar e listar modelos disponíveis do Google Gemini
"""
import google.generativeai as genai
import os

# Configurar API key
api_key = "AIzaSyD85sIgqiKIF1dpUlfM4sjrx2L4gNMNL2o"
genai.configure(api_key=api_key)

print("=" * 60)
print("LISTANDO MODELOS DISPONÍVEIS NO GOOGLE GEMINI")
print("=" * 60)

# Listar todos os modelos disponíveis
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"✅ {model.name}")
        print(f"   Descrição: {model.display_name}")
        print()

print("=" * 60)
print("TESTANDO MODELO")
print("=" * 60)

# Testar com o primeiro modelo disponível
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Olá, isso é um teste. Responda com uma frase curta.")
    print(f"✅ SUCESSO com gemini-pro:")
    print(f"   Resposta: {response.text}")
except Exception as e:
    print(f"❌ ERRO com gemini-pro: {e}")
    print()
    print("Tentando outros modelos...")

    # Tentar outros modelos
    test_models = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'gemini-1.5-flash',
        'gemini-1.5-pro'
    ]

    for model_name in test_models:
        try:
            print(f"\nTestando: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Teste")
            print(f"✅ FUNCIONOU: {model_name}")
            print(f"   Resposta: {response.text[:100]}...")
            break
        except Exception as e2:
            print(f"❌ Falhou: {e2}")
