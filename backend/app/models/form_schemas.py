from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class LLMFormSchema(BaseModel):
    """Schema for LLM form definition"""
    id: str = Field(..., description="Unique identifier for the form")
    title: str = Field(..., description="Form title")
    description: str = Field(..., description="Form description")
    fields: List["LLMFormSchemaField"] = Field(..., description="Form fields")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class LLMFormSchemaField(BaseModel):
    """Schema for a field in an LLM form"""
    id: str = Field(..., description="Field identifier")
    type: str = Field(..., description="Field type")
    label: str = Field(..., description="Field label")
    required: bool = Field(default=True, description="Whether the field is required")
    options: Optional[List[Dict[str, Any]]] = Field(None, description="Options for select/radio fields")
    placeholder: Optional[str] = Field(None, description="Placeholder text")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class RegistrarVendaData(BaseModel):
    """Data for registering a sale"""
    customer_id: str = Field(..., description="Customer identifier")
    items: List["ItemVendaData"] = Field(..., description="Items in the sale")
    channel: str = Field(..., description="Sales channel")
    notes: Optional[str] = Field(None, description="Additional notes")
    client_order_ref: Optional[str] = Field(None, description="Client order reference")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class ItemVendaData(BaseModel):
    """Data for an item in a sale"""
    product_id: str = Field(..., description="Product identifier")
    quantity: int = Field(..., description="Quantity sold")
    price_per_unit_str: str = Field(..., description="Price per unit as string")
    name: str = Field(..., description="Product name")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class GatewayResponseAPI(BaseModel):
    """API response model from the gateway"""
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

class LLMInterpretationResponse(BaseModel):
    """Response from LLM interpretation"""
    intent: str = Field(..., description="Detected intent")
    entities: Dict[str, Any] = Field(default_factory=dict, description="Extracted entities")
    confidence: float = Field(..., description="Confidence score")
    
    model_config = {
        "json_encoders": {datetime: lambda dt: dt.isoformat()}
    }

# Make the circular reference work
LLMFormSchema.model_rebuild()
