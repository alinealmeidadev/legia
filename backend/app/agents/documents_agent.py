"""
LEGIA PLATFORM - Agente Organizador de Documentos
Especialista em gestão documental completa
"""
from typing import Dict, Optional, Any, List
from .base_agent import BaseAgent
from datetime import datetime, timedelta
import os
from pathlib import Path


class DocumentsAgent(BaseAgent):
    """
    Agente Organizador de Documentos - Gestão documental completa

    Responsabilidades:
    - Criar estrutura de pastas padronizada
    - Indexar e catalogar documentos
    - Busca avançada de documentos
    - Controle de versões
    - Alertas de vencimentos
    - Relatórios gerenciais
    """

    def __init__(self):
        super().__init__(
            name="Organizador de Documentos",
            role="especialista em gestão e organização documental"
        )

        # Estrutura de pastas padrão
        self.folder_structure = {
            "societario": {
                "nome": "Societário",
                "subpastas": [
                    "contratos_sociais",
                    "alteracoes_contratuais",
                    "atas",
                    "certidoes_societarias",
                    "procuracoes"
                ],
                "tipos_arquivo": ["pdf", "docx", "jpg", "png"]
            },
            "tributario": {
                "nome": "Tributário",
                "subpastas": [
                    "cnpj",
                    "inscricoes",
                    "certidoes_negativas",
                    "parcelamentos",
                    "declaracoes"
                ],
                "tipos_arquivo": ["pdf", "xml", "txt"]
            },
            "licencas": {
                "nome": "Licenças e Alvarás",
                "subpastas": [
                    "alvara_funcionamento",
                    "licenca_sanitaria",
                    "corpo_bombeiros",
                    "meio_ambiente",
                    "outras_licencas"
                ],
                "tipos_arquivo": ["pdf", "jpg", "png"]
            },
            "contratos": {
                "nome": "Contratos Comerciais",
                "subpastas": [
                    "prestacao_servicos",
                    "compra_venda",
                    "locacao",
                    "fornecedores",
                    "outros"
                ],
                "tipos_arquivo": ["pdf", "docx"]
            },
            "processos": {
                "nome": "Processos por Órgão",
                "subpastas": [
                    "junta_comercial",
                    "receita_federal",
                    "prefeitura",
                    "secretaria_fazenda",
                    "outros_orgaos"
                ],
                "tipos_arquivo": ["pdf", "xml", "jpg", "png"]
            },
            "comunicacoes": {
                "nome": "Comunicações Oficiais",
                "subpastas": [
                    "oficios_enviados",
                    "oficios_recebidos",
                    "requerimentos",
                    "respostas_exigencias",
                    "notificacoes"
                ],
                "tipos_arquivo": ["pdf", "docx"]
            },
            "diversos": {
                "nome": "Diversos",
                "subpastas": [
                    "procuracoes",
                    "documentos_socios",
                    "comprovantes_endereco",
                    "outros"
                ],
                "tipos_arquivo": ["pdf", "jpg", "png", "docx"]
            }
        }

        # Tipos de documentos com vencimento
        self.docs_com_vencimento = {
            "certidao_negativa_federal": {"validade_dias": 180, "categoria": "tributario"},
            "certidao_negativa_estadual": {"validade_dias": 180, "categoria": "tributario"},
            "certidao_negativa_municipal": {"validade_dias": 180, "categoria": "tributario"},
            "certidao_negativa_trabalhista": {"validade_dias": 180, "categoria": "tributario"},
            "certidao_negativa_fgts": {"validade_dias": 180, "categoria": "tributario"},
            "alvara_funcionamento": {"validade_dias": 365, "categoria": "licencas"},
            "licenca_sanitaria": {"validade_dias": 365, "categoria": "licencas"},
            "avcb": {"validade_dias": 365, "categoria": "licencas"},  # Auto Vistoria Corpo Bombeiros
            "licenca_ambiental": {"validade_dias": 730, "categoria": "licencas"},
        }

        # Metadados padrão para indexação
        self.metadata_fields = [
            "tipo_documento",
            "categoria",
            "subcategoria",
            "data_emissao",
            "data_vencimento",
            "numero_documento",
            "orgao_emissor",
            "empresa_cnpj",
            "tags",
            "observacoes"
        ]

    def get_system_prompt(self) -> str:
        """Retorna o system prompt do organizador de documentos"""
        return """
        Como Organizador de Documentos, você é especialista em:

        1. ORGANIZAÇÃO:
           - Estrutura de pastas padronizada
           - Nomenclatura consistente
           - Categorização correta
           - Arquivamento lógico

        2. INDEXAÇÃO:
           - Extração de metadados
           - Catalogação completa
           - Tags e palavras-chave
           - Relacionamento entre documentos

        3. BUSCA:
           - Busca por múltiplos critérios
           - Filtros avançados
           - Busca por conteúdo (OCR)
           - Sugestões inteligentes

        4. CONTROLE:
           - Versionamento de documentos
           - Histórico de alterações
           - Controle de acesso
           - Auditoria completa

        5. ALERTAS:
           - Vencimentos próximos
           - Documentos pendentes
           - Renovações necessárias
           - Relatórios automáticos

        IMPORTANTE:
        - Mantenha organização consistente
        - Indexe todos metadados
        - Alerte proativamente
        - Facilite busca e recuperação
        """

    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa solicitações de gestão documental

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada
        """
        message_lower = message.lower()

        # Detectar tipo de operação
        operation = self._detect_operation(message_lower)

        # Gerar resposta
        response = await self.generate_response(
            message,
            context={
                **(context or {}),
                "operation": operation,
                "folder_structure": list(self.folder_structure.keys())
            },
            temperature=0.5
        )

        return {
            "agent": self.name,
            "response": response,
            "operation": operation,
            "folder_structure": self.folder_structure
        }

    def _detect_operation(self, message: str) -> str:
        """Detecta tipo de operação"""
        if any(word in message for word in ["buscar", "procurar", "encontrar", "onde está"]):
            return "search"
        elif any(word in message for word in ["organizar", "arquivar", "salvar"]):
            return "organize"
        elif any(word in message for word in ["vencimento", "vence", "validade"]):
            return "expiry_check"
        elif any(word in message for word in ["versão", "versao", "histórico", "historico"]):
            return "version_control"
        elif any(word in message for word in ["relatório", "relatorio", "listar"]):
            return "report"
        else:
            return "general"

    def criar_estrutura_pastas(self, base_path: str, client_cnpj: str) -> Dict[str, Any]:
        """
        Cria estrutura de pastas para cliente

        Args:
            base_path: Caminho base
            client_cnpj: CNPJ do cliente

        Returns:
            Estrutura criada
        """
        client_folder = os.path.join(base_path, f"cliente_{client_cnpj}")
        created_folders = []

        try:
            # Criar pasta raiz do cliente
            os.makedirs(client_folder, exist_ok=True)
            created_folders.append(client_folder)

            # Criar estrutura de pastas
            for category_key, category_info in self.folder_structure.items():
                category_path = os.path.join(client_folder, category_key)
                os.makedirs(category_path, exist_ok=True)
                created_folders.append(category_path)

                # Criar subpastas
                for subfolder in category_info["subpastas"]:
                    subfolder_path = os.path.join(category_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
                    created_folders.append(subfolder_path)

            return {
                "success": True,
                "client_cnpj": client_cnpj,
                "root_path": client_folder,
                "folders_created": len(created_folders),
                "structure": created_folders
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "folders_created": len(created_folders)
            }

    def sugerir_localizacao(
        self,
        tipo_documento: str,
        metadados: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Sugere localização para documento

        Args:
            tipo_documento: Tipo do documento
            metadados: Metadados adicionais

        Returns:
            Sugestão de localização
        """
        tipo_lower = tipo_documento.lower()

        # Mapeamento de palavras-chave para categorias
        mappings = {
            "contrato social": ("societario", "contratos_sociais"),
            "alteração contratual": ("societario", "alteracoes_contratuais"),
            "ata": ("societario", "atas"),
            "cnpj": ("tributario", "cnpj"),
            "certidão": ("tributario", "certidoes_negativas"),
            "alvará": ("licencas", "alvara_funcionamento"),
            "licença": ("licencas", "outras_licencas"),
            "ofício": ("comunicacoes", "oficios_enviados"),
            "requerimento": ("comunicacoes", "requerimentos"),
            "procuração": ("diversos", "procuracoes"),
            "rg": ("diversos", "documentos_socios"),
            "cpf": ("diversos", "documentos_socios"),
            "comprovante": ("diversos", "comprovantes_endereco")
        }

        # Buscar correspondência
        for keyword, (category, subfolder) in mappings.items():
            if keyword in tipo_lower:
                return {
                    "categoria": category,
                    "subcategoria": subfolder,
                    "caminho_sugerido": f"{category}/{subfolder}",
                    "confidence": 0.9,
                    "categoria_nome": self.folder_structure[category]["nome"]
                }

        # Se não encontrou, sugerir "diversos"
        return {
            "categoria": "diversos",
            "subcategoria": "outros",
            "caminho_sugerido": "diversos/outros",
            "confidence": 0.5,
            "categoria_nome": "Diversos"
        }

    def indexar_documento(
        self,
        file_path: str,
        metadata: Dict[str, Any],
        client_cnpj: str
    ) -> Dict[str, Any]:
        """
        Indexa documento no sistema

        Args:
            file_path: Caminho do arquivo
            metadata: Metadados do documento
            client_cnpj: CNPJ do cliente

        Returns:
            Resultado da indexação
        """
        # Em produção, salvar no banco de dados
        documento_indexado = {
            "id": self._gerar_id_documento(),
            "client_cnpj": client_cnpj,
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "file_size": self._get_file_size(file_path),
            "file_extension": Path(file_path).suffix.lower(),
            "metadata": metadata,
            "indexed_at": datetime.now().isoformat(),
            "version": 1,
            "status": "active"
        }

        return {
            "success": True,
            "document": documento_indexado,
            "message": "Documento indexado com sucesso"
        }

    def buscar_documentos(
        self,
        client_cnpj: str,
        criterios: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Busca documentos por critérios

        Args:
            client_cnpj: CNPJ do cliente
            criterios: Critérios de busca

        Returns:
            Documentos encontrados
        """
        # Em produção, buscar no banco de dados
        # Simulação de busca
        resultados = []

        # Critérios possíveis:
        # - tipo_documento
        # - categoria
        # - data_inicio, data_fim
        # - texto (busca full-text)
        # - tags
        # - orgao_emissor

        return {
            "success": True,
            "total_results": len(resultados),
            "criterios_usados": criterios,
            "documentos": resultados,
            "query_time_ms": 45
        }

    def verificar_vencimentos(
        self,
        client_cnpj: str,
        dias_antecedencia: int = 30
    ) -> Dict[str, Any]:
        """
        Verifica documentos vencendo

        Args:
            client_cnpj: CNPJ do cliente
            dias_antecedencia: Dias de antecedência para alertar

        Returns:
            Documentos vencendo
        """
        data_limite = datetime.now() + timedelta(days=dias_antecedencia)

        # Em produção, buscar no banco
        # Simulação de vencimentos
        vencimentos = {
            "vencidos": [],
            "vencendo_7_dias": [],
            "vencendo_15_dias": [],
            "vencendo_30_dias": []
        }

        return {
            "success": True,
            "client_cnpj": client_cnpj,
            "data_verificacao": datetime.now().isoformat(),
            "dias_antecedencia": dias_antecedencia,
            "vencimentos": vencimentos,
            "total_alertas": sum(len(v) for v in vencimentos.values())
        }

    def calcular_data_vencimento(
        self,
        tipo_documento: str,
        data_emissao: datetime
    ) -> Optional[datetime]:
        """
        Calcula data de vencimento baseado no tipo

        Args:
            tipo_documento: Tipo do documento
            data_emissao: Data de emissão

        Returns:
            Data de vencimento ou None
        """
        doc_info = self.docs_com_vencimento.get(tipo_documento.lower())

        if doc_info:
            validade_dias = doc_info["validade_dias"]
            return data_emissao + timedelta(days=validade_dias)

        return None

    def versionar_documento(
        self,
        document_id: str,
        new_file_path: str,
        change_description: str,
        changed_by: str
    ) -> Dict[str, Any]:
        """
        Cria nova versão de documento

        Args:
            document_id: ID do documento original
            new_file_path: Caminho do novo arquivo
            change_description: Descrição da mudança
            changed_by: Quem fez a mudança

        Returns:
            Nova versão criada
        """
        # Em produção, buscar versão atual do banco
        current_version = 1  # Simular

        new_version = {
            "document_id": document_id,
            "version": current_version + 1,
            "file_path": new_file_path,
            "change_description": change_description,
            "changed_by": changed_by,
            "changed_at": datetime.now().isoformat(),
            "previous_version": current_version
        }

        return {
            "success": True,
            "new_version": new_version,
            "message": f"Versão {new_version['version']} criada com sucesso"
        }

    def gerar_relatorio_documental(
        self,
        client_cnpj: str,
        periodo_inicio: Optional[datetime] = None,
        periodo_fim: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Gera relatório de documentos

        Args:
            client_cnpj: CNPJ do cliente
            periodo_inicio: Data início
            periodo_fim: Data fim

        Returns:
            Relatório completo
        """
        # Em produção, buscar do banco
        relatorio = {
            "client_cnpj": client_cnpj,
            "periodo": {
                "inicio": periodo_inicio.isoformat() if periodo_inicio else None,
                "fim": periodo_fim.isoformat() if periodo_fim else None
            },
            "estatisticas": {
                "total_documentos": 0,
                "por_categoria": {},
                "documentos_vencidos": 0,
                "documentos_vencendo": 0,
                "ultimos_30_dias": 0
            },
            "documentos_criticos": [],
            "recomendacoes": []
        }

        return {
            "success": True,
            "relatorio": relatorio,
            "gerado_em": datetime.now().isoformat()
        }

    def _gerar_id_documento(self) -> str:
        """Gera ID único para documento"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        return f"DOC-{timestamp}"

    def _get_file_size(self, file_path: str) -> int:
        """Retorna tamanho do arquivo em bytes"""
        try:
            return os.path.getsize(file_path)
        except:
            return 0

    def get_folder_structure_info(self) -> Dict[str, Any]:
        """
        Retorna informações da estrutura de pastas

        Returns:
            Estrutura completa
        """
        structure_info = {}

        for key, category in self.folder_structure.items():
            structure_info[key] = {
                "nome": category["nome"],
                "total_subpastas": len(category["subpastas"]),
                "subpastas": category["subpastas"],
                "tipos_suportados": category["tipos_arquivo"]
            }

        return structure_info

    def validar_tipo_arquivo(
        self,
        file_extension: str,
        categoria: str
    ) -> bool:
        """
        Valida se tipo de arquivo é permitido na categoria

        Args:
            file_extension: Extensão do arquivo (ex: 'pdf')
            categoria: Categoria destino

        Returns:
            True se permitido
        """
        category_info = self.folder_structure.get(categoria)

        if not category_info:
            return False

        return file_extension.lower() in category_info["tipos_arquivo"]
