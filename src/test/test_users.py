import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from models import UserRole

def test_create_user(client):
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123",
        "full_name": "New User",
        "role": "staff"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"

def test_create_duplicate_user(client, test_user):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "newpass123",
        "full_name": "Duplicate User"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400

def test_get_users(client, test_user, auth_headers):
    response = client.get("/users/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["username"] == "testuser"

def test_get_user_by_id(client, test_user, auth_headers):
    response = client.get(f"/users/{test_user.id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == "testuser"

def test_update_user(client, test_user, auth_headers):
    update_data = {"full_name": "Updated Name"}
    response = client.put(f"/users/{test_user.id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_delete_user(client, test_user, auth_headers, db):
    # Create another user to delete (can't delete the authenticated user)
    from auth import get_password_hash
    import models
    user_to_delete = models.User(
        username="deleteuser",
        email="delete@example.com",
        hashed_password=get_password_hash("deletepass"),
        full_name="Delete User",
        role=models.UserRole.staff
    )
    db.add(user_to_delete)
    db.commit()
    db.refresh(user_to_delete)
    
    response = client.delete(f"/users/{user_to_delete.id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify user is deleted
    response = client.get(f"/users/{user_to_delete.id}", headers=auth_headers)
    assert response.status_code == 404