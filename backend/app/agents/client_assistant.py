"""
LEGIA PLATFORM - Assistente ao Cliente
Atendimento humanizado e suporte
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent


class ClientAssistant(BaseAgent):
    """
    Assistente ao Cliente - Atendimento humanizado

    Responsabilidades:
    - Primeiro contato (triagem)
    - Responder dúvidas gerais
    - Orientar procedimentos
    - Consultar base de conhecimento
    - Follow-up proativo
    - Tom 100% HUMANO (não parecer robô)
    """

    def __init__(self):
        super().__init__(
            name="Assistente ao Cliente",
            role="especialista em atendimento humanizado para legalização empresarial"
        )

        # Base de conhecimento (FAQ)
        self.knowledge_base = {
            "cnpj": {
                "question": "O que é CNPJ?",
                "answer": "CNPJ é o Cadastro Nacional de Pessoa Jurídica, como se fosse o CPF da sua empresa. É obrigatório para operar legalmente no Brasil."
            },
            "me_mei": {
                "question": "Diferença entre ME e MEI?",
                "answer": "MEI é para faturamento até R$ 81 mil/ano e um funcionário. ME permite faturamento até R$ 360 mil/ano e mais funcionários. ME tem mais flexibilidade de atividades."
            },
            "prazo": {
                "question": "Quanto tempo demora?",
                "answer": "Em média 30-45 dias úteis para abertura completa. Pode variar conforme município e tipo de atividade. Acompanhamos tudo para você!"
            },
            "documentos": {
                "question": "Quais documentos preciso?",
                "answer": "Para sócios: RG, CPF, comprovante de residência. Para empresa: endereço comercial, atividades (CNAEs) e nome empresarial. Te orientamos em cada etapa!"
            },
            "custos": {
                "question": "Quanto custa manter uma empresa?",
                "answer": "Depende do tipo. ME no Simples pode pagar a partir de R$ 70/mês em impostos. Inclui também contabilidade (R$ 200-500/mês) e eventuais taxas."
            },
            "simples": {
                "question": "O que é Simples Nacional?",
                "answer": "É um regime tributário simplificado que unifica vários impostos em uma guia só. Geralmente mais vantajoso para empresas pequenas e médias."
            },
            "alvara": {
                "question": "O que é alvará?",
                "answer": "É a autorização da prefeitura para funcionar no endereço. Verificamos questões de zoneamento, vigilância sanitária (se necessário) e outras exigências."
            },
            "junta": {
                "question": "O que é Junta Comercial?",
                "answer": "É o órgão estadual que registra empresas. Cada estado tem a sua (JUCESP em SP, JUCERJA no RJ, etc). Protocolamos tudo para você!"
            }
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do assistente"""
        return """
Você é um Assistente ao Cliente altamente treinado em legalização empresarial no Brasil.

Sua missão é proporcionar a MELHOR experiência de atendimento humanizado.

CARACTERÍSTICAS ESSENCIAIS:
✅ Empático e acolhedor
✅ Paciente e educado
✅ Claro e objetivo
✅ Proativo (antecipa dúvidas)
✅ 100% HUMANO (NUNCA pareça robô ou IA)

TOM DE VOZ HUMANIZADO:
✅ "Oi! Como posso te ajudar hoje?"
✅ "Deixa eu te explicar isso de forma simples..."
✅ "Entendo sua dúvida! É super comum..."
✅ "Vou te orientar passo a passo, fica tranquilo!"
✅ "Olha, pela minha experiência, o ideal é..."

❌ "Como assistente virtual..."
❌ "Meu sistema processou..."
❌ "Baseado em meus algoritmos..."
❌ Respostas muito formais e robóticas

QUANDO ATENDER:
1. Saudações e apresentações
2. Dúvidas gerais sobre processos
3. Orientações sobre documentação
4. Explicações sobre termos técnicos
5. Consultas de status (delegar ao Monitor)
6. Orçamentos (delegar ao Comercial)
7. Processos técnicos (delegar à Legalização)

ESTRATÉGIA DE ATENDIMENTO:
1. Cumprimentar de forma amigável
2. Escutar/ler atentamente a necessidade
3. Responder de forma clara e simples
4. Perguntar se ficou dúvida
5. Oferecer próximos passos
6. Delegar para agente especializado se necessário

SE NÃO SOUBER:
✅ "Ótima pergunta! Deixa eu verificar isso com mais detalhes para te dar uma resposta precisa..."
✅ "Isso depende de alguns fatores. Vou te conectar com nosso especialista para uma resposta personalizada!"

NUNCA:
❌ Inventar informações
❌ Dar valores sem certeza (delegar ao Comercial)
❌ Prometer prazos impossíveis
❌ Ser impaciente ou rude

LINGUAGEM:
- Use você/seu (nunca "senhor/senhora" demais)
- Emojis com moderação (apenas quando apropriado)
- Contrações naturais: "tá", "pra", "né"
- Gírias leves se contexto permitir

LEMBRE-SE: Você é a PRIMEIRA impressão! Seja memorável pela experiência INCRÍVEL!
"""

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa mensagem do cliente

        Args:
            message: Mensagem do cliente
            context: Contexto da conversa

        Returns:
            Resposta humanizada e orientações
        """
        # Detectar tipo de interação
        interaction_type = self._detect_interaction_type(message)

        # Buscar na base de conhecimento
        kb_match = self._search_knowledge_base(message)

        # Gerar resposta humanizada
        response = await self.generate_response(
            message,
            context={
                **(context or {}),
                "interaction_type": interaction_type,
                "knowledge_base_match": kb_match
            },
            temperature=0.8  # Mais criativo/humanizado
        )

        # Sugerir próximos passos
        suggestions = self._suggest_actions(interaction_type)

        return {
            "response": response,
            "interaction_type": interaction_type,
            "suggestions": suggestions,
            "delegate_to": self._should_delegate(interaction_type),
            "metadata": {
                "agent": "assistente",
                "tone": "humanizado",
                "knowledge_match": kb_match is not None
            }
        }

    def _detect_interaction_type(self, message: str) -> str:
        """Detecta o tipo de interação"""
        message_lower = message.lower()

        # Saudações
        if any(word in message_lower for word in ["oi", "olá", "bom dia", "boa tarde", "boa noite", "alô"]):
            return "saudacao"

        # Agradecimento
        if any(word in message_lower for word in ["obrigad", "valeu", "thanks"]):
            return "agradecimento"

        # Dúvida geral
        if any(word in message_lower for word in ["o que é", "como funciona", "qual", "explica", "não entendi", "dúvida"]):
            return "duvida"

        # Reclamação/problema
        if any(word in message_lower for word in ["problema", "erro", "não funciona", "reclamação", "insatisfeito"]):
            return "problema"

        # Elogio
        if any(word in message_lower for word in ["parabéns", "excelente", "ótimo", "muito bom", "adorei"]):
            return "elogio"

        # Solicitação de ajuda
        if any(word in message_lower for word in ["ajuda", "preciso", "pode me", "auxílio"]):
            return "ajuda"

        return "geral"

    def _search_knowledge_base(self, message: str) -> Optional[Dict]:
        """Busca na base de conhecimento"""
        message_lower = message.lower()

        for key, content in self.knowledge_base.items():
            # Busca por palavras-chave
            if key in message_lower or any(word in message_lower for word in key.split("_")):
                return content

        return None

    def _suggest_actions(self, interaction_type: str) -> List[str]:
        """Sugere ações baseado no tipo de interação"""
        suggestions = {
            "saudacao": [
                "Ver nossos serviços",
                "Solicitar orçamento",
                "Tirar dúvidas"
            ],
            "duvida": [
                "Falar com especialista",
                "Ver documentação necessária",
                "Agendar consulta gratuita"
            ],
            "problema": [
                "Falar com suporte prioritário",
                "Abrir ticket",
                "Solicitar retorno"
            ],
            "ajuda": [
                "Pedir orçamento",
                "Verificar processos",
                "Agendar atendimento"
            ],
            "geral": [
                "Ver serviços disponíveis",
                "Solicitar orçamento",
                "Falar com especialista"
            ]
        }
        return suggestions.get(interaction_type, suggestions["geral"])

    def _should_delegate(self, interaction_type: str) -> Optional[str]:
        """Determina se deve delegar para outro agente"""
        delegation_map = {
            "orcamento": "comercial",
            "tecnico": "legalizacao",
            "status": "monitor"
        }
        return delegation_map.get(interaction_type)

    async def handle_faq(self, question: str) -> Dict[str, Any]:
        """
        Responde perguntas frequentes

        Args:
            question: Pergunta do cliente

        Returns:
            Resposta da FAQ ou indicação de consulta especializada
        """
        match = self._search_knowledge_base(question)

        if match:
            return {
                "question": match["question"],
                "answer": match["answer"],
                "source": "knowledge_base",
                "helpful": True
            }
        else:
            return {
                "question": question,
                "answer": "Ótima pergunta! Para te dar a melhor resposta possível, vou te conectar com um de nossos especialistas.",
                "source": "delegate",
                "helpful": False,
                "delegate_to": "especialista"
            }

    def get_greeting(self, time_of_day: str = "geral") -> str:
        """Retorna saudação apropriada para o horário"""
        greetings = {
            "manha": "Bom dia! ☀️",
            "tarde": "Boa tarde! 🌤️",
            "noite": "Boa noite! 🌙",
            "geral": "Olá! 👋"
        }
        return greetings.get(time_of_day, greetings["geral"])
