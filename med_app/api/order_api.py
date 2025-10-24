from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from fastapi.responses import FileResponse
import os

from ..schemas.order_schema import OrderDataCreateModel, OrderDataReadModel, OrderDataUpdateModel
from ..crud.order_manager import OrderManager
from ..utils.get_db_manager import get_order_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderDataReadModel)
async def create_order(order: OrderDataCreateModel, manager: OrderManager = Depends(get_order_manager)):
    try:
        return await manager.create_order(order)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.get("/", response_model=List[OrderDataReadModel])
async def list_orders(skip: int = 0, limit: int = 10, manager: OrderManager = Depends(get_order_manager)):
    try:
        return await manager.get_all_orders(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/{order_id}", response_model=OrderDataReadModel)
async def get_order(order_id: int, manager: OrderManager = Depends(get_order_manager)):
    try:
        return await manager.get_order_by_id(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.put("/{order_id}", response_model=OrderDataReadModel)
async def update_order(order_id: int, update_data: OrderDataUpdateModel, manager: OrderManager = Depends(get_order_manager)):
    try:
        return await manager.update_order(order_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.delete("/{order_id}")
async def delete_order(order_id: int, manager: OrderManager = Depends(get_order_manager)):
    try:
        await manager.delete_order(order_id)
        return {"status": "success", "deleted": True, "order_id": order_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/user/{user_id}", response_model=List[OrderDataReadModel])
async def get_orders_by_user_id(user_id: int, skip: int = 0, limit: int = 10, manager: OrderManager = Depends(get_order_manager)):
    try:
        return await manager.get_orders_by_user_id(user_id, skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Added: Get Orders by Retailer ID
@router.get("/retailer/{retailer_id}", response_model=List[OrderDataReadModel])
async def get_orders_by_retailer_id(
    retailer_id: int,
    skip: int = 0,
    limit: int = 10,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Get all orders placed with a specific retailer.
    """
    try:
        return await manager.get_orders_by_retailer_id(retailer_id, skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/invoice/{order_id}", response_class=FileResponse)
async def download_invoice_pdf(order_id: int):
    file_path = f"invoices/invoice_{order_id}.pdf"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return FileResponse(path=file_path, filename=f"invoice_{order_id}.pdf", media_type="application/pdf")
