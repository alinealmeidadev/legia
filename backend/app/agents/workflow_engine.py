"""
LEGIA PLATFORM - Workflow Engine
Coordena múltiplos agentes trabalhando juntos em processos complexos
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class WorkflowStage(Enum):
    """Estágios do workflow"""
    COMMERCIAL = "commercial"  # Orçamento e vendas
    LEGALIZATION = "legalization"  # Análise e planejamento
    CONTRACTS = "contracts"  # Geração de documentos
    CLIENT_FORM = "client_form"  # Formulário para cliente
    DOCUMENT_COLLECTION = "document_collection"  # Coleta de docs
    PROTOCOL = "protocol"  # Protocolização
    MONITORING = "monitoring"  # Acompanhamento
    COMPLETED = "completed"  # Concluído


class WorkflowEngine:
    """Engine que orquestra workflows entre agentes"""

    def __init__(self):
        self.workflows = {}

    def create_workflow(
        self,
        workflow_type: str,
        client_id: int,
        tenant_id: int,
        initial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Cria novo workflow

        Args:
            workflow_type: Tipo do workflow (ex: alteracao_endereco)
            client_id: ID do cliente
            tenant_id: ID do tenant
            initial_data: Dados iniciais

        Returns:
            Workflow criado
        """
        workflow_id = f"WF-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        workflow = {
            "id": workflow_id,
            "type": workflow_type,
            "client_id": client_id,
            "tenant_id": tenant_id,
            "current_stage": WorkflowStage.COMMERCIAL.value,
            "stages": self._get_workflow_stages(workflow_type),
            "data": initial_data,
            "forms": [],
            "documents": [],
            "tasks": [],
            "history": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "active"
        }

        self.workflows[workflow_id] = workflow
        self._add_history(workflow_id, "workflow_created", "Workflow criado")

        return workflow

    def _get_workflow_stages(self, workflow_type: str) -> List[Dict]:
        """Define estágios baseado no tipo de workflow"""

        # Workflow para alteração contratual
        if workflow_type.startswith("alteracao_"):
            return [
                {
                    "stage": WorkflowStage.COMMERCIAL.value,
                    "agent": "commercial",
                    "name": "Orçamento",
                    "description": "Gerar orçamento e fechar venda",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.LEGALIZATION.value,
                    "agent": "legalization",
                    "name": "Análise Legal",
                    "description": "Analisar viabilidade e requisitos",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.CLIENT_FORM.value,
                    "agent": "workflow",
                    "name": "Formulário Cliente",
                    "description": "Cliente preenche dados necessários",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.DOCUMENT_COLLECTION.value,
                    "agent": "workflow",
                    "name": "Coleta Documentos",
                    "description": "Cliente envia documentos",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.CONTRACTS.value,
                    "agent": "contracts",
                    "name": "Geração Documentos",
                    "description": "Gerar contratos e documentos",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.PROTOCOL.value,
                    "agent": "protocol",
                    "name": "Protocolização",
                    "description": "Protocolar nos órgãos",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.MONITORING.value,
                    "agent": "monitor",
                    "name": "Acompanhamento",
                    "description": "Acompanhar andamento",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.COMPLETED.value,
                    "agent": None,
                    "name": "Concluído",
                    "description": "Processo finalizado",
                    "required_data": [],
                    "completed": False
                }
            ]

        # Workflow para abertura de empresa
        elif workflow_type == "abertura_empresa":
            return [
                {
                    "stage": WorkflowStage.COMMERCIAL.value,
                    "agent": "commercial",
                    "name": "Orçamento",
                    "description": "Gerar orçamento e fechar venda",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.LEGALIZATION.value,
                    "agent": "legalization",
                    "name": "Análise Tipo Empresa",
                    "description": "Recomendar tipo empresarial",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.CLIENT_FORM.value,
                    "agent": "workflow",
                    "name": "Formulário Cliente",
                    "description": "Cliente preenche dados da empresa",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.DOCUMENT_COLLECTION.value,
                    "agent": "workflow",
                    "name": "Coleta Documentos",
                    "description": "Cliente envia documentos dos sócios",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.CONTRACTS.value,
                    "agent": "contracts",
                    "name": "Elaboração Contrato Social",
                    "description": "Gerar contrato social",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.PROTOCOL.value,
                    "agent": "protocol",
                    "name": "Protocolização",
                    "description": "Protocolar na Junta Comercial",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.MONITORING.value,
                    "agent": "monitor",
                    "name": "Acompanhamento",
                    "description": "Acompanhar deferimento",
                    "required_data": [],
                    "completed": False
                },
                {
                    "stage": WorkflowStage.COMPLETED.value,
                    "agent": None,
                    "name": "Concluído",
                    "description": "Empresa constituída",
                    "required_data": [],
                    "completed": False
                }
            ]

        # Workflow padrão
        return []

    def advance_stage(self, workflow_id: str, completion_data: Dict = None) -> Dict[str, Any]:
        """
        Avança para próximo estágio

        Args:
            workflow_id: ID do workflow
            completion_data: Dados do estágio concluído

        Returns:
            Workflow atualizado
        """
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return {"error": "Workflow não encontrado"}

        # Marcar estágio atual como completo
        current_stage = workflow["current_stage"]
        for stage in workflow["stages"]:
            if stage["stage"] == current_stage:
                stage["completed"] = True
                stage["completed_at"] = datetime.now().isoformat()
                if completion_data:
                    stage["completion_data"] = completion_data
                break

        # Encontrar próximo estágio
        current_index = next(
            (i for i, s in enumerate(workflow["stages"]) if s["stage"] == current_stage),
            -1
        )

        if current_index >= 0 and current_index < len(workflow["stages"]) - 1:
            next_stage = workflow["stages"][current_index + 1]
            workflow["current_stage"] = next_stage["stage"]

            self._add_history(
                workflow_id,
                "stage_advanced",
                f"Avançou para: {next_stage['name']}"
            )

            # Executar ações do próximo estágio
            self._execute_stage_actions(workflow_id, next_stage)
        else:
            workflow["status"] = "completed"
            workflow["completed_at"] = datetime.now().isoformat()
            self._add_history(workflow_id, "workflow_completed", "Workflow concluído")

        workflow["updated_at"] = datetime.now().isoformat()
        return workflow

    def _execute_stage_actions(self, workflow_id: str, stage: Dict):
        """Executa ações automáticas do estágio"""
        workflow = self.workflows[workflow_id]

        # Gerar formulário para cliente
        if stage["stage"] == WorkflowStage.CLIENT_FORM.value:
            form = self._generate_client_form(workflow)
            workflow["forms"].append(form)
            self._add_history(workflow_id, "form_generated", f"Formulário gerado: {form['id']}")

        # Solicitar documentos
        elif stage["stage"] == WorkflowStage.DOCUMENT_COLLECTION.value:
            doc_list = self._generate_document_request(workflow)
            workflow["documents"] = doc_list
            self._add_history(workflow_id, "documents_requested", f"Solicitados {len(doc_list)} documentos")

    def _generate_client_form(self, workflow: Dict) -> Dict[str, Any]:
        """Gera formulário dinâmico para cliente"""
        form_id = f"FORM-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        workflow_type = workflow["type"]

        fields = []

        # Formulário para alteração de endereço
        if workflow_type == "alteracao_endereco":
            fields = [
                {
                    "id": "novo_endereco",
                    "label": "Novo Endereço Completo",
                    "type": "text",
                    "required": True,
                    "placeholder": "Rua, número, complemento"
                },
                {
                    "id": "cep",
                    "label": "CEP",
                    "type": "text",
                    "required": True,
                    "mask": "99999-999"
                },
                {
                    "id": "cidade",
                    "label": "Cidade",
                    "type": "text",
                    "required": True
                },
                {
                    "id": "estado",
                    "label": "Estado",
                    "type": "select",
                    "required": True,
                    "options": ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
                },
                {
                    "id": "tipo_imovel",
                    "label": "Tipo de Imóvel",
                    "type": "select",
                    "required": True,
                    "options": ["Comercial", "Residencial", "Industrial"],
                    "alert": {
                        "condition": {"value": "Comercial"},
                        "message": "⚠️ Para imóvel comercial será necessária licença do Corpo de Bombeiros"
                    }
                },
                {
                    "id": "tem_placa",
                    "label": "Terá placa de anúncio?",
                    "type": "radio",
                    "required": True,
                    "options": ["Sim", "Não"],
                    "alert": {
                        "condition": {"value": "Sim"},
                        "message": "⚠️ Placa de anúncio requer autorização da prefeitura"
                    }
                },
                {
                    "id": "metragem",
                    "label": "Metragem utilizada (m²)",
                    "type": "number",
                    "required": True,
                    "alert": {
                        "condition": {"operator": ">", "value": 200},
                        "message": "⚠️ Imóveis acima de 200m² requerem vistoria do Corpo de Bombeiros"
                    }
                },
                {
                    "id": "outras_alteracoes",
                    "label": "Deseja realizar outras alterações junto com esta?",
                    "type": "checkbox",
                    "options": [
                        "Alterar atividade (CNAE)",
                        "Alterar capital social",
                        "Alterar quadro societário",
                        "Alterar nome/razão social"
                    ]
                }
            ]

        # Formulário para alteração de sócios
        elif workflow_type == "alteracao_socios":
            fields = [
                {
                    "id": "tipo_alteracao",
                    "label": "Tipo de Alteração",
                    "type": "select",
                    "required": True,
                    "options": ["Inclusão de sócio", "Exclusão de sócio", "Alteração de participação"]
                },
                {
                    "id": "nome_socio",
                    "label": "Nome Completo do Sócio",
                    "type": "text",
                    "required": True
                },
                {
                    "id": "cpf_socio",
                    "label": "CPF",
                    "type": "text",
                    "required": True,
                    "mask": "999.999.999-99"
                },
                {
                    "id": "participacao",
                    "label": "Participação (%)",
                    "type": "number",
                    "required": True,
                    "min": 0,
                    "max": 100
                },
                {
                    "id": "forma_integralizacao",
                    "label": "Forma de Integralização",
                    "type": "select",
                    "required": True,
                    "options": ["Dinheiro", "Bens", "Direitos", "Mista"]
                }
            ]

        return {
            "id": form_id,
            "workflow_id": workflow["id"],
            "workflow_type": workflow_type,
            "title": self._get_form_title(workflow_type),
            "description": self._get_form_description(workflow_type),
            "fields": fields,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "expires_at": None  # Adicionar expiração se necessário
        }

    def _get_form_title(self, workflow_type: str) -> str:
        """Retorna título do formulário"""
        titles = {
            "alteracao_endereco": "Alteração de Endereço - Dados Necessários",
            "alteracao_socios": "Alteração de Sócios - Informações do Sócio",
            "alteracao_capital": "Alteração de Capital - Dados da Alteração",
            "abertura_empresa": "Abertura de Empresa - Dados da Empresa"
        }
        return titles.get(workflow_type, "Formulário de Dados")

    def _get_form_description(self, workflow_type: str) -> str:
        """Retorna descrição do formulário"""
        return "Por favor, preencha as informações abaixo para darmos continuidade ao processo."

    def _generate_document_request(self, workflow: Dict) -> List[Dict]:
        """Gera lista de documentos necessários"""
        workflow_type = workflow["type"]
        documents = []

        if workflow_type == "alteracao_endereco":
            documents = [
                {
                    "id": "iptu",
                    "name": "IPTU do novo endereço",
                    "description": "Carnê de IPTU atualizado",
                    "required": True,
                    "status": "pending"
                },
                {
                    "id": "comprovante_endereco",
                    "name": "Comprovante de Endereço",
                    "description": "Conta de luz, água ou telefone",
                    "required": True,
                    "status": "pending"
                },
                {
                    "id": "contrato_social",
                    "name": "Contrato Social Vigente",
                    "description": "Última alteração contratual",
                    "required": True,
                    "status": "pending"
                }
            ]

            # Adicionar documentos condicionais baseado nas respostas do formulário
            form_data = workflow.get("data", {}).get("form_responses", {})
            if form_data.get("tipo_imovel") == "Comercial":
                documents.append({
                    "id": "bombeiros",
                    "name": "Licença do Corpo de Bombeiros",
                    "description": "AVCB ou protocolo",
                    "required": True,
                    "status": "pending"
                })

        return documents

    def _add_history(self, workflow_id: str, event_type: str, description: str):
        """Adiciona evento ao histórico"""
        workflow = self.workflows.get(workflow_id)
        if workflow:
            workflow["history"].append({
                "timestamp": datetime.now().isoformat(),
                "event_type": event_type,
                "description": description
            })

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """Retorna workflow"""
        return self.workflows.get(workflow_id)

    def update_workflow_data(self, workflow_id: str, data: Dict):
        """Atualiza dados do workflow"""
        workflow = self.workflows.get(workflow_id)
        if workflow:
            workflow["data"].update(data)
            workflow["updated_at"] = datetime.now().isoformat()
            self._add_history(workflow_id, "data_updated", "Dados atualizados")


# Instância global
workflow_engine = WorkflowEngine()
