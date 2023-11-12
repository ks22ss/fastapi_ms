# Unit Test

# Path: test/test_product_controller.py

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from fastapi.testclient import TestClient


def test_create_get_update_remove_products():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test.unit@unittest.com", "password": "unittest"},
        )
        token = response.json()["data"]["access_token"]
        assert response.status_code == 200

        response = client.post(
            "/api/v1/product",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "test.product",
                "model": "test.model",
                "description": "test.description",
                "price": 250,
                "start_date": "2023-05-21T00:00:00",
            },
        )
        assert response.status_code == 201
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.product"
        assert response.json()["data"]["model"] == "test.model"
        assert response.json()["data"]["description"] == "test.description"
        assert response.json()["data"]["price"] == 250
        assert response.json()["data"]["start_date"] == "2023-05-21T00:00:00"
        product_id = response.json()["data"]["id"]

        response = client.get(
            "/api/v1/product", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert len(response.json()["data"]) > 0

        response = client.get(
            f"/api/v1/product/{product_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "test.product"
        assert response.json()["data"]["model"] == "test.model"
        assert response.json()["data"]["description"] == "test.description"
        assert response.json()["data"]["price"] == 250
        assert response.json()["data"]["start_date"] == "2023-05-21T00:00:00"
        assert response.json()["data"]["id"] == product_id

        response = client.put(
            f"/api/v1/product/{product_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "modify.product",
                "model": "modify.model",
                "description": "modify.description",
                "price": 1234,
                "start_date": "2023-05-24T00:00:00",
            },
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "modify.product"
        assert response.json()["data"]["model"] == "modify.model"
        assert response.json()["data"]["description"] == "modify.description"
        assert response.json()["data"]["price"] == 1234
        assert response.json()["data"]["start_date"] == "2023-05-24T00:00:00"
        assert response.json()["data"]["id"] == product_id

        response = client.delete(
            f"/api/v1/product/{product_id}",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["message"] == "success"
        assert response.json()["data"]["name"] == "modify.product"
        assert response.json()["data"]["model"] == "modify.model"
        assert response.json()["data"]["description"] == "modify.description"
        assert response.json()["data"]["price"] == 1234
        assert response.json()["data"]["start_date"] == "2023-05-24T00:00:00"
        assert response.json()["data"]["id"] == product_id
