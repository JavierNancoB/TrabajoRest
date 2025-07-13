import csv

CSV_PATH = r"C:\Users\javie\OneDrive\Documentos\Trabajo Paralela\eldoria.csv"
NUM_FILAS = 10  # cuántas filas mostrar

def mostrar_primeras_filas(path, num_filas=10):
    with open(path, newline='', encoding='utf-8') as f:
        lector = csv.reader(f, delimiter=';')
        for i, fila in enumerate(lector):
            print(f"Fila {i+1}: {fila}")
            if i + 1 >= num_filas:
                break

if __name__ == "__main__":
    mostrar_primeras_filas(CSV_PATH, NUM_FILAS)
