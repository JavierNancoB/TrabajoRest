from db_utils import get_connection

def imprimir_primeros_10_persons():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM isekai.persons
            ORDER BY pk
            LIMIT 10;
        """)
        filas = cur.fetchall()
        columnas = [desc[0] for desc in cur.description]

        print(f"\n🧾 Primeros 10 registros de isekai.persons:")
        for fila in filas:
            fila_dict = dict(zip(columnas, fila))
            print(f" - {fila_dict}")

if __name__ == "__main__":
    imprimir_primeros_10_persons()
