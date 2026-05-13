from fastapi.testclient  import TestClient
from main import app
from database import Base, engine
import uuid
Base.metadata.create_all(bind = engine)
client = TestClient(app)

def test_register():
    username = f"user_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/register",
        json = {
            "username": username,
            "password": "12345",
        }
    )
    print(response.json())
    assert response.status_code == 200

def test_login():
    username = f"user_{uuid.uuid4().hex[:8]}"
    client.post(
        "/register",
        json = {
            "username": username,
            "password": "12345",
        }
    )
    response = client.post(
        "/token",
        data = {"username": username, "password": "12345"}
    )
    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_create_note():
    username = f"user_{uuid.uuid4().hex[:8]}"

    client.post(
        "/register",
        json = {
            "username": username,
            "password": "12345",
        }
    )
    login_response = client.post(
        "/token",
        data = {
            "username": username,
            "password": "12345",
        }
    )
    token = login_response.json()["access_token"]
    response = client.post(
        "/notes",
        json = {
            "title": "New Note",
            "content": "New Note",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200