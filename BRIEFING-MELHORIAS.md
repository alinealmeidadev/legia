# 🚀 LEGIA PLATFORM - BRIEFING DE MELHORIAS

## 📋 INSTRUÇÕES PARA VOCÊ (CLAUDE CODE)

**Antes de fazer QUALQUER coisa:**

1. ✅ LEIA este documento COMPLETO
2. ✅ ANALISE o código existente do projeto
3. ✅ IDENTIFIQUE quais arquivos precisam ser modificados
4. ✅ SUGIRA a melhor abordagem para cada melhoria
5. ✅ PERGUNTE se pode prosseguir antes de implementar
6. ✅ Implemente uma FASE de cada vez

**Você tem autonomia para:**
- Decidir qual a melhor estrutura de código
- Escolher quais arquivos criar ou modificar
- Sugerir melhorias além do solicitado
- Perguntar quando tiver dúvidas

---

## 🎯 CONTEXTO DO PROJETO

**LEGIA Platform** é um SaaS B2B multi-tenant para escritórios contábeis que automatiza processos de legalização empresarial usando 8 agentes de IA.

**Stack atual:**
- Backend: Python 3.11+, FastAPI, SQLAlchemy, PostgreSQL
- Frontend: Next.js 14+, TypeScript, TailwindCSS, shadcn/ui
- Já tem: Login, Dashboard, CRUD básico de clientes e tenants

**Problema:** Sistema funciona, mas falta otimizações essenciais para ser competitivo.

---

## 🔥 MELHORIAS PRIORITÁRIAS

Implemente nesta ordem:

### FASE 1: Corrigir Fluxo de Automação de Processos ⚠️ CRÍTICO

**PROBLEMA ATUAL:**

O sistema tem páginas/rotas SEPARADAS para cada tipo de alteração:
- Uma página para "Alteração de Endereço"
- Uma página para "Alteração de Sócios"
- Uma página para "Alteração de Capital"
- Etc.

**Isso está ERRADO porque:**
- Cliente pode querer fazer MÚLTIPLAS alterações ao mesmo tempo
- Não reflete como escritórios trabalham na vida real
- Cada alteração cria um processo separado (errado!)

**COMPORTAMENTO ESPERADO:**

Sistema de referência (Acessórias) funciona assim:
1. Usuário clica "Alteração Contratual"
2. Sistema mostra opções do que pode alterar (múltipla escolha)
3. Usuário marca: ☑ Endereço + ☑ Sócios + ☑ Capital
4. Sistema cria **UM único processo** com as 3 alterações
5. Processo executa todas as etapas necessárias

**REQUISITOS:**

✅ **UMA** página/rota de "Automação de Processos"
✅ Cards/botões para cada TIPO de processo (Abertura, Alteração, Baixa)
✅ Ao clicar "Alteração Contratual" → Abre modal/dialog
✅ Modal tem checkboxes de múltipla escolha:
   - [ ] Alteração de Endereço
   - [ ] Alteração de Sócios
   - [ ] Alteração de Capital Social
   - [ ] Alteração de Atividade (CNAEs)
   - [ ] Alteração de Razão Social
   - [ ] Alteração de Nome Fantasia
✅ Cliente pode marcar quantas quiser
✅ Ao confirmar, cria **UM processo** com todas marcadas
✅ Backend salva quais alterações foram selecionadas

**DECISÕES QUE VOCÊ DEVE TOMAR:**

- Onde fica melhor a página de automação? (analise rotas existentes)
- Qual padrão de modal usar? (shadcn/ui Dialog?)
- Como salvar as alterações no processo? (JSON? tabela relacionada?)
- Precisa deletar arquivos antigos? (identifique quais)

---

### FASE 2: Consulta Automática de CNPJ (Receita Federal)

**OBJETIVO:**

Cliente digita CNPJ → Sistema busca dados na Receita Federal → Preenche formulário automaticamente

**TEMPO:** Cadastro cai de 5 minutos para 30 segundos!

---

#### 🔧 IMPLEMENTAÇÃO (Código Pronto - Economiza Crédito!)

