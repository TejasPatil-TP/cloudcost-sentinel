from app.db.session import engine
from app.models.base import Base
from app.models.billing import BillingRecord # Import to register

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Creating initial data...")
    init_db()
    print("Initial data created")
