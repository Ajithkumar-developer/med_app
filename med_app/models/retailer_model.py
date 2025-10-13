from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from ..models.base_class import Base
# from .retailer_stock_model import RetailerStockDbModel


class RetailerDbModel(Base):
    __tablename__ = "retailers"

    retailer_id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    gst_number = Column(String, nullable=False)
    license_number = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=True, unique=True)
    password_hash = Column(String, nullable=False)
    address_line1 = Column(String, nullable=False)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    gps_latitude = Column(DECIMAL(10, 7), nullable=True)
    gps_longitude = Column(DECIMAL(10, 7), nullable=True)
    registration_date = Column(DateTime, default=datetime.utcnow)

    # ✅ Relationship
    stock_items = relationship("RetailerStockDbModel", back_populates="retailer", cascade="all, delete-orphan")
