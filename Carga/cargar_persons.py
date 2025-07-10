import psycopg2
import multiprocessing
import unicodedata
import os




DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432

BATCH_SIZE = 10_000
TOTAL_BATCHES = 10_000  # Para cubrir 100 millones (100_000_000 / 10_000)
NUM_WORKERS = os.cpu_count() or 4  # Usa núcleos disponibles o 4 si no detecta

def normalizar_str(s):
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    return s.strip().title()

especie_map = {
    "Humana": "HU",
    "Elfica": "EL",
    "Enana": "EN",
    "Hombre Bestia": "HB"
}

genero_map = {
    "MACHO": "M",
    "HEMBRA": "F",
    "OTRO": "O"
}

def get_fk_maps(cur):
    def fetch_map(table):
        cur.execute(f"SELECT code, id FROM {table}")
        return {code: id_ for code, id_ in cur.fetchall()}
    
    species = fetch_map("species")
    genders = fetch_map("genders")
    strata = fetch_map("strata")

    return species, genders, strata

def procesar_lote(rows, fk_species, fk_genders, fk_strata):
    datos_insertar = []
    errores = []

    for row in rows:
        identificador, especie_es, genero_es, nombre, apellido, fecha_nac, cp_origen, _ = row

        especie_code = especie_map.get(normalizar_str(especie_es))
        genero_code = genero_map.get(genero_es.upper())

        if not especie_code:
            errores.append((identificador, "Especie no mapeada", especie_es))
            continue
        if not genero_code:
            errores.append((identificador, "Género no mapeado", genero_es))
            continue

        species_fk = fk_species.get(especie_code)
        gender_fk = fk_genders.get(genero_code)

        try:
            cp_str = str(int(cp_origen)).zfill(7)
            strata_code = cp_str[0]
            strata_fk = fk_strata.get(strata_code)
            if strata_fk is None:
                errores.append((identificador, "Strata no encontrada", strata_code))
                continue
        except Exception:
            errores.append((identificador, "Error al procesar cp_origen", str(cp_origen)))
            continue

        if not all([species_fk, gender_fk, strata_fk]):
            errores.append((identificador, "FK faltante", (species_fk, gender_fk, strata_fk)))
            continue

        datos_insertar.append((
            species_fk, strata_fk, gender_fk,
            identificador, fecha_nac, nombre, apellido
        ))

    return datos_insertar, errores

def worker(offset):
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()
        fk_species, fk_genders, fk_strata = get_fk_maps(cur)

        cur.execute(f"""
            SELECT identificador, especie, genero, nombre, apellido, fecha_nacimiento, cp_origen, cp_destino
            FROM eldoria
            ORDER BY identificador
            OFFSET %s LIMIT %s;
        """, (offset, BATCH_SIZE))

        rows = cur.fetchall()
        if not rows:
            print(f"[{offset}] Lote vacío.")
            return

        datos, errores = procesar_lote(rows, fk_species, fk_genders, fk_strata)

        insert_query = """
            INSERT INTO persons (species_fk, strata_fk, gender_fk, rut, birthdate, firstname, lastname)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (rut) DO NOTHING;
        """
        cur.executemany(insert_query, datos)
        conn.commit()

        print(f"[{offset}] ✅ {len(datos)} insertados. ❌ {len(errores)} errores.")

        if errores:
            for e in errores[:3]:
                print(f"[{offset}] ⚠️  Error: {e}")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"[{offset}] 💥 Excepción: {e}")

def cargar_paralelo():
    offsets = [i * BATCH_SIZE for i in range(TOTAL_BATCHES)]
    with multiprocessing.Pool(NUM_WORKERS) as pool:
        pool.map(worker, offsets)

if __name__ == "__main__":
    cargar_paralelo()
