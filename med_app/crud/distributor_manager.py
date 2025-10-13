from typing import List
from ..models.distributor_model import DistributorDbModel
from ..schemas.distributor_schema import DistributorDataCreateModel, DistributorDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DistributorManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create Distributor
    async def create_distributor(self, distributor: DistributorDataCreateModel) -> DistributorDbModel:
        logger.info(f"Creating distributor: {distributor.company_name}")
        try:
            created = await self.database_manager.create(DistributorDbModel, distributor.dict())
            logger.info(f"Distributor created successfully with ID: {created.distributor_id}")
            return created
        except Exception:
            logger.exception("Error creating distributor.")
            raise

    # 📋 Get All Distributors
    async def get_all_distributors(self, skip: int = 0, limit: int = 10) -> List[DistributorDbModel]:
        logger.info("Fetching all distributors.")
        try:
            distributors = await self.database_manager.read(DistributorDbModel)
            return distributors[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching distributors.")
            raise

    # 🔍 Get Distributor by ID
    async def get_distributor_by_id(self, distributor_id: int) -> DistributorDbModel:
        logger.info(f"Fetching distributor with ID: {distributor_id}")
        try:
            result = await self.database_manager.read(DistributorDbModel, filters={"distributor_id": distributor_id})
            if not result:
                raise NotFoundException(f"Distributor ID {distributor_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching distributor by ID.")
            raise

    # ✏️ Update Distributor
    async def update_distributor(self, distributor_id: int, update_data: DistributorDataUpdateModel) -> DistributorDbModel:
        logger.info(f"Updating distributor ID: {distributor_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_distributor_by_id(distributor_id)
            await self.database_manager.update(DistributorDbModel, filters={"distributor_id": distributor_id}, updates=updates)
            updated = await self.get_distributor_by_id(distributor_id)
            logger.info(f"Distributor ID {distributor_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating distributor.")
            raise

    # 🗑️ Delete Distributor
    async def delete_distributor(self, distributor_id: int) -> bool:
        logger.info(f"Deleting distributor ID: {distributor_id}")
        try:
            await self.get_distributor_by_id(distributor_id)
            await self.database_manager.delete(DistributorDbModel, filters={"distributor_id": distributor_id})
            logger.info(f"Distributor ID {distributor_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting distributor.")
            raise
