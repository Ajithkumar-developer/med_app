from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class DistributorNotificationBaseModel(BaseModel):
    title: str
    message: str
    type: str
    distributor_id: Optional[int]

class DistributorNotificationCreateModel(DistributorNotificationBaseModel):
    pass

class DistributorNotificationReadModel(DistributorNotificationBaseModel):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        orm_mode = True
