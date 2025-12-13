import pandas as pd
from typing import List
import uuid
from datetime import timezone
from .base import BillingIngestionAdapter
from app.models.billing import BillingRecord

class AzureCostIngestionAdapter(BillingIngestionAdapter):
    provider_name = "azure"
    
    def parse_file(self, file_path: str) -> List[BillingRecord]:
        df = pd.read_csv(file_path)
        
        required_cols = [
            'SubscriptionId', 'MeterCategory',
            'Date', 'CostInBillingCurrency', 'BillingCurrencyCode'
        ]
        self.validate_schema(df, required_cols)
        
        records = []
        ingestion_time = pd.Timestamp.now(tz=timezone.utc)
        
        for _, row in df.iterrows():
            cost = float(row['CostInBillingCurrency'])
            if cost == 0:
                continue
            
            # Azure commonly uses daily rollups in standard exports
            start_time = pd.to_datetime(row['Date']).replace(tzinfo=timezone.utc)
            end_time = start_time + pd.Timedelta(days=1)
            
            record = BillingRecord(
                id=str(uuid.uuid4()),
                provider=self.provider_name,
                account_id=str(row['SubscriptionId']),
                service=str(row['MeterCategory']),
                region=row.get('ResourceLocation', None),
                usage_start_time=start_time,
                usage_end_time=end_time,
                cost=cost,
                currency=str(row['BillingCurrencyCode']),
                usage_quantity=float(row.get('Quantity', 0)),
                usage_unit=str(row.get('UnitOfMeasure', '')),
                tags={}, # Parsed later if 'Tags' column exists
                source_file=file_path,
                ingestion_time=ingestion_time
            )
            records.append(record)
        return records
