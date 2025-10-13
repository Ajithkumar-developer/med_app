from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Date
from sqlalchemy.orm import relationship
from ..models.base_class import Base
from .retailer_model import RetailerDbModel
from .medicine_model import MedicineDbModel


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
