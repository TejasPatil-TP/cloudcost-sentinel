from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
import uuid
from .base import Base

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    period = Column(String, nullable=False, default="monthly") # monthly, quarterly, annual
    provider_filter = Column(String, nullable=True) # if null, applies to all
    service_filter = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False)
    service = Column(String, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    expected_cost = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=False)
    deviation_percentage = Column(Float, nullable=False)
    status = Column(String, default="open") # open, acknowledged, resolved
    created_at = Column(DateTime(timezone=True), nullable=False)
