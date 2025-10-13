from typing import List
from ..models.customer_model import CustomerDbModel
from ..schemas.customer_schema import CustomerDataCreateModel, CustomerDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CustomerManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create new customer
    async def create_customer(self, customer: CustomerDataCreateModel) -> CustomerDbModel:
        logger.info(f"Creating new customer: {customer.full_name}")
        try:
            created = await self.database_manager.create(CustomerDbModel, customer.dict())
            logger.info(f"Customer created successfully with ID: {created.customer_id}")
            return created
        except Exception:
            logger.exception("Error creating customer.")
            raise

    # 📋 Get all customers
    async def get_all_customers(self, skip: int = 0, limit: int = 10) -> List[CustomerDbModel]:
        try:
            customers = await self.database_manager.read(CustomerDbModel)
            return customers[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching customers.")
            raise

    # 🔍 Get single customer
    async def get_customer_by_id(self, customer_id: int) -> CustomerDbModel:
        try:
            result = await self.database_manager.read(CustomerDbModel, filters={"customer_id": customer_id})
            if not result:
                raise NotFoundException(f"Customer ID {customer_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching customer by ID.")
            raise

    # ✏️ Update customer
    async def update_customer(self, customer_id: int, update_data: CustomerDataUpdateModel) -> CustomerDbModel:
        logger.info(f"Updating customer ID: {customer_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_customer_by_id(customer_id)
            await self.database_manager.update(CustomerDbModel, filters={"customer_id": customer_id}, updates=updates)
            updated = await self.get_customer_by_id(customer_id)
            logger.info(f"Customer ID {customer_id} updated successfully.")
            return updated
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating customer.")
            raise

    # 🗑️ Delete customer
    async def delete_customer(self, customer_id: int) -> bool:
        logger.info(f"Deleting customer ID: {customer_id}")
        try:
            await self.get_customer_by_id(customer_id)
            await self.database_manager.delete(CustomerDbModel, filters={"customer_id": customer_id})
            logger.info(f"Customer ID {customer_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting customer.")
            raise
