from pydantic import (
    BaseSettings,
    AnyHttpUrl,
    Field,
    SecretStr,
    validator
)
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
    MONGO_URL: AnyHttpUrl = Field(
        ..., env="MONGO_URL",
        description="URI de conexão com MongoDB (mongodb:// ou mongodb+srv://)"
    )

    # — Redis (para cache, sessões e refresh tokens) —
    REDIS_URL: AnyHttpUrl = Field(
        "redis://localhost:6379",
        env="REDIS_URL",
        description="URI de conexão com Redis"
    )

    # — Open Policy Agent —
    OPA_URL: Optional[AnyHttpUrl] = Field(
        None, env="OPA_URL",
        description="Endpoint do OPA para políticas (quando enabled)"
    )
    OPA_ENABLED: bool = Field(
        False, env="OPA_ENABLED",
        description="Ativa validações OPA (false para desativado)"
    )

    # — Autenticação JWT —
    JWT_SECRET: SecretStr = Field(
        ..., env="JWT_SECRET",
        min_length=32,
        description="Chave secreta para assinatura de JWT (SecretStr para não expor)"
    )
    JWT_ALGORITHM: str = Field(
        "HS256", env="JWT_ALGORITHM",
        description="Algoritmo de assinatura JWT"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        60, env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="Tempo de expiração do access token (minutos)"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        7, env="REFRESH_TOKEN_EXPIRE_DAYS",
        description="Dias de expiração do refresh token"
    )

    # — CORS —
    BACKEND_CORS_ALLOW_ORIGINS: Optional[str] = Field(
        None, env="BACKEND_CORS_ALLOW_ORIGINS",
        description="Origens permitidas, separadas por vírgula"
    )
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default_factory=list,
        description="Origens permitidas para CORS"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

    @validator("MONGO_URL")
    def validate_mongo_scheme(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        txt = str(v)
        if not (txt.startswith("mongodb://") or txt.startswith("mongodb+srv://")):
            raise ValueError("MONGO_URL deve começar com mongodb:// ou mongodb+srv://")
        return v

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v, values):
        """
        Monta a lista de CORS a partir de uma string vírgula-separada se fornecida.
        """
        raw = values.get("BACKEND_CORS_ALLOW_ORIGINS")
        if raw and isinstance(raw, str):
            return [origin.strip() for origin in raw.split(",") if origin.strip()]
        return v

    @validator("JWT_SECRET")
    def check_jwt_secret_strength(cls, v: SecretStr) -> SecretStr:
        """
        Garante que o JWT_SECRET tenha pelo menos 32 caracteres.
        """
        if len(v.get_secret_value()) < 32:
            raise ValueError("JWT_SECRET deve ter ao menos 32 caracteres")
        return v


# Instância global
settings = Settings()