from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from fund_management.core.enums import TransactionTypeEnum

class TransactionCreate(BaseModel):
    user_id: UUID
    fund_id: UUID
    amount: int
    type:TransactionTypeEnum
class TransactionResponse(BaseModel):
    id: UUID
    user_id: UUID
    fund_id: UUID
    amount: int
    type: str
    timestamp: datetime

    class Config:
        from_attributes = True
