import psycopg2
from psycopg2.extras import RealDictCursor
import os

DB_CONFIG ={
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user" : os.getenv("DB_USER"),
    "password" : os.getenv("DB_PASSWORD")
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        raise