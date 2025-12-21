"""
LEGIA PLATFORM - Configurações da Aplicação
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Configurações da aplicação"""

    # Application
    PROJECT_NAME: str = "LEGIA PLATFORM"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Google Gemini
    GEMINI_API_KEY: str

    # Asaas Payment Gateway
    ASAAS_API_KEY: str
    ASAAS_SANDBOX: bool = True
    ASAAS_BASE_URL: str = "https://sandbox.asaas.com/api/v3"

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000,https://legia-git-main-aline-almeidas-projects.vercel.app,https://legia-aline-almeidas-projects.vercel.app,https://legia.vercel.app,https://*.vercel.app,https://legia-backend.onrender.com"

    @property
    def cors_origins_list(self) -> List[str]:
        """Retorna CORS_ORIGINS como lista"""
        origins = []
        if isinstance(self.CORS_ORIGINS, str):
            origins = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        elif isinstance(self.CORS_ORIGINS, list):
            origins = self.CORS_ORIGINS

        # Adicionar origens padrão do Vercel se não estiverem presentes
        vercel_origins = [
            "https://legia-git-main-aline-almeidas-projects.vercel.app",
            "https://legia-aline-almeidas-projects.vercel.app",
            "https://legia.vercel.app"
        ]
        for origin in vercel_origins:
            if origin not in origins:
                origins.append(origin)

        return origins

    # Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "./uploads"

    # Timezone
    TZ: str = "America/Sao_Paulo"

    # Superadmin padrão (primeiro acesso)
    FIRST_SUPERUSER_EMAIL: str = "admin@legia.com.br"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"  # Mudar no primeiro login!
    FIRST_SUPERUSER_NAME: str = "Admin Legia"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de configurações
settings = Settings()
