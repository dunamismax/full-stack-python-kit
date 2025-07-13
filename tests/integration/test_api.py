"""Integration tests for the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from packages.database.models import User


def test_root_endpoint(client: TestClient):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Welcome to the Full-Stack Python Kit API"


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] in ["healthy", "unhealthy"]
    assert "version" in data
    assert "database" in data


def test_login_endpoint(client: TestClient, test_user: User):
    """Test user login."""
    login_data = {
        "username": test_user.username,
        "password": "testpassword",
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == test_user.email


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword",
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    
    data = response.json()
    assert "detail" in data


def test_register_endpoint(client: TestClient):
    """Test user registration."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpassword123",
        "full_name": "New User",
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "hashed_password" not in data  # Should not expose password


def test_register_duplicate_email(client: TestClient, test_user: User):
    """Test registration with duplicate email."""
    user_data = {
        "email": test_user.email,  # Duplicate email
        "username": "newuser",
        "password": "newpassword123",
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "already registered" in data["detail"].lower()


def test_get_current_user(client: TestClient, auth_headers: dict[str, str]):
    """Test getting current user information."""
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "email" in data
    assert "username" in data
    assert "id" in data


def test_unauthorized_access(client: TestClient):
    """Test accessing protected endpoint without authentication."""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_invalid_token(client: TestClient):
    """Test accessing protected endpoint with invalid token."""
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 401