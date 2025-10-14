from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from ..models.base_class import Base

class DistributorDbModel(Base):
    __tablename__ = "distributors"

    distributor_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=True)
    contact_person = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
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

    stock_items = relationship("DistributorStockDbModel", back_populates="distributor")
