import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from models import Inventory

def test_create_order(client, test_product, test_customer, test_user, auth_headers, db):
    # Create inventory for the product
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=0,
        available_stock=100
    )
    db.add(inventory)
    db.commit()
    
    order_data = {
        "customer_id": test_customer.id,
        "total_amount": 199.98,
        "notes": "Test order",
        "items": [
            {
                "product_id": test_product.id,
                "quantity": 2,
                "unit_price": 99.99,
                "total_price": 199.98
            }
        ]
    }
    response = client.post("/orders/", json=order_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == test_customer.id
    assert data["total_amount"] == 199.98
    assert "order_number" in data

def test_get_orders(client, test_user, auth_headers):
    response = client.get("/orders/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_filter_orders_by_customer(client, test_customer, test_user, auth_headers):
    response = client.get(f"/orders/?customer_id={test_customer.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_order_status(client, test_product, test_customer, test_user, auth_headers, db):
    # Create inventory and order first
    inventory = Inventory(
        product_id=test_product.id,
        current_stock=100,
        reserved_stock=0,
        available_stock=100
    )
    db.add(inventory)
    db.commit()
    
    order_data = {
        "customer_id": test_customer.id,
        "total_amount": 99.99,
        "items": [
            {
                "product_id": test_product.id,
                "quantity": 1,
                "unit_price": 99.99,
                "total_price": 99.99
            }
        ]
    }
    response = client.post("/orders/", json=order_data, headers=auth_headers)
    order_id = response.json()["id"]
    
    # Update order status
    update_data = {"status": "confirmed"}
    response = client.put(f"/orders/{order_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"