from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from ..schemas.retailer_stock_schema import (
    RetailerStockCreateModel,
    RetailerStockReadModel,
    RetailerStockUpdateModel,
)
from ..crud.retailer_stock_manager import RetailerStockManager
from ..utils.get_db_manager import get_retailer_stock_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailer-stock", tags=["Retailer Stock"])


# 🧾 Create Stock Entry
@router.post("/", response_model=RetailerStockReadModel)
async def create_stock(
    stock: RetailerStockCreateModel,
    manager: RetailerStockManager = Depends(get_retailer_stock_manager),
):
    """
    Add a new medicine stock entry for a retailer.
    """
    try:
        return await manager.create_stock(stock)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 📋 Get All Stock
@router.get("/", response_model=List[RetailerStockReadModel])
async def list_stock(
    skip: int = 0,
    limit: int = 10,
    manager: RetailerStockManager = Depends(get_retailer_stock_manager),
):
    """
    Get paginated list of all stock entries.
    """
    try:
        return await manager.get_all_stock(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get Stock by ID
@router.get("/{stock_id}", response_model=RetailerStockReadModel)
async def get_stock(
    stock_id: int,
    manager: RetailerStockManager = Depends(get_retailer_stock_manager),
):
    """
    Get stock details by ID.
    """
    try:
        return await manager.get_stock_by_id(stock_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update Stock
@router.put("/{stock_id}", response_model=RetailerStockReadModel)
async def update_stock(
    stock_id: int,
    update_data: RetailerStockUpdateModel,
    manager: RetailerStockManager = Depends(get_retailer_stock_manager),
):
    """
    Update stock details (quantity, price, expiry, etc.).
    """
    try:
        return await manager.update_stock(stock_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete Stock
@router.delete("/{stock_id}")
async def delete_stock(
    stock_id: int,
    manager: RetailerStockManager = Depends(get_retailer_stock_manager),
):
    """
    Delete a retailer stock entry.
    """
    try:
        await manager.delete_stock(stock_id)
        return {"status": "success", "deleted": True, "stock_id": stock_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
