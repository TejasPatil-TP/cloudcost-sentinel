from abc import ABC, abstractmethod
from typing import List
from app.models.billing import BillingRecord
import pandas as pd
import uuid
from datetime import datetime, timezone

class BillingIngestionAdapter(ABC):
    provider_name: str
    
    @abstractmethod
    def parse_file(self, file_path: str) -> List[BillingRecord]:
        """Parse a provider-specific billing file and return normalized BillingRecord objects."""
        pass
    
    def validate_schema(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns for {self.provider_name}: {missing_cols}")
        return True

