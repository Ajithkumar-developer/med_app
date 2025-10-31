from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from datetime import datetime
from ...models.base_class import Base


class RetailerInvoiceDbModel(Base):
    __tablename__ = "retailer_invoices"

    invoice_id = Column(Integer, primary_key=True, index=True)
    retailer_id = Column(Integer, nullable=False)
    customer_id = Column(Integer, nullable=True)
    invoice_number = Column(String(50), unique=True, index=True)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String(255), nullable=True)


class RetailerInvoiceItemDbModel(Base):
    __tablename__ = "retailer_invoice_items"

    item_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("retailer_invoices.invoice_id"))
    medicine_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)
