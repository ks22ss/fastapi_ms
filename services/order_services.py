import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.model import Order, Product, Customer, User
from DTO.dto import OrderDTO, UserReadDTO
from icecream import ic
from services import create_connection
from typing import List
from datetime import datetime
from fastapi import HTTPException, status


def get_order_by_id(id: int) -> Order:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                    SELECT 
                      o.id,
                      o.qty,
                      p.id as product_id,
                      p.name as product_name,
                      p.model as product_model,
                      p.price  as product_price,
                      p.description as product_description,
                      p.start_date as product_start_date,
                      o.order_date,
                      o.ship_date,
                      c.id as customer_id,
                      c.name as customer_name,
                      c.email as customer_email,
                      c.address as customer_address,
                      c.phone as customer_phone,
                      c.signup_ts as customer_signup_ts,
                      u.name as service_officer_name,
                      u.email as service_officer_email,   
                      u.signup_ts as service_officer_signup_ts
                    FROM fastms.orders o
                    JOIN fastms.product p ON o.product_id = p.id
                    JOIN fastms.customer c ON o.customer_id = c.id
                    JOIN fastms.user u ON o.service_officer = u.email 
                    WHERE o.id = %s
                    
                    """,
            (id,),
        )
        results = cursor.fetchall()

        if len(results) == 0:
            raise Exception("Order not found")

        product = Product(
            id=results[0][2],
            name=results[0][3],
            model=results[0][4],
            price=results[0][5],
            description=results[0][6],
            start_date=results[0][7],
        )

        customer = Customer(
            id=results[0][10],
            name=results[0][11],
            email=results[0][12],
            address=results[0][13],
            phone=results[0][14],
            signup_ts=results[0][15],
        )
        user = UserReadDTO(
            email=results[0][17], name=results[0][16], signup_ts=results[0][18]
        )

        order = Order(
            id=results[0][0],
            qty=results[0][1],
            product=product,
            order_date=results[0][8],
            ship_date=results[0][9],
            customer=customer,
            service_officer=user,
        )

        return order
    except Exception as e:
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Order not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def get_order_by_customer_id(id: int) -> Order:
    try:
        orders = []
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                    SELECT 
                      o.id,
                      o.qty,
                      p.id as product_id,
                      p.name as product_name,
                      p.model as product_model,
                      p.price  as product_price,
                      p.description as product_description,
                      p.start_date as product_start_date,
                      o.order_date,
                      o.ship_date,
                      c.id as customer_id,
                      c.name as customer_name,
                      c.email as customer_email,
                      c.address as customer_address,
                      c.phone as customer_phone,
                      c.signup_ts as customer_signup_ts,
                      u.name as service_officer_name,
                      u.email as service_officer_email,   
                      u.signup_ts as service_officer_signup_ts
                    FROM fastms.orders o
                    JOIN fastms.product p ON o.product_id = p.id
                    JOIN fastms.customer c ON o.customer_id = c.id
                    JOIN fastms.user u ON o.service_officer = u.email 
                    WHERE c.id = %s
                    
                    """,
            (id,),
        )
        results = cursor.fetchall()

        if len(results) == 0:
            return orders
        for order in results:
            product = Product(
                id=results[0][2],
                name=results[0][3],
                model=results[0][4],
                price=results[0][5],
                description=results[0][6],
                start_date=results[0][7],
            )

            customer = Customer(
                id=results[0][10],
                name=results[0][11],
                email=results[0][12],
                address=results[0][13],
                phone=results[0][14],
                signup_ts=results[0][15],
            )
            user = UserReadDTO(
                email=results[0][17], name=results[0][16], signup_ts=results[0][18]
            )

            order = Order(
                id=results[0][0],
                qty=results[0][1],
                product=product,
                order_date=results[0][8],
                ship_date=results[0][9],
                customer=customer,
                service_officer=user,
            )
            orders.append(order)

        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def get_orders() -> List[Order]:
    try:
        orders = []
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                    SELECT 
                      o.id,
                      o.qty,
                      p.id as product_id,
                      p.name as product_name,
                      p.model as product_model,
                      p.price  as product_price,
                      p.description as product_description,
                      p.start_date as product_start_date,
                      o.order_date,
                      o.ship_date,
                      c.id as customer_id,
                      c.name as customer_name,
                      c.email as customer_email,
                      c.address as customer_address,
                      c.phone as customer_phone,
                      c.signup_ts as customer_signup_ts,
                      u.name as service_officer_name,
                      u.email as service_officer_email,   
                      u.signup_ts as service_officer_signup_ts
                    FROM fastms.orders o
                    JOIN fastms.product p ON o.product_id = p.id
                    JOIN fastms.customer c ON o.customer_id = c.id
                    JOIN fastms.user u ON o.service_officer = u.email 
                    """
        )
        results = cursor.fetchall()

        if len(results) == 0:
            return None
        for order in results:
            product = Product(
                id=order[2],
                name=order[3],
                model=order[4],
                price=order[5],
                description=order[6],
                start_date=order[7],
            )

            customer = Customer(
                id=order[10],
                name=order[11],
                email=order[12],
                address=order[13],
                phone=order[14],
                signup_ts=order[15],
            )
            user = UserReadDTO(email=order[17], name=order[16], signup_ts=order[18])

            order = Order(
                id=order[0],
                qty=order[1],
                product=product,
                order_date=order[8],
                ship_date=order[9],
                customer=customer,
                service_officer=user,
            )

            orders.append(order)

        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def create_order(orderDto: OrderDTO) -> int:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fastms.orders (qty, product_id, ship_date, customer_id, service_officer) VALUES (%s, %s, %s, %s, %s) RETURNING *",
            (
                orderDto.qty,
                orderDto.product_id,
                orderDto.ship_date,
                orderDto.customer_id,
                orderDto.service_officer_email,
            ),
        )
        inserted_order = cursor.fetchone()
        if inserted_order is None:
            raise Exception("Fail to create order")
        conn.commit()
        return inserted_order[0]
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Fail to create order":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def update_order(order_id: int, orderDto: OrderDTO) -> int:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE fastms.orders SET qty = %s, product_id = %s, ship_date = %s, customer_id = %s, service_officer = %s WHERE id = %s RETURNING *",
            (
                orderDto.qty,
                orderDto.product_id,
                orderDto.ship_date,
                orderDto.customer_id,
                orderDto.service_officer_email,
                order_id,
            ),
        )
        updated_order = cursor.fetchone()
        if updated_order is None:
            raise Exception("Order not found")
        conn.commit()
        return updated_order[0]
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Order not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def remove_order(order_id) -> int:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM fastms.orders WHERE id = %s RETURNING *", (order_id,)
        )
        deleted_order = cursor.fetchone()
        if len(deleted_order) == 0:
            raise Exception("Order not found")
        conn.commit()
        return deleted_order[0]
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "Order not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()
