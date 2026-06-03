from dotenv import load_dotenv
load_dotenv(".env.test", override=True)

from fastapi.testclient  import TestClient
from main import app
from database import Base, engine
import uuid
import pytest
Base.metadata.create_all(bind = engine)
client = TestClient(app)


@pytest.fixture
def auth_client():
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
    headers = {"Authorization": f"Bearer {token}"}
    return token,headers


@pytest.fixture
def note(auth_client):
    token,headers = auth_client
    response = client.post(
        "/notes",
        json = {
            "title": "New Note",
            "content": "New Note",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    note_id = response.json()["id"]
    return note_id,headers


def test_register():
    username = f"user_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/register",
        json = {
            "username": username,
            "password": "12345",
        }
    )
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

def test_create_note(auth_client):
    token,headers = auth_client
    response = client.post(
        "/notes",
        json = {
            "title": "New Note",
            "content": "New Note",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200 , response.json()

def test_create_note_unauthorized():
    response = client.post(
        "/notes",
        json = {
            "title": "New Note",
            "content": "New Note",
        }
    )
    assert response.status_code == 401


def test_create_note_validation():
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
            "title": "",
            "content": "New Note",
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422


def test_delete_note(note):
    note_id,headers = note
    response = client.delete(f"/notes/{note_id}",headers = headers)
    assert response.status_code == 200