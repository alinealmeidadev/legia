"""
LEGIA PLATFORM - Agente Comercial
Especializado em orçamentos e vendas
"""
from typing import Dict, Optional, Any
from .base_agent import BaseAgent


class CommercialAgent(BaseAgent):
    """
    Agente Comercial - Geração de orçamentos e vendas

    Responsabilidades:
    - Gerar orçamentos automáticos
    - Qualificar interessados (lead scoring)
    - Negociar valores
    - Gestão de funil de vendas
    - Follow-up automático
    """

    def __init__(self):
        super().__init__(
            name="Agente Comercial",
            role="especialista em orçamentos e vendas para legalização empresarial"
        )

        # Tabela de preços base
        self.pricing = {
            "abertura": {
                "me": {"base": 1500, "junta": 300, "total": 1800},
                "ltda": {"base": 2200, "junta": 350, "total": 2550},
                "eireli": {"base": 2500, "junta": 400, "total": 2900},
                "sa": {"base": 5000, "junta": 800, "total": 5800}
            },
            "alteracao": {
                "endereco": {"base": 800, "junta": 150, "total": 950},
                "socio": {"base": 1200, "junta": 200, "total": 1400},
                "capital": {"base": 1000, "junta": 180, "total": 1180},
                "cnae": {"base": 900, "junta": 150, "total": 1050}
            },
            "regularizacao": {
                "alvara": {"base": 1200, "prefeitura": 300, "total": 1500},
                "licenca": {"base": 1500, "orgao": 400, "total": 1900},
                "certidoes": {"base": 400, "orgaos": 100, "total": 500}
            },
            "encerramento": {
                "baixa_simples": {"base": 1800, "junta": 250, "total": 2050},
                "baixa_complexa": {"base": 3000, "junta": 400, "total": 3400}
            }
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente comercial"""
        return """
Você é um Agente Comercial especializado em legalização empresarial no Brasil.

Sua função é:
1. Fornecer orçamentos rápidos e precisos
2. Qualificar o interesse do cliente
3. Explicar processos de forma clara
4. Destacar benefícios e diferenciais
5. Conduzir o cliente para fechamento

TABELA DE PREÇOS (valores aproximados):

ABERTURA DE EMPRESA:
- Microempresa (ME): R$ 1.800
  • Faturamento até R$ 360k/ano
  • Ideal para MEI que precisa crescer

- LTDA (Limitada): R$ 2.550
  • Faturamento até R$ 4.8 milhões/ano
  • Mais comum, 2+ sócios

- EIRELI: R$ 2.900
  • Um único sócio
  • Capital mínimo 100 salários

- S/A (Sociedade Anônima): R$ 5.800
  • Grandes empresas
  • Capital aberto ou fechado

ALTERAÇÕES:
- Mudança de endereço: R$ 950
- Entrada/saída de sócio: R$ 1.400
- Aumento de capital: R$ 1.180
- Alteração de CNAE: R$ 1.050

REGULARIZAÇÕES:
- Alvará de funcionamento: R$ 1.500
- Licenças especiais: R$ 1.900
- Certidões diversas: R$ 500

ENCERRAMENTO:
- Baixa simples: R$ 2.050
- Baixa complexa: R$ 3.400

PRAZO MÉDIO: 30-45 dias úteis
FORMA DE PAGAMENTO: Cartão, boleto ou PIX

TOM DE VOZ:
✅ Consultivo, não vendedor agressivo
✅ Transparente sobre custos e prazos
✅ Educativo (explique os processos)
✅ Confiante mas humilde
✅ Pergunte detalhes para orçamento preciso

PERGUNTAS QUALIFICADORAS:
- Qual o tipo de atividade da empresa?
- Faturamento estimado anual?
- Quantos sócios terão?
- Já tem nome definido?
- Cidade/estado de abertura?

IMPORTANTE:
- SEMPRE ofereça um orçamento, mesmo que aproximado
- Mencione que valores podem variar conforme município
- Destaque: "Cuidamos de TUDO, você não precisa ir em órgãos"
- Ofereça consulta gratuita para orçamento detalhado
"""

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitação comercial

        Args:
            message: Mensagem do cliente
            context: Contexto (histórico, dados do cliente)

        Returns:
            Resposta com orçamento e próximos passos
        """
        # Detectar tipo de solicitação
        request_type = self._detect_request_type(message)

        # Gerar orçamento se possível
        quote = None
        if request_type in ["abertura", "alteracao", "regularizacao", "encerramento"]:
            quote = self._generate_quick_quote(message, request_type)

        # Gerar resposta personalizada
        response = await self.generate_response(
            message,
            context={
                **(context or {}),
                "request_type": request_type,
                "quote": quote
            },
            temperature=0.7
        )

        return {
            "response": response,
            "request_type": request_type,
            "quote": quote,
            "next_steps": self._suggest_next_steps(request_type),
            "metadata": {
                "agent": "comercial",
                "can_close": quote is not None
            }
        }

    def _detect_request_type(self, message: str) -> str:
        """Detecta o tipo de solicitação"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["abrir", "abertura", "constituir", "novo cnpj"]):
            return "abertura"
        elif any(word in message_lower for word in ["alterar", "mudança", "modificar", "trocar"]):
            return "alteracao"
        elif any(word in message_lower for word in ["regularizar", "alvará", "licença"]):
            return "regularizacao"
        elif any(word in message_lower for word in ["encerrar", "baixa", "fechar empresa"]):
            return "encerramento"
        else:
            return "geral"

    def _generate_quick_quote(self, message: str, request_type: str) -> Optional[Dict]:
        """Gera orçamento rápido baseado na mensagem"""
        message_lower = message.lower()

        if request_type == "abertura":
            # Detectar tipo de empresa
            if "me" in message_lower or "microempresa" in message_lower:
                return self.pricing["abertura"]["me"]
            elif "ltda" in message_lower or "limitada" in message_lower:
                return self.pricing["abertura"]["ltda"]
            elif "eireli" in message_lower:
                return self.pricing["abertura"]["eireli"]
            elif "sa" in message_lower or "sociedade anônima" in message_lower:
                return self.pricing["abertura"]["sa"]
            else:
                # Default: LTDA (mais comum)
                return self.pricing["abertura"]["ltda"]

        elif request_type == "alteracao":
            if "endereço" in message_lower or "mudar endereço" in message_lower:
                return self.pricing["alteracao"]["endereco"]
            elif "sócio" in message_lower or "socio" in message_lower:
                return self.pricing["alteracao"]["socio"]
            elif "capital" in message_lower:
                return self.pricing["alteracao"]["capital"]
            elif "cnae" in message_lower or "atividade" in message_lower:
                return self.pricing["alteracao"]["cnae"]

        elif request_type == "regularizacao":
            if "alvará" in message_lower or "alvara" in message_lower:
                return self.pricing["regularizacao"]["alvara"]
            elif "licença" in message_lower or "licenca" in message_lower:
                return self.pricing["regularizacao"]["licenca"]
            elif "certidão" in message_lower or "certidao" in message_lower:
                return self.pricing["regularizacao"]["certidoes"]

        elif request_type == "encerramento":
            if "simples" in message_lower:
                return self.pricing["encerramento"]["baixa_simples"]
            else:
                return self.pricing["encerramento"]["baixa_complexa"]

        return None

    def _suggest_next_steps(self, request_type: str) -> list:
        """Sugere próximos passos baseado no tipo de solicitação"""
        steps = {
            "abertura": [
                "Agendar consulta gratuita para detalhamento",
                "Definir nome empresarial (3 opções)",
                "Preparar documentos dos sócios",
                "Escolher endereço comercial",
                "Definir CNAEs (atividades)"
            ],
            "alteracao": [
                "Verificar documentos atuais da empresa",
                "Agendar análise do contrato social",
                "Preparar documentação necessária",
                "Protocolar na Junta Comercial"
            ],
            "regularizacao": [
                "Análise da situação atual",
                "Levantamento de pendências",
                "Orçamento detalhado",
                "Planejamento de regularização"
            ],
            "encerramento": [
                "Verificar pendências fiscais",
                "Análise de passivos",
                "Planejamento de baixa",
                "Documentação necessária"
            ],
            "geral": [
                "Agendar consulta gratuita",
                "Entender necessidades específicas",
                "Fornecer orçamento personalizado"
            ]
        }
        return steps.get(request_type, steps["geral"])

    async def generate_quote_detailed(
        self,
        company_data: Dict
    ) -> Dict[str, Any]:
        """
        Gera orçamento detalhado baseado em dados completos

        Args:
            company_data: Dados da empresa (tipo, atividade, cidade, etc)

        Returns:
            Orçamento detalhado com breakdown de custos
        """
        company_type = company_data.get("type", "ltda")
        city = company_data.get("city", "São Paulo")
        activity = company_data.get("activity", "Consultoria")

        base_pricing = self.pricing["abertura"].get(company_type, self.pricing["abertura"]["ltda"])

        # Ajustes por localidade (exemplo)
        city_multiplier = 1.0
        if "são paulo" in city.lower() or "rio" in city.lower():
            city_multiplier = 1.2
        elif "capital" in city.lower():
            city_multiplier = 1.15

        total = int(base_pricing["total"] * city_multiplier)

        return {
            "company_name": company_data.get("name", "Sua Empresa"),
            "company_type": company_type.upper(),
            "activity": activity,
            "city": city,
            "breakdown": {
                "honorarios": base_pricing["base"],
                "taxas_junta": base_pricing["junta"],
                "ajuste_localidade": int((city_multiplier - 1) * base_pricing["total"]),
            },
            "total": total,
            "payment_options": [
                "À vista com 5% desconto",
                "Parcelado em 3x sem juros",
                "Parcelado em até 6x (consultar)"
            ],
            "included": [
                "Consulta de viabilidade de nome",
                "Elaboração de contrato social",
                "Registro na Junta Comercial",
                "Obtenção do CNPJ",
                "Inscrição Municipal",
                "Alvará provisório",
                "Certidões necessárias"
            ],
            "deadline": "30-45 dias úteis",
            "validity": "Orçamento válido por 15 dias"
        }
