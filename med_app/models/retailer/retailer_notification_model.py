from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from ...models.base_class import Base


class RetailerNotificationDbModel(Base):
    __tablename__ = "retailer_notifications"

    id = Column(Integer, primary_key=True, index=True)
    retailer_id = Column(Integer, nullable=True)  # optional if per-user
    title = Column(String(100), nullable=False)
    message = Column(String(500), nullable=False)
    type = Column(String(50), nullable=False)  # e.g. 'low_stock', 'new_order', etc.
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
