"""
LEGIA PLATFORM - Agente de Legalização
Especialista em processos de abertura e regularização de empresas
"""
from typing import Dict, Optional, Any
from .base_agent import BaseAgent


class LegalizationAgent(BaseAgent):
    """Agente especializado em processos de legalização de empresas"""

    def __init__(self):
        super().__init__(
            name="Agente de Legalização",
            role="especialista em abertura e regularização de empresas"
        )

        # Base de conhecimento sobre tipos de empresa
        self.company_types = {
            "mei": {
                "nome": "Microempreendedor Individual (MEI)",
                "faturamento_max": "R$ 81.000,00/ano",
                "funcionarios_max": 1,
                "atividades": "Limitadas (consultar lista)",
                "tributacao": "Simples Nacional - Fixo mensal",
                "vantagens": [
                    "Menor custo mensal",
                    "Processo simplificado",
                    "CNPJ próprio",
                    "Benefícios previdenciários"
                ],
                "ideal_para": "Profissionais autônomos, pequenos negócios"
            },
            "me": {
                "nome": "Microempresa (ME)",
                "faturamento_max": "R$ 360.000,00/ano",
                "funcionarios_max": "9 (comércio/serviços) ou 19 (indústria)",
                "atividades": "Quase todas",
                "tributacao": "Simples Nacional",
                "vantagens": [
                    "Pode contratar funcionários",
                    "Mais atividades permitidas",
                    "Pode ter sócios",
                    "Tributação simplificada"
                ],
                "ideal_para": "Pequenas empresas em crescimento"
            },
            "epp": {
                "nome": "Empresa de Pequeno Porte (EPP)",
                "faturamento_max": "R$ 4.800.000,00/ano",
                "funcionarios_max": "49 (comércio/serviços) ou 99 (indústria)",
                "atividades": "Quase todas",
                "tributacao": "Simples Nacional ou Lucro Presumido",
                "vantagens": [
                    "Maior limite de faturamento",
                    "Pode contratar mais funcionários",
                    "Flexibilidade tributária"
                ],
                "ideal_para": "Empresas em crescimento acelerado"
            },
            "ltda": {
                "nome": "Sociedade Limitada (LTDA)",
                "faturamento_max": "Sem limite",
                "funcionarios_max": "Sem limite",
                "atividades": "Todas",
                "tributacao": "Simples, Presumido ou Real",
                "vantagens": [
                    "Sem limites de faturamento",
                    "Proteção patrimonial dos sócios",
                    "Credibilidade no mercado",
                    "Flexibilidade operacional"
                ],
                "ideal_para": "Empresas com múltiplos sócios e grande porte"
            }
        }

        # Documentos necessários
        self.required_docs = {
            "pessoa_fisica": [
                "RG e CPF",
                "Comprovante de residência",
                "Título de eleitor (se aplicável)",
                "Declaração de Imposto de Renda (últimos 2 anos)"
            ],
            "empresa": [
                "Contrato Social ou Requerimento de Empresário",
                "Comprovante de endereço comercial",
                "IPTU do imóvel",
                "Consulta de viabilidade aprovada",
                "FCN - Ficha de Cadastro Nacional"
            ],
            "especificos_atividade": {
                "alimentos": ["Alvará Sanitário", "Curso de manipulação de alimentos"],
                "saude": ["Registro no conselho profissional", "Responsável técnico"],
                "educacao": ["Autorização da Secretaria de Educação"],
                "comercio": ["Corpo de Bombeiros (se área > 200m²)"]
            }
        }

        # Etapas do processo
        self.process_steps = {
            "mei": [
                {
                    "ordem": 1,
                    "etapa": "Consulta de Viabilidade",
                    "descricao": "Verificar se a atividade pode ser exercida no endereço",
                    "prazo": "1-3 dias",
                    "orgao": "Prefeitura Municipal"
                },
                {
                    "ordem": 2,
                    "etapa": "Registro no Portal do Empreendedor",
                    "descricao": "Formalização online do MEI",
                    "prazo": "Imediato",
                    "orgao": "Receita Federal"
                },
                {
                    "ordem": 3,
                    "etapa": "Emissão do CCMEI",
                    "descricao": "Certificado da Condição de Microempreendedor Individual",
                    "prazo": "Imediato",
                    "orgao": "Portal do Empreendedor"
                },
                {
                    "ordem": 4,
                    "etapa": "Alvará de Funcionamento",
                    "descricao": "Licença municipal (se necessário)",
                    "prazo": "5-15 dias",
                    "orgao": "Prefeitura Municipal"
                }
            ],
            "ltda": [
                {
                    "ordem": 1,
                    "etapa": "Consulta de Viabilidade",
                    "descricao": "Verificar nome empresarial e localização",
                    "prazo": "1-3 dias",
                    "orgao": "Junta Comercial"
                },
                {
                    "ordem": 2,
                    "etapa": "Elaboração do Contrato Social",
                    "descricao": "Documento que rege a empresa",
                    "prazo": "2-5 dias",
                    "orgao": "Contador/Advogado"
                },
                {
                    "ordem": 3,
                    "etapa": "Registro na Junta Comercial",
                    "descricao": "Formalização da empresa",
                    "prazo": "5-10 dias",
                    "orgao": "Junta Comercial"
                },
                {
                    "ordem": 4,
                    "etapa": "Emissão do NIRE",
                    "descricao": "Número de Identificação do Registro de Empresa",
                    "prazo": "Imediato após registro",
                    "orgao": "Junta Comercial"
                },
                {
                    "ordem": 5,
                    "etapa": "Inscrição no CNPJ",
                    "descricao": "Registro federal",
                    "prazo": "1-3 dias",
                    "orgao": "Receita Federal"
                },
                {
                    "ordem": 6,
                    "etapa": "Inscrição Estadual",
                    "descricao": "Para empresas com circulação de mercadorias",
                    "prazo": "5-10 dias",
                    "orgao": "Secretaria da Fazenda Estadual"
                },
                {
                    "ordem": 7,
                    "etapa": "Inscrição Municipal",
                    "descricao": "Cadastro na prefeitura",
                    "prazo": "3-7 dias",
                    "orgao": "Prefeitura Municipal"
                },
                {
                    "ordem": 8,
                    "etapa": "Alvará de Funcionamento",
                    "descricao": "Licença para operar",
                    "prazo": "10-30 dias",
                    "orgao": "Prefeitura Municipal"
                }
            ]
        }

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do agente de legalização"""
        return """
        Como Agente de Legalização, você é especialista em:

        1. ORIENTAÇÃO SOBRE TIPOS DE EMPRESA:
           - Explicar diferenças entre MEI, ME, EPP, LTDA
           - Recomendar o melhor tipo baseado no negócio do cliente
           - Esclarecer vantagens e limitações de cada tipo

        2. PROCESSOS DE ABERTURA:
           - Detalhar todas as etapas necessárias
           - Informar prazos realistas
           - Listar documentação obrigatória

        3. REQUISITOS ESPECÍFICOS:
           - Identificar exigências por tipo de atividade
           - Informar sobre licenças especiais
           - Orientar sobre responsável técnico quando necessário

        4. REGULARIZAÇÃO:
           - Ajudar empresas já abertas a regularizar pendências
           - Orientar sobre renovações e atualizações cadastrais

        IMPORTANTE:
        - Seja claro e objetivo nas explicações
        - Use linguagem acessível, evite jargão excessivo
        - Sempre pergunte sobre a atividade do cliente para dar orientação precisa
        - Mencione que os prazos podem variar por município
        - Reforce que o escritório pode cuidar de todo o processo
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações sobre legalização

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        message_lower = message.lower()

        # Detectar tipo de consulta
        consulta_tipo = self._detect_query_type(message_lower)

        # Construir contexto específico
        specific_context = self._build_specific_context(consulta_tipo, message_lower)

        # Gerar resposta com IA
        response = await self.generate_response(
            message,
            context={**(context or {}), **specific_context},
            temperature=0.7
        )

        return {
            "agent": self.name,
            "response": response,
            "query_type": consulta_tipo,
            "context_used": specific_context
        }

    def _detect_query_type(self, message: str) -> str:
        """Detecta o tipo de consulta"""
        if any(word in message for word in ["abrir", "abertura", "criar", "montar", "começar"]):
            return "abertura_empresa"
        elif any(word in message for word in ["mei", "microempreendedor"]):
            return "mei"
        elif any(word in message for word in ["ltda", "limitada", "sociedade"]):
            return "ltda"
        elif any(word in message for word in ["documento", "documentação", "papeis"]):
            return "documentacao"
        elif any(word in message for word in ["quanto tempo", "prazo", "demora"]):
            return "prazos"
        elif any(word in message for word in ["etapa", "processo", "passo"]):
            return "processo"
        elif any(word in message for word in ["regularizar", "regularização", "pendência"]):
            return "regularizacao"
        else:
            return "geral"

    def _build_specific_context(self, query_type: str, message: str) -> Dict:
        """Constrói contexto específico baseado no tipo de consulta"""
        context = {}

        if query_type == "mei":
            context["tipo_empresa"] = self.company_types["mei"]
            context["etapas"] = self.process_steps["mei"]

        elif query_type == "ltda":
            context["tipo_empresa"] = self.company_types["ltda"]
            context["etapas"] = self.process_steps["ltda"]

        elif query_type == "abertura_empresa":
            # Incluir todos os tipos para comparação
            context["tipos_disponiveis"] = self.company_types

        elif query_type == "documentacao":
            context["documentos_pf"] = self.required_docs["pessoa_fisica"]
            context["documentos_empresa"] = self.required_docs["empresa"]

        elif query_type == "processo" or query_type == "prazos":
            # Detectar qual tipo específico
            if "mei" in message:
                context["etapas"] = self.process_steps["mei"]
            elif "ltda" in message or "limitada" in message:
                context["etapas"] = self.process_steps["ltda"]
            else:
                # Mostrar ambos para comparação
                context["etapas_mei"] = self.process_steps["mei"]
                context["etapas_ltda"] = self.process_steps["ltda"]

        return context

    def get_company_recommendation(self,
                                  faturamento_anual: float,
                                  num_funcionarios: int,
                                  atividade: str) -> Dict[str, Any]:
        """
        Recomenda tipo de empresa baseado em características

        Args:
            faturamento_anual: Faturamento anual esperado
            num_funcionarios: Número de funcionários
            atividade: Descrição da atividade

        Returns:
            Recomendação de tipo empresarial
        """
        recomendacoes = []

        # MEI
        if faturamento_anual <= 81000 and num_funcionarios <= 1:
            recomendacoes.append({
                "tipo": "MEI",
                "adequacao": "alta",
                "info": self.company_types["mei"]
            })

        # ME
        if faturamento_anual <= 360000:
            recomendacoes.append({
                "tipo": "ME",
                "adequacao": "alta" if num_funcionarios <= 9 else "media",
                "info": self.company_types["me"]
            })

        # EPP
        if faturamento_anual <= 4800000:
            recomendacoes.append({
                "tipo": "EPP",
                "adequacao": "alta" if num_funcionarios <= 49 else "media",
                "info": self.company_types["epp"]
            })

        # LTDA sempre é opção
        recomendacoes.append({
            "tipo": "LTDA",
            "adequacao": "alta" if faturamento_anual > 360000 else "media",
            "info": self.company_types["ltda"]
        })

        return {
            "recomendacoes": recomendacoes,
            "faturamento_informado": faturamento_anual,
            "funcionarios_informados": num_funcionarios,
            "atividade_informada": atividade
        }
