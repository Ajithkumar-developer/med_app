from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.exc import SQLAlchemyError
from ...schemas.distributor.distributor_order_schema import DistributorOrderCreate, DistributorOrderRead, DistributorOrderUpdate
from ...crud.distributor.distributor_order_manager import DistributorOrderManager
from ...utils.get_db_manager import get_distributor_order_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributor-orders", tags=["Distributor Orders"])

@router.post("/")
async def create_order(order: DistributorOrderCreate, manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    try:
        return await manager.create_order(order)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/")
async def get_all_orders(manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    """
    Get all distributor orders (for all distributors)
    """
    try:
        return await manager.get_all_orders()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/{distributor_id}")
async def get_orders_by_distributor(distributor_id: int, manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    try:
        return await manager.get_orders_by_distributor(distributor_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


@router.get("/{order_id}")
async def get_order_by_id(order_id: int, manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    """
    Get a specific order by order_id
    """
    try:
        return await manager.get_order_by_id(order_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.put("/{order_id}")
async def update_order_status(order_id: int, update_data: DistributorOrderUpdate, manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    try:
        return await manager.update_order_status(order_id, update_data)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

@router.delete("/{order_id}")
async def delete_order(order_id: int, manager: DistributorOrderManager = Depends(get_distributor_order_manager)):
    try:
        await manager.delete_order(order_id)
        return {"status": "success", "deleted": True, "order_id": order_id}
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
