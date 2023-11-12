from fastapi import APIRouter, Depends
from services import order_services, auth_services
from DTO.dto import OrderDTO
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()


@router.get("/api/v1/order", status_code=200)
def get_order(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    auth_services.route_authenticate(token)
    order = order_services.get_orders()
    order = [order.dict() for order in order]
    return {"message": "success", "data": order}


@router.get("/api/v1/order/{order_id}", status_code=200)
def get_order_by_id(
    order_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    order = order_services.get_order_by_id(order_id)
    order = order.dict()
    return {"message": "success", "data": order}


@router.get("/api/v1/order/customer/{customer_id}", status_code=200)
def get_order_by_customer_id(
    customer_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    order = order_services.get_order_by_customer_id(customer_id)
    order = [order.dict() for order in order]
    return {"message": "success", "data": order}


@router.post("/api/v1/order", status_code=201)
def create_order(
    orderDto: OrderDTO, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    order_id = order_services.create_order(orderDto)
    return {"message": "success", "data": {"order_id": order_id}}


@router.put("/api/v1/order/{order_id}", status_code=200)
def update_order(
    order_id: int,
    orderDto: OrderDTO,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    auth_services.route_authenticate(token)
    order_id = order_services.update_order(order_id, orderDto)
    return {"message": "success", "data": {"order_id": order_id}}


@router.delete("/api/v1/order/{order_id}", status_code=200)
def remove_order(
    order_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    order_id = order_services.remove_order(order_id)
    return {"message": "success", "data": {"order_id": order_id}}
