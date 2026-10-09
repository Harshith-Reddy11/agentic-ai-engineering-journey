from pydantic import BaseModel, Field


class AgentState(BaseModel):
    goal: str
    step: int = 0
    max_steps: int = 5
    status: str = "running"
    observations: list[str] = Field(default_factory=list)
    final_answer: str | None = None
