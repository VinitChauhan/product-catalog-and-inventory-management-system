import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from main import app
from database_connection import get_db, Base
import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    from auth import get_password_hash
    user = models.User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        role=models.UserRole.staff
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def test_category(db):
    category = models.Category(
        name="Test Category",
        description="Test category description"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

@pytest.fixture
def test_product(db, test_category):
    product = models.Product(
        sku="TEST001",
        name="Test Product",
        description="Test product description",
        price=99.99,
        cost_price=50.00,
        category_id=test_category.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@pytest.fixture
def test_customer(db):
    customer = models.Customer(
        name="Test Customer",
        email="customer@example.com",
        phone="+1234567890",
        address="123 Test St"
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@pytest.fixture
def test_supplier(db):
    supplier = models.Supplier(
        name="Test Supplier",
        contact_person="John Doe",
        email="supplier@example.com",
        phone="+1234567890",
        address="456 Supplier Ave"
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

@pytest.fixture
def auth_headers(client, test_user):
    response = client.post("/token", params={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}