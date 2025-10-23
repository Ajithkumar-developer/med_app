from typing import List
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from ..models.order_model import OrderDbModel, OrderItemDbModel, OrderTypeEnum
from ..schemas.order_schema import OrderDataCreateModel, OrderDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger
from ..utils.invoice_generator import generate_invoice_pdf  # Your async invoice generation
from ..models.retailer_model import RetailerDbModel

logger = get_logger(__name__)


class OrderManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create Order
    async def create_order(self, order: OrderDataCreateModel) -> OrderDbModel:
        logger.info(f"Creating new order of type {order.order_type}")
        try:
            # Save main order
            order_data = order.dict(exclude={"items"})
            created_order = await self.database_manager.create(OrderDbModel, order_data)

            # Save order items
            for item in order.items:
                item_data = item.dict()
                item_data["order_id"] = created_order.order_id
                await self.database_manager.create(OrderItemDbModel, item_data)

            # Eager load order with items
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(OrderDbModel.order_id == created_order.order_id)
                )
                result = await session.execute(stmt)
                full_order = result.scalar_one()

            logger.info(f"Order created successfully with ID: {created_order.order_id}")

            # ✅ Fetch retailer data
            retailer = (await self.database_manager.read(RetailerDbModel, filters={"retailer_id": full_order.retailer_id}))[0]

            # 🧾 Generate and save invoice PDF
            pdf_path = generate_invoice_pdf(
                full_order,
                retailer_data=retailer,
                order_id=full_order.order_id
            )

            # print(pdf_path)
            
            return full_order

        except Exception:
            logger.exception("Error creating order.")
            raise

    # 📋 Get All Orders
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

    # 🔍 Get Order by ID
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

    # ✏️ Update Order
    async def update_order(self, order_id: int, update_data: OrderDataUpdateModel) -> OrderDbModel:
        logger.info(f"Updating order ID: {order_id}")
        try:
            updates = update_data.dict(exclude_unset=True)
            await self.get_order_by_id(order_id)
            await self.database_manager.update(OrderDbModel, filters={"order_id": order_id}, updates=updates)
            updated_order = await self.get_order_by_id(order_id)
            logger.info(f"Order ID {order_id} updated successfully.")
            return updated_order
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error updating order.")
            raise

    # 🗑️ Delete Order
    async def delete_order(self, order_id: int) -> bool:
        logger.info(f"Deleting order ID: {order_id}")
        try:
            await self.get_order_by_id(order_id)
            await self.database_manager.delete(OrderDbModel, filters={"order_id": order_id})
            logger.info(f"Order ID {order_id} deleted successfully.")
            return True
        except NotFoundException:
            raise
        except Exception:
            logger.exception("Error deleting order.")
            raise

    # 🔍 Get Orders by User ID
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

    # 🔍 Get B2C Orders by Retailer
    async def get_b2c_orders_by_retailer_id(self, retailer_id: int, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info(f"Fetching B2C orders for retailer ID: {retailer_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(
                        (OrderDbModel.retailer_id == retailer_id) &
                        (OrderDbModel.order_type == OrderTypeEnum.B2C)
                    )
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching B2C orders for retailer.")
            raise

    # 🔍 Get B2B Orders by Retailer
    async def get_b2b_orders_by_retailer_id(self, retailer_id: int, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info(f"Fetching B2B orders placed by retailer ID: {retailer_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(
                        (OrderDbModel.retailer_id == retailer_id) &
                        (OrderDbModel.order_type == OrderTypeEnum.B2B)
                    )
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching B2B orders by retailer.")
            raise

    # 🔍 Get B2B Orders by Distributor
    async def get_b2b_orders_by_distributor_id(self, distributor_id: int, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info(f"Fetching B2B orders received by distributor ID: {distributor_id}")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .options(selectinload(OrderDbModel.items))
                    .where(
                        (OrderDbModel.distributor_id == distributor_id) &
                        (OrderDbModel.order_type == OrderTypeEnum.B2B)
                    )
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching B2B orders by distributor.")
            raise
