"""
stats_service.py

Servicios para calcular estadísticas sobre los personajes del mundo isekai,
como proporciones y análisis de edad.

Incluye funciones que traducen códigos a llaves foráneas y ejecutan consultas SQL
paralelizadas para optimizar el rendimiento.
"""

from utils.db_utils import get_connection, PERSONS_TABLE
from concurrent.futures import ThreadPoolExecutor
import time

# Cache para evitar consultas repetidas
FK_CACHE = {}

# Tiempo de vida del caché (en segundos)
CACHE_TTL = 300

# Mapeo de tablas a sus columnas de clave primaria
FK_COLUMNS = {
    "strata": "pk",
    "species": "pk",
    "genders": "pk"
}

def get_fk_from_code(conn, table: str, code: str) -> int:
    """
    Obtiene la clave primaria asociada a un código desde una tabla dada.

    Usa una caché con tiempo de vida (TTL) para evitar repetir consultas idénticas.

    Args:
        conn: Conexión activa a la base de datos.
        table (str): Nombre de la tabla ('strata', 'species' o 'genders').
        code (str): Código textual a traducir.

    Returns:
        int: Clave primaria correspondiente.

    Raises:
        ValueError: Si la tabla no es válida o el código no existe.
    """
    key = (table, code)
    now = time.time()

    if key in FK_CACHE:
        cached_time, cached_value = FK_CACHE[key]
        if now - cached_time < CACHE_TTL:
            return cached_value
        else:
            # Expiró el caché, eliminar entrada
            del FK_CACHE[key]

    column = FK_COLUMNS.get(table)
    if not column:
        raise ValueError(f"No se conoce la columna PK de la tabla {table}")

    with conn.cursor() as cur:
        cur.execute(f"SELECT {column} FROM isekai.{table} WHERE code = %s;", (code,))
        result = cur.fetchone()
        if not result:
            raise ValueError(f"No se encontró código '{code}' en {table}")

        FK_CACHE[key] = (now, result[0])
        return result[0]

def get_fks_parallel(conn, strata_code, species_code, gender_code):
    """
    Traduce los códigos a claves primarias usando paralelización.

    Ejecuta tres consultas simultáneamente mediante `ThreadPoolExecutor`.

    Args:
        conn: Conexión activa a la base de datos.
        strata_code (str): Código del estrato social.
        species_code (str): Código de especie.
        gender_code (str): Código de género.

    Returns:
        tuple: Claves primarias (strata_fk, species_fk, gender_fk).
    """
    with ThreadPoolExecutor() as executor:
        future_strata = executor.submit(get_fk_from_code, conn, "strata", strata_code)
        future_species = executor.submit(get_fk_from_code, conn, "species", species_code)
        future_gender = executor.submit(get_fk_from_code, conn, "genders", gender_code)

        strata_fk = future_strata.result()
        species_fk = future_species.result()
        gender_fk = future_gender.result()

    return strata_fk, species_fk, gender_fk

def count_and_percentage_by_codes(strata_code: str, species_code: str, gender_code: str) -> dict:
    """
    Calcula el conteo de personas que cumplen con los tres filtros y su proporción.

    Realiza una consulta SQL que filtra por claves foráneas y devuelve tanto el total
    como el subconjunto coincidente.

    Args:
        strata_code (str): Código del estrato social.
        species_code (str): Código de especie.
        gender_code (str): Código de género.

    Returns:
        dict: Diccionario con el conteo filtrado y el porcentaje respecto al total.
    """
    with get_connection() as conn:
        strata_fk, species_fk, gender_fk = get_fks_parallel(conn, strata_code, species_code, gender_code)

        query = f"""
        SELECT 
            COUNT(*) FILTER (WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s) AS filtered_count,
            COUNT(*) AS total_count
        FROM {PERSONS_TABLE};
        """
        with conn.cursor() as cur:
            cur.execute(query, (strata_fk, species_fk, gender_fk))
            filtered_count, total_count = cur.fetchone()

    percentage = round(filtered_count / total_count, 6) if total_count > 0 else 0.0
    return {"count": filtered_count, "percentage": percentage}

def age_stats_by_codes(strata_code: str, species_code: str, gender_code: str) -> dict:
    """
    Calcula estadísticas de edad (mínima, máxima, promedio y desviación estándar).

    Filtra por combinación de claves foráneas para calcular métricas sobre los personajes.

    Args:
        strata_code (str): Código del estrato social.
        species_code (str): Código de especie.
        gender_code (str): Código de género.

    Returns:
        dict: Diccionario con `min_age`, `max_age`, `avg_age`, y `stddev_age`.
              Todos los valores están redondeados a dos decimales, o `None` si no hay datos.
    """
    with get_connection() as conn:
        strata_fk, species_fk, gender_fk = get_fks_parallel(conn, strata_code, species_code, gender_code)

        query = f"""
        SELECT
            MIN(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS min_age,
            MAX(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS max_age,
            AVG(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS avg_age,
            STDDEV(EXTRACT(epoch FROM (CURRENT_DATE - birthdate)) / 86400 / 365.25) AS stddev_age
        FROM {PERSONS_TABLE}
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
