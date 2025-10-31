import bcrypt
from typing import List
from ...models.retailer.retailer_model import RetailerDbModel
from ...schemas.retailer.retailer_schema import (
    RetailerDataCreateModel, RetailerDataUpdateModel, RetailerLoginRequest
)
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)

class RetailerManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    async def create_retailer(self, retailer: RetailerDataCreateModel) -> RetailerDbModel:
        logger.info(f"Creating retailer: {retailer.shop_name}")
        try:
            hashed_password = bcrypt.hashpw(retailer.password_hash.encode('utf-8'), bcrypt.gensalt())
            retailer_dict = retailer.dict()
            retailer_dict["password_hash"] = hashed_password.decode("utf-8")
            return await self.database_manager.create(RetailerDbModel, retailer_dict)
        except Exception:
            logger.exception("Error creating retailer.")
            raise

    async def get_all_retailers(self, skip: int = 0, limit: int = 10) -> List[RetailerDbModel]:
        return (await self.database_manager.read(RetailerDbModel))[skip:skip + limit]

    async def get_retailer_by_id(self, retailer_id: int) -> RetailerDbModel:
        result = await self.database_manager.read(RetailerDbModel, filters={"retailer_id": retailer_id})
        if not result:
            raise NotFoundException(f"Retailer ID {retailer_id} not found.")
        return result[0]

    async def update_retailer(self, retailer_id: int, update_data: RetailerDataUpdateModel) -> RetailerDbModel:
        updates = update_data.dict(exclude_unset=True)
        if "password_hash" in updates:
            updates["password_hash"] = bcrypt.hashpw(updates["password_hash"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        await self.get_retailer_by_id(retailer_id)
        await self.database_manager.update(RetailerDbModel, filters={"retailer_id": retailer_id}, updates=updates)
        return await self.get_retailer_by_id(retailer_id)

    async def delete_retailer(self, retailer_id: int) -> bool:
        await self.get_retailer_by_id(retailer_id)
        await self.database_manager.delete(RetailerDbModel, filters={"retailer_id": retailer_id})
        return True

    async def login(self, credentials: RetailerLoginRequest) -> RetailerDbModel:
        result = await self.database_manager.read(RetailerDbModel, filters={"email": credentials.email})
        if not result:
            raise NotFoundException("Invalid email or password")
        retailer = result[0]
        if not bcrypt.checkpw(credentials.password.encode("utf-8"), retailer.password_hash.encode("utf-8")):
            raise NotFoundException("Invalid email or password")
        return retailer


    async def get_retailers_by_zip_code(self, zip_code: str) -> List[RetailerDbModel]:
        result = await self.database_manager.read(RetailerDbModel, filters={"zip_code": zip_code})
        if not result:
            raise NotFoundException(f"No retailers found in ZIP code {zip_code}.")
        return result
