from typing import List
from ...db.base.database_manager import DatabaseManager
from ...models.distributor.distributor_order_model import (
    DistributorOrderDbModel,
    DistributorOrderItemDbModel
)
from ...schemas.distributor.distributor_order_schema import DistributorOrderCreate, DistributorOrderUpdate
from ...exceptions.custom_exceptions import NotFoundException

class DistributorOrderManager:
    def __init__(self, db: DatabaseManager):
        self.db = db

    # Create order
    async def create_order(self, order: DistributorOrderCreate) -> DistributorOrderDbModel:
        total_amount = order.total_amount
        created_order = await self.db.create(DistributorOrderDbModel, order.dict(exclude={"items"}))
        for item in order.items:
            await self.db.create(
                DistributorOrderItemDbModel,
                {"order_id": created_order.order_id, **item.dict()}
            )
        return await self.get_order_by_id(created_order.order_id)
    

     # Get all orders (for all distributors)
    async def get_all_orders(self) -> List[DistributorOrderDbModel]:
        return await self.db.read(DistributorOrderDbModel)

    # Get order by ID
    async def get_order_by_id(self, order_id: int) -> DistributorOrderDbModel:
        orders = await self.db.read(DistributorOrderDbModel, filters={"order_id": order_id})
        if not orders:
            raise NotFoundException(f"Order {order_id} not found")
        return orders

    # Get all orders for a distributor
    async def get_orders_by_distributor(self, distributor_id: int) -> List[DistributorOrderDbModel]:
        return await self.db.read(DistributorOrderDbModel, filters={"distributor_id": distributor_id})

    # Update order status
    async def update_order_status(self, order_id: int, update_data: DistributorOrderUpdate) -> DistributorOrderDbModel:
        order = await self.get_order_by_id(order_id)
        updates = update_data.dict(exclude_unset=True)
        await self.db.update(DistributorOrderDbModel, filters={"order_id": order_id}, updates=updates)
        return await self.get_order_by_id(order_id)

    # Delete order
    async def delete_order(self, order_id: int) -> bool:
        await self.get_order_by_id(order_id)
        await self.db.delete(DistributorOrderDbModel, filters={"order_id": order_id})
        await self.db.delete(DistributorOrderItemDbModel, filters={"order_id": order_id})
        return True
