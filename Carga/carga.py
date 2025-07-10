import psycopg2
import unicodedata

DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432
TABLE_NAME = "eldoria"
CSV_PATH = r"C:\Users\javie\OneDrive\Documentos\Trabajo Paralela\eldoria.csv"

def clean_column_name(s):
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    s = s.replace(" ", "_")
    s = ''.join(c for c in s if c.isalnum() or c == '_')
    return s.lower()

def cargar_csv():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        header_line = f.readline().strip()
        header = header_line.split(";")
        header = [clean_column_name(h) for h in header]

    print(f"Columnas detectadas para COPY: {header}")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        next(f)  # saltar header
        try:
            cur.copy_expert(f"COPY {TABLE_NAME} ({', '.join(header)}) FROM STDIN WITH CSV DELIMITER ';'", f)
            conn.commit()
            print("Carga finalizada exitosamente.")
        except psycopg2.Error as e:
            print("Error durante COPY:", e)
            conn.rollback()

    cur.close()
    conn.close()

if __name__ == "__main__":
    cargar_csv()
