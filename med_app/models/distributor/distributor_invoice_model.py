from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from datetime import datetime
from ...models.base_class import Base


class DistributorInvoiceDbModel(Base):
    __tablename__ = "distributor_invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)
    distributor_id = Column(Integer, nullable=False)
    retailer_id = Column(Integer, nullable=True)
    invoice_number = Column(String(50), unique=True, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(255), nullable=True)


class DistributorInvoiceItemDbModel(Base):
    __tablename__ = "distributor_invoice_items"

    item_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("distributor_invoices.invoice_id"))
    medicine_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
