from pydantic import BaseModel
from uuid import UUID

class FundCreate(BaseModel):
    name: str
    min_investment_amount: int
    category: str

class FundResponse(BaseModel):
    id: UUID
    name: str
    min_investment_amount: int
    category: str

    class Config:
        from_attributes = True
