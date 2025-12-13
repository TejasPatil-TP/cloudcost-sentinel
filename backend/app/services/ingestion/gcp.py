import pandas as pd
from typing import List
import uuid
from datetime import timezone
from .base import BillingIngestionAdapter
from app.models.billing import BillingRecord

class GCPBillingIngestionAdapter(BillingIngestionAdapter):
    provider_name = "gcp"
    
    def parse_file(self, file_path: str) -> List[BillingRecord]:
        df = pd.read_csv(file_path)
        
        required_cols = [
            'billing_account_id', 'service.description',
            'usage_start_time', 'usage_end_time',
            'cost', 'currency'
        ]
        self.validate_schema(df, required_cols)
        
        records = []
        ingestion_time = pd.Timestamp.now(tz=timezone.utc)
        
        for _, row in df.iterrows():
            cost = float(row['cost'])
            if cost == 0:
                continue
            
            start_time = pd.to_datetime(row['usage_start_time']).replace(tzinfo=timezone.utc)
            end_time = pd.to_datetime(row['usage_end_time']).replace(tzinfo=timezone.utc)
            
            record = BillingRecord(
                id=str(uuid.uuid4()),
                provider=self.provider_name,
                account_id=str(row['billing_account_id']),
                service=str(row['service.description']),
                region=row.get('location.location', None),
                usage_start_time=start_time,
                usage_end_time=end_time,
                cost=cost,
                currency=str(row['currency']),
                usage_quantity=float(row.get('usage.amount', 0)),
                usage_unit=str(row.get('usage.unit', '')),
                tags={}, # Labels parsing logic could go here
                source_file=file_path,
                ingestion_time=ingestion_time
            )
            records.append(record)
        return records
