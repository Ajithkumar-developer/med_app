from datetime import datetime
from typing import List, Optional
from ...models.retailer.retailer_notification_model import RetailerNotificationDbModel
from ...schemas.retailer.retailer_notification_schema import RetailerNotificationCreateModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)


class RetailerNotificationManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # ➕ Create notification
    async def create_notification(self, data: RetailerNotificationCreateModel):
        logger.info(f"Creating notification: {data.title}")
        notif_dict = data.dict()
        notif_dict["created_at"] = datetime.utcnow()
        return await self.database_manager.create(RetailerNotificationDbModel, notif_dict)

    # 📋 List notifications (optionally filtered by retailer)
    async def list_notifications(self, retailer_id: Optional[int] = None) -> List[RetailerNotificationDbModel]:
        filters = {}
        if retailer_id:
            filters["retailer_id"] = retailer_id
        return await self.database_manager.read(RetailerNotificationDbModel, filters=filters)

    # ✅ Mark notification as read
    async def mark_as_read(self, notification_id: int):
        notification_list = await self.database_manager.read(RetailerNotificationDbModel, {"id": notification_id})
        if not notification_list:
            raise NotFoundException(f"Notification ID {notification_id} not found")

        notification = notification_list[0]
        await self.database_manager.update(RetailerNotificationDbModel, {"id": notification_id}, {"is_read": True})
        return notification

    # ❌ Clear (delete) notification
    async def clear_notification(self, notification_id: int):
        notification_list = await self.database_manager.read(RetailerNotificationDbModel, {"id": notification_id})
        if not notification_list:
            raise NotFoundException(f"Notification ID {notification_id} not found")
        await self.database_manager.delete(RetailerNotificationDbModel, {"id": notification_id})
        return {"message": "Notification cleared"}
