from utils.db_utils import get_connection

def imprimir_strata():
    conn = get_connection()
    with conn.cursor() as cur:
        print("\n🧾 Contenido de isekai.strata:")
        cur.execute("SELECT code, name FROM isekai.strata;")
        rows = cur.fetchall()
        for code, name in rows:
            print(f"   - {code}: {name}")

if __name__ == "__main__":
    imprimir_strata()
