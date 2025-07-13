import socket
import time
import psycopg2
from db_utils import CONN_INFO

def medir_ping(host, port=5432, timeout=1):
    """Mide el tiempo de respuesta TCP haciendo un intento de conexión."""
    start = time.perf_counter()
    try:
        with socket.create_connection((host, port), timeout):
            pass
    except Exception as e:
        print(f"Error en ping TCP: {e}")
        return None
    end = time.perf_counter()
    return (end - start) * 1000  # ms

def medir_conexion_y_consulta():
    host = CONN_INFO['host']
    port = CONN_INFO.get('port', 5432)
    
    ping_ms = medir_ping(host, port)
    print(f"🏓 Ping TCP a {host}:{port} = {ping_ms:.2f} ms")

    # Medir apertura de conexión
    start_conn = time.perf_counter()
    conn = psycopg2.connect(**CONN_INFO)
    end_conn = time.perf_counter()
    print(f"⏱️ Tiempo apertura conexión: {(end_conn - start_conn)*1000:.2f} ms")

    # Medir consulta rápida (ejemplo: SELECT 1)
    start_query = time.perf_counter()
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        _ = cur.fetchone()
    end_query = time.perf_counter()
    print(f"⏱️ Tiempo consulta simple: {(end_query - start_query)*1000:.2f} ms")

    # Medir cierre conexión
    start_close = time.perf_counter()
    conn.close()
    end_close = time.perf_counter()
    print(f"⏱️ Tiempo cierre conexión: {(end_close - start_close)*1000:.2f} ms")

    total = (end_close - start_conn)*1000
    print(f"⌛ Tiempo total (conexión + consulta + cierre): {total:.2f} ms")

if __name__ == "__main__":
    medir_conexion_y_consulta()
