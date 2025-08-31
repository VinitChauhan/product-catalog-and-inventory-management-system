import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from models import Inventory, TransactionType

def test_create_inventory_transaction(client, test_product, test_user, auth_headers, db):
    # Create inventory for the product
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=50,
        reserved_stock=0,
        available_stock=50
    )
    db.add(inventory)
    db.commit()
    
    transaction_data = {
        "product_id": test_product.id,
        "transaction_type": "purchase",
        "quantity": 20,
        "notes": "Stock replenishment"
    }
    response = client.post("/inventory-transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == test_product.id
    assert data["transaction_type"] == "purchase"
    assert data["quantity"] == 20
    assert data["previous_stock"] == 50
    assert data["new_stock"] == 70

def test_create_sale_transaction(client, test_product, test_user, auth_headers, db):
    # Create inventory for the product
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=10,
        available_stock=90
    )
    db.add(inventory)
    db.commit()
    
    transaction_data = {
        "product_id": test_product.id,
        "transaction_type": "sale",
        "quantity": 5,
        "reference_id": 1,
        "reference_type": "order",
        "notes": "Sale transaction"
    }
    response = client.post("/inventory-transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_type"] == "sale"
    assert data["quantity"] == 5
    assert data["previous_stock"] == 100
    assert data["new_stock"] == 95

def test_create_adjustment_transaction(client, test_product, test_user, auth_headers, db):
    # Create inventory for the product
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=0,
        available_stock=100
    )
    db.add(inventory)
    db.commit()
    
    transaction_data = {
        "product_id": test_product.id,
        "transaction_type": "adjustment",
        "quantity": 85,  # Adjust to 85
        "notes": "Inventory adjustment after physical count"
    }
    response = client.post("/inventory-transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["transaction_type"] == "adjustment"
    assert data["previous_stock"] == 100
    assert data["new_stock"] == 85

def test_get_inventory_transactions(client, test_user, auth_headers):
    response = client.get("/inventory-transactions/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_filter_transactions_by_product(client, test_product, test_user, auth_headers):
    response = client.get(f"/inventory-transactions/?product_id={test_product.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_transaction_with_nonexistent_product(client, test_user, auth_headers):
    transaction_data = {
        "product_id": 999,
        "transaction_type": "purchase",
        "quantity": 10
    }
    response = client.post("/inventory-transactions/", json=transaction_data, headers=auth_headers)
    assert response.status_code == 404