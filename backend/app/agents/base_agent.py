"""
LEGIA PLATFORM - Agente Base
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import google.generativeai as genai
from app.core.config import settings


class BaseAgent(ABC):
    """Classe base para todos os agentes"""

    def __init__(self, name: str, role: str):
        """
        Inicializa o agente

        Args:
            name: Nome do agente
            role: Papel/função do agente
        """
        self.name = name
        self.role = role
        self.model = None
        self._configure_gemini()

    def _configure_gemini(self):
        """Configura o modelo Gemini"""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            # Usando modelo Gemini 2.5 Flash (disponível na API v1beta)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            print(f"Erro ao configurar Gemini para {self.name}: {e}")
            self.model = None

    async def generate_response(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        temperature: float = 0.7
    ) -> str:
        """
        Gera uma resposta usando Gemini

        Args:
            prompt: Prompt para o modelo
            context: Contexto adicional
            temperature: Temperatura (0-1, quanto maior mais criativo)

        Returns:
            Resposta gerada
        """
        if not self.model:
            return "Desculpe, estou temporariamente indisponível. Por favor, tente novamente."

        try:
            # Adicionar contexto ao prompt se fornecido
            full_prompt = self._build_prompt(prompt, context)

            # Gerar resposta
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=2048,
                )
            )

            return response.text
        except Exception as e:
            print(f"Erro ao gerar resposta em {self.name}: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."

    def _build_prompt(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Constrói o prompt completo com contexto

        Args:
            prompt: Prompt base
            context: Contexto adicional

        Returns:
            Prompt completo
        """
        parts = [
            f"Você é {self.name}, um {self.role}.",
            f"\n{self.get_system_prompt()}\n",
        ]

        if context:
            parts.append("\nContexto:")
            for key, value in context.items():
                parts.append(f"- {key}: {value}")
            parts.append("\n")

        parts.append(f"\nSolicitação do usuário:\n{prompt}")

        return "".join(parts)

    @abstractmethod
    def get_system_prompt(self) -> str:
        """
        Retorna o system prompt específico do agente

        Returns:
            System prompt
        """
        pass

    @abstractmethod
    async def process(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa uma mensagem

        Args:
            message: Mensagem do usuário
            context: Contexto adicional

        Returns:
            Resposta estruturada do agente
        """
        pass

    def get_info(self) -> Dict[str, str]:
        """Retorna informações sobre o agente"""
        return {
            "name": self.name,
            "role": self.role,
            "status": "online" if self.model else "offline"
        }
