import time
import os

import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]  # los mismos de la Parte 3

def medir() -> dict[str, list[float]]:
    """Mide el tiempo de insertion_sort y merge_sort sobre el escenario A.

    Returns:
        Diccionario con "insertion_sort" y "merge_sort", cada uno
        con la lista de tiempos alineada con TAMANOS.
    """
    resultados = {"insertion_sort": [], "merge_sort": []}

    for n in TAMANOS:
        datos = generar_aleatorio(n, semilla=42)

        inicio = time.perf_counter()
        insertion_sort(datos)
        fin = time.perf_counter()
        resultados["insertion_sort"].append(fin - inicio)

        inicio = time.perf_counter()
        merge_sort(datos)
        fin = time.perf_counter()
        resultados["merge_sort"].append(fin - inicio)

        print(f"n={n} | insertion_sort={resultados['insertion_sort'][-1]:.4f}s "
              f"| merge_sort={resultados['merge_sort'][-1]:.4f}s")

    return resultados


def graficar_tiempo(resultados: dict) -> None:
    """Genera graficas/parte4_tiempo.png."""
    plt.figure(figsize=(8, 5))
    plt.plot(TAMANOS, resultados["insertion_sort"], marker="o", label="Insertion sort")
    plt.plot(TAMANOS, resultados["merge_sort"], marker="o", label="Merge sort")

    plt.title("Insertion sort vs. merge sort: tiempo vs. tamano de entrada (escenario A)")
    plt.xlabel("Tamano de entrada (n)")
    plt.ylabel("Tiempo (segundos)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/parte4_tiempo.png")
    plt.close()



if __name__ == "__main__":
    os.makedirs("graficas", exist_ok=True)
    resultados = medir()
    graficar_tiempo(resultados)
    print("Grafica guardada en graficas/parte4_tiempo.png")