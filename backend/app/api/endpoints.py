from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from app.db.session import get_db
from app.models.billing import BillingRecord
from app.models.finops import Budget, Anomaly
from app.worker.tasks import process_billing_file, detect_anomalies
from pydantic import BaseModel
import shutil
import os
from datetime import datetime

router = APIRouter()

class CostSummary(BaseModel):
    provider: str
    total_cost: float

class CostHistory(BaseModel):
    date: str
    total: float

class AnomalyResponse(BaseModel):
    message: str

class BudgetResponse(BaseModel):
    name: str
    amount: float
    period: str
    provider_filter: Optional[str]

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB limit

@router.post("/upload/{provider}")
async def upload_billing_file(provider: str, file: UploadFile = File(...)):
    if provider not in ["aws", "azure", "gcp"]:
        raise HTTPException(status_code=400, detail="Unsupported provider")
    
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Limit is 10MB.")
    
    # Save file and start background task
    os.makedirs("/tmp", exist_ok=True)
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
        
    process_billing_file.delay(file_location, provider)
    
    return {"info": f"file '{file.filename}' saved and processing started"}

@router.get("/costs", response_model=List[CostSummary])
def get_costs(db: Session = Depends(get_db)):
    results = db.query(
        BillingRecord.provider,
        func.sum(BillingRecord.cost).label('total_cost')
    ).group_by(BillingRecord.provider).all()
    
    return [{"provider": r.provider, "total_cost": r.total_cost} for r in results]

@router.get("/costs/history", response_model=List[CostHistory])
def get_cost_history(db: Session = Depends(get_db)):
    # Group by date for trends. SQLite requires string manipulation for date grouping.
    results = db.query(
        func.date(BillingRecord.usage_start_time).label('date'),
        func.sum(BillingRecord.cost).label('total_cost')
    ).group_by(func.date(BillingRecord.usage_start_time)).order_by('date').all()
    
    return [{"date": str(r.date), "total": r.total_cost} for r in results]

class IngestionView(BaseModel):
    id: str
    provider: str
    file_name: str
    status: str
    records_processed: int
    started_at: str

@router.get("/ingestions", response_model=List[IngestionView])
def get_ingestions(db: Session = Depends(get_db)):
    results = db.query(IngestionJob).order_by(desc(IngestionJob.started_at)).limit(5).all()
    return [IngestionView(
        id=i.id, provider=i.provider, file_name=i.file_name,
        status=i.status, records_processed=i.records_processed,
        started_at=str(i.started_at)
    ) for i in results]

class AnomalyView(BaseModel):
    id: str
    provider: str
    service: str
    date: str
    expected_cost: float
    actual_cost: float
    deviation_percentage: float
    status: str

@router.get("/anomalies", response_model=List[AnomalyView])
def get_anomalies(db: Session = Depends(get_db)):
    results = db.query(Anomaly).all()
    return [AnomalyView(
        id=a.id, provider=a.provider, service=a.service, 
        date=str(a.date), expected_cost=a.expected_cost, 
        actual_cost=a.actual_cost, deviation_percentage=a.deviation_percentage, 
        status=a.status
    ) for a in results]

@router.post("/budgets/seed")
def seed_budgets(db: Session = Depends(get_db)):
    # Create sample budgets
    b1 = Budget(name="Overall Cloud Spend", amount=50000.0, period="monthly", created_at=datetime.now(), updated_at=datetime.now())
    b2 = Budget(name="AWS Compute", amount=10000.0, period="monthly", provider_filter="aws", service_filter="AmazonEC2", created_at=datetime.now(), updated_at=datetime.now())
    db.add(b1)
    db.add(b2)
    db.commit()
    return {"message": "Budgets seeded successfully"}

@router.get("/budgets", response_model=List[BudgetResponse])
def get_budgets(db: Session = Depends(get_db)):
    results = db.query(Budget).all()
    return [BudgetResponse(name=b.name, amount=b.amount, period=b.period, provider_filter=b.provider_filter) for b in results]

@router.post("/anomalies/detect", response_model=AnomalyResponse)
def trigger_anomaly_detection():
    detect_anomalies.delay()
    return {"message": "Anomaly detection started"}

