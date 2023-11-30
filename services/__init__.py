# Establish a connection

import psycopg2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
import os


def create_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
