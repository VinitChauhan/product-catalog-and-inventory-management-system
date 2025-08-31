import pytest
import sys
import os

backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from auth import verify_password, get_password_hash, authenticate_user

def test_password_hashing():
    password = "testpassword"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)

def test_authenticate_user(db, test_user):
    # Test valid authentication
    user = authenticate_user(db, "testuser", "testpass")
    assert user is not None
    assert user.username == "testuser"
    
    # Test invalid username
    user = authenticate_user(db, "wronguser", "testpass")
    assert user is False
    
    # Test invalid password
    user = authenticate_user(db, "testuser", "wrongpass")
    assert user is False

def test_login_endpoint(client, test_user):
    # Test valid login
    response = client.post("/token", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    
    # Test invalid login
    response = client.post("/token", params={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401