import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from models import Inventory

def test_get_inventory(client, test_product, test_user, auth_headers, db):
    # Create inventory record
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=10,
        available_stock=90
    )
    db.add(inventory)
    db.commit()
    
    response = client.get("/inventory/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_product_inventory(client, test_product, db):
    # Create inventory record
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=10,
        available_stock=90
    )
    db.add(inventory)
    db.commit()
    
    response = client.get(f"/inventory/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["product_id"] == test_product.id
    assert data["current_stock"] == 100

def test_update_inventory(client, test_product, test_user, auth_headers, db):
    # Create inventory record
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=10,
        available_stock=90
    )
    db.add(inventory)
    db.commit()
    
    update_data = {"current_stock": 150}
    response = client.put(f"/inventory/{test_product.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["current_stock"] == 150

def test_get_low_stock_products(client, test_product, test_user, auth_headers, db):
    # Create inventory with low stock
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=5,  # Below min_stock_level (default 0)
        reserved_stock=0,
        available_stock=5
    )
    db.add(inventory)
    db.commit()
    
    # Update product min_stock_level
    test_product.min_stock_level = 10
    db.commit()
    
    response = client.get("/inventory/low-stock/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1