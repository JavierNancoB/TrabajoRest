from db_utils import get_connection

def listar_columnas_por_tabla():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_schema, table_name, column_name, data_type
            FROM information_schema.columns
            ORDER BY table_schema, table_name, ordinal_position;
        """)
        columnas = cur.fetchall()

        print("📑 Columnas por tabla:")
        tabla_actual = (None, None)
        for schema, tabla, columna, tipo in columnas:
            if (schema, tabla) != tabla_actual:
                print(f"\n🧾 Tabla: {schema}.{tabla}")
                tabla_actual = (schema, tabla)
            print(f"   - {columna} ({tipo})")

if __name__ == "__main__":
    listar_columnas_por_tabla()
