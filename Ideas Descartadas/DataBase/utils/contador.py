import psycopg2

# Datos de conexión
DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432

TABLAS = ["species", "genders", "strata", "persons", "eldoria"]

def contar_filas_tablas():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cur = conn.cursor()

        print("📊 Conteo de filas por tabla:\n")

        for tabla in TABLAS:
            cur.execute(f'SELECT COUNT(*) FROM public."{tabla}";')
            count = cur.fetchone()[0]
            print(f"🧾 {tabla}: {count} filas")

        cur.close()
        conn.close()
    except Exception as e:
        print("💥 Error:", e)

if __name__ == "__main__":
    contar_filas_tablas()
