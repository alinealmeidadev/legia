"""
LEGIA PLATFORM - Agente Monitor
Especialista em acompanhamento de protocolos em órgãos públicos
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent
from datetime import datetime, timedelta


class MonitorAgent(BaseAgent):
    """Agente especializado em monitoramento de protocolos"""

    def __init__(self):
        super().__init__(
            name="Agente Monitor",
            role="especialista em acompanhamento de processos em órgãos públicos"
        )

        # Órgãos que o agente monitora
        self.organs = {
            "junta_comercial": {
                "nome": "Junta Comercial",
                "site": "junta.gov.br",
                "prazo_medio": "5-10 dias úteis",
                "horario_consulta": "8h às 18h"
            },
            "receita_federal": {
                "nome": "Receita Federal",
                "site": "www.gov.br/receitafederal",
                "prazo_medio": "1-3 dias úteis",
                "horario_consulta": "24h"
            },
            "prefeitura": {
                "nome": "Prefeitura Municipal",
                "site": "prefeitura.local",
                "prazo_medio": "10-30 dias úteis",
                "horario_consulta": "8h às 17h"
            },
            "estado": {
                "nome": "Secretaria Estadual",
                "site": "fazenda.estado.gov.br",
                "prazo_medio": "5-10 dias úteis",
                "horario_consulta": "8h às 18h"
            },
            "bombeiros": {
                "nome": "Corpo de Bombeiros",
                "site": "bombeiros.gov.br",
                "prazo_medio": "15-30 dias úteis",
                "horario_consulta": "8h às 17h"
            }
        }

        # Status possíveis de protocolo
        self.status_types = {
            "protocolado": "Protocolo criado, aguardando análise",
            "em_analise": "Em análise pelo órgão",
            "pendente_documento": "Aguardando documentos complementares",
            "deferido": "Deferido - aprovado",
            "indeferido": "Indeferido - negado",
            "finalizado": "Processo finalizado"
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente monitor"""
        return """
        Como Agente Monitor, você é especialista em:

        1. ACOMPANHAMENTO DE PROTOCOLOS:
           - Consultar status em órgãos públicos
           - Identificar pendências
           - Alertar sobre prazos

        2. NOTIFICAÇÕES:
           - Avisar quando houver mudança de status
           - Alertar sobre documentos pendentes
           - Notificar quando processo for deferido

        3. ANÁLISE DE PRAZOS:
           - Calcular tempo decorrido
           - Estimar tempo restante
           - Identificar atrasos

        4. RECOMENDAÇÕES:
           - Sugerir ações quando houver pendência
           - Orientar sobre próximos passos
           - Indicar quando fazer contato com órgão

        IMPORTANTE:
        - Seja claro sobre o status atual
        - Explique o que cada status significa
        - Forneça datas e prazos quando disponível
        - Alerte proativamente sobre problemas
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações de monitoramento

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        message_lower = message.lower()

        # Detectar tipo de consulta
        query_type = self._detect_query_type(message_lower)

        # Construir contexto específico
        specific_context = {}
        if context and "protocol_id" in context:
            specific_context["protocol_info"] = self._get_protocol_info(context["protocol_id"])

        # Gerar resposta
        response = await self.generate_response(
            message,
            context={**(context or {}), **specific_context},
            temperature=0.5
        )

        return {
            "agent": self.name,
            "response": response,
            "query_type": query_type
        }

    def _detect_query_type(self, message: str) -> str:
        """Detecta tipo de consulta"""
        if any(word in message for word in ["status", "andamento", "situação"]):
            return "status_check"
        elif any(word in message for word in ["prazo", "demora", "quanto tempo"]):
            return "deadline_check"
        elif any(word in message for word in ["pendência", "pendente", "falta"]):
            return "pending_check"
        else:
            return "general"

    def _get_protocol_info(self, protocol_id: str) -> Dict:
        """Simula busca de informações do protocolo"""
        # Aqui conectaria com sistema real
        return {
            "protocol_id": protocol_id,
            "organ": "junta_comercial",
            "status": "em_analise",
            "created_at": (datetime.now() - timedelta(days=5)).isoformat()
        }

    def check_protocol_status(
        self,
        protocol_number: str,
        organ: str
    ) -> Dict[str, Any]:
        """
        Consulta status de protocolo

        Args:
            protocol_number: Número do protocolo
            organ: Órgão onde foi protocolado

        Returns:
            Status do protocolo
        """
        organ_info = self.organs.get(organ, {})

        # Simular consulta (em produção, faria request real)
        return {
            "protocol_number": protocol_number,
            "organ": organ_info.get("nome", organ),
            "status": "em_analise",
            "status_description": self.status_types["em_analise"],
            "last_update": datetime.now().isoformat(),
            "estimated_completion": (datetime.now() + timedelta(days=3)).isoformat(),
            "messages": [
                {
                    "date": datetime.now().isoformat(),
                    "message": "Protocolo recebido e em análise"
                }
            ],
            "next_steps": [
                "Aguardar análise do órgão",
                "Verificar novamente em 2 dias úteis"
            ]
        }

    def get_all_protocols_status(
        self,
        client_id: int,
        tenant_id: int
    ) -> List[Dict[str, Any]]:
        """
        Lista status de todos protocolos de um cliente

        Args:
            client_id: ID do cliente
            tenant_id: ID do tenant

        Returns:
            Lista de protocolos com status
        """
        # Aqui buscaria do banco de dados
        # Por enquanto retorna exemplo
        return [
            {
                "protocol_number": "JC202501001",
                "organ": "Junta Comercial",
                "type": "Alteração Contratual",
                "status": "deferido",
                "days_elapsed": 7,
                "created_at": (datetime.now() - timedelta(days=7)).isoformat()
            },
            {
                "protocol_number": "RF202501002",
                "organ": "Receita Federal",
                "type": "Atualização Cadastral",
                "status": "em_analise",
                "days_elapsed": 2,
                "created_at": (datetime.now() - timedelta(days=2)).isoformat()
            }
        ]

    def check_delays(
        self,
        protocols: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        Verifica se há protocolos atrasados

        Args:
            protocols: Lista de protocolos

        Returns:
            Lista de protocolos atrasados
        """
        delayed = []

        for protocol in protocols:
            # Calcular se está atrasado baseado no prazo médio do órgão
            organ = protocol.get("organ", "")
            organ_info = next(
                (o for o in self.organs.values() if o["nome"] == organ),
                None
            )

            if organ_info:
                # Extrair prazo máximo (simplificado)
                prazo_texto = organ_info["prazo_medio"]
                prazo_dias = int(prazo_texto.split("-")[1].split()[0])

                days_elapsed = protocol.get("days_elapsed", 0)

                if days_elapsed > prazo_dias:
                    delayed.append({
                        **protocol,
                        "days_delayed": days_elapsed - prazo_dias,
                        "expected_days": prazo_dias,
                        "alert_level": "high" if days_elapsed > prazo_dias * 1.5 else "medium"
                    })

        return delayed

    def generate_status_report(
        self,
        client_id: int,
        tenant_id: int
    ) -> Dict[str, Any]:
        """
        Gera relatório completo de status

        Args:
            client_id: ID do cliente
            tenant_id: ID do tenant

        Returns:
            Relatório estruturado
        """
        protocols = self.get_all_protocols_status(client_id, tenant_id)
        delayed = self.check_delays(protocols)

        # Contar por status
        status_count = {}
        for protocol in protocols:
            status = protocol.get("status", "unknown")
            status_count[status] = status_count.get(status, 0) + 1

        return {
            "client_id": client_id,
            "total_protocols": len(protocols),
            "status_breakdown": status_count,
            "delayed_count": len(delayed),
            "delayed_protocols": delayed,
            "all_protocols": protocols,
            "generated_at": datetime.now().isoformat()
        }
