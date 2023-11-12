from fastapi import APIRouter
from services import auth_services
from models.model import User
from DTO.dto import UserCreateDTO, UserReadDTO, LoginDTO

router = APIRouter()


@router.post("/api/v1/auth/login", status_code=200)
def login(loginDTO: LoginDTO):
    try:
        auth = auth_services.login(loginDTO)
    except Exception as e:
        return {"message": str(e)}
    return {"message": "success", "data": auth}


@router.post("/api/v1/auth/register", status_code=201)
def register(user: UserCreateDTO):
    try:
        user = auth_services.create_user(user)
        user = user.dict()
    except Exception as e:
        return {"message": str(e)}
    return {"message": "success", "data": user}
