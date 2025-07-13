import psycopg2
from utils.db_utils import CONN_INFO

def contar_todas_las_filas():
    try:
        conn = psycopg2.connect(**CONN_INFO)
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM isekai.persons;")
        total = cur.fetchone()[0]
        print(f"📊 Total de filas en isekai.persons (sin filtros): {total}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error al conectar o consultar: {e}")

if __name__ == "__main__":
    contar_todas_las_filas()
