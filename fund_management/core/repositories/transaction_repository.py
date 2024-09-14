from abc import ABC, abstractmethod
from typing import List
from fund_management.core.entities import Transaction

class TransactionRepository(ABC):
    @abstractmethod
    async def save(self, transaction: Transaction) -> None:
        """Save a transaction."""
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: str) -> List[Transaction]:
        """Find transactions by user Id"""
        pass

