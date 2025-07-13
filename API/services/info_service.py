from typing import List
from models.schemas import InfoItem
from utils.db_utils import get_connection
from fastapi import HTTPException

def fetch_table_data(schema: str, table: str) -> List[InfoItem]:
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
