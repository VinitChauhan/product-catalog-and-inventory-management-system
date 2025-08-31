import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from models import User, Category, Product, Inventory, Customer, Supplier, Order, OrderItem
from models import UserRole, ProductStatus, OrderStatus, TransactionType

def test_user_model(db):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="hashedpass",
        full_name="Test User",
        role=UserRole.staff
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.role == UserRole.staff
    assert user.is_active is True

def test_category_model(db):
    category = Category(
        name="Electronics",
        description="Electronic devices"
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    
    assert category.id is not None
    assert category.name == "Electronics"
    assert category.is_active is True

def test_product_model(db, test_category):
    product = Product(
        sku="PROD001",
        name="Test Product",
        price=99.99,
        cost_price=50.00,
        category_id=test_category.id
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    
    assert product.id is not None
    assert product.sku == "PROD001"
    assert product.status == ProductStatus.active
    assert product.category_id == test_category.id

def test_inventory_model(db, test_product):
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=10,
        available_stock=90
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    
    assert inventory.id is not None
    assert inventory.product_id == test_product.id
    assert inventory.current_stock == 100

def test_customer_model(db):
    customer = Customer(
        name="John Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    
    assert customer.id is not None
    assert customer.name == "John Doe"
    assert customer.is_active is True

def test_supplier_model(db):
    supplier = Supplier(
        name="ABC Supplies",
        contact_person="Jane Smith",
        email="jane@abc.com"
    )
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    
    assert supplier.id is not None
    assert supplier.name == "ABC Supplies"
    assert supplier.is_active is True

def test_order_model(db, test_customer, test_user):
    order = Order(
        order_number="ORD-001",
        customer_id=test_customer.id,
        user_id=test_user.id,
        total_amount=199.98,
        status=OrderStatus.pending
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    assert order.id is not None
    assert order.order_number == "ORD-001"
    assert order.status == OrderStatus.pending

def test_order_item_model(db, test_product, test_customer, test_user):
    order = Order(
        order_number="ORD-002",
        customer_id=test_customer.id,
        user_id=test_user.id,
        total_amount=99.99
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=1,
        unit_price=99.99,
        total_price=99.99
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    
    assert order_item.id is not None
    assert order_item.order_id == order.id
    assert order_item.product_id == test_product.id