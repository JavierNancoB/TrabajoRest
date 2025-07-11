import psycopg2
import unicodedata
import time

DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432

BATCH_SIZE = 10_000
MAX_BATCHES = 10000  # Esto te da hasta 100 millones si hay suficientes datos

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

def normalizar_str(s):
    s = unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII')
    return s.strip().title()

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

def crear_tabla_persons(cur):
    cur.execute("DROP TABLE IF EXISTS persons CASCADE;")
    cur.execute("""
        CREATE TABLE persons (
            id SERIAL PRIMARY KEY,
            species_fk INTEGER REFERENCES species(id),
            strata_fk INTEGER REFERENCES strata(id),
            gender_fk INTEGER REFERENCES genders(id),
            rut VARCHAR(30) UNIQUE,
            birthdate TIMESTAMP,
            firstname VARCHAR(50),
            lastname VARCHAR(50),
            created TIMESTAMP DEFAULT now(),
            updated TIMESTAMP DEFAULT now()
        );
    """)

def cargar_secuencial():
    try:
        conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
        cur = conn.cursor()

        print("🧨 Dropeando y creando tabla persons...")
        crear_tabla_persons(cur)
        conn.commit()

        fk_species, fk_genders, fk_strata = get_fk_maps(cur)

        last_id = ""  # Comienza desde el string vacío
        for i in range(MAX_BATCHES):
            print(f"🔄 Procesando lote {i+1} (identificador > '{last_id}')...")

            cur.execute("""
                SELECT identificador, especie, genero, nombre, apellido, fecha_nacimiento, cp_origen, cp_destino
                FROM eldoria
                WHERE identificador > %s
                ORDER BY identificador
                LIMIT %s;
            """, (last_id, BATCH_SIZE))

            rows = cur.fetchall()
            if not rows:
                print("⚠️  No hay más filas que procesar.")
                break

            last_id = rows[-1][0]  # Último RUT insertado

            datos, errores = procesar_lote(rows, fk_species, fk_genders, fk_strata)

            insert_query = """
                INSERT INTO persons (species_fk, strata_fk, gender_fk, rut, birthdate, firstname, lastname)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (rut) DO NOTHING;
            """
            cur.executemany(insert_query, datos)
            conn.commit()

            print(f"✅ Insertados: {len(datos)} | ❌ Errores: {len(errores)}")

            for e in errores[:3]:
                print(f"⚠️  Ejemplo error: {e}")

            # Puedes comentarlo si estás en modo turbo
            # time.sleep(0.5)

        cur.close()
        conn.close()

    except KeyboardInterrupt:
        print("\n🛑 Interrumpido por el usuario (Ctrl+C).")
    except Exception as e:
        print(f"💥 Excepción general: {e}")

if __name__ == "__main__":
    cargar_secuencial()
