import sys
import os
import base64

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from DTO.dto import UserCreateDTO, UserReadDTO
from models.model import User
from icecream import ic
from services import create_connection, auth_services
from typing import List
from fastapi import HTTPException, status


def get_user_by_email(email: str) -> UserReadDTO:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT email, name, signup_ts FROM fastms.user WHERE email = %s", (email,)
        )
        results = cursor.fetchall()
        if len(results) == 0:
            raise Exception("User not found")
        user = UserReadDTO(
            email=results[0][0], name=results[0][1], signup_ts=results[0][2]
        )
        return user
    except Exception as e:
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "User not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def get_users() -> List[UserReadDTO]:
    try:
        users = []
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT email, name, signup_ts FROM fastms.user")
        results = cursor.fetchall()

        if len(results) == 0:
            return users

        for user in results:
            users.append(UserReadDTO(email=user[0], name=user[1], signup_ts=user[2]))

        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def update_user(cur_email: str, userCreateDTO: UserCreateDTO) -> UserReadDTO:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        encoded_password = base64.b64encode(
            userCreateDTO.password.encode("utf-8")
        ).decode("utf-8")
        cursor.execute(
            "UPDATE fastms.user SET name = %s, email = %s, encoded_password=%s WHERE email = %s RETURNING email, name, signup_ts",
            (
                userCreateDTO.name,
                userCreateDTO.email,
                encoded_password,
                cur_email,
            ),
        )
        updated_user = cursor.fetchone()
        if len(updated_user) == 0:
            raise Exception("User not found")
        updated_user = UserReadDTO(
            email=updated_user[0], name=updated_user[1], signup_ts=updated_user[2]
        )
        conn.commit()
        return updated_user
    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "User not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))
    finally:
        conn.close()


def remove_user(cur_email) -> UserReadDTO:
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM fastms.user WHERE email = %s RETURNING *", (cur_email,)
        )
        deleted_user = cursor.fetchone()
        print(deleted_user)
        if len(deleted_user) == 0:
            raise Exception("User not found")
        deleted_user = UserReadDTO(
            email=deleted_user[0], name=deleted_user[1], signup_ts=deleted_user[2]
        )
        conn.commit()
        return deleted_user

    except Exception as e:
        conn.rollback()
        error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        if str(e) == "User not found":
            error_status = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=error_status, detail=str(e))

    finally:
        conn.close()
