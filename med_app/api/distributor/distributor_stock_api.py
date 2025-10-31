from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from ...schemas.distributor.distributor_stock_schema import (
    DistributorStockCreateModel,
    DistributorStockReadModel,
    DistributorStockUpdateModel,
)
from ...crud.distributor.distributor_stock_manager import DistributorStockManager
from ...utils.get_db_manager import get_distributor_stock_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributor-stock", tags=["Distributor Stock"])

# ✅ Create Stock
@router.post("/", response_model=DistributorStockReadModel)
async def create_stock(
    stock: DistributorStockCreateModel,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        return await manager.create_stock(stock)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ✅ Get All Stock
@router.get("/", response_model=List[DistributorStockReadModel])
async def list_stock(
    skip: int = 0,
    limit: int = 10,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        return await manager.get_all_stock(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Get Stock by ID
@router.get("/{stock_id}", response_model=DistributorStockReadModel)
async def get_stock(
    stock_id: int,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        return await manager.get_stock_by_id(stock_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Update Stock
@router.put("/{stock_id}", response_model=DistributorStockReadModel)
async def update_stock(
    stock_id: int,
    update_data: DistributorStockUpdateModel,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        return await manager.update_stock(stock_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Delete Stock
@router.delete("/{stock_id}")
async def delete_stock(
    stock_id: int,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        await manager.delete_stock(stock_id)
        return {"status": "success", "deleted": True, "stock_id": stock_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ---------------- Get Stock by Distributor ID ----------------
@router.get("/{distributor_id}", response_model=List[DistributorStockReadModel])
async def get_stock_by_distributor(
    distributor_id: int,
    manager: DistributorStockManager = Depends(get_distributor_stock_manager),
):
    try:
        stocks = await manager.get_stock_by_distributor(distributor_id)
        return stocks
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")