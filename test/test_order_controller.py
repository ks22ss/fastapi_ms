# Unit Test

# Path: test/test_product_controller.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient


def test_create_get_update_remove_order():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )

        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.post(
            "/api/v1/order",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "qty": 10,
                "product_id": 1,
                "service_officer_email": "test.unit@unittest.com",
                "customer_id": 1,
            },
        )

        assert response.status_code == 201
        assert response.json()["message"] == "success"
        order_id = response.json()["data"]["order_id"]

        response = client.get(
            f"/api/v1/order/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["id"] == order_id
        assert response.json()["data"]["qty"] == 10
        assert response.json()["data"]["product"]["id"] == 1
        assert (
            response.json()["data"]["service_officer"]["email"]
            == "test.unit@unittest.com"
        )
        assert response.json()["data"]["customer"]["id"] == 1

        response = client.get(
            f"/api/v1/order", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert len(response.json()["data"]) > 0

        response = client.get(
            f"/api/v1/order/customer/1", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert len(response.json()["data"]) > 0

        response = client.put(
            f"/api/v1/order/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "qty": 10,
                "product_id": 1,
                "ship_date": "2023-11-11T00:00:00",
                "service_officer_email": "test.unit@unittest.com",
                "customer_id": 1,
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"

        response = client.get(
            f"/api/v1/order/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["qty"] == 10
        assert response.json()["data"]["product"]["id"] == 1
        assert (
            response.json()["data"]["service_officer"]["email"]
            == "test.unit@unittest.com"
        )
        assert response.json()["data"]["customer"]["id"] == 1

        response = client.delete(
            f"/api/v1/order/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["order_id"] == order_id

        response = client.get(
            f"/api/v1/order/{order_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 404
