from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class DistributorInvoiceItemBaseModel(BaseModel):
    medicine_id: int
    quantity: int
    price: float
    subtotal: float


class DistributorInvoiceItemCreateModel(DistributorInvoiceItemBaseModel):
    pass


class DistributorInvoiceItemReadModel(DistributorInvoiceItemBaseModel):
    item_id: int

    class Config:
        orm_mode = True


class DistributorInvoiceBaseModel(BaseModel):
    distributor_id: int
    retailer_id: Optional[int]
    total_amount: float
    payment_method: Optional[str]
    notes: Optional[str]


class DistributorInvoiceCreateModel(DistributorInvoiceBaseModel):
    items: List[DistributorInvoiceItemCreateModel]


class DistributorInvoiceReadModel(DistributorInvoiceBaseModel):
    invoice_id: int
    invoice_number: str
    created_at: datetime
    items: Optional[List[DistributorInvoiceItemReadModel]]

    class Config:
        orm_mode = True
