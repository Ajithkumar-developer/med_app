from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
from ...schemas.retailer.retailer_order_schema import (
    RetailerOrderCreateModel,
    RetailerOrderReadModel,
    RetailerOrderUpdateModel
)
from ...crud.retailer.retailer_order_manager import RetailerOrderManager
from ...utils.get_db_manager import get_retailer_order_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailer-orders", tags=["Retailer Orders"])

@router.post("/", response_model=RetailerOrderReadModel)
async def place_order(data: RetailerOrderCreateModel, manager: RetailerOrderManager = Depends(get_retailer_order_manager)):
    try:
        return await manager.create_order(data)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/{order_id}", response_model=RetailerOrderReadModel)
async def get_order(order_id: int, manager: RetailerOrderManager = Depends(get_retailer_order_manager)):
    try:
        return await manager.get_order_by_id(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/", response_model=List[RetailerOrderReadModel])
async def list_orders(
    retailer_id: Optional[int] = Query(None),
    distributor_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    manager: RetailerOrderManager = Depends(get_retailer_order_manager),
):
    try:
        return await manager.list_orders(retailer_id, distributor_id, status, start_date, end_date)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/retailer/{retailer_id}", response_model=List[RetailerOrderReadModel])
async def list_orders_by_retailer(
    retailer_id: int,
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    manager: RetailerOrderManager = Depends(get_retailer_order_manager),
):
    try:
        return await manager.list_orders(retailer_id=retailer_id, status=status, start_date=start_date, end_date=end_date)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.get("/distributor/{distributor_id}", response_model=List[RetailerOrderReadModel])
async def list_orders_by_distributor(
    distributor_id: int,
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    manager: RetailerOrderManager = Depends(get_retailer_order_manager),
):
    try:
        return await manager.list_orders(distributor_id=distributor_id, status=status, start_date=start_date, end_date=end_date)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.put("/{order_id}", response_model=RetailerOrderReadModel)
async def update_order(order_id: int, update_data: RetailerOrderUpdateModel, manager: RetailerOrderManager = Depends(get_retailer_order_manager)):
    try:
        return await manager.update_order_status(order_id, update_data.status)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.delete("/{order_id}")
async def delete_order(order_id: int, manager: RetailerOrderManager = Depends(get_retailer_order_manager)):
    try:
        await manager.delete_order(order_id)
        return {"status": "success", "deleted": True, "order_id": order_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
