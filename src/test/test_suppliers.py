import pytest

def test_create_supplier(client, test_user, auth_headers):
    supplier_data = {
        "name": "ABC Supplies",
        "contact_person": "Jane Smith",
        "email": "jane@abcsupplies.com",
        "phone": "+1234567890",
        "address": "456 Business Ave"
    }
    response = client.post("/suppliers/", json=supplier_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "ABC Supplies"
    assert data["contact_person"] == "Jane Smith"

def test_get_suppliers(client, test_supplier):
    response = client.get("/suppliers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Supplier"

def test_get_supplier_by_id(client, test_supplier):
    response = client.get(f"/suppliers/{test_supplier.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_supplier.id
    assert data["name"] == "Test Supplier"

def test_update_supplier(client, test_supplier, test_user, auth_headers):
    update_data = {"contact_person": "Updated Contact"}
    response = client.put(f"/suppliers/{test_supplier.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["contact_person"] == "Updated Contact"

def test_delete_supplier(client, test_supplier, test_user, auth_headers):
    response = client.delete(f"/suppliers/{test_supplier.id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify supplier is deleted
    response = client.get(f"/suppliers/{test_supplier.id}")
    assert response.status_code == 404