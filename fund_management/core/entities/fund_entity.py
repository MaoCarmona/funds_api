from pydantic import BaseModel, Field
from typing import Optional
from uuid import uuid4

class Fund(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: uuid4().hex, alias="_id")
    name: str
    min_investment_amount: float
    category: str

