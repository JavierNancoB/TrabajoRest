from db_utils import get_connection

# Lista de tablas objetivo (schema, tabla)
tablas_objetivo = {
    ("isekai", "genders"),
    ("isekai", "persons"),
    ("isekai", "species"),
    ("isekai", "strata")
}

def listar_columnas_filtradas():
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_schema, table_name, column_name, data_type
            FROM information_schema.columns
            WHERE (table_schema, table_name) IN (
                ('isekai', 'genders'),
                ('isekai', 'persons'),
                ('isekai', 'species'),
                ('isekai', 'strata')
            )
            ORDER BY table_schema, table_name, ordinal_position;
        """)
        columnas = cur.fetchall()

        print("📑 Columnas de las tablas seleccionadas:")
        tabla_actual = (None, None)
        for schema, tabla, columna, tipo in columnas:
            if (schema, tabla) != tabla_actual:
                print(f"\n🧾 Tabla: {schema}.{tabla}")
                tabla_actual = (schema, tabla)
            print(f"   - {columna} ({tipo})")

if __name__ == "__main__":
    listar_columnas_filtradas()
