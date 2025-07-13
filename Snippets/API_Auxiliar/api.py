from fastapi import FastAPI, HTTPException
import json
import os
from datetime import datetime
import psycopg2
from db_utils import CONN_INFO

app = FastAPI(title="Isekai API", description="API para contar personas por combinación de FKs")

CACHE_PATH = "./cache/personas_count.json"
MAX_UPDATED_REFRESH_INTERVAL = 30  # segundos

# 🧠 Cache intermedio en memoria
max_updated_cache = {
    "timestamp": None,
    "value": None
}

def obtener_max_updated_con_cache():
    global max_updated_cache
    now = datetime.utcnow()

    if (
        max_updated_cache["timestamp"] is None or
        (now - max_updated_cache["timestamp"]).total_seconds() > MAX_UPDATED_REFRESH_INTERVAL
    ):
        try:
            conn = psycopg2.connect(**CONN_INFO)
            with conn.cursor() as cur:
                cur.execute("SELECT MAX(updated) FROM isekai.persons;")
                result = cur.fetchone()[0]
            conn.close()

            max_updated_cache["timestamp"] = now
            max_updated_cache["value"] = result.isoformat() if result else None
        except Exception as e:
            print(f"⚠️ Error al consultar MAX(updated): {e}")
            max_updated_cache["timestamp"] = now
            max_updated_cache["value"] = None

    return max_updated_cache["value"]

def cargar_cache():
    if not os.path.exists(CACHE_PATH):
        raise FileNotFoundError("El archivo de cache no existe")

    with open(CACHE_PATH, "r") as f:
        cache = json.load(f)

    cache_db_updated = cache.get("db_updated")
    db_actual = obtener_max_updated_con_cache()

    if cache_db_updated != db_actual:
        raise RuntimeError("Cache desactualizado")

    return cache["data"]

@app.get("/personas/count")
def contar_personas(strata_fk: int, species_fk: int, gender_fk: int):
    try:
        cache = cargar_cache()
        key = f"{strata_fk}-{gender_fk}-{species_fk}"
        print(f"🔎 Buscando clave: {key}")

        if key not in cache:
            return {
                "error": "Clave no encontrada",
                "requested_key": key,
                "available_keys_sample": list(cache.keys())[:10]
            }

        return {
            "count": cache[key],
            "cache": "hit"
        }
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Cache no generado aún")
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Cache expirado, espera su actualización")
