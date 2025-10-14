from typing import List
from passlib.context import CryptContext
from ..models.distributor_model import DistributorDbModel
from ..schemas.distributor_schema import (
    DistributorDataCreateModel,
    DistributorDataUpdateModel,
    DistributorLoginRequest,
)
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger

logger = get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DistributorManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    async def create_distributor(self, distributor: DistributorDataCreateModel) -> DistributorDbModel:
        logger.info(f"Creating distributor: {distributor.company_name}")
        try:
            dist_dict = distributor.dict()
            # Hash the password
            dist_dict["password_hash"] = pwd_context.hash(dist_dict["password_hash"])
            created = await self.database_manager.create(DistributorDbModel, dist_dict)
            logger.info(f"Distributor created with ID: {created.distributor_id}")
            return created
        except Exception:
            logger.exception("Error creating distributor.")
            raise

    async def get_all_distributors(self, skip: int = 0, limit: int = 10) -> List[DistributorDbModel]:
        try:
            dists = await self.database_manager.read(DistributorDbModel)
            return dists[skip : skip + limit]
        except Exception:
            logger.exception("Error fetching distributors.")
            raise

    async def get_distributor_by_id(self, distributor_id: int) -> DistributorDbModel:
        try:
            result = await self.database_manager.read(DistributorDbModel, filters={"distributor_id": distributor_id})
            if not result:
                raise NotFoundException(f"Distributor ID {distributor_id} not found.")
            return result[0]
        except Exception:
            logger.exception("Error fetching distributor by ID.")
            raise

    async def update_distributor(
        self, distributor_id: int, update_data: DistributorDataUpdateModel
    ) -> DistributorDbModel:
        logger.info(f"Updating distributor ID: {distributor_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            # If password being updated, hash it
            if "password_hash" in updates:
                updates["password_hash"] = pwd_context.hash(updates["password_hash"])
            await self.get_distributor_by_id(distributor_id)
            await self.database_manager.update(
                DistributorDbModel, filters={"distributor_id": distributor_id}, updates=updates
            )
            return await self.get_distributor_by_id(distributor_id)
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating distributor.")
            raise

    async def delete_distributor(self, distributor_id: int) -> bool:
        logger.info(f"Deleting distributor ID: {distributor_id}")
        try:
            await self.get_distributor_by_id(distributor_id)
            await self.database_manager.delete(DistributorDbModel, filters={"distributor_id": distributor_id})
            logger.info(f"Distributor ID {distributor_id} deleted.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting distributor.")
            raise

    async def login(self, login_req: DistributorLoginRequest) -> DistributorDbModel:
        logger.info(f"Login attempt for distributor email: {login_req.email}")
        try:
            results = await self.database_manager.read(DistributorDbModel, filters={"email": login_req.email})
            if not results:
                raise NotFoundException("Invalid email or password")
            distributor = results[0]
            if not pwd_context.verify(login_req.password, distributor.password_hash):
                raise NotFoundException("Invalid email or password")
            return distributor
        except Exception:
            logger.exception("Error during distributor login.")
            raise
