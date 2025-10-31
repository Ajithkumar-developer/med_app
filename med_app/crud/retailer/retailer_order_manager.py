from decimal import Decimal
from typing import List, Optional
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from ...models.retailer.retailer_order_model import RetailerOrderDbModel, RetailerOrderItemDbModel
from ...schemas.retailer.retailer_order_schema import RetailerOrderCreateModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger
from sqlalchemy.exc import SQLAlchemyError
from ...models.distributor.distributor_stock_model import DistributorStockDbModel

logger = get_logger(__name__)

class RetailerOrderManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # 🧾 Create new order
    async def create_order(self, data: RetailerOrderCreateModel) -> RetailerOrderDbModel:
        logger.info(f"Creating new order for retailer {data.retailer_id} to distributor {data.distributor_id}")

        session = self.database_manager.get_session()
        async with session.begin():
            try:
                total_amount = Decimal(0)
                order_items_data = []

                # 🔍 Step 1: Validate distributor stock (use FIFO: earliest expiry first)
                for item in data.items:
                    stmt = select(DistributorStockDbModel).where(
                        DistributorStockDbModel.distributor_id == data.distributor_id,
                        DistributorStockDbModel.medicine_id == item.medicine_id,
                        DistributorStockDbModel.quantity > 0
                    ).order_by(DistributorStockDbModel.expiry_date)  # FIFO

                    result = await session.execute(stmt)
                    stock_item = result.scalars().first()

                    if not stock_item:
                        raise HTTPException(
                            status_code=404,
                            detail=f"Medicine ID {item.medicine_id} not found or out of stock in distributor inventory"
                        )

                    if stock_item.quantity < item.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Insufficient stock for medicine {item.medicine_id}. "
                                   f"Available: {stock_item.quantity}, Requested: {item.quantity}"
                        )

                    item_total = Decimal(item.price) * item.quantity
                    total_amount += item_total

                    order_items_data.append({
                        "medicine_id": item.medicine_id,
                        "quantity": item.quantity,
                        "price": item.price,
                        "stock_id": stock_item.stock_id,
                        "new_stock": stock_item.quantity - item.quantity
                    })

                # ✅ Step 2: Create order
                order_data = {
                    "retailer_id": data.retailer_id,
                    "distributor_id": data.distributor_id,
                    "total_amount": total_amount
                }
                order = await self.database_manager.create(RetailerOrderDbModel, order_data)

                # ✅ Step 3: Create order items & update distributor stock
                for item_data in order_items_data:
                    await self.database_manager.create(
                        RetailerOrderItemDbModel,
                        {
                            "order_id": order.order_id,
                            "medicine_id": item_data["medicine_id"],
                            "quantity": item_data["quantity"],
                            "price": item_data["price"]
                        }
                    )

                    await self.database_manager.update(
                        DistributorStockDbModel,
                        filters={"stock_id": item_data["stock_id"]},
                        updates={"quantity": item_data["new_stock"]}
                    )

                logger.info(f"✅ Retailer order {order.order_id} created and stock updated.")
                return await self.get_order_by_id(order.order_id)

            except HTTPException:
                raise
            except SQLAlchemyError as e:
                logger.exception("Database error while creating retailer order")
                raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
            except Exception as e:
                logger.exception("Unexpected error during retailer order creation")
                raise HTTPException(status_code=500, detail=str(e))
                                                
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
