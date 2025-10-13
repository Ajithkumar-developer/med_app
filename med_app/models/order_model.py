from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from ..models.base_class import Base


class OrderTypeEnum(str, enum.Enum):
    B2C = "B2C"
    B2B = "B2B"


class OrderStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderDbModel(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    order_type = Column(Enum(OrderTypeEnum), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    retailer_id = Column(Integer, ForeignKey("retailers.retailer_id"), nullable=True)
    distributor_id = Column(Integer, ForeignKey("distributors.distributor_id"), nullable=True)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.PENDING)
    total_amount = Column(DECIMAL(10, 2), nullable=False)

    # relationships
    items = relationship("OrderItemDbModel", back_populates="order", cascade="all, delete")


class OrderItemDbModel(Base):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.medicine_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    # relationships
    order = relationship("OrderDbModel", back_populates="items")
