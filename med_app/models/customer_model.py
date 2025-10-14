from sqlalchemy import Column, Integer, String, Date, Enum, DECIMAL, DateTime
from datetime import datetime
import enum
from ..models.base_class import Base

class GenderEnum(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class CustomerDbModel(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    phone_number = Column(String, nullable=True, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    gps_latitude = Column(DECIMAL(10, 7), nullable=True)
    gps_longitude = Column(DECIMAL(10, 7), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)
