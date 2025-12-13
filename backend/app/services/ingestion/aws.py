import pandas as pd
from typing import List
import uuid
from datetime import timezone
from .base import BillingIngestionAdapter
from app.models.billing import BillingRecord

class AWSCURIngestionAdapter(BillingIngestionAdapter):
    provider_name = "aws"
    
    def parse_file(self, file_path: str) -> List[BillingRecord]:
        df = pd.read_csv(file_path)
        
        required_cols = [
            'lineItem/UsageAccountId', 'lineItem/ProductCode',
            'lineItem/UsageStartDate', 'lineItem/UsageEndDate',
            'lineItem/BlendedCost', 'lineItem/CurrencyCode'
        ]
        self.validate_schema(df, required_cols)
        
        records = []
        ingestion_time = pd.Timestamp.now(tz=timezone.utc)
        
        for _, row in df.iterrows():
            cost = float(row['lineItem/BlendedCost'])
            if cost == 0:
                continue # Skip zero cost lines for efficiency
            
            start_time = pd.to_datetime(row['lineItem/UsageStartDate']).replace(tzinfo=timezone.utc)
            end_time = pd.to_datetime(row['lineItem/UsageEndDate']).replace(tzinfo=timezone.utc)
            
            record = BillingRecord(
                id=uuid.uuid4(),
                provider=self.provider_name,
                account_id=str(row['lineItem/UsageAccountId']),
                service=str(row['lineItem/ProductCode']),
                region=row.get('product/region', None),
                usage_start_time=start_time,
                usage_end_time=end_time,
                cost=cost,
                currency=str(row['lineItem/CurrencyCode']),
                usage_quantity=float(row.get('lineItem/UsageAmount', 0)),
                usage_unit=str(row.get('lineItem/Operation', '')),
                tags={}, # Extract user-defined tags later
                source_file=file_path,
                ingestion_time=ingestion_time
            )
            records.append(record)
        return records
