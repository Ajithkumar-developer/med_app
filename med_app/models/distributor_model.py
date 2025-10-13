from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from ..models.base_class import Base
# from .distributor_stock_model import DistributorStockDbModel


class DistributorDbModel(Base):
    __tablename__ = "distributors"

    distributor_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    contact_person = Column(String, nullable=False)
    gst_number = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    gps_latitude = Column(DECIMAL(10, 7), nullable=True)
    gps_longitude = Column(DECIMAL(10, 7), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)

    stock_items = relationship("DistributorStockDbModel", back_populates="distributor")
