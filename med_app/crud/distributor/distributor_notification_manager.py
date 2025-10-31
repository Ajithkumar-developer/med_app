from datetime import datetime
from typing import List, Optional
from ...models.distributor.distributor_notification_model import DistributorNotificationDbModel
from ...schemas.distributor.distributor_notification_schema import DistributorNotificationCreateModel
from ...db.base.database_manager import DatabaseManager
from ...exceptions.custom_exceptions import NotFoundException
from ...utils.logger import get_logger

logger = get_logger(__name__)

class DistributorNotificationManager:
    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager

    # ➕ Create notification
    async def create_notification(self, data: DistributorNotificationCreateModel):
        logger.info(f"Creating distributor notification: {data.title}")
        notif_dict = data.dict()
        notif_dict["created_at"] = datetime.utcnow()
        return await self.database_manager.create(DistributorNotificationDbModel, notif_dict)

    # 📋 List notifications (optionally filtered by distributor)
    async def list_notifications(self, distributor_id: Optional[int] = None) -> List[DistributorNotificationDbModel]:
        filters = {}
        if distributor_id:
            filters["distributor_id"] = distributor_id
        return await self.database_manager.read(DistributorNotificationDbModel, filters=filters)

    # ✅ Mark notification as read
    async def mark_as_read(self, notification_id: int):
        notification_list = await self.database_manager.read(DistributorNotificationDbModel, {"id": notification_id})
        if not notification_list:
            raise NotFoundException(f"Notification ID {notification_id} not found")

        notification = notification_list[0]
        await self.database_manager.update(DistributorNotificationDbModel, {"id": notification_id}, {"is_read": True})
        return notification

    # ❌ Clear (delete) notification
    async def clear_notification(self, notification_id: int):
        notification_list = await self.database_manager.read(DistributorNotificationDbModel, {"id": notification_id})
        if not notification_list:
            raise NotFoundException(f"Notification ID {notification_id} not found")
        await self.database_manager.delete(DistributorNotificationDbModel, {"id": notification_id})
        return {"message": "Notification cleared"}
