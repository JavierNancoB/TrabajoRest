import psycopg2
from psycopg2 import OperationalError

conn_info = {
    'host': '159.223.200.213',
    'port': 5432,
    'user': 'isekai',
    'password': 'Fr9tL28mQxD7vKcp',
    'dbname': 'isekaidb'
}

def conectar_y_obtener_info():
    try:
        with psycopg2.connect(**conn_info) as conn:
            with conn.cursor() as cur:
                print("✅ Conexión exitosa a la base de datos 'isekaidb'.")

                # Consultar las bases disponibles (opcional)
                cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                bases = cur.fetchall()
                print("📦 Bases de datos disponibles:")
                for base in bases:
                    print(f"- {base[0]}")

                # Obtener número de CPUs visibles para PostgreSQL
                cur.execute("SHOW max_parallel_workers;")  # Puede usarse también: 'SHOW max_worker_processes;'
                max_workers = cur.fetchone()[0]
                print(f"🧠 Número de workers paralelos permitidos: {max_workers}")

    except OperationalError as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    conectar_y_obtener_info()
