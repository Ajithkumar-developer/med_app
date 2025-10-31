from sqlalchemy import Column, Integer, String, DECIMAL, Date
from ...models.base_class import Base

class DistributorStockDbModel(Base):
    __tablename__ = "distributor_stock"

    stock_id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, nullable=False)  
    medicine_id = Column(Integer, nullable=False)     
    batch_number = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    expiry_date = Column(Date, nullable=False)
