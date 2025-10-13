from typing import List
from ..models.retailer_stock_model import RetailerStockDbModel
from ..schemas.retailer_stock_schema import (
    RetailerStockCreateModel,
    RetailerStockUpdateModel,
)
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class RetailerStockManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create stock entry
    async def create_stock(self, stock: RetailerStockCreateModel) -> RetailerStockDbModel:
        logger.info(f"Creating stock entry for retailer {stock.retailer_id}")
        try:
            created = await self.database_manager.create(RetailerStockDbModel, stock.dict())
            logger.info(f"Stock created successfully (ID: {created.stock_id})")
            return created
        except Exception:
            logger.exception("Error creating stock.")
            raise

    # 📋 Get all stock
    async def get_all_stock(self, skip: int = 0, limit: int = 10) -> List[RetailerStockDbModel]:
        logger.info("Fetching all retailer stock entries.")
        try:
            stocks = await self.database_manager.read(RetailerStockDbModel)
            return stocks[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching stock list.")
            raise

    # 🔍 Get stock by ID
    async def get_stock_by_id(self, stock_id: int) -> RetailerStockDbModel:
        logger.info(f"Fetching stock ID: {stock_id}")
        try:
            result = await self.database_manager.read(RetailerStockDbModel, filters={"stock_id": stock_id})
            if not result:
                raise NotFoundException(f"Stock ID {stock_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching stock by ID.")
            raise

    # ✏️ Update stock
    async def update_stock(self, stock_id: int, update_data: RetailerStockUpdateModel) -> RetailerStockDbModel:
        logger.info(f"Updating stock ID: {stock_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_stock_by_id(stock_id)
            await self.database_manager.update(RetailerStockDbModel, filters={"stock_id": stock_id}, updates=updates)
            updated = await self.get_stock_by_id(stock_id)
            logger.info(f"Stock ID {stock_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating stock.")
            raise

    # 🗑️ Delete stock
    async def delete_stock(self, stock_id: int) -> bool:
        logger.info(f"Deleting stock ID: {stock_id}")
        try:
            await self.get_stock_by_id(stock_id)
            await self.database_manager.delete(RetailerStockDbModel, filters={"stock_id": stock_id})
            logger.info(f"Stock ID {stock_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting stock.")
            raise
