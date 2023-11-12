from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from services import user_services, auth_services
from models.model import User
from DTO.dto import UserCreateDTO, UserReadDTO

router = APIRouter()


@router.get("/api/v1/user", status_code=200)
def get_users(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    auth_services.route_authenticate(token)
    users = user_services.get_users()
    users = [user.dict() for user in users]
    return {"message": "success", "data": users}


@router.get("/api/v1/user/{user_email}", status_code=200)
def get_user_by_id(
    user_email: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    user = user_services.get_user_by_email(user_email)
    user = user.dict()
    return {"message": "success", "data": user}


@router.post("/api/v1/user", status_code=201)
def create_user(
    user: UserCreateDTO, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    user = user_services.create_user(user)
    user = user.dict()
    return {"message": "success", "data": user}


@router.put("/api/v1/user/{user_email}", status_code=200)
def update_user(
    user_email: str,
    user: UserCreateDTO,
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
):
    auth_services.route_authenticate(token)
    user = user_services.update_user(user_email, user)
    user = user.dict()
    return {"message": "success", "data": user}


@router.delete("/api/v1/user/{user_email}", status_code=200)
def remove_user(
    user_email: str, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    auth_services.route_authenticate(token)
    user = user_services.remove_user(user_email)
    user = user.dict()
    return {"message": "success", "data": user}
