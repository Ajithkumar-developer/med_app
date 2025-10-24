import asyncio
import enum
from datetime import datetime
from sqlalchemy import (
    DECIMAL, Boolean, Column, Date, DateTime, Enum,
    ForeignKey, Integer, String
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, relationship

# ✅ Async SQLite Database URL
DATABASE_URL = "sqlite+aiosqlite:///./medical.db"

# ✅ Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# ✅ Declarative base for all models
Base = declarative_base()

# --------------------------------------------------------------------------
# ENUMS
# --------------------------------------------------------------------------

class GenderEnum(str, enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class OrderStatusEnum(str, enum.Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

# --------------------------------------------------------------------------
# MODELS
# --------------------------------------------------------------------------

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

    orders = relationship("OrderDbModel", back_populates="customer")


# class RetailerDbModel(Base):
#     __tablename__ = "retailers"

#     retailer_id = Column(Integer, primary_key=True, index=True)
#     shop_name = Column(String, nullable=True)
#     owner_name = Column(String, nullable=True)
#     gst_number = Column(String, nullable=True)
#     license_number = Column(String, nullable=True)
#     phone_number = Column(String, nullable=True, unique=True)
#     email = Column(String, nullable=False, unique=True)
#     password_hash = Column(String, nullable=False)
#     address_line1 = Column(String, nullable=True)
#     address_line2 = Column(String, nullable=True)
#     city = Column(String, nullable=True)
#     state = Column(String, nullable=True)
#     zip_code = Column(String, nullable=True)
#     gps_latitude = Column(DECIMAL(10, 7), nullable=True)
#     gps_longitude = Column(DECIMAL(10, 7), nullable=True)
#     registration_date = Column(DateTime, default=datetime.utcnow)

#     # ✅ Relationship
#     stock_items = relationship("RetailerStockDbModel", back_populates="retailer", cascade="all, delete-orphan")


class RetailerDbModel(Base):
    __tablename__ = "retailers"

    retailer_id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    license_number = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)
    address_line1 = Column(String, nullable=True)
    address_line2 = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    gps_latitude = Column(DECIMAL(10, 7), nullable=True)
    gps_longitude = Column(DECIMAL(10, 7), nullable=True)
    # registration_date = Column(DateTime, default=datetime.utcnow)

    stock_items = relationship("RetailerStockDbModel", back_populates="retailer", cascade="all, delete-orphan")

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

    distributor_orders = relationship("OrderDbModel", back_populates="distributor")
    stock_items = relationship("DistributorStockDbModel", back_populates="distributor")


class MedicineDbModel(Base):
    __tablename__ = "medicines"

    medicine_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    generic_name = Column(String, nullable=True)
    category = Column(String, nullable=False)
    dosage_form = Column(String, nullable=False)
    strength = Column(String, nullable=False)
    manufacturer = Column(String, nullable=True)
    prescription_required = Column(Boolean, default=False)

    order_items = relationship("OrderItemDbModel", back_populates="medicine")
    retailer_stock = relationship("RetailerStockDbModel", back_populates="medicine")


class OrderDbModel(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"), nullable=True)
    retailer_id = Column(Integer, ForeignKey("retailers.retailer_id"), nullable=True)
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

class RetailerStockDbModel(Base):
    __tablename__ = "retailer_stock"

    stock_id = Column(Integer, primary_key=True, index=True)
    retailer_id = Column(Integer, ForeignKey("retailers.retailer_id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.medicine_id"), nullable=False)
    batch_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    expiry_date = Column(Date, nullable=False)

    # ✅ Relationships
    retailer = relationship("RetailerDbModel", back_populates="stock_items")
    medicine = relationship("MedicineDbModel")  # Optional: Add back_populates if Medicine has reverse relation


class DistributorStockDbModel(Base):
    __tablename__ = "distributor_stock"

    stock_id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, ForeignKey("distributors.distributor_id", ondelete="CASCADE"), nullable=False)
    medicine_id = Column(Integer, ForeignKey("medicines.medicine_id"), nullable=False)
    batch_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    expiry_date = Column(Date, nullable=False)

    # Relationships
    distributor = relationship("DistributorDbModel", back_populates="stock_items")
    medicine = relationship("MedicineDbModel")



# --------------------------------------------------------------------------
# DB Initialization
# --------------------------------------------------------------------------

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully.")
    await engine.dispose()

# --------------------------------------------------------------------------
# Run directly
# --------------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(init_db())
