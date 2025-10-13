from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class DistributorStockBase(BaseModel):
    distributor_id: int
    medicine_id: int
    batch_number: Optional[str] = None
    quantity: int = Field(..., gt=0)
    price: Decimal
    expiry_date: date


class DistributorStockCreateModel(DistributorStockBase):
    pass


class DistributorStockReadModel(DistributorStockBase):
    stock_id: int

    class Config:
        orm_mode = True


class DistributorStockUpdateModel(BaseModel):
    batch_number: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = None
    expiry_date: Optional[date] = None
