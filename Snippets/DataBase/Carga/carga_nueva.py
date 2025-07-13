import psycopg2
from pathlib import Path
import time

DB_CONFIG = {
    "dbname": "trabajo2paralela",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": 5432,
}
TABLE_NAME = "eldoria"
CSV_PATH = Path(r"C:\Users\javie\OneDrive\Documentos\Trabajo Paralela\eldoria.csv")

def crear_tabla(cur):
    cur.execute(f"""
        DROP TABLE IF EXISTS {TABLE_NAME};
        CREATE TABLE {TABLE_NAME} (
            identificador VARCHAR(30) PRIMARY KEY,
            especie VARCHAR(50),
            genero VARCHAR(20),
            nombre VARCHAR(50),
            apellido VARCHAR(50),
            fecha_nacimiento TIMESTAMP,
            cp_origen BIGINT,
            cp_destino BIGINT
        );
    """)

def cargar_csv():
    start_total = time.time()
    try:
        with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
            print("🧨 Dropeando y creando tabla...")
            crear_tabla(cur)
            conn.commit()

            with open(CSV_PATH, "r", encoding="utf-8") as f:
                next(f)  # saltar header si la tabla ya tiene columnas en orden
                cur.copy_expert(
                    f"COPY {TABLE_NAME} FROM STDIN WITH CSV DELIMITER ';'",
                    f
                )
            conn.commit()
        total_time = time.time() - start_total
        print(f"✅ Carga completa. Tiempo total: {total_time:.2f} segundos.")

    except Exception as e:
        print("❌ Error durante la carga:", e)

if __name__ == "__main__":
    cargar_csv()
