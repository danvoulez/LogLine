from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any, Literal, List

class LogEventBase(BaseModel):
    """Estrutura mínima para representar eventos institucionais (LogLine)."""
    who: str = Field(..., description="Autor da ação (ID ou e-mail)")
    did: str = Field(..., description="Tipo de ação executada (ex: confirm_delivery)")
    this: Dict[str, Any] = Field(..., description="Entidade ou objeto alvo da ação")
    when: datetime = Field(default_factory=datetime.utcnow, description="Timestamp da criação")
    confirm_by: Optional[str] = Field(None, description="Responsável pela confirmação do evento")
    if_ok: Optional[str] = Field(None, description="Consequência se for confirmado")
    if_doubt: Optional[str] = Field(None, description="Condição se houver dúvida")
    if_denied: Optional[str] = Field(None, description="Consequência se for negado")
    status: Literal["pending", "confirmed", "denied"] = Field(default="pending", description="Estado atual")
    dispatch: Optional[str] = Field(None, description="Destino de encaminhamento automático (serviço, módulo, etc.)")
    tags: Optional[List[str]] = Field(default_factory=list, description="Tags de auditoria semântica")
    meta: Dict[str, Any] = Field(default_factory=dict, description="Dados adicionais opcionais (não institucionais)")

class LogEventCreate(LogEventBase):
    """Payload de criação. Mesmo formato que LogEventBase."""

class LogEventOut(LogEventBase):
    """Resposta ao registrar ou recuperar um log event."""
    id: str = Field(..., description="ID único do evento")
    user_id: str = Field(..., description="ID interno do autor")
    
    model_config = {
        "from_attributes": True,  # replaces orm_mode
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }