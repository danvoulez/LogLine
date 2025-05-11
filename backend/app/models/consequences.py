from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class LogEventConsequenceDetail(BaseModel):
    """Details of a log event consequence"""
    id: str = Field(..., description="Unique identifier for the consequence")
    event_id: str = Field(..., description="Log event ID this consequence relates to")
    consequence_type: str = Field(..., description="Type of consequence")
    status: str = Field(..., description="Current status of the consequence")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional details")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="When created")
    executed_at: Optional[datetime] = Field(None, description="When executed")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class TriggeredConsequenceData(BaseModel):
    """Data for a triggered consequence"""
    source_event_id: str = Field(..., description="ID of the source event")
    consequence_type: str = Field(..., description="Type of consequence")
    details: Dict[str, Any] = Field(default_factory=dict, description="Consequence details")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }
