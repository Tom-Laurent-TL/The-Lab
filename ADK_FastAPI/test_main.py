import requests

def test_ping():
    print("Testing public ping endpoint...")
    response = requests.get("http://127.0.0.1:8000/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "pong from Professional FastAPI Service"}
    print("✓ Ping test passed")

def test_login():
    print("Testing user login...")
    response = requests.post("http://127.0.0.1:8000/auth/token", data={"username": "testuser", "password": "password"})
    if response.status_code != 200:
        print(f"Login failed: {response.status_code} - {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    print("✓ Login test passed")
    return data["access_token"]

def test_google_status(token):
    print("Testing protected Google status endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://127.0.0.1:8000/google/status", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "api_key_loaded" in data
    assert data["api_key_loaded"] == True
    print("✓ Google status test passed")

def test_get_current_user(token):
    print("Testing get current user endpoint...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("http://127.0.0.1:8000/auth/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    print("✓ Get current user test passed")

def test_unauthorized_google_status():
    print("Testing unauthorized access to Google status...")
    response = requests.get("http://127.0.0.1:8000/google/status")
    assert response.status_code == 401
    print("✓ Unauthorized access test passed")

if __name__ == "__main__":
    print("Starting FastAPI authentication tests...")
    test_ping()
    token = test_login()
    test_google_status(token)
    test_get_current_user(token)
    test_unauthorized_google_status()
    print("All tests passed! ✅")
