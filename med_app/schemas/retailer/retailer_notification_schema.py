from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class RetailerNotificationBaseModel(BaseModel):
    title: str
    message: str
    type: str
    retailer_id: Optional[int]


class RetailerNotificationCreateModel(RetailerNotificationBaseModel):
    pass


class RetailerNotificationReadModel(RetailerNotificationBaseModel):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
