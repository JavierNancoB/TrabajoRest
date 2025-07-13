# import psycopg2
# from multiprocessing import Pool
# from utils.db_utils import CONN_INFO
# import time

# FILTERS = {
#     'strata_fk': 2,   # Cambia según necesites
#     'species_fk': 3,
#     'gender_fk': 1,
# }

# N_PROC = 8

# def contar_parcial_rango_filas(args):
#     start_rn, end_rn, filters = args
#     query = """
#     WITH filas_filtradas AS (
#         SELECT pk, ROW_NUMBER() OVER (ORDER BY pk) AS rn
#         FROM isekai.persons
#         WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s
#     )
#     SELECT COUNT(*) FROM filas_filtradas WHERE rn BETWEEN %s AND %s;
#     """
#     conn = psycopg2.connect(**CONN_INFO)
#     with conn.cursor() as cur:
#         cur.execute(query, (
#             filters['strata_fk'],
#             filters['species_fk'],
#             filters['gender_fk'],
#             start_rn,
#             end_rn
#         ))
#         resultado = cur.fetchone()[0]
#     conn.close()
#     print(f"Filas {start_rn}-{end_rn}: {resultado} registros")
#     return resultado

# def contar_total_con_row_number(filters):
#     conn = psycopg2.connect(**CONN_INFO)
#     with conn.cursor() as cur:
#         cur.execute("""
#             SELECT COUNT(*) FROM isekai.persons
#             WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s
#         """, (filters['strata_fk'], filters['species_fk'], filters['gender_fk']))
#         total_registros = cur.fetchone()[0]
#     conn.close()

#     chunk_size = total_registros // N_PROC
#     rangos = []
#     for i in range(N_PROC):
#         start = i * chunk_size + 1
#         end = (i + 1) * chunk_size if i < N_PROC - 1 else total_registros
#         rangos.append((start, end, filters))

#     with Pool(N_PROC) as pool:
#         resultados = pool.map(contar_parcial_rango_filas, rangos)

#     return sum(resultados)

# if __name__ == "__main__":
#     start_time = time.perf_counter()
#     total = contar_total_con_row_number(FILTERS)
#     elapsed = time.perf_counter() - start_time
#     print(f"\nTotal registros con filtro: {total}")
#     print(f"Tiempo total (paralelo): {elapsed:.2f} segundos")

import psycopg2
from utils.db_utils import CONN_INFO

def explain_analyze_count(filters):
    query = """
    EXPLAIN ANALYZE
    SELECT COUNT(*) FROM isekai.persons
    WHERE strata_fk = %s AND species_fk = %s AND gender_fk = %s;
    """
    conn = psycopg2.connect(**CONN_INFO)
    with conn.cursor() as cur:
        cur.execute(query, (filters['strata_fk'], filters['species_fk'], filters['gender_fk']))
        plan = cur.fetchall()
    conn.close()

    print("\nPlan de ejecución EXPLAIN ANALYZE:")
    for line in plan:
        print(line[0])

if __name__ == "__main__":
    FILTERS = {
        'strata_fk': 2,
        'species_fk': 3,
        'gender_fk': 1,
    }
    explain_analyze_count(FILTERS)
