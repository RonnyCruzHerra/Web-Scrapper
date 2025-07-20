# db/db_connection.py

import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import OperationalError

# Cargar las variables desde .env
load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except OperationalError as e:
        print("❌ Error al conectar a la base de datos:", e)
        return None
