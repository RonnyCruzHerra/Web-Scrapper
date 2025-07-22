# db/db_connection.py

import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import OperationalError

# Cargar variables del entorno
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

def insert_data_pg(title, url, content):
    conn = get_connection()
    if conn is None:
        print("❌ No se pudo insertar el dato porque no hay conexión.")
        return

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scraped_data (title, url, content)
            VALUES (%s, %s, %s)
            ON CONFLICT (url) DO UPDATE SET content = EXCLUDED.content
        """, (title, url, content))
        conn.commit()
        cur.close()
    except Exception as e:
        print("❌ Error al insertar en la base de datos:", e)
    finally:
        conn.close()

