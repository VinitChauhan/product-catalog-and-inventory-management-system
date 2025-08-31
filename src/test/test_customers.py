import pytest

def test_create_customer(client, test_user, auth_headers):
    customer_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "address": "123 Main St"
    }
    response = client.post("/customers/", json=customer_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"

def test_get_customers(client, test_customer):
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Customer"

def test_get_customer_by_id(client, test_customer):
    response = client.get(f"/customers/{test_customer.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_customer.id
    assert data["name"] == "Test Customer"

def test_update_customer(client, test_customer, test_user, auth_headers):
    update_data = {"phone": "+9876543210"}
    response = client.put(f"/customers/{test_customer.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+9876543210"

def test_delete_customer(client, test_customer, test_user, auth_headers):
    response = client.delete(f"/customers/{test_customer.id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify customer is deleted
    response = client.get(f"/customers/{test_customer.id}")
    assert response.status_code == 404