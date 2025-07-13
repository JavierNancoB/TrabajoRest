"""
db_utils.py

Módulo de utilidades para manejar la conexión a la base de datos PostgreSQL.

Este módulo carga las credenciales desde un archivo `.env` utilizando `dotenv`
y proporciona una función reutilizable para obtener una conexión persistente a la base de datos.
"""

import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Información de conexión a la base de datos extraída de las variables de entorno
CONN_INFO = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'dbname': os.getenv('DB_NAME')
}
"""
Diccionario con los parámetros necesarios para conectarse a la base de datos PostgreSQL.

Los valores se obtienen desde variables de entorno definidas en un archivo `.env`.
"""

# Tabla principal utilizada para las estadísticas
PERSONS_TABLE = os.getenv("PERSONS_TABLE", "isekai.persons")
"""
Nombre completo de la tabla de personas con esquema incluido (por ejemplo: 'isekai.persons').

Este valor se utiliza en las consultas estadísticas y se puede configurar desde el archivo `.env`.
"""

conexion = None
"""Conexión global reutilizable a la base de datos PostgreSQL."""

def get_connection():
    """
    Retorna una conexión activa a la base de datos PostgreSQL.

    Si no existe una conexión previa o está cerrada, se crea una nueva utilizando
    los parámetros definidos en `CONN_INFO`. En caso de error de conexión, se
    lanza una excepción.

    Returns:
        connection (psycopg2.extensions.connection): Objeto de conexión a la base de datos.

    Raises:
        OperationalError: Si ocurre un error al intentar conectarse a la base de datos.
    """
    global conexion
    if conexion is None or conexion.closed:
        try:
            conexion = psycopg2.connect(**CONN_INFO)
            print("✅ Conexión creada correctamente.")
        except OperationalError as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            raise
    return conexion
