from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class DistributorBase(BaseModel):
    company_name: str
    contact_person: str
    gst_number: str
    license_number: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: EmailStr
    password_hash: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

class DistributorDataCreateModel(DistributorBase):
    pass

class DistributorDataReadModel(DistributorBase):
    distributor_id: int
    registration_date: datetime

    class Config:
        orm_mode = True

class DistributorDataUpdateModel(BaseModel):
    company_name: Optional[str] = None
    contact_person: Optional[str] = None
    gst_number: Optional[str] = None
    license_number: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

class DistributorLoginRequest(BaseModel):
    email: EmailStr
    password: str

class DistributorLoginResponse(BaseModel):
    distributor_id: int
    company_name: str
    email: EmailStr
