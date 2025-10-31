from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from ...models.retailer.retailer_order_model import OrderStatusEnum


class RetailerOrderItemCreateModel(BaseModel):
    medicine_id: int
    quantity: int
    price: Decimal


class RetailerOrderCreateModel(BaseModel):
    retailer_id: int
    distributor_id: int
    total_amount: Decimal
    items: List[RetailerOrderItemCreateModel]


class RetailerOrderItemReadModel(RetailerOrderItemCreateModel):
    order_item_id: int
    order_id: int

    class Config:
        orm_mode = True


class RetailerOrderReadModel(BaseModel):
    order_id: int
    retailer_id: Optional[int]
    distributor_id: Optional[int]
    order_date: datetime
    status: OrderStatusEnum
    total_amount: Decimal
    items: List[RetailerOrderItemReadModel] = []

    class Config:
        orm_mode = True


class RetailerOrderUpdateModel(BaseModel):
    status: OrderStatusEnum