**PASSO 1:** Instalar dependência

```bash
pip install httpx --break-system-packages
```

**PASSO 2:** Criar serviço de CNPJ

**Arquivo:** `backend/app/services/receita_service.py`

```python
import httpx
from typing import Optional, Dict

class ReceitaService:
    """Serviço para consultar CNPJ na Receita Federal (ReceitaWS - GRÁTIS)"""
    
    BASE_URL = "https://www.receitaws.com.br/v1/cnpj"
    
    def limpar_cnpj(self, cnpj: str) -> str:
        """Remove formatação do CNPJ"""
        return cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
    
    async def consultar_cnpj(self, cnpj: str) -> Optional[Dict]:
        """
        Consulta CNPJ na Receita Federal
        
        Args:
            cnpj: CNPJ com ou sem formatação
            
        Returns:
            Dict com dados da empresa ou None se não encontrado
        """
        cnpj_limpo = self.limpar_cnpj(cnpj)
        
        if len(cnpj_limpo) != 14 or not cnpj_limpo.isdigit():
            return None
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.BASE_URL}/{cnpj_limpo}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("status") == "ERROR":
                        return None
                    
                    return {
                        "cnpj": data.get("cnpj"),
                        "razao_social": data.get("nome"),
                        "nome_fantasia": data.get("fantasia") or data.get("nome"),
                        "data_abertura": data.get("abertura"),
                        "capital_social": data.get("capital_social"),
                        "situacao": data.get("situacao"),
                        "cep": data.get("cep", "").replace(".", ""),
                        "logradouro": data.get("logradouro"),
                        "numero": data.get("numero"),
                        "complemento": data.get("complemento"),
                        "bairro": data.get("bairro"),
                        "cidade": data.get("municipio"),
                        "estado": data.get("uf"),
                        "telefone": data.get("telefone"),
                        "email": data.get("email"),
                        "atividade_principal": data.get("atividade_principal", [{}])[0] if data.get("atividade_principal") else {},
                        "atividades_secundarias": data.get("atividades_secundarias", [])
                    }
                
                return None
        except Exception as e:
            print(f"Erro ao consultar CNPJ: {e}")
            return None
```

**PASSO 3:** Adicionar endpoint em `backend/app/api/v1/clients.py`

```python
from app.services.receita_service import ReceitaService
from app.utils.validators import validar_cnpj
from fastapi import HTTPException

@router.get("/consultar-cnpj/{cnpj}")
async def consultar_cnpj(
    cnpj: str,
    current_user = Depends(get_current_tenant_user)
):
    """Consulta CNPJ na Receita Federal"""
    if not validar_cnpj(cnpj):
        raise HTTPException(status_code=400, detail="CNPJ inválido")
    
    receita = ReceitaService()
    dados = await receita.consultar_cnpj(cnpj)
    
    if not dados:
        raise HTTPException(status_code=404, detail="CNPJ não encontrado na Receita Federal")
    
    return dados
```

---

#### 📝 FRONTEND (Você Decide Como Integrar)

**REQUISITOS:**

O frontend precisa:
1. ✅ Detectar quando usuário terminou de digitar CNPJ (onBlur)
2. ✅ Chamar endpoint `/api/clients/consultar-cnpj/{cnpj}`
3. ✅ Mostrar loading: "🔄 Consultando Receita Federal..."
4. ✅ Preencher campos automaticamente com resposta
5. ✅ Mostrar toast de sucesso/erro
6. ✅ Permitir edição manual após preencher

**DECISÕES QUE VOCÊ DEVE TOMAR:**

- Onde está o formulário de cadastro de cliente?
- Como adicionar onBlur no input de CNPJ?
- Qual componente de loading usar?
- Como fazer a chamada à API? (fetch? axios?)

---

### FASE 3: Consulta Automática de CEP

#### 🔧 IMPLEMENTAÇÃO (Código Pronto)

**Arquivo:** `backend/app/services/cep_service.py`

