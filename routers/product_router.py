from fastapi import APIRouter, Depends
from services import product_services, auth_services
from models.model import Product
from DTO.dto import ProductDTO
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

router = APIRouter()


@router.get("/api/v1/product", status_code=200)
def get_products(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    auth_services.route_authenticate(token)
    products = product_services.get_products()
    products = [product.dict() for product in products]
    return {"message": "success", "data": products}


@router.get("/api/v1/product/{product_id}", status_code=200)
def get_product_by_id(
    product_id: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    product = product_services.get_product_by_id(product_id)
    product = product.dict()
    return {"message": "success", "data": product}


@router.post("/api/v1/product", status_code=201)
def create_product(
    product: ProductDTO, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    product = product_services.create_product(product)
    product = product.dict()
    return {"message": "success", "data": product}


@router.put("/api/v1/product/{product_id}", status_code=200)
def update_product(
    product_id: str,
    product: ProductDTO,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    auth_services.route_authenticate(token)
    product = product_services.update_product(product_id, product)
    product = product.dict()
    return {"message": "success", "data": product}


@router.delete("/api/v1/product/{product_id}", status_code=200)
def remove_product(
    product_id: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    product = product_services.remove_product(product_id)
    product = product.dict()
    return {"message": "success", "data": product}
