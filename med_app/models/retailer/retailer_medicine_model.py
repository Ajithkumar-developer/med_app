from sqlalchemy import Column, Integer, ForeignKey, String, DECIMAL, Date
from sqlalchemy.orm import relationship
from ..base_class import Base


class RetailerMedicineDbModel(Base):
    __tablename__ = "retailer_medicines"

    retailer_medicine_id = Column(Integer, primary_key=True, index=True)
    retailer_id = Column(Integer, nullable=False)

    # Medicine information (specific to retailer)
    name = Column(String, nullable=False)
    generic_name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    dosage_form = Column(String, nullable=True)
    strength = Column(String, nullable=True)
    manufacturer = Column(String, nullable=True)

    # Inventory details
    batch_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    expiry_date = Column(Date, nullable=False)

