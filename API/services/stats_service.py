from utils.db_utils import get_connection
from concurrent.futures import ThreadPoolExecutor

# Cache para evitar consultas repetidas
FK_CACHE = {}

FK_COLUMNS = {
    "strata": "pk",
    "species": "pk",
    "genders": "pk"
}

def get_fk_from_code(conn, table: str, code: str) -> int:
    key = (table, code)
    if key in FK_CACHE:
        return FK_CACHE[key]

    column = FK_COLUMNS.get(table)
    if not column:
        raise ValueError(f"No se conoce la columna PK de la tabla {table}")

    with conn.cursor() as cur:
        cur.execute(f"SELECT {column} FROM isekai.{table} WHERE code = %s;", (code,))
        result = cur.fetchone()
        if not result:
            raise ValueError(f"No se encontró código '{code}' en {table}")
        FK_CACHE[key] = result[0]
        return result[0]

def get_fks_parallel(conn, strata_code, species_code, gender_code):
    with ThreadPoolExecutor() as executor:
        future_strata = executor.submit(get_fk_from_code, conn, "strata", strata_code)
        future_species = executor.submit(get_fk_from_code, conn, "species", species_code)
        future_gender = executor.submit(get_fk_from_code, conn, "genders", gender_code)

        strata_fk = future_strata.result()
        species_fk = future_species.result()
        gender_fk = future_gender.result()

    return strata_fk, species_fk, gender_fk

def count_and_percentage_by_codes(strata_code: str, species_code: str, gender_code: str) -> dict:
    with get_connection() as conn:
        strata_fk, species_fk, gender_fk = get_fks_parallel(conn, strata_code, species_code, gender_code)

        query = """
        SELECT 
            COUNT(*) FILTER (WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s) AS filtered_count,
            COUNT(*) AS total_count
        FROM isekai.persons;
        """
        with conn.cursor() as cur:
            cur.execute(query, (strata_fk, species_fk, gender_fk))
            filtered_count, total_count = cur.fetchone()

    percentage = round(filtered_count / total_count, 6) if total_count > 0 else 0.0
    return {"count": filtered_count, "percentage": percentage}

def age_stats_by_codes(strata_code: str, species_code: str, gender_code: str) -> dict:
    with get_connection() as conn:
        strata_fk, species_fk, gender_fk = get_fks_parallel(conn, strata_code, species_code, gender_code)

        query = """
        SELECT
            MIN(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS min_age,
            MAX(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS max_age,
            AVG(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS avg_age,
            STDDEV(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS stddev_age
        FROM isekai.persons
        WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s;
        """

        with conn.cursor() as cur:
            cur.execute(query, (strata_fk, species_fk, gender_fk))
            result = cur.fetchone()

        if not result or result[3] is None:  # No hay personas o stddev null
            return {
                "min_age": None,
                "max_age": None,
                "avg_age": None,
                "stddev_age": None
            }

        min_age, max_age, avg_age, stddev_age = result
        return {
            "min_age": round(min_age, 2),
            "max_age": round(max_age, 2),
            "avg_age": round(avg_age, 2),
            "stddev_age": round(stddev_age, 2) if stddev_age is not None else None
        }

