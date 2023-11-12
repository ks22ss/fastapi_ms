# Unit Test

# Path: test/test_user_controller.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient


def test_get_users():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.get(
            "/api/v1/user", headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "success"


def test_get_user_by_email():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.get(
            "/api/v1/user/test.unit@unittest.com",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "success"


def test_create_and_remove_user():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test.unit.create.user@unittest.com",
                "name": "created.user",
                "password": "unittest",
            },
        )
        assert response.status_code == 201
        assert response.json()["message"] == "success"

        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test.unit.create.user@unittest.com",
                "password": "unittest",
            },
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        # clean up

        response = client.delete(
            "/api/v1/user/test.unit.create.user@unittest.com",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["email"] == "test.unit.create.user@unittest.com"


def test_update_user():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.put(
            "/api/v1/user/test.unit@unittest.com",
            json={
                "email": "test.unit@unittest.com",
                "name": "New Name",
                "password": "unittest234",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200

        response = client.put(
            "/api/v1/user/test.unit@unittest.com",
            json={
                "email": "test.unit@unittest.com",
                "name": "Old Name",
                "password": "unittest",
            },
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
