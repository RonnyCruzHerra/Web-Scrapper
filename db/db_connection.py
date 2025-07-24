# db/db_connection.py

import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

# SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Cargar .env
load_dotenv()

# Datos desde .env
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# URL para SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 🔹 Motor SQLAlchemy y sesión
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
