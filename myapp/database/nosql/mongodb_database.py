# app/database/nosql/mongodb_database.py

from motor.motor_asyncio import AsyncIOMotorClient
from ..base.idatabase import IDatabase
from datetime import datetime

class MongoDBDatabase(IDatabase):
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = self.client["app"]

    async def disconnect(self):
        self.client.close()
