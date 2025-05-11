from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class ActionResponseAPI(BaseModel):
    """API response model for actions"""
    success: bool = Field(..., description="Whether the action was successful")
    message: str = Field(..., description="Message describing the action result")
    data: Optional[Dict[str, Any]] = Field(None, description="Optional data returned by the action")
    log_event_id: Optional[str] = Field(None, description="ID of any log event created by this action")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class LogEvent(BaseModel):
    """Base LogEvent model"""
    id: str = Field(..., description="Unique identifier for the log event")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the event occurred")
    event_type: str = Field(..., description="Type of log event")
    user_id: str = Field(..., description="User who created the event")
    details: Dict[str, Any] = Field(default_factory=dict, description="Event specific details")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class AcionarLogEventActionAPIPayload(BaseModel):
    """Payload for triggering a log event action"""
    target_log_id: str = Field(..., description="ID of the log event to trigger action on")
    action_type: str = Field(..., description="Type of action to perform")
    details: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional details for the action")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class LogAcionadoData(BaseModel):
    """Data for an activated log"""
    target_log_id: str = Field(..., description="ID of the target log")
    status: str = Field(..., description="Status of the activated log")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")

class CurrentStateOrderStatus(BaseModel):
    """Current state of an order"""
    status: str = Field(..., description="Current status")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="When last updated")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional status details")

class LogAcionamentoInfo(BaseModel):
    """Information about a log activation"""
    log_id: str = Field(..., description="ID of the log")
    activated_by: str = Field(..., description="User who activated the log")
    activated_at: datetime = Field(default_factory=datetime.utcnow, description="When activated")
    status: str = Field(..., description="Activation status")
