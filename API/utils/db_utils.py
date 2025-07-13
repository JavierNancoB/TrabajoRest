# db_utils.py
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el .env
load_dotenv()

CONN_INFO = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME')
}

conexion = None

def get_connection():
    global conexion
    if conexion is None or conexion.closed:
        try:
            conexion = psycopg2.connect(**CONN_INFO)
            print("✅ Conexión creada correctamente.")
        except OperationalError as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            raise
    return conexion
