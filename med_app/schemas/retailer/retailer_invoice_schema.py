from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class RetailerInvoiceItemBaseModel(BaseModel):
    medicine_id: int
    quantity: int
    price: float
    subtotal: float


class RetailerInvoiceItemCreateModel(RetailerInvoiceItemBaseModel):
    pass


class RetailerInvoiceItemReadModel(RetailerInvoiceItemBaseModel):
    item_id: int

    class Config:
        orm_mode = True


class RetailerInvoiceBaseModel(BaseModel):
    retailer_id: int
    customer_id: Optional[int]
    total_amount: float
    payment_method: Optional[str]
    notes: Optional[str]


class RetailerInvoiceCreateModel(RetailerInvoiceBaseModel):
    items: List[RetailerInvoiceItemCreateModel]


class RetailerInvoiceReadModel(RetailerInvoiceBaseModel):
    invoice_id: int
    invoice_number: str
    created_at: datetime
    items: Optional[List[RetailerInvoiceItemReadModel]]

    class Config:
        orm_mode = True
