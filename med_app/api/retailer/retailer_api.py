from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from ...schemas.retailer.retailer_schema import (
    RetailerDataCreateModel, RetailerDataReadModel,
    RetailerDataUpdateModel, RetailerLoginRequest, RetailerLoginResponse
)
from ...crud.retailer.retailer_manager import RetailerManager
from ...utils.get_db_manager import get_retailer_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailers", tags=["Retailers"])

@router.post("/", response_model=RetailerDataReadModel)
async def register_retailer(retailer: RetailerDataCreateModel, manager: RetailerManager = Depends(get_retailer_manager)):
    try:
        return await manager.create_retailer(retailer)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=RetailerLoginResponse)
async def login_retailer(credentials: RetailerLoginRequest, manager: RetailerManager = Depends(get_retailer_manager)):
    try:
        retailer = await manager.login(credentials)
        return RetailerLoginResponse(
            retailer_id=retailer.retailer_id,
            shop_name=retailer.shop_name,
            email=retailer.email,
        )
    except NotFoundException as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/", response_model=List[RetailerDataReadModel])
async def list_retailers(skip: int = 0, limit: int = 10, manager: RetailerManager = Depends(get_retailer_manager)):
    return await manager.get_all_retailers(skip, limit)

@router.get("/{retailer_id}", response_model=RetailerDataReadModel)
async def get_retailer(retailer_id: int, manager: RetailerManager = Depends(get_retailer_manager)):
    try:
        return await manager.get_retailer_by_id(retailer_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{retailer_id}", response_model=RetailerDataReadModel)
async def update_retailer(retailer_id: int, update_data: RetailerDataUpdateModel, manager: RetailerManager = Depends(get_retailer_manager)):
    return await manager.update_retailer(retailer_id, update_data)

@router.delete("/{retailer_id}")
async def delete_retailer(retailer_id: int, manager: RetailerManager = Depends(get_retailer_manager)):
    await manager.delete_retailer(retailer_id)
    return {"status": "success", "deleted": True, "retailer_id": retailer_id}


@router.get("/zip/{zip_code}", response_model=List[RetailerDataReadModel])
async def get_retailers_by_zip_code(zip_code: str, manager: RetailerManager = Depends(get_retailer_manager)):
    try:
        return await manager.get_retailers_by_zip_code(zip_code)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
