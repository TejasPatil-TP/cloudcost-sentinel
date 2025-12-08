from sqlalchemy import Column, String, Integer, DateTime
import uuid
from .base import Base

class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    provider = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    status = Column(String, default="pending") # pending, processing, completed, failed
    records_processed = Column(Integer, default=0)
    error_message = Column(String, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
