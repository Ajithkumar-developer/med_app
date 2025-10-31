from datetime import datetime
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

# Order status enum
class DistributorOrderStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class DistributorOrderDbModel(Base):
    __tablename__ = "distributor_orders"

    order_id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, nullable=False)
    retailer_id = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(DistributorOrderStatusEnum), default=DistributorOrderStatusEnum.PENDING)
    total_amount = Column(DECIMAL(10,2), nullable=False)


class DistributorOrderItemDbModel(Base):
    __tablename__ = "distributor_order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    medicine_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)
