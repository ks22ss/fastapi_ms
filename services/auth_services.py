import sys
import os
from jose import jwt, JWTError
import base64
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DTO.dto import LoginDTO, UserCreateDTO, UserReadDTO
from services import create_connection
from icecream import ic
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import logging


def verify_password(plain_password, encoded_password):
    res = base64.b64encode(plain_password.encode("utf-8")).decode("utf-8")
    return res == encoded_password


def jwt_authenticate(token: str):
    payload = jwt.decode(token.credentials, os.getenv("SECRET"), algorithms=["HS256"])
    email = payload.get("sub")
    expiration = datetime.fromtimestamp(payload.get("exp"))
    current_time = datetime.utcnow()
    if email is None or expiration < current_time:
        return False
    return True


def route_authenticate(token: str):
    try:
        if not jwt_authenticate(token):
            raise Exception
    except Exception as e:
        raise HTTPException(status_code=403, detail={"message": "fail", "data": str(e)})


def login(loginDto: LoginDTO):
    try:
        # check if user exists
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT email, name, encoded_password FROM fastms.user WHERE email = %s",
            (loginDto.email,),
        )
        results = cursor.fetchall()
        if len(results) == 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        # check if password is correct
        user = results[0]
        encoded_password = user[2]

        if not verify_password(loginDto.password, encoded_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Password incorrect"
            )

        # generate a jwt token
        access_token = jwt.encode(
            {"sub": loginDto.email, "exp": datetime.utcnow() + timedelta(minutes=30)},
            os.getenv("SECRET"),
            algorithm="HS256",
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise e
    finally:
        conn.close()


def create_user(userCreateDTO: UserCreateDTO) -> UserReadDTO:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        encoded_password = base64.b64encode(
            userCreateDTO.password.encode("utf-8")
        ).decode("utf-8")
        cursor.execute(
            "INSERT INTO fastms.user (email, name, encoded_password) VALUES (%s, %s, %s) RETURNING email, name, signup_ts",
            (
                userCreateDTO.email,
                userCreateDTO.name,
                encoded_password,
            ),
        )
        inserted_user = cursor.fetchone()
        if len(inserted_user) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        inserted_user = UserReadDTO(
            email=inserted_user[0], name=inserted_user[1], signup_ts=inserted_user[2]
        )
        conn.commit()
        return inserted_user
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


if __name__ == "__main__":
    loginDto = LoginDTO(email="another3@gmail.com", password="testpassword2")
    jwtToken = login(loginDto)
    ic(jwtToken)
