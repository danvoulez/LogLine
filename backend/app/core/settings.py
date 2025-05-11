# backend/app/core/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field, AnyUrl, SecretStr, validator
from typing import List, Optional


class Settings(BaseSettings):
    """
    Configurações essenciais para inicialização mínima do LogLine.
    Aceita vários nomes de variáveis de ambiente conforme seu .env:
      - MONGO_URL ou MONGO_URI
      - JWT_SECRET ou JWT_SECRET_KEY
      - ACCESS_TOKEN_EXPIRE_MINUTES ou JWT_ACCESS_TOKEN_EXPIRE_MINUTES
      - LLM_PROVIDER ou llm_provider
    Usa AnyUrl para Redis e Mongo (aceita redis://, mongodb:// e mongodb+srv://).
    """

    PROJECT_NAME: str = Field("LogLine", description="Nome do projeto")
    VERSION: str = Field("1.0.0", description="Versão da aplicação")
    API_V1_PREFIX: str = Field("/api/v1", description="Prefixo para todas as rotas")

    MONGO_URL: AnyUrl = Field(
        ..., 
        env=["MONGO_URL", "MONGO_URI"],
        description="URI de conexão com MongoDB (mongodb:// ou mongodb+srv://)"
    )
    REDIS_URL: AnyUrl = Field(
        "redis://localhost:6379",
        env="REDIS_URL",
        description="URI de conexão com Redis (redis://)"
    )

    OPA_URL: Optional[AnyUrl] = Field(
        None,
        env="OPA_URL",
        description="Endpoint do Open Policy Agent"
    )
    OPA_ENABLED: bool = Field(
        False,
        env="OPA_ENABLED",
        description="Ativa checagem de políticas via OPA"
    )

    JWT_SECRET: SecretStr = Field(
        ...,
        env=["JWT_SECRET", "JWT_SECRET_KEY"],
        min_length=32,
        description="Chave secreta para assinatura de JWT"
    )
    JWT_ALGORITHM: str = Field(
        "HS256",
        env="JWT_ALGORITHM",
        description="Algoritmo de assinatura JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60,
        env=["ACCESS_TOKEN_EXPIRE_MINUTES", "JWT_ACCESS_TOKEN_EXPIRE_MINUTES"],
        description="Tempo de expiração do access token em minutos"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7,
        env="REFRESH_TOKEN_EXPIRE_DAYS",
        description="Tempo de expiração do refresh token em dias"
    )

    LLM_PROVIDER: str = Field(
        "mock",
        env=["LLM_PROVIDER", "llm_provider"],
        description="Provider para serviço LLM (mock, openai, etc.)"
    )

    BACKEND_CORS_ORIGINS: List[str] = Field(
        default_factory=list,
        env="BACKEND_CORS_ORIGINS",
        description="Origens permitidas para CORS (comma-separated)"
    )

    LOG_LEVEL: str = Field(
        "INFO",
        env="LOG_LEVEL",
        description="Nível de log (DEBUG, INFO, WARNING, ERROR)"
    )
    RELOAD: bool = Field(
        False,
        env="RELOAD",
        description="Habilita hot-reload no Uvicorn (dev)"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("MONGO_URL")
    def validate_mongo_scheme(cls, v: AnyUrl) -> AnyUrl:
        scheme = v.scheme.lower()
        if scheme not in ("mongodb", "mongodb+srv"):
            raise ValueError("MONGO_URL deve usar esquema mongodb:// ou mongodb+srv://")
        return v

settings = Settings()

    OPA_URL: Optional[AnyHttpUrl] = Field(None, env="OPA_URL", description="Endpoint do OPA")
    OPA_ENABLED: bool = Field(False, env="OPA_ENABLED", description="Ativa checagem OPA")

    JWT_SECRET: SecretStr = Field(..., env="JWT_SECRET", min_length=32, description="Chave secreta JWT")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM", description="Algoritmo JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES", description="Validade do Access Token em minutos")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS", description="Validade do Refresh Token em dias")

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list, env="BACKEND_CORS_ORIGINS", description="Origens permitidas (CORS)")

    # Logging e reload
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL", description="Nível de log (DEBUG, INFO, ...)")
    RELOAD: bool = Field(False, env="RELOAD", description="Habilita reload no Uvicorn (dev)")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("MONGO_URL")
    def check_mongo_scheme(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        txt = str(v)
        if not (txt.startswith("mongodb://") or txt.startswith("mongodb+srv://")):
            raise ValueError("MONGO_URL deve iniciar com mongodb:// ou mongodb+srv://")
        return v

# Instância global de Settings
settings = Settings()
