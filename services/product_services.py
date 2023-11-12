import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import Product
from DTO.dto import ProductDTO
from icecream import ic
from services import create_connection
from typing import List
from datetime import datetime
from fastapi import HTTPException, status


def get_product_by_id(id: int) -> Product:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fastms.product WHERE id = %s", (id,))
        results = cursor.fetchall()
        if len(results) == 0:
            raise Exception("Product not found")
        product = Product(
            id=results[0][0],
            name=results[0][1],
            model=results[0][2],
            price=results[0][3],
            description=results[0][4],
            start_date=results[0][5],
        )
        return product
    except Exception as e:
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Product not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def get_products() -> List[Product]:
    try:
        products = []
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fastms.product")
        results = cursor.fetchall()
        conn.close()

        if len(results) == 0:
            return products

        for product in results:
            products.append(
                Product(
                    id=product[0],
                    name=product[1],
                    model=product[2],
                    price=product[3],
                    description=product[4],
                    start_date=product[5],
                )
            )

        return products
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def create_product(productDto: ProductDTO) -> Product:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fastms.product (name, model, price, description, start_date) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (
                productDto.name,
                productDto.model,
                productDto.price,
                productDto.description,
                productDto.start_date,
            ),
        )
        inserted_product = cursor.fetchone()
        if len(inserted_product) == 0:
            raise Exception("Fail to create product")
        inserted_product = Product(
            id=inserted_product[0],
            name=inserted_product[1],
            model=inserted_product[2],
            price=inserted_product[3],
            description=inserted_product[4],
            start_date=inserted_product[5],
        )

        conn.commit()
        return inserted_product
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Fail to create product":
            error_status = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def update_product(product_id: int, productDto: ProductDTO) -> Product:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE fastms.product 
              SET name = %s, 
                  model = %s,
                  price = %s,
                  description = %s,
                  start_date = %s
            WHERE id = %s RETURNING *""",
            (
                productDto.name,
                productDto.model,
                productDto.price,
                productDto.description,
                productDto.start_date,
                product_id,
            ),
        )
        updated_product = cursor.fetchone()
        if len(updated_product) == 0:
            raise Exception("Product not found")
        updated_product = Product(
            id=updated_product[0],
            name=updated_product[1],
            model=updated_product[2],
            price=updated_product[3],
            description=updated_product[4],
            start_date=updated_product[5],
        )
        conn.commit()
        return updated_product
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Product not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def remove_product(product_id: int) -> Product:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM fastms.product WHERE id = %s RETURNING *", (product_id,)
        )
        deleted_product = cursor.fetchone()
        if len(deleted_product) == 0:
            raise Exception("Product not found")
        deleted_product = Product(
            id=deleted_product[0],
            name=deleted_product[1],
            model=deleted_product[2],
            price=deleted_product[3],
            description=deleted_product[4],
            start_date=deleted_product[5],
        )
        conn.commit()
        return deleted_product
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Product not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()
