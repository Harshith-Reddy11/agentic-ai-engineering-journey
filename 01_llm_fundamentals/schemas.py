from pydantic import BaseModel
from typing import Optional

class RequestClassification(BaseModel):
    intent: str
    operation: Optional[str] = None
    number1: Optional[float] = None
    number2: Optional[float] = None
    topic: Optional[str] = None
    action: Optional[str] = None
    
# test = RequestClassification(
#     intent="Calculator",
#     operation="add",
#     number1=5,
#     number2=10
# )

# print(test)
# print(test.model_dump())