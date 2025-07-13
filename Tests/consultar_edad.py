# age_stats_standalone.py

from utils.db_utils import get_connection
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json

# 🔧 Códigos que quieres usar
STRATA_CODE = "0"
SPECIES_CODE = "HU"
GENDER_CODE = "F"

# Mapping de la columna PK por tabla
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

def compute_age_stats(strata_fk: int, species_fk: int, gender_fk: int):
    query = """
    SELECT birthdate FROM isekai.persons
    WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s;
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, (strata_fk, species_fk, gender_fk))
        birthdates = cur.fetchall()
        
        if not birthdates:
            return {
                "min_age": None,
                "max_age": None,
                "avg_age": None,
                "count": 0
            }

        today = datetime.now()
        ages = [(today - bd[0]).days // 365 for bd in birthdates]  # Edad en años aprox

        return {
            "min_age": min(ages),
            "max_age": max(ages),
            "avg_age": round(sum(ages) / len(ages), 2),
            "count": len(ages)
        }

def run_age_analysis():
    try:
        strata_fk = get_fk_from_code("strata", STRATA_CODE)
        species_fk = get_fk_from_code("species", SPECIES_CODE)
        gender_fk = get_fk_from_code("genders", GENDER_CODE)

        with ThreadPoolExecutor() as executor:
            future_stats = executor.submit(compute_age_stats, strata_fk, species_fk, gender_fk)
            result = future_stats.result()

        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_age_analysis()
