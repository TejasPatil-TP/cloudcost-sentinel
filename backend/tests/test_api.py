import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import get_db
from app.models.base import Base
from app.models.billing import BillingRecord
from app.models.finops import Budget, Anomaly
from app.models.ingestion import IngestionJob

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "1.0.0"}

def test_get_costs_empty():
    response = client.get("/api/v1/costs")
    assert response.status_code == 200
    assert response.json() == []

def test_upload_invalid_provider():
    # Attempt to upload to an unsupported provider
    response = client.post(
        "/api/v1/upload/invalid_provider",
        files={"file": ("test.csv", b"dummy content", "text/csv")}
    )
    assert response.status_code == 400
    assert "Unsupported provider" in response.text

def test_upload_file_too_large():
    # 11MB file
    large_content = b"0" * (11 * 1024 * 1024)
    response = client.post(
        "/api/v1/upload/aws",
        files={"file": ("test.csv", large_content, "text/csv")}
    )
    assert response.status_code == 413
    assert "too large" in response.text
