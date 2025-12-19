"""
LEGIA PLATFORM - Agente de Comunicações
Especialista em comunicações oficiais com órgãos públicos
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent
from datetime import datetime


class CommunicationsAgent(BaseAgent):
    """
    Agente de Comunicações - Ofícios e comunicações oficiais

    Responsabilidades:
    - Elaborar ofícios para órgãos públicos
    - Gerar requerimentos administrativos
    - Criar respostas a exigências
    - Elaborar notificações
    - Preparar recursos administrativos
    """

    def __init__(self):
        super().__init__(
            name="Agente de Comunicações",
            role="especialista em comunicações oficiais com órgãos públicos"
        )

        # Templates de comunicações
        self.templates = {
            "oficio": {
                "nome": "Ofício",
                "estrutura": [
                    "timbre",
                    "numero_oficio",
                    "data",
                    "destinatario",
                    "assunto",
                    "corpo",
                    "fechamento",
                    "assinatura"
                ]
            },
            "requerimento": {
                "nome": "Requerimento",
                "estrutura": [
                    "orgao_destinatario",
                    "identificacao_requerente",
                    "exposicao",
                    "pedido",
                    "local_data",
                    "assinatura"
                ]
            },
            "resposta_exigencia": {
                "nome": "Resposta à Exigência",
                "estrutura": [
                    "numero_processo",
                    "identificacao",
                    "referencia_exigencia",
                    "resposta_fundamentada",
                    "documentos_anexos",
                    "pedido_deferimento",
                    "assinatura"
                ]
            },
            "recurso": {
                "nome": "Recurso Administrativo",
                "estrutura": [
                    "orgao",
                    "identificacao",
                    "decisao_recorrida",
                    "fundamentos",
                    "pedido",
                    "assinatura"
                ]
            },
            "notificacao": {
                "nome": "Notificação",
                "estrutura": [
                    "destinatario",
                    "assunto",
                    "corpo_notificacao",
                    "prazo_resposta",
                    "consequencias",
                    "assinatura"
                ]
            }
        }

        # Órgãos destinatários comuns
        self.orgaos = {
            "jucesp": {
                "nome": "Junta Comercial do Estado de São Paulo - JUCESP",
                "endereco": "Rua Conselheiro Crispiniano, 105 - Centro - São Paulo/SP",
                "tratamento": "Ilmo(a). Sr(a). Presidente da JUCESP"
            },
            "receita_federal": {
                "nome": "Receita Federal do Brasil",
                "endereco": "Conforme jurisdição",
                "tratamento": "Ilmo(a). Sr(a). Delegado(a) da Receita Federal"
            },
            "prefeitura": {
                "nome": "Prefeitura Municipal",
                "endereco": "Conforme município",
                "tratamento": "Ilmo(a). Sr(a). Prefeito(a) Municipal"
            },
            "secretaria_fazenda": {
                "nome": "Secretaria da Fazenda Estadual",
                "endereco": "Conforme estado",
                "tratamento": "Ilmo(a). Sr(a). Secretário(a) da Fazenda"
            }
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente de comunicações"""
        return """
        Como Agente de Comunicações, você é especialista em:

        1. ELABORAÇÃO DE OFÍCIOS:
           - Estrutura formal correta
           - Linguagem oficial adequada
           - Referências legais quando necessário
           - Tom respeitoso e técnico

        2. REQUERIMENTOS:
           - Fundamentação legal
           - Exposição clara dos fatos
           - Pedido objetivo e específico
           - Documentação de suporte

        3. RESPOSTAS A EXIGÊNCIAS:
           - Análise da exigência
           - Resposta pontual e fundamentada
           - Anexação de documentos comprobatórios
           - Pedido de reconsideração quando cabível

        4. RECURSOS ADMINISTRATIVOS:
           - Identificação da decisão recorrida
           - Fundamentos legais
           - Argumentação técnica
           - Pedido de reforma

        5. NOTIFICAÇÕES:
           - Clareza na comunicação
           - Prazos explícitos
           - Consequências do não atendimento
           - Tom profissional

        IMPORTANTE:
        - Use linguagem formal e técnica
        - Seja claro e objetivo
        - Cite legislação quando relevante
        - Mantenha tom respeitoso
        - Estruture de forma lógica
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações de comunicações

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        message_lower = message.lower()

        # Detectar tipo de comunicação
        comm_type = self._detect_communication_type(message_lower)

        # Gerar resposta
        response = await self.generate_response(
            message,
            context={
                **(context or {}),
                "tipo_comunicacao": comm_type,
                "templates_disponiveis": list(self.templates.keys())
            },
            temperature=0.5  # Mais conservador para documentos oficiais
        )

        return {
            "agent": self.name,
            "response": response,
            "communication_type": comm_type,
            "available_templates": list(self.templates.keys())
        }

    def _detect_communication_type(self, message: str) -> str:
        """Detecta tipo de comunicação baseado na mensagem"""
        if any(word in message for word in ["ofício", "oficio", "encaminhar documento"]):
            return "oficio"
        elif any(word in message for word in ["requerimento", "solicitar", "requerer"]):
            return "requerimento"
        elif any(word in message for word in ["exigência", "exigencia", "responder", "complementar"]):
            return "resposta_exigencia"
        elif any(word in message for word in ["recurso", "recorrer", "indeferido"]):
            return "recurso"
        elif any(word in message for word in ["notificar", "notificação", "comunicar"]):
            return "notificacao"
        else:
            return "geral"

    async def gerar_oficio(
        self,
        destinatario: str,
        orgao: str,
        assunto: str,
        corpo: str,
        remetente: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Gera ofício oficial

        Args:
            destinatario: Nome do destinatário
            orgao: Órgão destinatário (chave do dict self.orgaos)
            assunto: Assunto do ofício
            corpo: Corpo do texto
            remetente: Dados do remetente (nome, cargo, empresa)

        Returns:
            Ofício gerado
        """
        orgao_info = self.orgaos.get(orgao, {})
        numero_oficio = self._gerar_numero_oficio()
        data_atual = datetime.now().strftime("%d de %B de %Y")

        oficio = f"""
{remetente.get('empresa', 'EMPRESA')}
{remetente.get('endereco', '')}

OFÍCIO Nº {numero_oficio}

{destinatario}, {data_atual}

{orgao_info.get('tratamento', 'Ilmo(a). Sr(a).')}
{orgao_info.get('nome', orgao)}
{orgao_info.get('endereco', '')}

Assunto: {assunto}

{corpo}

Atenciosamente,

_________________________________
{remetente.get('nome', '')}
{remetente.get('cargo', '')}
{remetente.get('documento', '')}
        """

        return {
            "success": True,
            "tipo": "oficio",
            "numero": numero_oficio,
            "conteudo": oficio.strip(),
            "data": datetime.now().isoformat(),
            "destinatario": orgao_info.get('nome', orgao),
            "assunto": assunto
        }

    async def gerar_requerimento(
        self,
        orgao: str,
        requerente: Dict[str, str],
        exposicao: str,
        pedido: str
    ) -> Dict[str, Any]:
        """
        Gera requerimento administrativo

        Args:
            orgao: Órgão destinatário
            requerente: Dados do requerente
            exposicao: Exposição dos fatos
            pedido: Pedido específico

        Returns:
            Requerimento gerado
        """
        orgao_info = self.orgaos.get(orgao, {"nome": orgao})
        data_local = f"{requerente.get('cidade', 'São Paulo')}, {datetime.now().strftime('%d de %B de %Y')}"

        requerimento = f"""
REQUERIMENTO

Ao(À)
{orgao_info.get('tratamento', 'Ilmo(a). Sr(a).')}
{orgao_info.get('nome')}

{requerente.get('nome', '')}, {requerente.get('nacionalidade', 'brasileiro(a)')},
{requerente.get('estado_civil', '')}, {requerente.get('profissao', '')},
portador(a) do RG nº {requerente.get('rg', '')} e CPF nº {requerente.get('cpf', '')},
residente e domiciliado(a) em {requerente.get('endereco', '')},
vem respeitosamente à presença de Vossa Senhoria, para REQUERER o que segue:

EXPOSIÇÃO

{exposicao}

DO PEDIDO

{pedido}

Nestes termos,
Pede deferimento.

{data_local}

_________________________________
{requerente.get('nome', '')}
CPF: {requerente.get('cpf', '')}
        """

        return {
            "success": True,
            "tipo": "requerimento",
            "conteudo": requerimento.strip(),
            "data": datetime.now().isoformat(),
            "orgao": orgao_info.get('nome'),
            "requerente": requerente.get('nome')
        }

    async def gerar_resposta_exigencia(
        self,
        numero_processo: str,
        exigencia: str,
        resposta: str,
        documentos_anexos: List[str],
        requerente: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Gera resposta a exigência

        Args:
            numero_processo: Número do processo
            exigencia: Texto da exigência
            resposta: Resposta fundamentada
            documentos_anexos: Lista de documentos anexados
            requerente: Dados do requerente

        Returns:
            Resposta à exigência gerada
        """
        data_atual = datetime.now().strftime("%d de %B de %Y")

        resposta_doc = f"""
RESPOSTA À EXIGÊNCIA

Processo nº: {numero_processo}

Ao(À)
Ilmo(a). Sr(a). Presidente da Junta Comercial

{requerente.get('nome', '')}, já qualificado(a) nos autos do processo em epígrafe,
vem, respeitosamente, à presença de Vossa Senhoria, apresentar RESPOSTA À EXIGÊNCIA,
nos seguintes termos:

DA EXIGÊNCIA

{exigencia}

DA RESPOSTA

{resposta}

DOS DOCUMENTOS

Seguem anexos os seguintes documentos:
{self._formatar_lista_documentos(documentos_anexos)}

DO PEDIDO

Diante do exposto, requer seja o presente processo analisado e DEFERIDO,
considerando sanadas as exigências apontadas.

Nestes termos,
Pede deferimento.

{requerente.get('cidade', 'São Paulo')}, {data_atual}

_________________________________
{requerente.get('nome', '')}
CPF: {requerente.get('cpf', '')}
        """

        return {
            "success": True,
            "tipo": "resposta_exigencia",
            "numero_processo": numero_processo,
            "conteudo": resposta_doc.strip(),
            "data": datetime.now().isoformat(),
            "documentos_anexos": documentos_anexos
        }

    def _gerar_numero_oficio(self) -> str:
        """Gera número sequencial de ofício"""
        # Em produção, buscar do banco de dados
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{timestamp[-6:]}/2025"

    def _formatar_lista_documentos(self, documentos: List[str]) -> str:
        """Formata lista de documentos"""
        if not documentos:
            return "Nenhum documento anexo."

        return "\n".join([f"- {doc}" for doc in documentos])

    def get_available_templates(self) -> List[Dict[str, Any]]:
        """
        Retorna templates disponíveis

        Returns:
            Lista de templates com informações
        """
        templates_list = []
        for key, template in self.templates.items():
            templates_list.append({
                "id": key,
                "nome": template["nome"],
                "estrutura": template["estrutura"],
                "uso": self._get_template_usage(key)
            })
        return templates_list

    def _get_template_usage(self, template_id: str) -> str:
        """Retorna descrição de uso do template"""
        usage = {
            "oficio": "Comunicação formal entre órgãos ou empresas",
            "requerimento": "Solicitação formal a órgão público",
            "resposta_exigencia": "Resposta a pendências em processos",
            "recurso": "Contestação de decisão administrativa",
            "notificacao": "Comunicação de fatos ou prazos"
        }
        return usage.get(template_id, "Uso geral")

    async def interpretar_exigencia(
        self,
        texto_exigencia: str,
        contexto_processo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Interpreta exigência usando IA

        Args:
            texto_exigencia: Texto da exigência da Junta
            contexto_processo: Dados do processo

        Returns:
            Interpretação da exigência
        """
        prompt = f"""
        Analise a seguinte exigência da Junta Comercial e forneça:
        1. Identificação do problema
        2. Documentos/dados que faltam
        3. Sugestão de resposta
        4. Documentos necessários para anexar

        EXIGÊNCIA:
        {texto_exigencia}

        CONTEXTO DO PROCESSO:
        Tipo: {contexto_processo.get('tipo', 'N/A')}
        Empresa: {contexto_processo.get('empresa', 'N/A')}
        Protocolo: {contexto_processo.get('protocolo', 'N/A')}

        Forneça resposta estruturada.
        """

        response = await self.generate_response(prompt, temperature=0.3)

        return {
            "exigencia_original": texto_exigencia,
            "interpretacao": response,
            "processo": contexto_processo.get('protocolo'),
            "data_analise": datetime.now().isoformat()
        }
