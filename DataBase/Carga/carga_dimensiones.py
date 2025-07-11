import psycopg2
from datetime import datetime

DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432

strata_data = [
    {"code": "9", "name": "Los Desposeídos"},
    {"code": "8", "name": "Los Jornaleros"},
    {"code": "7", "name": "Obreros Especializados"},
    {"code": "6", "name": "Comerciantes Menores"},
    {"code": "5", "name": "Artesanos Cualificados"},
    {"code": "4", "name": "Funcionarios Reales"},
    {"code": "3", "name": "Profesionales Liberales"},
    {"code": "2", "name": "Grandes mercaderes"},
    {"code": "1", "name": "Alta Nobleza Urbana"},
    {"code": "0", "name": "Nobleza Suprema"}
]

gender_data = [
    {"code": "M", "name": "MALE"},
    {"code": "F", "name": "FEMALE"},
    {"code": "O", "name": "OTHER"}
]

species_data = [
    {"code": "HU", "name": "Humana."},
    {"code": "EL", "name": "Elfica."},
    {"code": "EN", "name": "Enana."},
    {"code": "HB", "name": "Hombre Bestia."}
]

def insertar_dimensiones():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    # Insertar strata
    for item in strata_data:
        cur.execute("""
            INSERT INTO strata (code, name, description)
            VALUES (%s, %s, NULL)
            ON CONFLICT (code) DO NOTHING;
        """, (item["code"], item["name"]))

    # Insertar genders
    for item in gender_data:
        cur.execute("""
            INSERT INTO genders (code, name)
            VALUES (%s, %s)
            ON CONFLICT (code) DO NOTHING;
        """, (item["code"], item["name"]))

    # Insertar species
    for item in species_data:
        cur.execute("""
            INSERT INTO species (code, name)
            VALUES (%s, %s)
            ON CONFLICT (code) DO NOTHING;
        """, (item["code"], item["name"]))

    conn.commit()
    cur.close()
    conn.close()
    print("Datos de dimensiones insertados correctamente.")

if __name__ == "__main__":
    insertar_dimensiones()
