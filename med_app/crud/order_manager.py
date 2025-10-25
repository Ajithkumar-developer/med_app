from typing import List
from decimal import Decimal
from sqlalchemy.future import select
from ..models.order_model import OrderDbModel, OrderItemDbModel
from ..schemas.order_schema import OrderDataCreateModel, OrderDataUpdateModel
from ..db.base.database_manager import DatabaseManager
from ..exceptions.custom_exceptions import NotFoundException
from ..utils.logger import get_logger
from ..utils.invoice_generator import generate_invoice_pdf
from ..models.retailer_model import RetailerDbModel
from ..models.customer_model import CustomerDbModel
from ..models.medicine_model import MedicineDbModel

logger = get_logger(__name__)


class OrderManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    async def create_order(self, order: OrderDataCreateModel) -> OrderDbModel:
        logger.info("Creating new order")
        try:
            # Prepare order data without items
            order_data = order.dict(exclude={"items"})
            created_order = await self.database_manager.create(OrderDbModel, order_data)

            # Add order items
            for item in order.items:
                item_data = item.dict()
                item_data["order_id"] = created_order.order_id
                await self.database_manager.create(OrderItemDbModel, item_data)

            # Fetch full order
            session = self.database_manager.get_session()
            async with session:
                stmt = select(OrderDbModel).where(OrderDbModel.order_id == created_order.order_id)
                result = await session.execute(stmt)
                full_order = result.scalar_one()

            # Fetch retailer for invoice
            retailer = (
                await self.database_manager.read(
                    RetailerDbModel, filters={"retailer_id": full_order.retailer_id}
                )
            )[0]

            # Optionally generate invoice
            # generate_invoice_pdf(full_order, retailer_data=retailer, order_id=full_order.order_id)

            return full_order
        except Exception:
            logger.exception("Error creating order.")
            raise


    async def get_all_orders(self, skip: int = 0, limit: int = 10) -> List[OrderDbModel]:
        logger.info("Fetching all orders.")
        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = select(OrderDbModel).offset(skip).limit(limit)
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
                stmt = select(OrderDbModel).where(OrderDbModel.order_id == order_id)
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
                    .where(OrderDbModel.customer_id == user_id)
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                return result.scalars().all()
        except Exception:
            logger.exception("Error fetching orders by user ID.")
            raise

    async def get_orders_by_retailer_id(self, retailer_id: int, skip: int = 0, limit: int = 10):
        """
        Returns all orders for a retailer, formatted with:
        - customer name & combined address
        - order info
        - item details (medicine name, price, totals)
        """
        logger.info(f"Fetching orders for retailer ID: {retailer_id}")

        try:
            session = self.database_manager.get_session()
            async with session:
                stmt = (
                    select(OrderDbModel)
                    .where(OrderDbModel.retailer_id == retailer_id)
                    .offset(skip)
                    .limit(limit)
                )
                result = await session.execute(stmt)
                orders = result.scalars().all()

                final_output = []

                for order in orders:
                    # Get customer info
                    customer = await self.database_manager.read(
                        CustomerDbModel, filters={"customer_id": order.customer_id}
                    )

                    customer_data = {}
                    if customer:
                        c = customer[0]
                        # Combine address fields safely
                        address_parts = [
                            c.address_line1,
                            c.address_line2,
                            c.city,
                            c.state,
                            c.zip_code,                            
                        ]
                        full_address = ", ".join([part for part in address_parts if part])
                        customer_data = {
                            "name": c.full_name or "Unknown Customer",
                            "address": full_address or "N/A",
                            "mobile": c.phone_number
                        }

                    # Get items for this order
                    items = await self.database_manager.read(
                        OrderItemDbModel, filters={"order_id": order.order_id}
                    )

                    formatted_items = []
                    for item in items:
                        medicine = await self.database_manager.read(
                            MedicineDbModel, filters={"medicine_id": item.medicine_id}
                        )
                        med_name = medicine[0].name if medicine else "Unknown Medicine"
                        unit_price = Decimal(item.price)
                        total_price = unit_price * Decimal(item.quantity)

                        formatted_items.append({
                            "item_name": med_name,
                            "quantity": item.quantity,
                            "unit_price": float(unit_price),
                            "total_price": float(total_price)
                        })

                    final_output.append({
                        "order_id": order.order_id,
                        "customer_name": customer_data["name"],
                        "address": customer_data["address"],
                        "mobile no. : ": customer_data["mobile"],
                        "order_date": order.order_date,
                        "status": order.status.value if hasattr(order.status, "value") else order.status,
                        "total_amount": float(order.total_amount),
                        "items": formatted_items
                    })

                return final_output

        except Exception:
            logger.exception("Error fetching orders by retailer ID.")
            raise