```python
import httpx
from typing import Optional, Dict

class CEPService:
    """Serviço para consultar CEP (ViaCEP - GRÁTIS)"""
    
    BASE_URL = "https://viacep.com.br/ws"
    
    def limpar_cep(self, cep: str) -> str:
        """Remove formatação do CEP"""
        return cep.replace("-", "").strip()
    
    async def consultar_cep(self, cep: str) -> Optional[Dict]:
        """
        Consulta CEP no ViaCEP
        
        Args:
            cep: CEP com ou sem formatação
            
        Returns:
            Dict com endereço ou None se não encontrado
        """
        cep_limpo = self.limpar_cep(cep)
        
        if len(cep_limpo) != 8 or not cep_limpo.isdigit():
            return None
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.BASE_URL}/{cep_limpo}/json/")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("erro"):
                        return None
                    
                    return {
                        "cep": data.get("cep"),
                        "logradouro": data.get("logradouro"),
                        "complemento": data.get("complemento"),
                        "bairro": data.get("bairro"),
                        "cidade": data.get("localidade"),
                        "estado": data.get("uf")
                    }
                
                return None
        except Exception as e:
            print(f"Erro ao consultar CEP: {e}")
            return None
```

**Endpoint em `backend/app/api/v1/clients.py`:**

```python
from app.services.cep_service import CEPService

@router.get("/consultar-cep/{cep}")
async def consultar_cep(
    cep: str,
    current_user = Depends(get_current_tenant_user)
):
    """Consulta CEP no ViaCEP"""
    cep_service = CEPService()
    dados = await cep_service.consultar_cep(cep)
    
    if not dados:
        raise HTTPException(status_code=404, detail="CEP não encontrado")
    
    return dados
```

**Frontend:** Mesma lógica do CNPJ, mas para CEP. Você decide como integrar!

---

### FASE 4: Validação Inteligente CPF/CNPJ

#### 🔧 IMPLEMENTAÇÃO (Código Pronto - Algoritmo Oficial)

**Arquivo:** `backend/app/utils/validators.py`

```python
def validar_cpf(cpf: str) -> bool:
    """Valida CPF usando algoritmo oficial brasileiro"""
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Validar primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    if int(cpf[9]) != digito1:
        return False
    
    # Validar segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    if int(cpf[10]) != digito2:
        return False
    
    return True


def validar_cnpj(cnpj: str) -> bool:
    """Valida CNPJ usando algoritmo oficial brasileiro"""
    cnpj = ''.join(filter(str.isdigit, cnpj))
    
    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False
    
    # Validar primeiro dígito verificador
    tamanho = 12
    soma = 0
    pos = tamanho - 7
    for i in range(tamanho):
        soma += int(cnpj[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    
    digito1 = 11 - (soma % 11)
    if digito1 > 9:
        digito1 = 0
    if int(cnpj[12]) != digito1:
        return False
    
    # Validar segundo dígito verificador
    tamanho = 13
    soma = 0
    pos = tamanho - 7
    for i in range(tamanho):
        soma += int(cnpj[i]) * pos
        pos -= 1
        if pos < 2:
            pos = 9
    
    digito2 = 11 - (soma % 11)
    if digito2 > 9:
        digito2 = 0
    if int(cnpj[13]) != digito2:
        return False
    
    return True


def formatar_cpf(cpf: str) -> str:
    """Formata CPF: 12345678901 -> 123.456.789-01"""
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return cpf
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ: 12345678000190 -> 12.345.678/0001-90"""
    cnpj = ''.join(filter(str.isdigit, cnpj))
    if len(cnpj) != 14:
        return cnpj
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def limpar_cpf_cnpj(cpf_cnpj: str) -> str:
    """Remove formatação de CPF/CNPJ"""
    return ''.join(filter(str.isdigit, cpf_cnpj))
```

**Frontend:** Usar essas validações nos inputs. Você decide onde/como!

---

### FASE 5: Importação de Clientes via Excel

**OBJETIVO:**

Escritório novo pode importar 100+ clientes em 5 minutos ao invés de cadastrar manualmente

**COMPORTAMENTO ESPERADO:**

