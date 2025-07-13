from utils.db_utils import get_connection

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

def count_and_percentage_by_codes(strata_code: str, species_code: str, gender_code: str) -> dict:
    with get_connection() as conn:
        strata_fk = get_fk_from_code(conn, "strata", strata_code)
        species_fk = get_fk_from_code(conn, "species", species_code)
        gender_fk = get_fk_from_code(conn, "genders", gender_code)

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
