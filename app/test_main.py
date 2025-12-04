from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# 1. Home Page Redirect Test
def test_read_main():
    response = client.get("/")
    # Redirect hona chahiye login par (Status 200 ya 307)
    assert response.status_code == 200 

#  load login page
def test_get_login_page():
    response = client.get("/login")
    assert response.status_code == 200
    assert "Login" in response.text  
# Galat Password Test
def test_login_failure():
    response = client.post("/login", data={
        "username": "wronguser",
        "password": "wrongpassword"
    })
    #return status code 200 with error message
    
    assert response.status_code == 200
    assert "Invalid username or password" in response.text

#  load register page
def test_get_register_page():
    response = client.get("/register")
    assert response.status_code == 200
    assert "Sign Up" in response.text