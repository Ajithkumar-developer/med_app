from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.order_model import OrderDbModel, OrderItemDbModel
from ..schemas.order_schema import OrderDataCreateModel, OrderDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger
from ..utils.invoice_generator import generate_invoice_pdf
from ..models.retailer_model import RetailerDbModel

logger = get_logger(__name__)


class OrderManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    async def create_order(self, order: OrderDataCreateModel) -> OrderDbModel:
        logger.info("Creating new order")
        try:
            order_data = order.dict(exclude={"items"})
            created_order = await self.database_manager.create(OrderDbModel, order_data)

            for item in order.items:
                item_data = item.dict()
                item_data["order_id"] = created_order.order_id
                await self.database_manager.create(OrderItemDbModel, item_data)

            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(OrderDbModel.order_id == created_order.order_id)
                )
                result = await session.execute(stmt)
                full_order = result.scalar_one()

            retailer = (
                await self.database_manager.read(
                    RetailerDbModel, filters={"retailer_id": full_order.retailer_id}
                )
            )[0]

            generate_invoice_pdf(
                full_order,
                retailer_data=retailer,
                order_id=full_order.order_id
            )

            return full_order
        except Exception:
            logger.exception("Error creating order.")
            raise

    async def get_all_orders(self, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info("Fetching all orders.")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching orders.")
            raise

    async def get_order_by_id(self, order_id: int) -> OrderDbModel:
        logger.info(f"Fetching order with ID: {order_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(OrderDbModel.order_id == order_id)
                )
                result = await session.execute(stmt)
                order = result.scalar_one_or_none()
            if not order:
                raise NotFoundException(f"Order ID {order_id} not found.")
            return order
        except Exception:
            logger.exception("Error fetching order by ID.")
            raise

    async def update_order(self, order_id: int, update_data: OrderDataUpdateModel) -> OrderDbModel:
        logger.info(f"Updating order ID: {order_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_order_by_id(order_id)
            await self.database_manager.update(OrderDbModel, filters={"order_id": order_id}, updates=updates)
            updated_order = await self.get_order_by_id(order_id)
            return updated_order
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating order.")
            raise

    async def delete_order(self, order_id: int) -> bool:
        logger.info(f"Deleting order ID: {order_id}")
        try:
            await self.get_order_by_id(order_id)
            await self.database_manager.delete(OrderDbModel, filters={"order_id": order_id})
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting order.")
            raise

    async def get_orders_by_user_id(self, user_id: int, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info(f"Fetching orders for user ID: {user_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(OrderDbModel.customer_id == user_id)
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching orders by user ID.")
            raise

    async def get_orders_by_retailer_id(self, retailer_id: int, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info(f"Fetching orders for retailer ID: {retailer_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(OrderDbModel.retailer_id == retailer_id)
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching orders by retailer ID.")
            raise
