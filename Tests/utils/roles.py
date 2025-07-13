import psycopg2
from db_utils import CONN_INFO

def ver_roles_y_permisos():
    query_rol = "SELECT current_user, session_user;"
    query_mis_privilegios = """
        SELECT grantee, privilege_type
        FROM information_schema.role_table_grants
        WHERE table_schema = 'isekai' AND table_name = 'persons';
    """
    try:
        conn = psycopg2.connect(**CONN_INFO)
        with conn.cursor() as cur:
            # Usuario actual
            cur.execute(query_rol)
            current_user, session_user = cur.fetchone()
            print(f"👤 Usuario actual: {current_user} (session user: {session_user})")

            # Permisos sobre la tabla
            print("\n🔐 Permisos sobre isekai.persons:")
            cur.execute(query_mis_privilegios)
            rows = cur.fetchall()
            if not rows:
                print("  ❌ No tienes permisos explícitos sobre isekai.persons.")
            else:
                for row in rows:
                    print(f"  ✅ {row[0]} tiene permiso: {row[1]}")

    except Exception as e:
        print(f"❌ Error al consultar roles o permisos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    ver_roles_y_permisos()
