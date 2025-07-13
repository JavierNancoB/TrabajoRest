# db_utils.py
import psycopg2
from psycopg2 import OperationalError

# 🔒 Conexión global compartida
CONN_INFO = {
    'host': '159.223.200.213',
    'port': 5432,
    'user': 'isekai',
    'password': 'Fr9tL28mQxD7vKcp',
    'dbname': 'isekaidb'
}

# Variable global de conexión (se crea cuando se llama `get_connection()`)
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
