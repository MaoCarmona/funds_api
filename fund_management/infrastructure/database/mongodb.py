from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None

    @staticmethod
    async def connect_to_database(uri: str):
        try:
            MongoDB.client = AsyncIOMotorClient(uri)
            await MongoDB.client.admin.command('ping')
            logging.info("Connection established ")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {e}")
            MongoDB.client = None
            raise  

    @staticmethod
    async def get_database(db_name: str):
        if MongoDB.client is None:
            raise RuntimeError("A connection to the database has not been established.")
        
        try:
            database = MongoDB.client[db_name]
            return database
        except Exception as e:
            logging.error(f"Error obtaining the database: {e}")
            raise
