import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ProductDTO(BaseModel):
    name: str
    model: str
    price: float
    description: str
    start_date: Optional[datetime] = None


class OrderDTO(BaseModel):
    qty: int
    product_id: int
    ship_date: Optional[datetime] = None
    customer_id: int
    service_officer_email: str


class CustomerDTO(BaseModel):
    name: str
    email: str
    address: str
    phone: str


class UserCreateDTO(BaseModel):
    email: str
    name: str
    password: str


class UserReadDTO(BaseModel):
    email: str
    name: str
    signup_ts: datetime


class LoginDTO(BaseModel):
    email: str
    password: str
