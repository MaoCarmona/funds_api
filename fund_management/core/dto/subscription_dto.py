from typing import Optional
from pydantic import BaseModel

class SubscriptionRequest(BaseModel):
    user_id: str
    amount: float
    phone: str

class UnSubscriptionRequest(BaseModel):
    user_id: str
    phone: str