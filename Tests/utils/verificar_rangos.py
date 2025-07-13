import psycopg2
from db_utils import CONN_INFO

def obtener_rango_fk(tabla, campo):
    query = f"SELECT MIN({campo}), MAX({campo}) FROM {tabla};"
    conn = psycopg2.connect(**CONN_INFO)
    with conn.cursor() as cur:
        cur.execute(query)
        minimo, maximo = cur.fetchone()
    conn.close()
    return minimo, maximo

if __name__ == "__main__":
    campos = {
        'strata_fk': '🔺 Strata',
        'gender_fk': '⚧️ Gender',
        'species_fk': '🐾 Species'
    }

    print("📊 Rangos de foreign keys en isekai.persons:\n")

    for campo, nombre in campos.items():
        min_fk, max_fk = obtener_rango_fk('isekai.persons', campo)
        print(f"{nombre}:")
        print(f"   🔢 Mínimo: {min_fk}")
        print(f"   🔝 Máximo: {max_fk}")
        if min_fk == 0:
            print(f"   ⚠️ Empieza desde 0")
        elif min_fk == 1:
            print(f"   ✅ Empieza desde 1")
        else:
            print(f"   🤔 Empieza desde {min_fk}, revisar manualmente")
        print()
