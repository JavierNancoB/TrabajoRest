import psycopg2
import time
from db_utils import CONN_INFO  # Asegúrate de tener esta variable definida

def medir_tiempo_max_updated():
    query = "SELECT MAX(updated) FROM isekai.persons;"
    conn = psycopg2.connect(**CONN_INFO)

    start_time = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute(query)
        max_updated = cur.fetchone()[0]
    elapsed = time.perf_counter() - start_time

    conn.close()

    print("🧪 Consulta ejecutada:")
    print(f"🕒 Tiempo de consulta MAX(updated): {elapsed:.4f} segundos")
    print(f"🗓️  Valor obtenido: {max_updated.isoformat() if max_updated else 'Sin resultados'}")

if __name__ == "__main__":
    medir_tiempo_max_updated()
