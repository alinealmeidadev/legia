"""
LEGIA PLATFORM - Serviço de Consulta Receita Federal
Consulta dados de CNPJ via ReceitaWS (API pública)
"""
import httpx
from typing import Optional, Dict, Any


class ReceitaService:
    """Serviço para consultar dados da Receita Federal"""

    BASE_URL = "https://www.receitaws.com.br/v1/cnpj"

    @staticmethod
    async def consultar_cnpj(cnpj: str) -> Optional[Dict[str, Any]]:
        """
        Consulta dados do CNPJ na ReceitaWS

        Args:
            cnpj: CNPJ (apenas números)

        Returns:
            Dict com dados da empresa ou None se não encontrado
        """
        # Limpar CNPJ (remover caracteres não numéricos)
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj_limpo) != 14:
            raise ValueError("CNPJ deve conter 14 dígitos")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{ReceitaService.BASE_URL}/{cnpj_limpo}")

                if response.status_code == 200:
                    data = response.json()

                    # Verificar se retornou erro da API
                    if data.get('status') == 'ERROR':
                        return None

                    # Formatar dados para nosso padrão
                    return {
                        'cnpj': data.get('cnpj'),
                        'razao_social': data.get('nome'),
                        'nome_fantasia': data.get('fantasia'),
                        'situacao': data.get('situacao'),
                        'data_abertura': data.get('abertura'),
                        'tipo': data.get('tipo'),
                        'porte': data.get('porte'),
                        'natureza_juridica': data.get('natureza_juridica'),
                        'capital_social': data.get('capital_social'),

                        # Endereço
                        'logradouro': data.get('logradouro'),
                        'numero': data.get('numero'),
                        'complemento': data.get('complemento'),
                        'bairro': data.get('bairro'),
                        'municipio': data.get('municipio'),
                        'uf': data.get('uf'),
                        'cep': data.get('cep'),

                        # Contato
                        'telefone': data.get('telefone'),
                        'email': data.get('email'),

                        # Atividades
                        'atividade_principal': data.get('atividade_principal'),
                        'atividades_secundarias': data.get('atividades_secundarias'),

                        # Sócios/QSA
                        'qsa': data.get('qsa', []),

                        # Dados brutos completos
                        '_raw': data
                    }

                elif response.status_code == 429:
                    # Rate limit
                    raise Exception("Limite de consultas excedido. Tente novamente em alguns minutos.")
                else:
                    return None

        except httpx.TimeoutException:
            raise Exception("Timeout ao consultar ReceitaWS. Tente novamente.")
        except httpx.RequestError as e:
            raise Exception(f"Erro ao conectar com ReceitaWS: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao consultar CNPJ: {str(e)}")

    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formata CNPJ para exibição (XX.XXX.XXX/XXXX-XX)"""
        cnpj_limpo = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj_limpo) != 14:
            return cnpj

        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
