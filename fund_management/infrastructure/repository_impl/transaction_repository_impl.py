from fund_management.core.entities import Transaction
from fund_management.core.repositories.transaction_repository import TransactionRepository
from motor.motor_asyncio import AsyncIOMotorCollection
from typing import Optional, List
from pymongo.errors import PyMongoError

from fund_management.infrastructure.database import MongoDB

class TransactionRepositoryImpl(TransactionRepository):
    def __init__(self):
        self.collection: Optional[AsyncIOMotorCollection] = None

    async def initialize(self, db_name: str):
        db = await MongoDB.get_database(db_name)
        self.collection = db['transactions']

    async def save(self, transaction: Transaction) -> None:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            await self.collection.insert_one(transaction.model_dump(by_alias=True))
        except PyMongoError as e:
            raise RuntimeError("Error saving transaction") from e

    async def find_by_user_id(self, user_id: str) -> List[Transaction]:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            transactions = await self.collection.find({"user_id": user_id}).to_list(None)
            return [Transaction(**transaction) for transaction in transactions]
        except PyMongoError as e:
            raise RuntimeError("Error finding transactions by user") from e
