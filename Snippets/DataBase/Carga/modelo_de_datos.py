import psycopg2

DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432

def crear_modelo_datos():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS persons CASCADE;
        DROP TABLE IF EXISTS genders CASCADE;
        DROP TABLE IF EXISTS species CASCADE;
        DROP TABLE IF EXISTS strata CASCADE;

        CREATE TABLE genders (
            id SERIAL PRIMARY KEY,
            code VARCHAR(10) UNIQUE,
            name VARCHAR(50),
            created TIMESTAMP DEFAULT now(),
            updated TIMESTAMP DEFAULT now()
        );

        CREATE TABLE species (
            id SERIAL PRIMARY KEY,
            code VARCHAR(10) UNIQUE,
            name VARCHAR(50),
            created TIMESTAMP DEFAULT now(),
            updated TIMESTAMP DEFAULT now()
        );

        CREATE TABLE strata (
            id SERIAL PRIMARY KEY,
            code VARCHAR(10) UNIQUE,
            name VARCHAR(50),
            description TEXT,
            created TIMESTAMP DEFAULT now(),
            updated TIMESTAMP DEFAULT now()
        );

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

    conn.commit()
    cur.close()
    conn.close()
    print("Modelo de datos creado correctamente.")

if __name__ == "__main__":
    crear_modelo_datos()
