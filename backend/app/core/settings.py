from pydantic_settings import BaseSettings, Field, AnyHttpUrl, SecretStr, validator
from typing import List, Optional, Union

class Settings(BaseSettings):
    """
    Configurações essenciais para inicialização mínima do LogLine.
    """
    PROJECT_NAME: str = Field("LogLine", description="Nome do projeto")
    VERSION: str = Field("1.0.0", description="Versão da aplicação")
    API_V1_PREFIX: str = Field("/api/v1", description="Prefixo para todas as rotas")

    MONGO_URL: AnyHttpUrl = Field(..., env="MONGO_URL", description="URI de conexão MongoDB")
    REDIS_URL: AnyHttpUrl = Field("redis://localhost:6379", env="REDIS_URL", description="URI de conexão Redis")

    OPA_URL: Optional[AnyHttpUrl] = Field(None, env="OPA_URL", description="Endpoint do OPA")
    OPA_ENABLED: bool = Field(False, env="OPA_ENABLED", description="Ativa checagem OPA")

    JWT_SECRET: SecretStr = Field(..., env="JWT_SECRET", min_length=32, description="Chave secreta JWT")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM", description="Algoritmo JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES", description="Validade do Access Token em minutos")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS", description="Validade do Refresh Token em dias")

    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = Field(default_factory=list, env="BACKEND_CORS_ORIGINS", description="Origens permitidas (CORS)")

    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL", description="Nível de log (DEBUG, INFO, ...)")
    RELOAD: bool = Field(False, env="RELOAD", description="Uvicorn reload (dev)")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("MONGO_URL")
    def check_mongo_scheme(cls, v: AnyHttpUrl) -> AnyHttpUrl:
        txt = str(v)
        if not (txt.startswith("mongodb://") or txt.startswith("mongodb+srv://")):
            raise ValueError("MONGO_URL deve iniciar com mongodb:// ou mongodb+srv://")
        return v

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            # Permite lista separada por vírgula no .env ou string única
            origins = [i.strip() for i in v.split(",") if i.strip()]
            return origins
        return v

settings = Settings()