```
1. Cliente clica "Importar Clientes"
2. Baixa template Excel do sistema
3. Preenche Excel com dados dos clientes
4. Faz upload
5. Sistema valida:
   - CPF/CNPJ válidos?
   - Campos obrigatórios OK?
   - Tem duplicatas?
6. Sistema mostra preview:
   ✅ 98 clientes prontos
   ⚠️ 2 com avisos (telefone inválido)
   ❌ 0 erros
7. Cliente confirma
8. Sistema importa todos de uma vez
9. Mostra relatório final
```

**REQUISITOS:**

✅ Criar template Excel com:
   - Aba "Instruções"
   - Aba "Dados Básicos" (tipo, cpf_cnpj, nome, email, telefone)
   - Aba "Dados Completos" (todos os campos)
   - Aba "Exemplo" (linhas preenchidas de exemplo)

✅ Endpoint para download do template

✅ Endpoint para upload e importação:
   - Validar cada linha
   - Detectar duplicatas
   - Validar CPF/CNPJ
   - Validar email
   - Retornar relatório detalhado

✅ Frontend:
   - Página de importação
   - Botão download template
   - Upload de arquivo
   - Mostrar preview antes de importar
   - Mostrar relatório após importação

**DECISÕES QUE VOCÊ DEVE TOMAR:**

- Qual biblioteca Excel? (openpyxl? xlsxwriter?)
- Processar síncrono ou assíncrono?
- Limite de linhas por importação?
- Como mostrar progresso? (chunked response?)

---

## 📊 INFORMAÇÕES TÉCNICAS

### APIs Disponíveis (GRÁTIS):

**ReceitaWS:**
- URL: `https://www.receitaws.com.br/v1/cnpj/{cnpj}`
- Limite: 3 requisições/minuto (suficiente!)
- Retorna: JSON com dados completos da empresa

**ViaCEP:**
- URL: `https://viacep.com.br/ws/{cep}/json/`
- Limite: Ilimitado
- Retorna: JSON com endereço

### Estrutura Atual do Projeto:

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── clients.py (CRUD de clientes)
│   │   ├── processes.py (CRUD de processos)
│   │   └── auth.py
│   ├── models/
│   ├── schemas/
│   └── db/

frontend/
├── app/
│   ├── tenant/
│   │   ├── dashboard/
│   │   ├── clients/
│   │   ├── processes/
│   │   └── automation/ (ANALISAR ESTA PASTA!)
│   └── ...
├── components/
└── lib/
```

---

## ❓ PERGUNTAS QUE VOCÊ DEVE FAZER

Antes de implementar cada fase:

1. **Análise:**
   - "Analisei a estrutura atual. Encontrei X arquivos relacionados."
   - "Identifiquei que [problema/padrão atual]."

2. **Sugestão:**
   - "Sugiro criar/modificar os seguintes arquivos: [lista]"
   - "Sugiro usar [tecnologia/padrão] porque [motivo]"

3. **Confirmação:**
   - "Posso prosseguir com essa abordagem?"
   - "Você prefere que eu faça X ou Y?"

4. **Alternativas:**
   - "Encontrei duas formas de fazer: [opção A] ou [opção B]"
   - "Qual você prefere?"

---

## ✅ COMO PROCEDER

### PASSO 1: Análise Inicial

Antes de fazer qualquer coisa:

```
Você: Analise o projeto e me diga:
1. Quais arquivos existem em frontend/app/tenant/automation/?
2. Como o cadastro de clientes está implementado?
3. Já existe algum serviço de API no backend?
4. Qual a estrutura atual de processos?

Me mostre o que você encontrou antes de sugerir mudanças.
```

### PASSO 2: Implementação por Fase

Para cada fase:

```
Você: [depois que eu analisar]
Para FASE 1, sugiro:
- Deletar: [arquivos X, Y, Z]
- Criar: [arquivos A, B, C]
- Modificar: [arquivo D]

