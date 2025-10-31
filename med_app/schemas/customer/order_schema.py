from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from ...models.customer.order_model import OrderStatusEnum


class OrderItemBase(BaseModel):
    medicine_id: int
    quantity: int = Field(..., gt=0)
    price: Decimal


class OrderItemCreateModel(OrderItemBase):
    pass


class OrderItemReadModel(OrderItemBase):
    order_item_id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    customer_id: Optional[int] = None
    retailer_id: Optional[int] = None
    total_amount: Decimal


class OrderDataCreateModel(OrderBase):
    items: List[OrderItemCreateModel]


class OrderDataReadModel(OrderBase):
    order_id: int
    order_date: datetime
    status: OrderStatusEnum
    items: List[OrderItemReadModel]

    class Config:
        orm_mode = True


class OrderDataUpdateModel(BaseModel):
    status: Optional[OrderStatusEnum] = None
