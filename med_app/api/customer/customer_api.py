from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from ...schemas.customer.customer_schema import (
    CustomerDataCreateModel,
    CustomerDataReadModel,
    CustomerDataUpdateModel,
    LoginModel,
    LoginResponseModel,
)
from ...crud.customer.customer_manager import CustomerManager
from ...utils.get_db_manager import get_customer_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/customers", tags=["Customers"])

# 🧾 Register
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

# 🔐 Login
@router.post("/login", response_model=LoginResponseModel)
async def login_customer(
    login_data: LoginModel,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        customer = await manager.login_customer(login_data.email, login_data.password)
        return LoginResponseModel(
            customer_id=customer.customer_id,
            full_name=customer.full_name,
            email=customer.email
        )
    except NotFoundException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

# 👤 Get profile (simulate authentication)
@router.get("/me", response_model=CustomerDataReadModel)
async def get_my_profile(
    customer_id: int,  # Normally extracted from JWT
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.get_customer_by_id(customer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

# ✏️ Update profile
@router.put("/me", response_model=CustomerDataReadModel)
async def update_my_profile(
    customer_id: int,
    update_data: CustomerDataUpdateModel,
    manager: CustomerManager = Depends(get_customer_manager),
):
    try:
        return await manager.update_customer(customer_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

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

# 🗑️ Delete customer
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
