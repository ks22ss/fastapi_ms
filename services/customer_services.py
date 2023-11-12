import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import Customer
from DTO.dto import CustomerDTO
from icecream import ic
from services import create_connection
from typing import List
from datetime import datetime
from fastapi import HTTPException, status


def get_customer_by_id(id: int) -> Customer:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fastms.customer WHERE id = %s", (id,))
        results = cursor.fetchall()

        if len(results) == 0:
            raise Exception("Customer not found")
        customer = Customer(
            id=results[0][0],
            name=results[0][1],
            email=results[0][2],
            address=results[0][3],
            phone=results[0][4],
            signup_ts=results[0][5],
        )
        return customer
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Customer not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def get_customers() -> List[Customer]:
    try:
        customers = []
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fastms.customer")
        results = cursor.fetchall()
        if len(results) == 0:
            return customers

        for customer in results:
            customers.append(
                Customer(
                    id=customer[0],
                    name=customer[1],
                    email=customer[2],
                    address=customer[3],
                    phone=customer[4],
                    signup_ts=customer[5],
                )
            )

        return customers
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def create_customer(customerDto: CustomerDTO) -> Customer:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fastms.customer (name, email, address, phone) VALUES (%s, %s, %s, %s) RETURNING *",
            (
                customerDto.name,
                customerDto.email,
                customerDto.address,
                customerDto.phone,
            ),
        )
        inserted_customer = cursor.fetchone()

        if inserted_customer is None:
            raise Exception("Fail to create customer")

        customer = Customer(
            id=inserted_customer[0],
            name=inserted_customer[1],
            email=inserted_customer[2],
            address=inserted_customer[3],
            phone=inserted_customer[4],
            signup_ts=inserted_customer[5],
        )
        conn.commit()
        return customer

    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Fail to create customer":
            error_status = status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=error_status, detail=str(e))

    finally:
        conn.close()


def update_customer(customer_id: int, customerDto: CustomerDTO) -> Customer:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE fastms.customer 
              SET name = %s, 
                  email = %s,
                  address = %s,
                  phone = %s
            WHERE id = %s RETURNING *""",
            (
                customerDto.name,
                customerDto.email,
                customerDto.address,
                customerDto.phone,
                customer_id,
            ),
        )

        update_customer = cursor.fetchone()
        if update_customer is None:
            raise Exception("Customer not found")
        update_customer = Customer(
            id=update_customer[0],
            name=update_customer[1],
            email=update_customer[2],
            address=update_customer[3],
            phone=update_customer[4],
            signup_ts=update_customer[5],
        )
        conn.commit()
        return update_customer
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Customer not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def remove_customer(customer_id: int) -> Customer:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM fastms.customer WHERE id = %s RETURNING *", (customer_id,)
        )
        deleted_customer = cursor.fetchone()
        if deleted_customer is None:
            raise Exception("Customer not found")
        deleted_customer = Customer(
            id=deleted_customer[0],
            name=deleted_customer[1],
            email=deleted_customer[2],
            address=deleted_customer[3],
            phone=deleted_customer[4],
            signup_ts=deleted_customer[5],
        )
        conn.commit()
        return deleted_customer
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Customer not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()
