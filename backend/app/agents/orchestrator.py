"""
LEGIA PLATFORM - Orquestrador
Agente principal que coordena todos os outros agentes
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent


class OrchestratorAgent(BaseAgent):
    """
    Orquestrador - Maestro que coordena todos os agentes

    Responsabilidades:
    - Receber mensagens de usuários
    - Analisar intenção
    - Decidir qual agente acionar
    - Gerenciar contexto e memória
    - Consolidar respostas
    - Atribuir processos a funcionários
    - Cadastrar clientes no sistema
    """

    def __init__(self):
        super().__init__(
            name="Orquestrador",
            role="coordenador de agentes especializados em legalização empresarial"
        )
        self.available_agents = [
            "comercial",      # Orçamentos e vendas
            "legalizacao",    # Execução de processos
            "monitor",        # Acompanhamento de protocolos
            "contratos",      # Elaboração de documentos
            "comunicacoes",   # Comunicações oficiais
            "documentos",     # Gestão documental
            "assistente"      # Atendimento ao cliente
        ]

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do orquestrador"""
        return f"""
Você é o Orquestrador do LEG.Agents, um sistema multi-agente especializado em legalização empresarial.

Sua função principal é:
1. Entender a intenção do usuário
2. Determinar qual agente especializado deve atender
3. Coordenar a execução de tarefas complexas
4. Consolidar respostas de múltiplos agentes

Agentes disponíveis:
- Comercial: Geração de orçamentos, qualificação de leads, vendas
- Legalização: Abertura, alteração, regularização e encerramento de empresas
- Monitor: Acompanhamento de protocolos em órgãos públicos
- Contratos: Elaboração de contratos sociais e documentos jurídicos
- Comunicações: Ofícios e comunicações oficiais com órgãos
- Documentos: Organização e gestão de documentos
- Assistente: Atendimento humanizado ao cliente

IMPORTANTE:
- Seja SEMPRE profissional mas humanizado
- NUNCA mencione que você é uma IA
- Use linguagem natural e acolhedora
- Se não souber, seja honesto e ofereça alternativas
- Pergunte quando precisar de mais informações

Tom de voz:
✅ "Claro! Vou te ajudar com isso..."
✅ "Deixa eu verificar aqui rapidinho..."
✅ "Pela minha experiência, o ideal é..."

❌ "Como IA, posso processar..."
❌ "Meu algoritmo indica..."
"""

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa uma mensagem e determina a ação apropriada

        Args:
            message: Mensagem do usuário
            context: Contexto da conversa (histórico, tenant, usuário)

        Returns:
            Resposta estruturada com:
            - response: Texto da resposta
            - agent: Agente que deve processar
            - action: Ação sugerida
            - confidence: Confiança na decisão (0-1)
            - metadata: Metadados adicionais
        """
        # Analisar intenção
        intent_result = await self._analyze_intent(message, context)

        # Determinar agente apropriado
        agent = self._route_to_agent(intent_result)

        # Gerar resposta
        response = await self.generate_response(
            message,
            context={
                **(context or {}),
                "intent": intent_result["intent"],
                "agent": agent
            }
        )

        return {
            "response": response,
            "agent": agent,
            "intent": intent_result["intent"],
            "action": intent_result.get("action"),
            "confidence": intent_result.get("confidence", 0.8),
            "metadata": {
                "orchestrator": "v1.0",
                "model": "gemini-1.5-flash"
            }
        }

    async def _analyze_intent(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Analisa a intenção da mensagem

        Returns:
            Dict com intent, action, entities, confidence
        """
        # Palavras-chave para detecção de intenção
        intents = {
            "orcamento": ["quanto custa", "preço", "valor", "orçamento", "cotação"],
            "abertura": ["abrir empresa", "abertura", "constituir", "cnpj novo"],
            "alteracao": ["alterar", "mudança", "modificar", "trocar sócio", "mudar endereço"],
            "consulta": ["status", "andamento", "como está", "protocolo"],
            "documento": ["contrato", "documento", "certidão", "alvará"],
            "duvida": ["como", "qual", "o que é", "dúvida", "?"],
            "saudacao": ["oi", "olá", "bom dia", "boa tarde", "boa noite"],
        }

        message_lower = message.lower()

        # Detectar intenção por palavras-chave
        detected_intent = "geral"
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intent = intent
                break

        return {
            "intent": detected_intent,
            "action": self._intent_to_action(detected_intent),
            "confidence": 0.85,
            "original_message": message
        }

    def _intent_to_action(self, intent: str) -> str:
        """Mapeia intenção para ação"""
        action_map = {
            "orcamento": "generate_quote",
            "abertura": "start_process",
            "alteracao": "start_process",
            "consulta": "check_status",
            "documento": "manage_document",
            "duvida": "answer_question",
            "saudacao": "greet"
        }
        return action_map.get(intent, "clarify")

    def _route_to_agent(self, intent_result: Dict) -> str:
        """
        Determina qual agente deve processar a solicitação

        Args:
            intent_result: Resultado da análise de intenção

        Returns:
            Nome do agente apropriado
        """
        intent = intent_result.get("intent", "geral")

        routing = {
            "orcamento": "comercial",
            "abertura": "legalizacao",
            "alteracao": "legalizacao",
            "consulta": "monitor",
            "documento": "documentos",
            "duvida": "assistente",
            "saudacao": "assistente",
            "geral": "assistente"
        }

        return routing.get(intent, "assistente")

    async def delegate_to_agent(
        self,
        agent_name: str,
        message: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Delega tarefa para agente especializado

        Args:
            agent_name: Nome do agente
            message: Mensagem para o agente
            context: Contexto adicional

        Returns:
            Resposta do agente especializado
        """
        # Importar agentes dinamicamente
        from .commercial_agent import CommercialAgent
        from .client_assistant import ClientAssistant
        from .legalization_agent import LegalizationAgent
        from .contracts_agent import ContractsAgent
        from .monitor_agent import MonitorAgent
        from .protocol_agent import ProtocolAgent

        # Mapa de agentes disponíveis
        agents_map = {
            "comercial": CommercialAgent(),
            "assistente": ClientAssistant(),
            "legalizacao": LegalizationAgent(),
            "contratos": ContractsAgent(),
            "monitor": MonitorAgent(),
            "protocolo": ProtocolAgent(),
        }

        # Buscar agente
        agent = agents_map.get(agent_name)

        if agent:
            # Delegar para agente especializado
            return await agent.process(message, context)
        else:
            # Agente não implementado, orquestrador responde
            return await self.process(message, context)

    def get_conversation_summary(self, messages: List[Dict]) -> str:
        """
        Gera resumo da conversa

        Args:
            messages: Lista de mensagens da conversa

        Returns:
            Resumo textual
        """
        if not messages:
            return "Nenhuma conversa ainda."

        summary_parts = [
            f"Conversa com {len(messages)} mensagens.",
        ]

        # Contar por tipo de intenção
        intents = {}
        for msg in messages:
            intent = msg.get("intent", "geral")
            intents[intent] = intents.get(intent, 0) + 1

        if intents:
            summary_parts.append("Tópicos discutidos:")
            for intent, count in intents.items():
                summary_parts.append(f"- {intent}: {count}x")

        return "\n".join(summary_parts)

    async def handle_multi_step_task(
        self,
        task: str,
        steps: List[Dict],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Gerencia tarefas multi-etapas envolvendo múltiplos agentes

        Args:
            task: Descrição da tarefa
            steps: Lista de etapas a executar
            context: Contexto da tarefa

        Returns:
            Resultado consolidado
        """
        results = []

        for step in steps:
            agent_name = step.get("agent")
            action = step.get("action")
            params = step.get("params", {})

            # Executar etapa
            step_result = await self.delegate_to_agent(
                agent_name,
                action,
                {**(context or {}), **params}
            )

            results.append({
                "step": step.get("description"),
                "agent": agent_name,
                "result": step_result,
                "status": "completed" if step_result else "failed"
            })

            # Atualizar contexto para próxima etapa
            if context:
                context["previous_results"] = results

        return {
            "task": task,
            "steps_completed": len([r for r in results if r["status"] == "completed"]),
            "steps_total": len(steps),
            "results": results,
            "status": "completed" if all(r["status"] == "completed" for r in results) else "partial"
        }
