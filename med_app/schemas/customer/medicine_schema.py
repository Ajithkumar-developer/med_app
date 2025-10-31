from typing import Optional
from pydantic import BaseModel


class MedicineBase(BaseModel):
    name: str
    generic_name: Optional[str] = None
    category: str
    dosage_form: str
    strength: str
    manufacturer: Optional[str] = None
    prescription_required: bool = False


class MedicineDataCreateModel(MedicineBase):
    pass


class MedicineDataReadModel(MedicineBase):
    medicine_id: int

    class Config:
        orm_mode = True


class MedicineDataUpdateModel(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    manufacturer: Optional[str] = None
    prescription_required: Optional[bool] = None
