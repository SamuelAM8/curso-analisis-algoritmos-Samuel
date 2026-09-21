"""Experimento de la Parte 3: peor caso, mejor caso y caso promedio."""

import os
import time

import matplotlib.pyplot as plt

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]

ESCENARIOS = {
    "A - Aleatorio": generar_aleatorio,
    "B - Casi ordenado": generar_casi_ordenado,
    "C - Orden inverso": generar_inverso,
}


def medir() -> dict[str, dict[str, list[float]]]:
    """Ejecuta insertion_sort sobre los tres escenarios y mide resultados.

    Returns:
        Diccionario escenario -> {"comparaciones": [...], "tiempos": [...]}
        alineado con TAMANOS.
    """
    resultados = {
        nombre: {"comparaciones": [], "tiempos": []} for nombre in ESCENARIOS
    }

    for nombre, generador in ESCENARIOS.items():
        for n in TAMANOS:
            if generador is generar_inverso:
                datos = generador(n)
            else:
                datos = generador(n, semilla=42)

            inicio = time.perf_counter()
            _, comparaciones = insertion_sort(datos)
            fin = time.perf_counter()

            resultados[nombre]["comparaciones"].append(comparaciones)
            resultados[nombre]["tiempos"].append(fin - inicio)

            print(
                f"{nombre} | n={n} | comparaciones={comparaciones} "
                f"| tiempo={fin - inicio:.4f}s"
            )

    return resultados


def graficar_comparaciones(resultados: dict) -> None:
    """Genera graficas/parte3_comparaciones.png.

    Args:
        resultados: salida de medir().
    """
    plt.figure(figsize=(8, 5))
    for nombre, datos in resultados.items():
        plt.plot(TAMANOS, datos["comparaciones"], marker="o", label=nombre)

    plt.title("Insertion sort: comparaciones vs. tamaño de entrada")
    plt.xlabel("Tamaño de entrada (n, número de registros)")
    plt.ylabel("Número de comparaciones")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/parte3_comparaciones.png")
    plt.close()


def graficar_tiempo(resultados: dict) -> None:
    """Genera graficas/parte3_tiempo.png.

    Args:
        resultados: salida de medir().
    """
    plt.figure(figsize=(8, 5))
    for nombre, datos in resultados.items():
        plt.plot(TAMANOS, datos["tiempos"], marker="o", label=nombre)

    plt.title("Insertion sort: tiempo de ejecución vs. tamaño de entrada")
    plt.xlabel("Tamaño de entrada (n, número de registros)")
    plt.ylabel("Tiempo (segundos)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("graficas/parte3_tiempo.png")
    plt.close()


if __name__ == "__main__":
    os.makedirs("graficas", exist_ok=True)
    resultados = medir()
    graficar_comparaciones(resultados)
    graficar_tiempo(resultados)
    print(
        "Graficas guardadas en graficas/parte3_comparaciones.png "
        "y graficas/parte3_tiempo.png"
    )