import pytest

def test_create_product(client, test_category, test_user, auth_headers):
    product_data = {
        "sku": "PROD001",
        "name": "Test Product",
        "description": "A test product",
        "price": 99.99,
        "cost_price": 50.00,
        "category_id": test_category.id,
        "brand": "TestBrand",
        "model": "TestModel"
    }
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["sku"] == "PROD001"
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99

def test_create_duplicate_sku(client, test_product, test_user, auth_headers):
    product_data = {
        "sku": "TEST001",
        "name": "Duplicate Product",
        "price": 99.99,
        "cost_price": 50.00,
        "category_id": test_product.category_id
    }
    response = client.post("/products/", json=product_data, headers=auth_headers)
    assert response.status_code == 400

def test_get_products(client, test_product):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["sku"] == "TEST001"

def test_get_product_by_id(client, test_product):
    response = client.get(f"/products/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_product.id
    assert data["sku"] == "TEST001"

def test_search_products(client, test_product):
    response = client.get("/products/?search=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Test" in data[0]["name"]

def test_filter_products_by_category(client, test_product):
    response = client.get(f"/products/?category_id={test_product.category_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["category_id"] == test_product.category_id

def test_update_product(client, test_product, test_user, auth_headers):
    update_data = {"price": 149.99}
    response = client.put(f"/products/{test_product.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 149.99

def test_delete_product(client, test_product, test_user, auth_headers):
    response = client.delete(f"/products/{test_product.id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify product is deleted
    response = client.get(f"/products/{test_product.id}")
    assert response.status_code == 404