from sqlalchemy import Column, Integer, String, Boolean
from ..models.base_class import Base


class MedicineDbModel(Base):
    __tablename__ = "medicines"

    medicine_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Brand or product name
    generic_name = Column(String, nullable=True)
    category = Column(String, nullable=False)  # e.g., Antibiotic, Painkiller
    dosage_form = Column(String, nullable=False)  # e.g., Tablet, Syrup
    strength = Column(String, nullable=False)  # e.g., 500 mg
    manufacturer = Column(String, nullable=True)
    prescription_required = Column(Boolean, default=False, nullable=False)

