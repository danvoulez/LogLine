from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    """
    Propriedades comuns entre criação e retorno de usuário.
    """
    email: EmailStr = Field(..., description="E-mail do usuário")


class UserCreate(UserBase):
    """
    Payload para registro de novo usuário.
    """
    password: str = Field(..., min_length=8, description="Senha com ao menos 8 caracteres")


class UserOut(UserBase):
    """
    DTO de usuário retornado pela API.
    """
    id: str = Field(..., description="ID único do usuário")
    is_active: bool = Field(..., description="Se o usuário está ativo")
    created_at: datetime = Field(..., description="Timestamp de criação")

    model_config = {
        "from_attributes": True,  # replaces orm_mode
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }