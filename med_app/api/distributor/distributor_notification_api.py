from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from ...schemas.distributor.distributor_notification_schema import (
    DistributorNotificationCreateModel,
    DistributorNotificationReadModel,
)
from ...crud.distributor.distributor_notification_manager import DistributorNotificationManager
from ...utils.get_db_manager import get_distributor_notification_manager
from ...exceptions.custom_exceptions import NotFoundException

router = APIRouter(prefix="/distributor-notifications", tags=["Distributor Notifications"])

# ➕ Create new notification
@router.post("", response_model=DistributorNotificationReadModel)
async def create_notification(
    data: DistributorNotificationCreateModel,
    manager: DistributorNotificationManager = Depends(get_distributor_notification_manager),
):
    try:
        return await manager.create_notification(data)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# 📋 List all notifications
@router.get("", response_model=List[DistributorNotificationReadModel])
async def list_notifications(
    distributor_id: Optional[int] = Query(None),
    manager: DistributorNotificationManager = Depends(get_distributor_notification_manager),
):
    try:
        return await manager.list_notifications(distributor_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")


# ✅ Mark notification as read
@router.put("/{notification_id}/read", response_model=DistributorNotificationReadModel)
async def mark_as_read(
    notification_id: int,
    manager: DistributorNotificationManager = Depends(get_distributor_notification_manager),
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
    manager: DistributorNotificationManager = Depends(get_distributor_notification_manager),
):
    try:
        return await manager.clear_notification(notification_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")
