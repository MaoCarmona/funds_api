from fund_management.core.entities import Fund
from typing import Optional, List
from pymongo.errors import PyMongoError
from motor.motor_asyncio import AsyncIOMotorCollection
from fund_management.core.repositories.fund_repository import FundRepository
from fund_management.infrastructure.database import MongoDB

class FundRepositoryImpl(FundRepository):
    def __init__(self):
        self.collection: Optional[AsyncIOMotorCollection] = None

    async def initialize(self, db_name: str):
        db = await MongoDB.get_database(db_name)
        self.collection = db.get_collection('funds')

    async def save(self, fund: Fund) -> None:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            fund_data = fund.model_dump(by_alias=True)
            print(fund_data)
            await self.collection.insert_one(fund_data)
        except PyMongoError as e:
            raise RuntimeError("Error al guardar el fondo") from e
        
    async def find_by_name(self, name: str) -> Optional[Fund]:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            fund = await self.collection.find_one({"name": name})
            if fund:
                return Fund(**fund)
            return None
        except PyMongoError as e:
            raise RuntimeError("Error al encontrar el fondo por nombre") from e

    async def  find_by_id(self, fund_id: str) -> Optional[Fund]:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            fund = await self.collection.find_one({"_id": fund_id})
            if fund:
                return Fund(**fund)
            return None
        except PyMongoError as e:
            raise RuntimeError("Error al encontrar el fondo por ID") from e

    async def find_all(self) -> List[Fund]:
        if self.collection is None:
            raise RuntimeError("Repository not initialized.")
        try:
            funds = await self.collection.find().to_list(None)
            return [Fund(**fund) for fund in funds]
        except PyMongoError as e:
            raise RuntimeError("Error al encontrar todos los fondos") from e
