# Unit Test

# Path: test/test_product_controller.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient
import icecream as ic


def test_create_get_update_remove_customer():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.post(
            "/api/v1/customer",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test.customer",
                "email": "test.customer.unit.test@email.com",
                "phone": "123456789",
                "address": "test.address",
            },
        )
        assert response.status_code == 201
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.customer"
        assert response.json()["data"]["email"] == "test.customer.unit.test@email.com"
        assert response.json()["data"]["phone"] == "123456789"
        assert response.json()["data"]["address"] == "test.address"
        customer_id = response.json()["data"]["id"]

        response = client.get(
            f"/api/v1/customer/{customer_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.customer"
        assert response.json()["data"]["email"] == "test.customer.unit.test@email.com"
        assert response.json()["data"]["phone"] == "123456789"
        assert response.json()["data"]["address"] == "test.address"

        response = client.get(
            f"/api/v1/customer", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert len(response.json()["data"]) > 0

        response = client.put(
            f"/api/v1/customer/{customer_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test.customer.update",
                "email": "test.customer.unit.test.updated.email.com",
                "phone": "987654321",
                "address": "test.address.update",
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.customer.update"
        assert (
            response.json()["data"]["email"]
            == "test.customer.unit.test.updated.email.com"
        )
        assert response.json()["data"]["phone"] == "987654321"
        assert response.json()["data"]["address"] == "test.address.update"

        response = client.delete(
            f"/api/v1/customer/{customer_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.customer.update"
        assert (
            response.json()["data"]["email"]
            == "test.customer.unit.test.updated.email.com"
        )
        assert response.json()["data"]["phone"] == "987654321"
        assert response.json()["data"]["address"] == "test.address.update"
        assert response.json()["data"]["id"] == customer_id
