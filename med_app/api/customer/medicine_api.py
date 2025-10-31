from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from ...schemas.customer.medicine_schema import (
    MedicineDataCreateModel,
    MedicineDataReadModel,
    MedicineDataUpdateModel,
)
from ...crud.customer.medicine_manager import MedicineManager
from ...utils.get_db_manager import get_medicine_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/medicines", tags=["Medicines"])


# 🧾 Create Medicine
@router.post("/", response_model=MedicineDataReadModel)
async def create_medicine(
    medicine: MedicineDataCreateModel,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        return await manager.create_medicine(medicine)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# 📋 Get All Medicines
@router.get("/", response_model=List[MedicineDataReadModel])
async def list_medicines(
    skip: int = 0,
    limit: int = 10,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        return await manager.get_all_medicines(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔎 Search Medicines
@router.get("/search", response_model=List[MedicineDataReadModel])
async def search_medicines(
    name: Optional[str] = None,
    generic_name: Optional[str] = None,
    category: Optional[str] = None,
    manufacturer: Optional[str] = None,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        results = await manager.search_medicines(
            name=name,
            generic_name=generic_name,
            category=category,
            manufacturer=manufacturer,
        )
        if not results:
            raise HTTPException(status_code=404, detail="No medicines found.")
        return results
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get Medicine by ID
@router.get("/{medicine_id}", response_model=MedicineDataReadModel)
async def get_medicine(
    medicine_id: int,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        return await manager.get_medicine_by_id(medicine_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update Medicine
@router.put("/{medicine_id}", response_model=MedicineDataReadModel)
async def update_medicine(
    medicine_id: int,
    update_data: MedicineDataUpdateModel,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        return await manager.update_medicine(medicine_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete Medicine
@router.delete("/{medicine_id}")
async def delete_medicine(
    medicine_id: int,
    manager: MedicineManager = Depends(get_medicine_manager),
):
    try:
        await manager.delete_medicine(medicine_id)
        return {"status": "success", "deleted": True, "medicine_id": medicine_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
