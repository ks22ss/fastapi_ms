from fastapi import APIRouter, Depends
from services import customer_services, auth_services
from models.model import Customer
from DTO.dto import CustomerDTO
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()


@router.get("/api/v1/customer", status_code=200)
def get_customers(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    auth_services.route_authenticate(token)
    customers = customer_services.get_customers()
    customers = [customer.dict() for customer in customers]
    return {"message": "success", "data": customers}


@router.get("/api/v1/customer/{customer_id}", status_code=200)
def get_customer_by_id(
    customer_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    customer = customer_services.get_customer_by_id(customer_id)
    customer = customer.dict()
    return {"message": "success", "data": customer}


@router.post("/api/v1/customer", status_code=201)
def create_customer(
    customer: CustomerDTO, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    customer = customer_services.create_customer(customer)
    customer = customer.dict()
    return {"message": "success", "data": customer}


@router.put("/api/v1/customer/{customer_id}", status_code=200)
def update_customer(
    customer_id: int,
    customer: CustomerDTO,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    auth_services.route_authenticate(token)
    customer = customer_services.update_customer(customer_id, customer)
    customer = customer.dict()
    return {"message": "success", "data": customer}


@router.delete("/api/v1/customer/{customer_id}", status_code=200)
def remove_customer(
    customer_id: int, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    customer = customer_services.remove_customer(customer_id)
    customer = customer.dict()
    return {"message": "success", "data": customer}
