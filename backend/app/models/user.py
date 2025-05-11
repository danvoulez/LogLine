from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, Any


class UserInDB(BaseModel):
    """
    Representa a estrutura de um usuário armazenado no MongoDB.
    """
    id: str = Field(..., alias="_id", description="ID interno do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")
    hashed_password: str = Field(..., description="Senha criptografada (bcrypt)")
    is_active: bool = Field(True, description="Flag de usuário ativo")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Quando foi criado")
    last_login: Optional[datetime] = Field(None, description="Último login efetuado")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}


class LogEventInDB(BaseModel):
    """
    Representa um evento de log armazenado no MongoDB.
    """
    id: str = Field(..., alias="_id", description="ID interno do evento")
    user_id: str = Field(..., description="ID do usuário que gerou o evento")
    action: str = Field(..., description="Nome da ação executada")
    details: Dict[str, Any] = Field(default_factory=dict, description="Dados adicionais livres")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Data/hora do evento")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}