"""
info_service.py

Servicio para obtener datos base desde tablas del esquema `isekai`, como especies,
estratos sociales y géneros.

Proporciona funciones que consultan tablas dinámicamente y devuelven resultados
formateados como objetos `InfoItem`.
"""

from typing import List
from models.schemas import InfoItem
from utils.db_utils import get_connection
from fastapi import HTTPException

def fetch_table_data(schema: str, table: str) -> List[InfoItem]:
    """
    Obtiene datos desde una tabla específica y los transforma en una lista de `InfoItem`.

    Esta función se utiliza para consultar tablas como `species`, `strata` o `genders`,
    y retornar los pares `code` y `name` para alimentar los endpoints informativos.

    Args:
        schema (str): Nombre del esquema en la base de datos (por lo general 'isekai').
        table (str): Nombre de la tabla a consultar.

    Returns:
        List[InfoItem]: Lista de objetos con código y nombre.

    Raises:
        HTTPException: Si no hay resultados (404) o ocurre un error en la consulta (500).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT code, name FROM {schema}.{table};")
            rows = cur.fetchall()
            if not rows:
                raise HTTPException(status_code=404, detail=f"No hay información de {table} disponible")
            return [InfoItem(code=str(code), name=str(name)) for code, name in rows]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar {table}: {e}")
