from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, Enum
from datetime import datetime
import enum
from ..models.base_class import Base


class OrderStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderDbModel(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, nullable=True)
    retailer_id = Column(Integer, nullable=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    total_amount = Column(DECIMAL(10, 2), nullable=False)


class OrderItemDbModel(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False)
    medicine_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
