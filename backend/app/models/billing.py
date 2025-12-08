from sqlalchemy import Column, String, Float, DateTime, JSON, Index
import uuid
from .base import Base

class BillingRecord(Base):
    __tablename__ = "billing_records"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False, index=True) # aws, azure, gcp
    account_id = Column(String, nullable=False, index=True)
    service = Column(String, nullable=False, index=True)
    region = Column(String, nullable=True)
    
    usage_start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    usage_end_time = Column(DateTime(timezone=True), nullable=False)
    
    cost = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    
    usage_quantity = Column(Float, nullable=True)
    usage_unit = Column(String, nullable=True)
    
    tags = Column(JSON, nullable=True) # JSONB in postgres
    
    source_file = Column(String, nullable=False)
    ingestion_time = Column(DateTime(timezone=True), nullable=False)
    
    __table_args__ = (
        Index('ix_billing_provider_time', 'provider', 'usage_start_time'),
        Index('ix_billing_service_time', 'service', 'usage_start_time'),
    )
