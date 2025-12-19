"""
LEGIA PLATFORM - Agente de Contratos
Especialista em elaboração e alteração de documentos contratuais
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent
from datetime import datetime


class ContractsAgent(BaseAgent):
    """Agente especializado em contratos e documentos legais"""

    def __init__(self):
        super().__init__(
            name="Agente de Contratos",
            role="especialista em elaboração e alteração de contratos sociais"
        )

        # Tipos de atos disponíveis
        self.available_acts = {
            "alteracao_endereco": {
                "nome": "Alteração de Endereço",
                "descricao": "Mudança do endereço da sede social",
                "campos_necessarios": ["novo_endereco", "cep", "cidade", "estado"],
                "documentos_necessarios": ["contrato_social_vigente", "comprovante_endereco", "iptu"],
                "prazo_medio": "15-20 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal", "Prefeitura"]
            },
            "alteracao_socios": {
                "nome": "Alteração de Quadro Societário",
                "descricao": "Inclusão, exclusão ou alteração de sócios",
                "campos_necessarios": ["tipo_alteracao", "dados_socio", "participacao"],
                "documentos_necessarios": ["contrato_social_vigente", "rg_cpf_socios", "comprovante_residencia"],
                "prazo_medio": "20-30 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal"]
            },
            "alteracao_capital": {
                "nome": "Alteração de Capital Social",
                "descricao": "Aumento ou redução do capital social",
                "campos_necessarios": ["capital_atual", "capital_novo", "forma_integralizacao"],
                "documentos_necessarios": ["contrato_social_vigente", "balanco_patrimonial"],
                "prazo_medio": "15-25 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal"]
            },
            "alteracao_atividade": {
                "nome": "Alteração de Atividade",
                "descricao": "Inclusão ou exclusão de CNAEs",
                "campos_necessarios": ["cnaes_incluir", "cnaes_excluir"],
                "documentos_necessarios": ["contrato_social_vigente", "consulta_viabilidade"],
                "prazo_medio": "15-20 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal", "Prefeitura"]
            },
            "alteracao_nome": {
                "nome": "Alteração de Nome Empresarial",
                "descricao": "Mudança da razão social ou nome fantasia",
                "campos_necessarios": ["nome_atual", "nome_novo"],
                "documentos_necessarios": ["contrato_social_vigente", "consulta_viabilidade"],
                "prazo_medio": "15-20 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal"]
            },
            "alteracao_administracao": {
                "nome": "Alteração de Administração",
                "descricao": "Mudança de administradores/diretores",
                "campos_necessarios": ["administradores_novos", "tipo_administracao"],
                "documentos_necessarios": ["contrato_social_vigente", "rg_cpf_administradores"],
                "prazo_medio": "15-20 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal"]
            },
            "distrato": {
                "nome": "Distrato Social",
                "descricao": "Encerramento da empresa",
                "campos_necessarios": ["motivo_encerramento", "data_encerramento"],
                "documentos_necessarios": ["contrato_social_vigente", "certidoes_negativas", "balanco_final"],
                "prazo_medio": "60-90 dias úteis",
                "orgaos": ["Junta Comercial", "Receita Federal", "Prefeitura", "Estado"]
            }
        }

        # Templates de cláusulas
        self.clause_templates = {
            "alteracao_endereco": """
CLÁUSULA {numero}ª - ENDEREÇO DA SEDE

O endereço da sede social passa a ser:

{endereco_completo}
CEP: {cep}
{cidade}/{estado}

Permanecendo inalteradas as demais cláusulas do Contrato Social.
""",
            "alteracao_socios_inclusao": """
CLÁUSULA {numero}ª - ALTERAÇÃO DO QUADRO SOCIETÁRIO

Fica incluído no quadro societário o(a) sócio(a):

Nome: {nome_socio}
CPF: {cpf_socio}
RG: {rg_socio}
Endereço: {endereco_socio}

Participação: {percentual}% do capital social
Quotas: {quantidade_quotas} quotas no valor de R$ {valor_quota} cada
Total: R$ {valor_total}

Permanecendo inalteradas as demais cláusulas do Contrato Social.
""",
            "alteracao_capital": """
CLÁUSULA {numero}ª - CAPITAL SOCIAL

O Capital Social passa de R$ {capital_anterior} ({capital_anterior_extenso}) para
R$ {capital_novo} ({capital_novo_extenso}), dividido em {total_quotas} quotas de
R$ {valor_quota} cada.

Forma de integralização: {forma_integralizacao}

A distribuição das quotas entre os sócios passa a ser:

{distribuicao_socios}

