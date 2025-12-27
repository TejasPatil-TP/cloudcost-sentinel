import pytest
import os
import pandas as pd
from app.services.ingestion.aws import AWSCURIngestionAdapter
from app.models.billing import BillingRecord
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base

# Setup sqlite in-memory db for testing
engine = create_engine("sqlite:///:memory:")
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def test_aws_ingestion():
    # Create synthetic mock file
    file_path = "test_aws_cur.csv"
    data = {
        'lineItem/UsageAccountId': ['123456789012', '123456789012'],
        'lineItem/ProductCode': ['AmazonEC2', 'AmazonS3'],
        'lineItem/UsageStartDate': ['2023-10-01T00:00:00Z', '2023-10-01T00:00:00Z'],
        'lineItem/UsageEndDate': ['2023-10-01T01:00:00Z', '2023-10-01T01:00:00Z'],
        'lineItem/BlendedCost': [0.15, 0.05],
        'lineItem/CurrencyCode': ['USD', 'USD']
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    
    adapter = AWSCURIngestionAdapter()
    records = adapter.parse_file(file_path)
    
    assert len(records) == 2
    assert records[0].provider == "aws"
    assert records[0].cost == 0.15
    assert records[1].service == "AmazonS3"
    
    # Clean up
    os.remove(file_path)

def test_aws_ingestion_validation():
    # Test missing columns
    file_path = "test_aws_cur_invalid.csv"
    data = {
        'lineItem/UsageAccountId': ['123456789012'],
        # missing ProductCode
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    
    adapter = AWSCURIngestionAdapter()
    with pytest.raises(ValueError, match="Missing required columns"):
        adapter.parse_file(file_path)
        
    os.remove(file_path)
