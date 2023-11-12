import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from DTO.dto import UserReadDTO


class User(BaseModel):
    email: str
    name: str
    encoded_password: str
    signup_ts: Optional[datetime] = None


class Product(BaseModel):
    id: int
    name: str
    model: str
    price: float
    description: str
    start_date: Optional[datetime] = None


class Customer(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str
    signup_ts: Optional[datetime] = None


class Order(BaseModel):
    id: int
    qty: int
    product: Product
    order_date: Optional[datetime] = None
    ship_date: Optional[datetime] = None
    service_officer: UserReadDTO
    customer: Customer
