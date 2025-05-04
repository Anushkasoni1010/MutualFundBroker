# tests/test_auth.py
from tests.conftest import client


def test_signup_success(client):
    response = client.post("/auth/signup/", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "user@example.com"


def test_login_success(client):
    # First, register the user
    client.post("/auth/signup/", json={"email": "user@example.com", "password": "password123"})

    # Then, log in
    response = client.post("/auth/login/", json={"email": "user@example.com", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_signup_existing_user(client):
    # First, register the user
    client.post("/auth/signup/", json={
        "email": "user@example.com",
        "password": "password123"
    })

    # Try to register it again
    response = client.post("/auth/signup/", json={
        "email": "user@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_wrong_password(client):
    client.post("/auth/signup/", json={
        "email": "user@example.com",
        "password": "password123"
    })
    response = client.post("/auth/login/", json={
        "email": "user@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"