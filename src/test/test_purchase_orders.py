import pytest
from datetime import datetime, timedelta

def test_create_purchase_order(client, test_product, test_supplier, test_user, auth_headers):
    po_data = {
        "supplier_id": test_supplier.id,
        "total_amount": 500.00,
        "expected_delivery": (datetime.now() + timedelta(days=7)).isoformat(),
        "notes": "Test purchase order",
        "items": [
            {
                "product_id": test_product.id,
                "quantity": 10,
                "unit_cost": 50.00,
                "total_cost": 500.00
            }
        ]
    }
    response = client.post("/purchase-orders/", json=po_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["supplier_id"] == test_supplier.id
    assert data["total_amount"] == 500.00
    assert "po_number" in data

def test_get_purchase_orders(client, test_user, auth_headers):
    response = client.get("/purchase-orders/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_filter_purchase_orders_by_supplier(client, test_supplier, test_user, auth_headers):
    response = client.get(f"/purchase-orders/?supplier_id={test_supplier.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_purchase_order_status(client, test_product, test_supplier, test_user, auth_headers):
    # Create purchase order first
    po_data = {
        "supplier_id": test_supplier.id,
        "total_amount": 500.00,
        "items": [
            {
                "product_id": test_product.id,
                "quantity": 10,
                "unit_cost": 50.00,
                "total_cost": 500.00
            }
        ]
    }
    response = client.post("/purchase-orders/", json=po_data, headers=auth_headers)
    po_id = response.json()["id"]
    
    # Update PO status
    update_data = {"status": "confirmed"}
    response = client.put(f"/purchase-orders/{po_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "confirmed"

def test_delete_purchase_order(client, test_product, test_supplier, test_user, auth_headers):
    # Create purchase order first
    po_data = {
        "supplier_id": test_supplier.id,
        "total_amount": 500.00,
        "items": [
            {
                "product_id": test_product.id,
                "quantity": 10,
                "unit_cost": 50.00,
                "total_cost": 500.00
            }
        ]
    }
    response = client.post("/purchase-orders/", json=po_data, headers=auth_headers)
    po_id = response.json()["id"]
    
    # Delete purchase order
    response = client.delete(f"/purchase-orders/{po_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify PO is deleted
    response = client.get(f"/purchase-orders/{po_id}", headers=auth_headers)
    assert response.status_code == 404