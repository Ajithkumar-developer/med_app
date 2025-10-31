from typing import List
from ...models.distributor.distributor_stock_model import DistributorStockDbModel
from ...schemas.distributor.distributor_stock_schema import (
    DistributorStockCreateModel,
    DistributorStockUpdateModel,
)
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)


class DistributorStockManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # ✅ Create
    async def create_stock(self, stock: DistributorStockCreateModel) -> DistributorStockDbModel:
        logger.info(f"Creating stock entry for distributor {stock.distributor_id}")
        try:
            created = await self.database_manager.create(DistributorStockDbModel, stock.dict())
            logger.info(f"Stock created successfully (ID: {created.stock_id})")
            return created
        except Exception:
            logger.exception("Error creating stock.")
            raise

    # ✅ Read all
    async def get_all_stock(self, skip: int = 0, limit: int = 10) -> List[DistributorStockDbModel]:
        logger.info("Fetching all distributor stock entries.")
        try:
            stocks = await self.database_manager.read(DistributorStockDbModel)
            return stocks[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching stock list.")
            raise

    # ✅ Read by ID
    async def get_stock_by_id(self, stock_id: int) -> DistributorStockDbModel:
        logger.info(f"Fetching stock ID: {stock_id}")
        try:
            result = await self.database_manager.read(DistributorStockDbModel, filters={"stock_id": stock_id})
            if not result:
                raise NotFoundException(f"Stock ID {stock_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching stock by ID.")
            raise

    # ✅ Update
    async def update_stock(self, stock_id: int, update_data: DistributorStockUpdateModel) -> DistributorStockDbModel:
        logger.info(f"Updating stock ID: {stock_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_stock_by_id(stock_id)
            await self.database_manager.update(DistributorStockDbModel, filters={"stock_id": stock_id}, updates=updates)
            updated = await self.get_stock_by_id(stock_id)
            logger.info(f"Stock ID {stock_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating stock.")
            raise

    # ✅ Delete
    async def delete_stock(self, stock_id: int) -> bool:
        logger.info(f"Deleting stock ID: {stock_id}")
        try:
            await self.get_stock_by_id(stock_id)
            await self.database_manager.delete(DistributorStockDbModel, filters={"stock_id": stock_id})
            logger.info(f"Stock ID {stock_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting stock.")
            raise

    # ---------------- Get stock by distributor ----------------
    async def get_stock_by_distributor(self, distributor_id: int) -> list[DistributorStockDbModel]:
        result = await self.database_manager.read(
            DistributorStockDbModel, filters={"distributor_id": distributor_id}
        )
        return result