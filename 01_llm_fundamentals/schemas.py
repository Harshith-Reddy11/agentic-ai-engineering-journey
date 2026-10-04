from typing import Optional, Any
from pydantic import BaseModel, ConfigDict


class RequestClassification(BaseModel):
    intent: str
    operation: Optional[str] = None
    number1: Optional[float] = None
    number2: Optional[float] = None
    topic: Optional[str] = None
    action: Optional[str] = None

class CalculatorArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")
    a: float
    b: float
    operation: str
    
class KnowledgeSearchArguments(BaseModel):
    query: str
    
class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]
    
