from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ..schemas.customer_schema import (
    CustomerDataCreateModel,
    CustomerDataReadModel,
    CustomerDataUpdateModel,
)
from ..crud.customer_manager import CustomerManager
from ..utils.get_db_manager import get_customer_manager
from ..exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/customers", tags=["Customers"])


# 🧾 Create Customer
@router.post("/", response_model=CustomerDataReadModel)
async def create_customer(
    customer: CustomerDataCreateModel,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.create_customer(customer)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# 📋 List all customers
@router.get("/", response_model=List[CustomerDataReadModel])
async def list_customers(
    skip: int = 0,
    limit: int = 10,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.get_all_customers(skip, limit)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🔍 Get single customer
@router.get("/{customer_id}", response_model=CustomerDataReadModel)
async def get_customer(
    customer_id: int,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.get_customer_by_id(customer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✏️ Update Customer
@router.put("/{customer_id}", response_model=CustomerDataReadModel)
async def update_customer(
    customer_id: int,
    update_data: CustomerDataUpdateModel,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.update_customer(customer_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 🗑️ Delete Customer
@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: int,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        await manager.delete_customer(customer_id)
        return {"status": "success", "deleted": True, "customer_id": customer_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
