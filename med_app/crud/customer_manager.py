from typing import List
from passlib.context import CryptContext
from ..models.customer_model import CustomerDbModel
from ..schemas.customer_schema import CustomerDataCreateModel, CustomerDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class CustomerManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    async def create_customer(self, customer: CustomerDataCreateModel) -> CustomerDbModel:
        logger.info(f"Creating new customer: {customer.full_name}")
        try:
            customer_dict = customer.dict()
            customer_dict["password_hash"] = pwd_context.hash(customer_dict["password_hash"])
            created = await self.database_manager.create(CustomerDbModel, customer_dict)
            return created
        except Exception:
            logger.exception("Error creating customer.")
            raise

    async def get_all_customers(self, skip: int = 0, limit: int = 10) -> List[CustomerDbModel]:
        try:
            customers = await self.database_manager.read(CustomerDbModel)
            return customers[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching customers.")
            raise

    async def get_customer_by_id(self, customer_id: int) -> CustomerDbModel:
        try:
            result = await self.database_manager.read(CustomerDbModel, filters={"customer_id": customer_id})
            if not result:
                raise NotFoundException(f"Customer ID {customer_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching customer by ID.")
            raise

    async def update_customer(self, customer_id: int, update_data: CustomerDataUpdateModel) -> CustomerDbModel:
        logger.info(f"Updating customer ID: {customer_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            if "password_hash" in updates:
                updates["password_hash"] = pwd_context.hash(updates["password_hash"])
            await self.get_customer_by_id(customer_id)
            await self.database_manager.update(CustomerDbModel, filters={"customer_id": customer_id}, updates=updates)
            return await self.get_customer_by_id(customer_id)
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating customer.")
            raise

    async def delete_customer(self, customer_id: int) -> bool:
        logger.info(f"Deleting customer ID: {customer_id}")
        try:
            await self.get_customer_by_id(customer_id)
            await self.database_manager.delete(CustomerDbModel, filters={"customer_id": customer_id})
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting customer.")
            raise

    async def login_customer(self, email: str, password: str) -> CustomerDbModel:
        logger.info(f"Attempting login for email: {email}")
        try:
            result = await self.database_manager.read(CustomerDbModel, filters={"email": email})
            if not result:
                raise NotFoundException("Invalid email or password")

            customer = result[0]
            if not pwd_context.verify(password, customer.password_hash):
                raise NotFoundException("Invalid email or password")

            return customer
        except Exception:
            logger.exception("Error during login.")
            raise
