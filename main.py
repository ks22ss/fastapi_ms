import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from fastapi import FastAPI
from routers import (
    user_router,
    customer_router,
    product_router,
    order_router,
    auth_router,
)


app = FastAPI()

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(customer_router.router)
app.include_router(product_router.router)
app.include_router(order_router.router)
