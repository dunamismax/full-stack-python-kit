"""Unit tests for authentication functionality."""

import pytest
from packages.auth.password import hash_password, verify_password
from packages.auth.auth import create_access_token, verify_token


def test_password_hashing():
    """Test password hashing and verification."""
    password = "testpassword123"
    hashed = hash_password(password)
    
    # Hash should be different from original password
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) is True
    
    # Wrong password should fail
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_token_creation_and_verification():
    """Test JWT token creation and verification."""
    data = {"sub": "test-user-id"}
    token = create_access_token(data)
    
    # Token should be created
    assert token is not None
    assert isinstance(token, str)
    
    # Token should be verifiable
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test-user-id"
    
    # Invalid token should return None
    invalid_payload = verify_token("invalid-token")
    assert invalid_payload is None


def test_jwt_token_with_custom_expiration():
    """Test JWT token with custom expiration."""
    from datetime import timedelta
    
    data = {"sub": "test-user-id"}
    token = create_access_token(data, expires_delta=timedelta(minutes=15))
    
    # Token should be verifiable
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "test-user-id"
    assert "exp" in payload