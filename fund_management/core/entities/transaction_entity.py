from typing import Optional
from uuid import uuid4
from datetime import datetime ,timezone
from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: uuid4().hex, alias="_id")
    user_id: str
    fund_id: str
    amount: float
    type: str
    timestamp: str = datetime.now(timezone.utc).isoformat()
