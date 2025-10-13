from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Date
from sqlalchemy.orm import relationship
from ..models.base_class import Base
from .distributor_model import DistributorDbModel
from .medicine_model import MedicineDbModel


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
