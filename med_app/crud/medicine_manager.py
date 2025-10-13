from typing import List
from ..models.medicine_model import MedicineDbModel
from ..schemas.medicine_schema import MedicineDataCreateModel, MedicineDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MedicineManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create Medicine
    async def create_medicine(self, medicine: MedicineDataCreateModel) -> MedicineDbModel:
        logger.info(f"Creating medicine: {medicine.name}")
        try:
            created = await self.database_manager.create(MedicineDbModel, medicine.dict())
            logger.info(f"Medicine created successfully: {created.medicine_id}")
            return created
        except Exception:
            logger.exception("Error creating medicine.")
            raise

    # 📋 Get All Medicines
    async def get_all_medicines(self, skip: int = 0, limit: int = 10) -> List[MedicineDbModel]:
        logger.info("Fetching all medicines.")
        try:
            medicines = await self.database_manager.read(MedicineDbModel)
            return medicines[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching medicines.")
            raise

    # 🔍 Get Medicine by ID
    async def get_medicine_by_id(self, medicine_id: int) -> MedicineDbModel:
        logger.info(f"Fetching medicine with ID: {medicine_id}")
        try:
            result = await self.database_manager.read(MedicineDbModel, filters={"medicine_id": medicine_id})
            if not result:
                raise NotFoundException(f"Medicine ID {medicine_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching medicine by ID.")
            raise

    # ✏️ Update Medicine
    async def update_medicine(self, medicine_id: int, update_data: MedicineDataUpdateModel) -> MedicineDbModel:
        logger.info(f"Updating medicine ID: {medicine_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_medicine_by_id(medicine_id)
            await self.database_manager.update(MedicineDbModel, filters={"medicine_id": medicine_id}, updates=updates)
            updated = await self.get_medicine_by_id(medicine_id)
            logger.info(f"Medicine ID {medicine_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating medicine.")
            raise

    # 🗑️ Delete Medicine
    async def delete_medicine(self, medicine_id: int) -> bool:
        logger.info(f"Deleting medicine ID: {medicine_id}")
        try:
            await self.get_medicine_by_id(medicine_id)
            await self.database_manager.delete(MedicineDbModel, filters={"medicine_id": medicine_id})
            logger.info(f"Medicine ID {medicine_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting medicine.")
            raise
