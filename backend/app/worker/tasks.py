from app.worker.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.billing import BillingRecord
from app.services.ingestion.aws import AWSCURIngestionAdapter
from app.services.ingestion.azure import AzureCostIngestionAdapter
from app.services.ingestion.gcp import GCPBillingIngestionAdapter
from sqlalchemy.orm import Session
import os

from app.models.ingestion import IngestionJob

@celery_app.task(name="process_billing_file")
def process_billing_file(file_path: str, provider: str):
    db: Session = SessionLocal()
    job = IngestionJob(
        provider=provider,
        file_name=os.path.basename(file_path),
        status="processing",
        started_at=datetime.now(timezone.utc)
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    try:
        if provider == "aws":
            adapter = AWSCURIngestionAdapter()
        elif provider == "azure":
            adapter = AzureCostIngestionAdapter()
        elif provider == "gcp":
            adapter = GCPBillingIngestionAdapter()
        else:
            return {"status": "skipped", "reason": f"Provider {provider} not fully implemented"}
        
        records = adapter.parse_file(file_path)
        
        # Identify existing records to avoid duplicates (basic implementation)
        # Using a very basic approach: bulk save without deep duplicate checking for now due to SQLite limitations
        # In a real database, we'd use ON CONFLICT DO NOTHING
        
        db.bulk_save_objects(records)
        
        job.status = "completed"
        job.records_processed = len(records)
        job.completed_at = datetime.now(timezone.utc)
        
        db.commit()
        return {"status": "success", "provider": provider, "records_processed": len(records)}
    except Exception as e:
        db.rollback()
        job.status = "failed"
        job.error_message = str(e)
        job.completed_at = datetime.now(timezone.utc)
        db.commit()
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
        if os.path.exists(file_path):
            os.remove(file_path)

from app.models.finops import Anomaly
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

@celery_app.task(name="detect_anomalies")
def detect_anomalies():
    db: Session = SessionLocal()
    try:
        # Simple rolling average over the last 7 days per provider and service
        # If today's cost > 1.5 * average of last 7 days, flag it.
        now = datetime.now(timezone.utc)
        start_of_period = now - timedelta(days=7)
        
        # Get baseline (avg per day per provider/service over last 7 days)
        # For SQLite simplicity in grouping, we'll do python-side aggregation for the mockup
        records = db.query(BillingRecord).filter(BillingRecord.usage_start_time >= start_of_period).all()
        
        from collections import defaultdict
        
        history = defaultdict(list)
        for r in records:
            history[(r.provider, r.service)].append(r.cost)
            
        anomalies_detected = 0
        for (provider, service), costs in history.items():
            if len(costs) < 2:
                continue # not enough data
                
            # very simplified: compare last record to avg of previous records
            latest = costs[-1]
            previous = costs[:-1]
            avg = sum(previous) / len(previous)
            
            if avg > 0 and latest > avg * 1.5:
                deviation = ((latest - avg) / avg) * 100
                
                # Check if already flagged today
                existing = db.query(Anomaly).filter_by(provider=provider, service=service, status="open").first()
                if not existing:
                    anomaly = Anomaly(
                        provider=provider,
                        service=service,
                        date=now,
                        expected_cost=avg,
                        actual_cost=latest,
                        deviation_percentage=deviation,
                        created_at=now
                    )
                    db.add(anomaly)
                    anomalies_detected += 1
        
        db.commit()
        return {"status": "success", "anomalies_detected": anomalies_detected}
    except Exception as e:
        db.rollback()
        return {"status": "error", "error": str(e)}
    finally:
        db.close()
