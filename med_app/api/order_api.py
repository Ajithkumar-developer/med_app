from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..schemas.order_schema import (
    OrderDataCreateModel,
    OrderDataReadModel,
    OrderDataUpdateModel,
)
from ..crud.order_manager import OrderManager
from ..utils.get_db_manager import get_order_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/orders", tags=["Orders"])


# 🧾 Create Order (B2C or B2B)
@router.post("/", response_model=OrderDataReadModel)
async def create_order(
    order: OrderDataCreateModel,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Create new order (B2C or B2B).
    """
    try:
        return await manager.create_order(order)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 📋 List All Orders
@router.get("/", response_model=List[OrderDataReadModel])
async def list_orders(
    skip: int = 0,
    limit: int = 10,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Get all orders with pagination.
    """
    try:
        return await manager.get_all_orders(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get Order by ID
@router.get("/{order_id}", response_model=OrderDataReadModel)
async def get_order(
    order_id: int,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Get full details of an order by ID.
    """
    try:
        return await manager.get_order_by_id(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update Order (Status)
@router.put("/{order_id}", response_model=OrderDataReadModel)
async def update_order(
    order_id: int,
    update_data: OrderDataUpdateModel,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Update order status.
    """
    try:
        return await manager.update_order(order_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete Order
@router.delete("/{order_id}")
async def delete_order(
    order_id: int,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Delete an order and its items.
    """
    try:
        await manager.delete_order(order_id)
        return {"status": "success", "deleted": True, "order_id": order_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
