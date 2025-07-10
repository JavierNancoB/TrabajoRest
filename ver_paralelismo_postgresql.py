import psycopg2
from psycopg2 import OperationalError

conn_info_base = {
    'host': '159.223.200.213',
    'port': 5432,
    'user': 'isekai',
    'password': 'Fr9tL28mQxD7vKcp'
}

# Lista de posibles nombres de bases para probar
posibles_bases = ['isekaidb', 'postgres', 'isekai', 'template1']

def probar_conexion_y_listar_bases(dbname):
    print(f"\nIntentando conectar a la base: {dbname}")
    try:
        conn_info = conn_info_base.copy()
        conn_info['dbname'] = dbname
        with psycopg2.connect(**conn_info) as conn:
            with conn.cursor() as cur:
                print(f"Conexión exitosa a '{dbname}'")
                cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
                bases = cur.fetchall()
                print("Bases disponibles en el servidor:")
                for base in bases:
                    print(f"- {base[0]}")
                return True
    except OperationalError as e:
        print(f"No se pudo conectar a '{dbname}': {e}")
        return False

if __name__ == "__main__":
    for db in posibles_bases:
        if probar_conexion_y_listar_bases(db):
            break
    else:
        print("\nNo fue posible conectarse a ninguna base de datos con los nombres probados.")
