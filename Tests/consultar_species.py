from utils.db_utils import get_connection

def imprimir_species():
    conn = get_connection()
    with conn.cursor() as cur:
        print("\n🧾 Contenido de isekai.species:")
        cur.execute("SELECT code, name FROM isekai.species;")
        rows = cur.fetchall()
        for code, name in rows:
            print(f"   - {code}: {name}")

if __name__ == "__main__":
    imprimir_species()
