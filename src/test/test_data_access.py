import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

import data_access, schemas
from models import UserRole, ProductStatus

def test_create_user(db):
    user_data = schemas.UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpass",
        full_name="Test User",
        role=UserRole.staff
    )
    user = data_access.create_user(db, user_data, "hashedpass")
    
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"

def test_get_user_by_username(db, test_user):
    user = data_access.get_user_by_username(db, "testuser")
    assert user is not None
    assert user.username == "testuser"

def test_get_user_by_email(db, test_user):
    user = data_access.get_user_by_email(db, "test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

def test_create_category(db):
    category_data = schemas.CategoryCreate(
        name="Electronics",
        description="Electronic devices"
    )
    category = data_access.create_category(db, category_data)
    
    assert category.name == "Electronics"
    assert category.description == "Electronic devices"

def test_create_product(db, test_category):
    product_data = schemas.ProductCreate(
        sku="PROD001",
        name="Test Product",
        price=99.99,
        cost_price=50.00,
        category_id=test_category.id
    )
    product = data_access.create_product(db, product_data)
    
    assert product.sku == "PROD001"
    assert product.name == "Test Product"
    assert product.category_id == test_category.id

def test_get_product_by_sku(db, test_product):
    product = data_access.get_product_by_sku(db, "TEST001")
    assert product is not None
    assert product.sku == "TEST001"

def test_search_products(db, test_product):
    products = data_access.search_products(db, "Test")
    assert len(products) >= 1
    assert "Test" in products[0].name

def test_create_customer(db):
    customer_data = schemas.CustomerCreate(
        name="John Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    customer = data_access.create_customer(db, customer_data)
    
    assert customer.name == "John Doe"
    assert customer.email == "john@example.com"

def test_create_supplier(db):
    supplier_data = schemas.SupplierCreate(
        name="ABC Supplies",
        contact_person="Jane Smith",
        email="jane@abc.com"
    )
    supplier = data_access.create_supplier(db, supplier_data)
    
    assert supplier.name == "ABC Supplies"
    assert supplier.contact_person == "Jane Smith"

def test_update_user(db, test_user):
    update_data = schemas.UserUpdate(full_name="Updated Name")
    updated_user = data_access.update_user(db, test_user.id, update_data)
    
    assert updated_user.full_name == "Updated Name"

def test_delete_user(db, test_user):
    deleted_user = data_access.delete_user(db, test_user.id)
    assert deleted_user is not None
    
    # Verify user is deleted
    user = data_access.get_user(db, test_user.id)
    assert user is None