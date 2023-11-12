# Establish a connection

import psycopg2


def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="admin",
    )
