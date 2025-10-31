from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from ...schemas.retailer.retailer_notification_schema import (
    RetailerNotificationCreateModel,
    RetailerNotificationReadModel,
)
from ...crud.retailer.retailer_notification_manager import RetailerNotificationManager
from ...utils.get_db_manager import get_retailer_notification_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/retailer-notifications", tags=["Retailer Notifications"])

# ➕ Create new notification
@router.post("", response_model=RetailerNotificationReadModel)
async def create_notification(
    data: RetailerNotificationCreateModel,
    manager: RetailerNotificationManager = Depends(get_retailer_notification_manager),
):
    try:
        return await manager.create_notification(data)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📋 List all notifications
@router.get("", response_model=List[RetailerNotificationReadModel])
async def list_notifications(
    retailer_id: Optional[int] = Query(None),
    manager: RetailerNotificationManager = Depends(get_retailer_notification_manager),
):
    try:
        return await manager.list_notifications(retailer_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Mark notification as read
@router.put("/{notification_id}/read", response_model=RetailerNotificationReadModel)
async def mark_as_read(
    notification_id: int,
    manager: RetailerNotificationManager = Depends(get_retailer_notification_manager),
):
    try:
        return await manager.mark_as_read(notification_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ❌ Clear (delete) notification
@router.delete("/{notification_id}")
async def clear_notification(
    notification_id: int,
    manager: RetailerNotificationManager = Depends(get_retailer_notification_manager),
):
    try:
        return await manager.clear_notification(notification_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
