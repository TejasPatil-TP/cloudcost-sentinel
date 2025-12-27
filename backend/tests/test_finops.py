import pytest
from app.models.billing import BillingRecord
from app.models.finops import Anomaly
from app.worker.tasks import detect_anomalies
from app.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta, timezone

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_anomaly_detection(monkeypatch):
    Base.metadata.create_all(bind=engine)
    
    # Mock SessionLocal in tasks
    monkeypatch.setattr("app.worker.tasks.SessionLocal", TestingSessionLocal)
    
    db = TestingSessionLocal()
    
    # Create baseline records
    now = datetime.now(timezone.utc)
    for i in range(1, 8):
        db.add(BillingRecord(
            provider="aws",
            account_id="123",
            service="AmazonEC2",
            usage_start_time=now - timedelta(days=i),
            usage_end_time=now - timedelta(days=i-1),
            cost=100.0,
            source_file="test",
            ingestion_time=now
        ))
        
    # Create an anomalous record today
    db.add(BillingRecord(
        provider="aws",
        account_id="123",
        service="AmazonEC2",
        usage_start_time=now,
        usage_end_time=now + timedelta(hours=1),
        cost=300.0, # 3x the average of 100
        source_file="test",
        ingestion_time=now
    ))
    db.commit()
    
    result = detect_anomalies()
    assert result["status"] == "success"
    assert result["anomalies_detected"] == 1
    
    anomalies = db.query(Anomaly).all()
    assert len(anomalies) == 1
    assert anomalies[0].provider == "aws"
    assert anomalies[0].service == "AmazonEC2"
    assert anomalies[0].actual_cost == 300.0
    assert anomalies[0].expected_cost == 100.0
    assert anomalies[0].deviation_percentage == 200.0
    
    db.query(BillingRecord).delete()
    db.query(Anomaly).delete()
    db.commit()
    db.close()
