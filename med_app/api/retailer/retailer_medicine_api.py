from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from ...schemas.retailer.retailer_medicine_schema import (
    RetailerMedicineCreateModel,
    RetailerMedicineReadModel,
    RetailerMedicineUpdateModel,
)
from ...crud.retailer.retailer_medicine_manager import RetailerMedicineManager
from ...utils.get_db_manager import get_retailer_medicine_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/products", tags=["Retailer Products"])

# 📋 List products
@router.get("/", response_model=List[RetailerMedicineReadModel])
async def list_products(
    retailer_id: int = Query(..., description="Filter products by retailer ID"),
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 10,
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.list_products(retailer_id, search, category, sort_by, skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🧾 Add new product
@router.post("/", response_model=RetailerMedicineReadModel)
async def add_product(
    data: RetailerMedicineCreateModel,
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.create_product(data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# ⚠️ Low-stock items
@router.get("/low-stock", response_model=List[RetailerMedicineReadModel])
async def get_low_stock(
    retailer_id: int = Query(..., description="Filter low stock by retailer ID"),
    threshold: int = 10,
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.get_low_stock_products(retailer_id, threshold)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ❌ No-stock items
@router.get("/no-stock", response_model=List[RetailerMedicineReadModel])
async def get_no_stock(
    retailer_id: int = Query(..., description="Filter out-of-stock by retailer ID"),
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.get_no_stock_products(retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get one product
@router.get("/{product_id}", response_model=RetailerMedicineReadModel)
async def get_product(
    product_id: int,
    retailer_id: int = Query(..., description="Filter product by retailer ID"),
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.get_product_by_id(retailer_id, product_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update product
@router.put("/{product_id}", response_model=RetailerMedicineReadModel)
async def update_product(
    product_id: int,
    update_data: RetailerMedicineUpdateModel,
    retailer_id: int = Query(..., description="Filter product by retailer ID"),
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.update_product(retailer_id, product_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete product
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    retailer_id: int = Query(..., description="Filter product by retailer ID"),
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        await manager.delete_product(retailer_id, product_id)
        return {"status": "success", "deleted": True, "product_id": product_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📦 Update stock
@router.put("/{product_id}/stock")
async def update_stock(
    product_id: int,
    quantity: int,
    retailer_id: int = Query(..., description="Filter product by retailer ID"),
    manager: RetailerMedicineManager = Depends(get_retailer_medicine_manager),
):
    try:
        return await manager.update_stock(retailer_id, product_id, quantity)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
