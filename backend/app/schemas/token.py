from pydantic import BaseModel, Field


class Token(BaseModel):
    """
    Estrutura dos tokens JWT gerados no login/refresh.
    """
    access_token: str = Field(..., description="JWT de acesso")
    token_type: str = Field(..., description="Tipo de token, ex: bearer")
    refresh_token: str = Field(..., description="JWT de refresh armazenado no Redis")