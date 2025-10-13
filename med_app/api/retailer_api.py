from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..schemas.retailer_schema import (
    RetailerDataCreateModel,
    RetailerDataReadModel,
    RetailerDataUpdateModel,
)
from ..crud.retailer_manager import RetailerManager
from ..utils.get_db_manager import get_retailer_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailers", tags=["Retailers"])


# 🧾 Create Retailer
@router.post("/", response_model=RetailerDataReadModel)
async def create_retailer(
    retailer: RetailerDataCreateModel,
    manager: RetailerManager = Depends(get_retailer_manager),
):
    try:
        return await manager.create_retailer(retailer)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 📋 List all retailers
@router.get("/", response_model=List[RetailerDataReadModel])
async def list_retailers(
    skip: int = 0,
    limit: int = 10,
    manager: RetailerManager = Depends(get_retailer_manager),
):
    try:
        return await manager.get_all_retailers(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get retailer by ID
@router.get("/{retailer_id}", response_model=RetailerDataReadModel)
async def get_retailer(
    retailer_id: int,
    manager: RetailerManager = Depends(get_retailer_manager),
):
    try:
        return await manager.get_retailer_by_id(retailer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update retailer
@router.put("/{retailer_id}", response_model=RetailerDataReadModel)
async def update_retailer(
    retailer_id: int,
    update_data: RetailerDataUpdateModel,
    manager: RetailerManager = Depends(get_retailer_manager),
):
    try:
        return await manager.update_retailer(retailer_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete retailer
@router.delete("/{retailer_id}")
async def delete_retailer(
    retailer_id: int,
    manager: RetailerManager = Depends(get_retailer_manager),
):
    try:
        await manager.delete_retailer(retailer_id)
        return {"status": "success", "deleted": True, "retailer_id": retailer_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
