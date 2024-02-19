from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user_route():
    response = client.post(
        "/user/",
        json={
            "username": "testuser",
            "hashed_password": "testpassword",
            "disabled": False,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "hashed_password" not in data
    assert data["disabled"] == False


def test_read_user_route():
    response = client.get("/user/testuser")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "hashed_password" not in data
    assert data["disabled"] == False


def test_update_user_route():
    response = client.put(
        "/user/",
        json={
            "username": "testuser",
            "hashed_password": "newpassword",
            "disabled": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "hashed_password" not in data
    assert data["disabled"] == True


def test_delete_user_route():
    response = client.delete("/user/testuser")
    assert response.status_code == 200
    assert response.json() == {"detail": "User deleted"}
