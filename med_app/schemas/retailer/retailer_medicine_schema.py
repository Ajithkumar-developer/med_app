from datetime import date
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class RetailerMedicineBase(BaseModel):
    retailer_id: int

    # Medicine-specific fields
    name: str
    generic_name: Optional[str] = None
    category: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None

    # Inventory fields
    batch_number: Optional[str] = None
    quantity: int # = Field(..., gt=0)
    price: Decimal
    expiry_date: date


class RetailerMedicineCreateModel(RetailerMedicineBase):
    """Used when creating a new retailer medicine record."""
    pass


class RetailerMedicineReadModel(RetailerMedicineBase):
    """Used when reading a retailer medicine record."""
    retailer_medicine_id: int

    class Config:
        orm_mode = True


class RetailerMedicineUpdateModel(BaseModel):
    """Used when updating a retailer medicine record."""
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    batch_number: Optional[str] = None
    quantity: Optional[int] = Field(None, gt=0)
    price: Optional[Decimal] = None
    expiry_date: Optional[date] = None