Permanecendo inalteradas as demais cláusulas do Contrato Social.
"""
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente de contratos"""
        return """
        Como Agente de Contratos, você é especialista em:

        1. ELABORAÇÃO DE CONTRATOS:
           - Contratos sociais (LTDA, SA, etc)
           - Alterações contratuais
           - Distratos

        2. ANÁLISE DE DOCUMENTOS:
           - Ler e extrair informações de contratos existentes
           - Identificar cláusulas importantes
           - Validar dados

        3. GERAÇÃO AUTOMÁTICA:
           - Criar cláusulas baseado em templates
           - Preencher automaticamente com dados do cliente
           - Gerar documentos completos

        4. ORIENTAÇÃO:
           - Explicar necessidade de cada documento
           - Listar órgãos envolvidos
           - Informar prazos

        IMPORTANTE:
        - Use linguagem jurídica adequada
        - Seja preciso com dados e valores
        - Sempre valide informações críticas
        - Indique quando precisa de documentos adicionais
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações de contratos

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        message_lower = message.lower()

        # Detectar tipo de ato
        act_type = self._detect_act_type(message_lower)

        # Construir resposta
        if act_type and act_type != "geral":
            act_info = self.available_acts.get(act_type)
            response = await self.generate_response(
                message,
                context={
                    **(context or {}),
                    "ato_detectado": act_info,
                    "tipo": act_type
                }
            )
        else:
            response = await self.generate_response(message, context)

        return {
            "agent": self.name,
            "response": response,
            "act_type": act_type,
            "act_info": self.available_acts.get(act_type) if act_type else None
        }

    def _detect_act_type(self, message: str) -> str:
        """Detecta tipo de ato baseado na mensagem"""
        if any(word in message for word in ["endereço", "endereco", "mudança de local", "mudar sede"]):
            return "alteracao_endereco"
        elif any(word in message for word in ["sócio", "socio", "quotista", "saída", "entrada", "inclusão"]):
            return "alteracao_socios"
        elif any(word in message for word in ["capital", "aumento de capital", "redução de capital"]):
            return "alteracao_capital"
        elif any(word in message for word in ["atividade", "cnae", "ramo"]):
            return "alteracao_atividade"
        elif any(word in message for word in ["nome", "razão social", "razao social"]):
            return "alteracao_nome"
        elif any(word in message for word in ["administr", "diretor", "gerente"]):
            return "alteracao_administracao"
        elif any(word in message for word in ["encerr", "distrato", "baixa", "fechar empresa"]):
            return "distrato"
        else:
            return "geral"

    def get_available_acts(self) -> List[Dict[str, Any]]:
        """
        Retorna lista de atos disponíveis para interface

        Returns:
            Lista de atos com informações
        """
        acts = []
        for key, act in self.available_acts.items():
            acts.append({
                "id": key,
                "nome": act["nome"],
                "descricao": act["descricao"],
                "prazo": act["prazo_medio"],
                "documentos": len(act["documentos_necessarios"])
            })
        return acts

    def get_act_details(self, act_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna detalhes completos de um ato

        Args:
            act_id: ID do ato

        Returns:
            Detalhes do ato
        """
        return self.available_acts.get(act_id)

    async def generate_contract_clause(
        self,
        act_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Gera cláusula contratual baseada em template

        Args:
            act_type: Tipo do ato
            data: Dados para preencher

        Returns:
            Cláusula gerada
        """
        template = self.clause_templates.get(act_type)

        if not template:
            return {
                "success": False,
                "error": "Template não encontrado para este tipo de ato"
            }

        try:
            # Preencher template com dados
            clause = template.format(**data)

            return {
                "success": True,
                "clause": clause,
                "act_type": act_type,
                "generated_at": datetime.now().isoformat()
            }
        except KeyError as e:
            return {
                "success": False,
                "error": f"Campo obrigatório faltando: {e}"
            }

    async def analyze_contract_document(
        self,
        document_text: str
    ) -> Dict[str, Any]:
        """
        Analisa documento de contrato e extrai informações

        Args:
            document_text: Texto do documento

        Returns:
            Informações extraídas
        """
        # Usar Gemini para análise
        prompt = f"""
        Analise o seguinte contrato social e extraia as informações:

        {document_text}

        Retorne em formato estruturado:
        - Razão Social
        - CNPJ
        - Endereço completo
        - Capital Social
        - Sócios (nome, CPF, participação)
        - Atividades (CNAEs)
        - Administradores
        """

        response = await self.generate_response(prompt, temperature=0.3)

        return {
            "success": True,
            "analysis": response,
            "extracted_at": datetime.now().isoformat()
        }

    def generate_document_checklist(
        self,
        act_type: str,
        company_data: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Gera checklist de documentos necessários

        Args:
            act_type: Tipo do ato
            company_data: Dados da empresa para personalizar

        Returns:
            Checklist estruturado
        """
        act_info = self.available_acts.get(act_type)

        if not act_info:
            return {
                "success": False,
                "error": "Ato não encontrado"
            }

        checklist = {
            "success": True,
            "act": act_info["nome"],
            "documents": []
        }

        # Documentos base
        for doc in act_info["documentos_necessarios"]:
            checklist["documents"].append({
                "document": doc,
                "required": True,
                "status": "pending"
            })

        # Adicionar campos de dados necessários
        checklist["data_fields"] = act_info["campos_necessarios"]
        checklist["estimated_timeline"] = act_info["prazo_medio"]
        checklist["agencies"] = act_info["orgaos"]

        return checklist

    async def validate_company_data(
        self,
        company_id: int,
        act_type: str
    ) -> Dict[str, Any]:
        """
        Valida se empresa tem dados suficientes para o ato

        Args:
            company_id: ID da empresa
            act_type: Tipo do ato

        Returns:
            Validação
        """
        act_info = self.available_acts.get(act_type)

        if not act_info:
            return {
                "valid": False,
                "error": "Ato não encontrado"
            }

        # Aqui conectaria com banco de dados para buscar dados da empresa
        # Por enquanto retornar estrutura

        return {
            "valid": True,
            "company_id": company_id,
            "act_type": act_type,
            "missing_data": [],
            "missing_documents": [],
            "ready_to_generate": True
        }
