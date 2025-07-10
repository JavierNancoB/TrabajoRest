import psycopg2

DB_NAME = "trabajo2paralela"
USER = "postgres"
PASSWORD = "postgres"
HOST = "localhost"
PORT = 5432
TABLE_NAME = "eldoria"

def crear_tabla():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    cur = conn.cursor()

    cur.execute(f"""
        DROP TABLE IF EXISTS {TABLE_NAME};
        CREATE TABLE {TABLE_NAME} (
            identificador VARCHAR(30) PRIMARY KEY,
            especie VARCHAR(50),
            genero VARCHAR(20),
            nombre VARCHAR(50),
            apellido VARCHAR(50),
            fecha_nacimiento TIMESTAMP,
            cp_origen BIGINT,
            cp_destino BIGINT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Tabla '{TABLE_NAME}' creada exitosamente.")

if __name__ == "__main__":
    crear_tabla()
