from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class RetailerBase(BaseModel):
    shop_name: str
    owner_name: str
    gst_number: str
    license_number: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    email: Optional[EmailStr] = None
    password_hash: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None

class RetailerDataCreateModel(RetailerBase):
    pass

class RetailerDataReadModel(RetailerBase):
    retailer_id: int
    registration_date: datetime

    class Config:
        orm_mode = True

class RetailerDataUpdateModel(BaseModel):
    shop_name: Optional[str] = None
    owner_name: Optional[str] = None
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

class RetailerLoginRequest(BaseModel):
    email: EmailStr
    password: str

class RetailerLoginResponse(BaseModel):
    retailer_id: int
    shop_name: str
    email: EmailStr
