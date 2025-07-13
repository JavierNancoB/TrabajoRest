# count_persons_standalone.py

from utils.db_utils import get_connection
from concurrent.futures import ThreadPoolExecutor
import json

# 🔧 Aquí defines los códigos que quieres usar
STRATA_CODE = "0"
SPECIES_CODE = "HU"
GENDER_CODE = "F"

# mapping de la columna PK de cada tabla
FK_COLUMNS = {
    "strata": "pk",
    "species": "pk",
    "genders": "pk"
}

def get_fk_from_code(table: str, code: str) -> int:
    column = FK_COLUMNS.get(table)
    if not column:
        raise ValueError(f"No se conoce la columna PK de la tabla {table}")
    
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(f"SELECT {column} FROM isekai.{table} WHERE code = %s;", (code,))
        result = cur.fetchone()
        if not result:
            raise ValueError(f"No se encontró código '{code}' en {table}")
        return result[0]

def count_filtered(strata_fk: int, species_fk: int, gender_fk: int) -> int:
    query = """
    SELECT COUNT(*) FROM isekai.persons
    WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s;
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, (strata_fk, species_fk, gender_fk))
        return cur.fetchone()[0]

def count_total() -> int:
    query = "SELECT COUNT(*) FROM isekai.persons;"
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchone()[0]

def run_count_analysis():
    try:
        strata_fk = get_fk_from_code("strata", STRATA_CODE)
        species_fk = get_fk_from_code("species", SPECIES_CODE)
        gender_fk = get_fk_from_code("genders", GENDER_CODE)

        with ThreadPoolExecutor() as executor:
            future_filtered = executor.submit(count_filtered, strata_fk, species_fk, gender_fk)
            future_total = executor.submit(count_total)

            count = future_filtered.result()
            total = future_total.result()

        percentage = round(count / total, 6) if total > 0 else 0.0

        result = {
            "count": count,
            "percentage": percentage
        }

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_count_analysis()
