import pytest
import os
import pandas as pd
from app.services.ingestion.azure import AzureCostIngestionAdapter
from app.services.ingestion.gcp import GCPBillingIngestionAdapter

def test_azure_ingestion():
    file_path = "test_azure_cost.csv"
    data = {
        'SubscriptionId': ['sub-123', 'sub-123'],
        'MeterCategory': ['Virtual Machines', 'Storage'],
        'Date': ['2023-10-01', '2023-10-01'],
        'CostInBillingCurrency': [10.50, 2.00],
        'BillingCurrencyCode': ['USD', 'USD']
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    
    adapter = AzureCostIngestionAdapter()
    records = adapter.parse_file(file_path)
    
    assert len(records) == 2
    assert records[0].provider == "azure"
    assert records[0].cost == 10.50
    assert records[1].service == "Storage"
    
    os.remove(file_path)

def test_gcp_ingestion():
    file_path = "test_gcp_billing.csv"
    data = {
        'billing_account_id': ['billing-456', 'billing-456'],
        'service.description': ['Compute Engine', 'Cloud Storage'],
        'usage_start_time': ['2023-10-01T00:00:00Z', '2023-10-01T00:00:00Z'],
        'usage_end_time': ['2023-10-01T01:00:00Z', '2023-10-01T01:00:00Z'],
        'cost': [5.25, 0.75],
        'currency': ['USD', 'USD']
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    
    adapter = GCPBillingIngestionAdapter()
    records = adapter.parse_file(file_path)
    
    assert len(records) == 2
    assert records[0].provider == "gcp"
    assert records[0].cost == 5.25
    assert records[1].service == "Cloud Storage"
    
    os.remove(file_path)
