from typing import List, Optional
from datetime import datetime
from ...models.retailer.retailer_order_model import RetailerOrderDbModel, RetailerOrderItemDbModel
from ...schemas.retailer.retailer_order_schema import RetailerOrderCreateModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)

class RetailerOrderManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create new order
    async def create_order(self, data: RetailerOrderCreateModel) -> RetailerOrderDbModel:
        logger.info(f"Creating new order for retailer {data.retailer_id}")
        order_data = {
            "retailer_id": data.retailer_id,
            "distributor_id": data.distributor_id,
            "total_amount": data.total_amount
        }
        order = await self.database_manager.create(RetailerOrderDbModel, order_data)
        
        # Create order items
        for item in data.items:
            item_data = {
                "order_id": order.order_id,
                "medicine_id": item.medicine_id,
                "quantity": item.quantity,
                "price": item.price
            }
            await self.database_manager.create(RetailerOrderItemDbModel, item_data)

        return await self.get_order_by_id(order.order_id)

    # 🔍 Get order by ID
    async def get_order_by_id(self, order_id: int) -> RetailerOrderDbModel:
        order = await self.database_manager.read(RetailerOrderDbModel, filters={"order_id": order_id})
        if not order:
            raise NotFoundException(f"Order ID {order_id} not found.")
        order_obj = order[0]
        items = await self.database_manager.read(RetailerOrderItemDbModel, filters={"order_id": order_id})
        order_obj.items = items
        return order_obj

    # 📋 List orders
    async def list_orders(
        self,
        retailer_id: Optional[int] = None,
        distributor_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[RetailerOrderDbModel]:
        filters = {}
        if retailer_id is not None:
            filters["retailer_id"] = retailer_id
        if distributor_id is not None:
            filters["distributor_id"] = distributor_id
        if status:
            filters["status"] = status

        orders = await self.database_manager.read(RetailerOrderDbModel, filters=filters)

        # Date range filter
        if start_date:
            orders = [o for o in orders if o.order_date >= start_date]
        if end_date:
            orders = [o for o in orders if o.order_date <= end_date]

        # Add items to each order
        for order in orders:
            order.items = await self.database_manager.read(RetailerOrderItemDbModel, filters={"order_id": order.order_id})

        return orders

    # ✏️ Update order status
    async def update_order_status(self, order_id: int, status: str) -> RetailerOrderDbModel:
        await self.get_order_by_id(order_id)
        await self.database_manager.update(RetailerOrderDbModel, filters={"order_id": order_id}, updates={"status": status})
        return await self.get_order_by_id(order_id)

    # 🗑️ Delete order
    async def delete_order(self, order_id: int) -> bool:
        await self.get_order_by_id(order_id)
        await self.database_manager.delete(RetailerOrderItemDbModel, filters={"order_id": order_id})
        await self.database_manager.delete(RetailerOrderDbModel, filters={"order_id": order_id})
        return True
