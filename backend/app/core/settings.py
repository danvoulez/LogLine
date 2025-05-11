from typing import Any, List, Union, Optional
import pathlib # Add this import

from pydantic_settings import BaseSettings, SettingsConfigDict # Updated import for Pydantic v2+
from pydantic import field_validator, Field, AnyHttpUrl, SecretStr
from pydantic.networks import MongoDsn, RedisDsn # Added for specific DSN validation

from typing import List, Optional


class Settings(BaseSettings):
    """
    Configurações centrais da aplicação, carregadas de .env ou do ambiente.
    """

    # — App Info —
    PROJECT_NAME: str = Field("LogLine", description="Nome do projeto")
    VERSION: str = Field("1.0.0", description="Versão da aplicação")
    API_V1_PREFIX: str = Field("/api/v1", description="Prefixo para todas as rotas da API")

    # — Logging & Runtime —
    LOG_LEVEL: str = Field("INFO", description="Nível de log padrão")
    RELOAD: bool = Field(False, description="Active reload (dev)")

    # — MongoDB —
    MONGO_URI: Optional[MongoDsn] = Field( # Renamed from MONGO_URL
        default=None,
        description="URI de conexão com MongoDB (mongodb:// ou mongodb+srv://)"
    )

    # — Redis (para cache, sessões e refresh tokens) —
    REDIS_URL: RedisDsn = Field(
        default="redis://localhost:6379", # Default is a valid RedisDsn
        description="URI de conexão com Redis" # pydantic-settings will look for REDIS_URL env var
    )

    # — Open Policy Agent —
    OPA_URL: Optional[AnyHttpUrl] = Field(
        default=None, # Explicitly set default
        description="Endpoint do OPA para políticas (quando enabled)" # pydantic-settings will look for OPA_URL
    )
    OPA_ENABLED: bool = Field(
        default=False, # Explicitly set default
        description="Ativa validações OPA (false para desativado)" # pydantic-settings will look for OPA_ENABLED
    )

    # — Autenticação JWT —
    JWT_SECRET_KEY: Optional[SecretStr] = Field( # Renamed from JWT_SECRET
        default=None,
        min_length=32,
        description="Chave secreta para assinatura de JWT (SecretStr para não expor)"
    )
    JWT_ALGORITHM: str = Field(
        default="HS256", # Explicitly set default
        description="Algoritmo de assinatura JWT" # pydantic-settings will look for JWT_ALGORITHM
    )
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field( # Renamed from ACCESS_TOKEN_EXPIRE_MINUTES
        default=60,
        description="Tempo de expiração do access token (minutos)"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7, # Explicitly set default
        description="Dias de expiração do refresh token" # pydantic-settings will look for REFRESH_TOKEN_EXPIRE_DAYS
    )

    # — CORS —
    BACKEND_CORS_ALLOW_ORIGINS: Optional[str] = Field(
        default=None, # Explicitly set default
        description="Origens permitidas, separadas por vírgula" # pydantic-settings will look for BACKEND_CORS_ALLOW_ORIGINS
    )
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default_factory=list,
        description="Origens permitidas para CORS"
    )

    # Added based on .env extra fields error
    LLM_PROVIDER: Optional[str] = Field(default=None, description="Provider for LLM service") # pydantic-settings will look for LLM_PROVIDER

    model_config = SettingsConfigDict(
        env_file=pathlib.Path(__file__).resolve().parent.parent.parent / ".env", # Corrected path to backend/.env
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore' # Ignore any other environment variables not defined in this model
    )

    # Pydantic v2+ uses field_validator instead of validator
    # Removed assemble_db_connection validator as MongoDsn will handle validation

    # Pydantic v2+ uses field_validator instead of validator
    @field_validator("BACKEND_CORS_ORIGINS", mode="before") # mode="before" keeps the pre=True behavior
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (List, str)):
            return v
        raise ValueError(v)

    # Removed assemble_jwt_secret validator as SecretStr will handle validation and it's optional


# Instância global
settings = Settings()