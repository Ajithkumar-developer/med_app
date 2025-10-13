from typing import List
from ..models.retailer_model import RetailerDbModel
from ..schemas.retailer_schema import RetailerDataCreateModel, RetailerDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RetailerManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create Retailer
    async def create_retailer(self, retailer: RetailerDataCreateModel) -> RetailerDbModel:
        logger.info(f"Creating retailer: {retailer.shop_name}")
        try:
            created = await self.database_manager.create(RetailerDbModel, retailer.dict())
            logger.info(f"Retailer created successfully with ID: {created.retailer_id}")
            return created
        except Exception:
            logger.exception("Error creating retailer.")
            raise

    # 📋 Get All Retailers
    async def get_all_retailers(self, skip: int = 0, limit: int = 10) -> List[RetailerDbModel]:
        logger.info("Fetching all retailers.")
        try:
            retailers = await self.database_manager.read(RetailerDbModel)
            return retailers[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching retailers.")
            raise

    # 🔍 Get Retailer by ID
    async def get_retailer_by_id(self, retailer_id: int) -> RetailerDbModel:
        logger.info(f"Fetching retailer with ID: {retailer_id}")
        try:
            result = await self.database_manager.read(RetailerDbModel, filters={"retailer_id": retailer_id})
            if not result:
                raise NotFoundException(f"Retailer ID {retailer_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching retailer by ID.")
            raise

    # ✏️ Update Retailer
    async def update_retailer(self, retailer_id: int, update_data: RetailerDataUpdateModel) -> RetailerDbModel:
        logger.info(f"Updating retailer ID: {retailer_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_retailer_by_id(retailer_id)
            await self.database_manager.update(RetailerDbModel, filters={"retailer_id": retailer_id}, updates=updates)
            updated = await self.get_retailer_by_id(retailer_id)
            logger.info(f"Retailer ID {retailer_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating retailer.")
            raise

    # 🗑️ Delete Retailer
    async def delete_retailer(self, retailer_id: int) -> bool:
        logger.info(f"Deleting retailer ID: {retailer_id}")
        try:
            await self.get_retailer_by_id(retailer_id)
            await self.database_manager.delete(RetailerDbModel, filters={"retailer_id": retailer_id})
            logger.info(f"Retailer ID {retailer_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting retailer.")
            raise
