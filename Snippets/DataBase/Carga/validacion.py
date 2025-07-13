import mmap
import multiprocessing as mp

CSV_PATH = r"C:\Users\javie\OneDrive\Documentos\Trabajo Paralela\eldoria.csv"
CPU_COUNT = mp.cpu_count()


def validar_chunk(file_path, start, end, encoding="utf-8"):
    with open(file_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        mm.seek(start)
        if start != 0:
            mm.readline()  # saltar línea incompleta al inicio

        while mm.tell() < end:
            line_start_pos = mm.tell()
            line = mm.readline()
            if not line:
                break
            try:
                decoded = line.decode(encoding).strip()
            except UnicodeDecodeError as e:
                print(f"❌ Error decodificando línea (byte pos {line_start_pos}):")
                print(f"  Línea completa (raw): {line}")
                mm.close()
                return False
        mm.close()
    return True


def validar_archivo_paralelo(file_path):
    with open(file_path, "rb") as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        file_size = mm.size()
        first_line_raw = mm.readline()
        start = mm.tell()
        chunk_size = (file_size - start) // CPU_COUNT
        mm.close()

    chunks = []
    pos = start
    for _ in range(CPU_COUNT):
        end = pos + chunk_size
        if end >= file_size:
            end = file_size
        else:
            with open(file_path, "rb") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                mm.seek(end)
                mm.readline()
                end = mm.tell()
                mm.close()
        chunks.append((file_path, pos, end))

        pos = end

    with mp.Pool(CPU_COUNT) as pool:
        resultados = pool.starmap(validar_chunk, chunks)

    return all(resultados)


def main():
    print("🔍 Validando archivo en paralelo...")
    success = validar_archivo_paralelo(CSV_PATH)
    if success:
        print("✅ Archivo validado correctamente.")
    else:
        print("⛔ Se encontraron errores en la codificación. Corrige el archivo primero.")


if __name__ == "__main__":
    main()
