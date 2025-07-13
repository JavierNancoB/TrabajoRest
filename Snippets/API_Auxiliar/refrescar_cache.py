import psycopg2
import json
from datetime import datetime
from db_utils import CONN_INFO
import os

CACHE_PATH = "./cache/personas_count.json"

def generar_cache_optimizado():
    print("🚀 Inicio de la generación del cache")
    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)  # crea carpeta si no existe
    try:
        conn = psycopg2.connect(**CONN_INFO)
        resultados = {}

        with conn.cursor() as cur:
            query = """
                SELECT strata_fk, gender_fk, species_fk, COUNT(*)
                FROM isekai.persons
                GROUP BY strata_fk, gender_fk, species_fk
                ORDER BY strata_fk, gender_fk, species_fk;
            """
            cur.execute(query)
            rows = cur.fetchall()

            for strata_fk, gender_fk, species_fk, count in rows:
                key = f"{strata_fk}-{gender_fk}-{species_fk}"
                resultados[key] = count

        conn.close()

        cache_data = {
            "last_update": datetime.utcnow().isoformat(),
            "data": resultados
        }

        with open(CACHE_PATH, "w") as f:
            json.dump(cache_data, f, indent=2)

        print(f"✅ Cache actualizado correctamente en {CACHE_PATH}")
    except Exception as e:
        print(f"❌ Error durante la generación del cache: {e}")

if __name__ == "__main__":
    generar_cache_optimizado()
    print("🏁 Script finalizado")
