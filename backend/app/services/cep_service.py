"""
LEGIA PLATFORM - Serviço de Consulta CEP
Consulta endereços via ViaCEP (API pública gratuita)
"""
import httpx
from typing import Optional, Dict, Any


class CEPService:
    """Serviço para consultar CEP via ViaCEP"""

    BASE_URL = "https://viacep.com.br/ws"

    @staticmethod
    async def consultar_cep(cep: str) -> Optional[Dict[str, Any]]:
        """
        Consulta endereço pelo CEP usando ViaCEP

        Args:
            cep: CEP (apenas números)

        Returns:
            Dict com dados do endereço ou None se não encontrado
        """
        # Limpar CEP (remover caracteres não numéricos)
        cep_limpo = ''.join(filter(str.isdigit, cep))

        if len(cep_limpo) != 8:
            raise ValueError("CEP deve conter 8 dígitos")

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{CEPService.BASE_URL}/{cep_limpo}/json/")

                if response.status_code == 200:
                    data = response.json()

                    # ViaCEP retorna erro como { "erro": true }
                    if data.get('erro'):
                        return None

                    # Formatar dados para nosso padrão
                    return {
                        'cep': data.get('cep'),
                        'logradouro': data.get('logradouro'),
                        'complemento': data.get('complemento'),
                        'bairro': data.get('bairro'),
                        'localidade': data.get('localidade'),  # cidade
                        'uf': data.get('uf'),
                        'ibge': data.get('ibge'),
                        'gia': data.get('gia'),
                        'ddd': data.get('ddd'),
                        'siafi': data.get('siafi'),
                        '_raw': data
                    }
                else:
                    return None

        except httpx.TimeoutException:
            raise Exception("Timeout ao consultar ViaCEP. Tente novamente.")
        except httpx.RequestError as e:
            raise Exception(f"Erro ao conectar com ViaCEP: {str(e)}")
        except Exception as e:
            raise Exception(f"Erro ao consultar CEP: {str(e)}")

    @staticmethod
    def formatar_cep(cep: str) -> str:
        """Formata CEP para exibição (XXXXX-XXX)"""
        cep_limpo = ''.join(filter(str.isdigit, cep))

        if len(cep_limpo) != 8:
            return cep

        return f"{cep_limpo[:5]}-{cep_limpo[5:]}"
