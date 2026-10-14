from typing import Optional, Any, Literal
from pydantic import BaseModel, ConfigDict, Field,  model_validator


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
    
class ToolCallBatch(BaseModel):
    tool_calls: list[ToolCall]



class AgentDecision(BaseModel):
    action: Literal["tool_call", "final"]
    tool_name: str | None = None
    arguments: dict[str, Any] = Field(default_factory=dict)
    final_answer: str | None = None

    @model_validator(mode="after")
    def validate_action(self):
        if self.action == "tool_call":
            if not self.tool_name or not self.tool_name.strip():
                raise ValueError("Tool call requires a tool name")

            if self.final_answer is not None:
                raise ValueError(
                    "Tool call cannot contain a final answer"
                )

        elif self.action == "final":
            if not self.final_answer or not self.final_answer.strip():
                raise ValueError("Final action requires an answer")

            if self.tool_name is not None:
                raise ValueError(
                    "Final action cannot specify a tool"
                )

        return self

