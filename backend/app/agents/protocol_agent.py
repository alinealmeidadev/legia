"""
LEGIA PLATFORM - Agente de Protocolos
Especialista em criação e envio de protocolos para órgãos públicos
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent
from datetime import datetime


class ProtocolAgent(BaseAgent):
    """Agente especializado em protocolização de documentos"""

    def __init__(self):
        super().__init__(
            name="Agente de Protocolos",
            role="especialista em protocolização em órgãos públicos"
        )

        # Templates de protocolos por órgão
        self.protocol_templates = {
            "junta_comercial": {
                "nome": "Junta Comercial",
                "documentos_obrigatorios": [
                    "Requerimento",
                    "Contrato Social ou Alteração",
                    "DBE (Documento Básico de Entrada)",
                    "Comprovante de pagamento"
                ],
                "taxa": 150.00,
                "formato": "PDF",
                "envio": "online"
            },
            "receita_federal": {
                "nome": "Receita Federal",
                "documentos_obrigatorios": [
                    "Formulário DBE",
                    "Documentos dos sócios",
                    "Comprovante NIRE"
                ],
                "taxa": 0.00,
                "formato": "PDF",
                "envio": "online"
            },
            "prefeitura": {
                "nome": "Prefeitura Municipal",
                "documentos_obrigatorios": [
                    "Requerimento",
                    "Contrato Social",
                    "IPTU",
                    "Consulta de Viabilidade"
                ],
                "taxa": 80.00,
                "formato": "PDF ou Físico",
                "envio": "presencial ou online"
            }
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente de protocolos"""
        return """
        Como Agente de Protocolos, você é especialista em:

        1. PREPARAÇÃO DE PROTOCOLOS:
           - Organizar documentos necessários
           - Preencher formulários corretos
           - Validar informações

        2. PROTOCOLIZAÇÃO:
           - Enviar para órgãos corretos
           - Gerar número de protocolo
           - Confirmar recebimento

        3. TAXAS E CUSTOS:
           - Calcular valores
           - Gerar guias de pagamento
           - Confirmar pagamentos

        4. ACOMPANHAMENTO INICIAL:
           - Confirmar que protocolo foi aceito
           - Identificar erros de envio
           - Solicitar correções se necessário

        IMPORTANTE:
        - Seja preciso com documentos
        - Valide tudo antes de enviar
        - Mantenha registro de todos protocolos
        - Informe números de protocolo claramente
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações de protocolização

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        response = await self.generate_response(message, context, temperature=0.5)

        return {
            "agent": self.name,
            "response": response
        }

    def create_protocol(
        self,
        organ: str,
        document_type: str,
        documents: List[str],
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cria novo protocolo

        Args:
            organ: Órgão onde protocolar
            document_type: Tipo de documento
            documents: Lista de documentos anexos
            data: Dados do protocolo

        Returns:
            Protocolo criado
        """
        template = self.protocol_templates.get(organ)
        if not template:
            return {
                "success": False,
                "error": "Órgão não encontrado"
            }

        # Validar documentos obrigatórios
        missing_docs = []
        for doc in template["documentos_obrigatorios"]:
            if doc not in documents:
                missing_docs.append(doc)

        if missing_docs:
            return {
                "success": False,
                "error": "Documentos faltando",
                "missing_documents": missing_docs
            }

        # Gerar número de protocolo
        protocol_number = self._generate_protocol_number(organ)

        protocol = {
            "protocol_number": protocol_number,
            "organ": template["nome"],
            "organ_id": organ,
            "document_type": document_type,
            "documents": documents,
            "data": data,
            "status": "protocolado",
            "taxa": template["taxa"],
            "taxa_paid": False,
            "created_at": datetime.now().isoformat(),
            "estimated_response": self._calculate_estimated_response(organ)
        }

        return {
            "success": True,
            "protocol": protocol,
            "next_steps": [
                f"Pagar taxa de R$ {template['taxa']:.2f}" if template['taxa'] > 0 else "Sem taxa",
                f"Acompanhar pelo número: {protocol_number}",
                "Aguardar resposta do órgão"
            ]
        }

    def _generate_protocol_number(self, organ: str) -> str:
        """Gera número de protocolo"""
        prefix = {
            "junta_comercial": "JC",
            "receita_federal": "RF",
            "prefeitura": "PM",
            "estado": "SE"
        }.get(organ, "XX")

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}{timestamp}"

    def _calculate_estimated_response(self, organ: str) -> str:
        """Calcula prazo estimado de resposta"""
        prazos = {
            "junta_comercial": "5-10 dias úteis",
            "receita_federal": "1-3 dias úteis",
            "prefeitura": "10-30 dias úteis",
            "estado": "5-10 dias úteis"
        }
        return prazos.get(organ, "Prazo indefinido")

    def generate_payment_slip(
        self,
        protocol_number: str,
        organ: str,
        amount: float
    ) -> Dict[str, Any]:
        """
        Gera guia de pagamento

        Args:
            protocol_number: Número do protocolo
            organ: Órgão
            amount: Valor

        Returns:
            Dados da guia
        """
        return {
            "protocol_number": protocol_number,
            "organ": organ,
            "amount": amount,
            "barcode": f"0000000000{int(amount * 100):010d}",
            "due_date": datetime.now().isoformat(),
            "instructions": "Pagar em qualquer banco ou lotérica"
        }

    def batch_protocol(
        self,
        protocols_data: List[Dict]
    ) -> Dict[str, Any]:
        """
        Protocola vários documentos em lote

        Args:
            protocols_data: Lista de dados de protocolos

        Returns:
            Resultado do lote
        """
        results = []
        success_count = 0
        error_count = 0

        for data in protocols_data:
            result = self.create_protocol(
                organ=data.get("organ"),
                document_type=data.get("document_type"),
                documents=data.get("documents", []),
                data=data.get("data", {})
            )

            if result.get("success"):
                success_count += 1
            else:
                error_count += 1

            results.append(result)

        return {
            "total": len(protocols_data),
            "success": success_count,
            "errors": error_count,
            "results": results
        }

    def get_protocol_checklist(
        self,
        organ: str,
        document_type: str
    ) -> Dict[str, Any]:
        """
        Retorna checklist para protocolização

        Args:
            organ: Órgão
            document_type: Tipo de documento

        Returns:
            Checklist completo
        """
        template = self.protocol_templates.get(organ)
        if not template:
            return {
                "success": False,
                "error": "Órgão não encontrado"
            }

        return {
            "success": True,
            "organ": template["nome"],
            "document_type": document_type,
            "documents_required": template["documentos_obrigatorios"],
            "fee": template["taxa"],
            "format": template["formato"],
            "submission_method": template["envio"],
            "steps": [
                "1. Reunir todos os documentos obrigatórios",
                "2. Converter para o formato exigido",
                f"3. Pagar taxa de R$ {template['taxa']:.2f}" if template['taxa'] > 0 else "3. Sem taxa",
                "4. Realizar protocolo",
                "5. Guardar número do protocolo",
                "6. Acompanhar andamento"
            ]
        }
