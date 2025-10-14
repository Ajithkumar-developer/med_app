from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from ..models.customer_model import GenderEnum

class CustomerBase(BaseModel):
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
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

class CustomerDataCreateModel(CustomerBase):
    pass

class CustomerDataReadModel(CustomerBase):
    customer_id: int
    registration_date: datetime

    class Config:
        orm_mode = True

class CustomerDataUpdateModel(BaseModel):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[GenderEnum] = None
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

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class LoginResponseModel(BaseModel):
    customer_id: int
    full_name: str
    email: EmailStr
