import pytest

def test_create_category(client, test_user, auth_headers):
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and accessories"
    }
    response = client.post("/categories/", json=category_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"
    assert data["description"] == "Electronic devices and accessories"

def test_get_categories(client, test_category):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Test Category"

def test_get_category_by_id(client, test_category):
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == "Test Category"

def test_update_category(client, test_category, test_user, auth_headers):
    update_data = {"description": "Updated description"}
    response = client.put(f"/categories/{test_category.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"

def test_delete_category(client, test_category, test_user, auth_headers):
    response = client.delete(f"/categories/{test_category.id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify category is deleted
    response = client.get(f"/categories/{test_category.id}")
    assert response.status_code == 404

def test_get_nonexistent_category(client):
    response = client.get("/categories/999")
    assert response.status_code == 404