from datetime import date
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Optional
from ...models.distributor.distributor_order_model import DistributorOrderStatusEnum

class DistributorOrderItemBase(BaseModel):
    medicine_id: int
    quantity: int = Field(..., gt=0)
    price: Decimal

class DistributorOrderItemCreate(DistributorOrderItemBase):
    pass

class DistributorOrderItemRead(DistributorOrderItemBase):
    order_item_id: int
    class Config:
        orm_mode = True

class DistributorOrderBase(BaseModel):
    distributor_id: int
    retailer_id: int
    total_amount: Decimal

class DistributorOrderCreate(DistributorOrderBase):
    items: List[DistributorOrderItemCreate]

class DistributorOrderRead(DistributorOrderBase):
    order_id: int
    status: DistributorOrderStatusEnum
    items: List[DistributorOrderItemRead]
    class Config:
        orm_mode = True

class DistributorOrderUpdate(BaseModel):
    status: Optional[DistributorOrderStatusEnum] = None