Posso prosseguir?
```

### PASSO 3: Validação

Depois de implementar cada fase:

```
Você: Implementei FASE 1. Para testar:
1. Abra http://localhost:3000/tenant/automation
2. Clique em "Alteração Contratual"
3. Marque múltiplas opções
4. Verifique se cria UM processo

Testou? Funcionou? Posso ir pra FASE 2?
```

---

## 💰 CUSTO ESTIMADO

**APIs usadas:** R$ 0,00 (grátis para sempre!)

**Crédito Claude Code:**

```
FASE 1 (Automação):
├─ Análise + Decisão + Código = US$ 2-3
└─ Precisa analisar estrutura e decidir arquitetura

FASE 2 (CNPJ):
├─ Copiar código pronto = US$ 0,20-0,50
├─ Integrar no frontend = US$ 0,50-1
└─ Total = US$ 0,70-1,50

FASE 3 (CEP):
├─ Copiar código pronto = US$ 0,20-0,50
├─ Integrar no frontend = US$ 0,30-0,50
└─ Total = US$ 0,50-1

FASE 4 (Validação):
├─ Copiar código pronto = US$ 0,10-0,30
├─ Usar no frontend = US$ 0,20-0,40
└─ Total = US$ 0,30-0,70

FASE 5 (Excel):
├─ Análise + Código = US$ 2-3
└─ Precisa criar template e processamento

━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL ESTIMADO: US$ 5,50-8,20
━━━━━━━━━━━━━━━━━━━━━━━━━━━

ECONOMIA com código pronto:
- Sem código pronto: US$ 10-15
- Com código pronto: US$ 5,50-8,20
- Você economiza: ~US$ 5-7! 💰
```

Você pode fazer uma fase de cada vez para gastar menos!

---

## 🎯 PRIORIDADES

**Se tiver pouco crédito, faça nesta ordem:**

1. ⭐⭐⭐ **FASE 1** (Automação) - **US$ 2-3** - Crítico, sistema está errado
2. ⭐⭐⭐ **FASE 2** (CNPJ) - **US$ 0,70-1,50** - Maior impacto, código pronto!
3. ⭐⭐ **FASE 3** (CEP) - **US$ 0,50-1** - Complementa FASE 2, barato!
4. ⭐⭐ **FASE 4** (Validação) - **US$ 0,30-0,70** - Evita erros, quase de graça!
5. ⭐ **FASE 5** (Excel) - **US$ 2-3** - Importante mas pode esperar

**COMBO ECONÔMICO:** Fases 2+3+4 juntas = **US$ 1,50-3** (super barato!)

**COMBO COMPLETO:** Todas as 5 fases = **US$ 5,50-8,20**

---

## 📝 NOTAS IMPORTANTES

### Para Você (Claude Code):

- ✅ **Analise PRIMEIRO**, codifique DEPOIS
- ✅ **Pergunte quando tiver dúvida**
- ✅ **Sugira melhorias** se identificar problemas
- ✅ **Implemente uma fase de cada vez**
- ✅ **Teste depois de cada fase**
- ❌ Não assuma estruturas - verifique primeiro
- ❌ Não crie código sem analisar o existente
- ❌ Não faça tudo de uma vez

### Sobre as APIs:

- ✅ ReceitaWS e ViaCEP são APIs PÚBLICAS e GRATUITAS
- ✅ Não precisa de API Key
- ✅ Sem custo de uso
- ⚠️ ReceitaWS tem limite de 3 req/min (suficiente)
- ⚠️ Sempre trate timeout (APIs podem demorar)

### Sobre Validações:

- ✅ CPF tem 11 dígitos
- ✅ CNPJ tem 14 dígitos
- ✅ Ambos têm algoritmo de validação oficial
- ✅ Rejeitar: 111.111.111-11, 000.000.000-00, etc

---

## 🚀 COMEÇE AGORA

**Primeiro comando que você deve executar:**

```bash
# Analisar estrutura do projeto
ls -la frontend/app/tenant/automation/
ls -la backend/app/api/v1/
cat frontend/app/tenant/clients/*/page.tsx
```

Depois me diga o que encontrou e sugira o plano de ação! 💪
