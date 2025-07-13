import psycopg2
from db_utils import CONN_INFO

def existe_indice_updated():
    query = """
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE schemaname = 'isekai' AND tablename = 'persons'
      AND indexdef ILIKE '%(updated)%';
    """
    conn = psycopg2.connect(**CONN_INFO)
    with conn.cursor() as cur:
        cur.execute(query)
        indices = cur.fetchall()
    conn.close()

    if indices:
        print("✅ Índices que incluyen la columna 'updated':")
        for idx in indices:
            print(f"- {idx[0]} : {idx[1]}")
    else:
        print("❌ No existe índice sobre la columna 'updated' en isekai.persons.")

if __name__ == "__main__":
    existe_indice_updated()
