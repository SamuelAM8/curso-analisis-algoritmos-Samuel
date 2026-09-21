"""Experimento de la Parte 4: insertion sort frente a merge sort."""

import math
import os
import time

import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]  # los mismos de la Parte 3
REGISTROS_TAMIZA = 1_200_000
VENTANA_SEGUNDOS = 4 * 3600


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

        print(
            f"n={n} | insertion_sort={resultados['insertion_sort'][-1]:.4f}s "
            f"| merge_sort={resultados['merge_sort'][-1]:.4f}s"
        )

    return resultados


def medir_escenarios() -> None:
    """Mide merge_sort e insertion_sort en los tres escenarios con n máximo.

    Imprime en consola una tabla con comparaciones y tiempo de cada
    algoritmo para los escenarios A, B y C, usando el mayor tamaño de
    TAMANOS. Estos datos respaldan la afirmación sobre la sensibilidad
    de cada algoritmo al orden de entrada.
    """
    n = TAMANOS[-1]
    escenarios = {
        "A - Aleatorio": generar_aleatorio(n, semilla=42),
        "B - Casi ordenado": generar_casi_ordenado(n, semilla=42),
        "C - Orden inverso": generar_inverso(n),
    }
    print(f"\nComparativa por escenario (n={n})")
    print("Escenario | algoritmo | comparaciones | tiempo (s)")
    for nombre, datos in escenarios.items():
        for etiqueta, algoritmo in (
            ("insertion_sort", insertion_sort),
            ("merge_sort", merge_sort),
        ):
            inicio = time.perf_counter()
            _, comparaciones = algoritmo(datos)
            fin = time.perf_counter()
            print(
                f"{nombre} | {etiqueta} | {comparaciones} "
                f"| {fin - inicio:.4f}"
            )


def extrapolar(resultados: dict[str, list[float]]) -> None:
    """Estima el tiempo para REGISTROS_TAMIZA a partir del mayor n medido.

    Es una estimación, no una medición: supone que el tiempo conserva la
    forma n^2 (insertion sort) y n log n (merge sort) al crecer.

    Args:
        resultados: salida de medir().
    """
    n0 = TAMANOS[-1]
    n = REGISTROS_TAMIZA
    factor_cuadratico = (n / n0) ** 2
    factor_nlogn = (n * math.log2(n)) / (n0 * math.log2(n0))

    estimado_insertion = resultados["insertion_sort"][-1] * factor_cuadratico
    estimado_merge = resultados["merge_sort"][-1] * factor_nlogn

    print(f"\nExtrapolación a n={n} desde n={n0} (estimación, no medición)")
    for nombre, factor, segundos in (
        ("insertion_sort", factor_cuadratico, estimado_insertion),
        ("merge_sort", factor_nlogn, estimado_merge),
    ):
        cabe = "CABE" if segundos <= VENTANA_SEGUNDOS else "NO CABE"
        print(
            f"{nombre}: factor={factor:.1f} | {segundos:.1f} s "
            f"= {segundos / 3600:.2f} h | {cabe} en 4 h"
        )
    print(
        "insertion_sort con servidor 2x: "
        f"{estimado_insertion / 2 / 3600:.2f} h"
    )


def graficar_tiempo(resultados: dict) -> None:
    """Genera graficas/parte4_tiempo.png.

    Args:
        resultados: salida de medir().
    """
    plt.figure(figsize=(8, 5))
    plt.plot(
        TAMANOS, resultados["insertion_sort"], marker="o",
        label="Insertion sort",
    )
    plt.plot(
        TAMANOS, resultados["merge_sort"], marker="o", label="Merge sort",
    )

    plt.title(
        "Insertion sort vs. merge sort: tiempo vs. tamaño de entrada "
        "(escenario A)"
    )
    plt.xlabel("Tamaño de entrada (n, número de registros)")
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
    medir_escenarios()
    extrapolar(resultados)
    print("Grafica guardada en graficas/parte4_tiempo.png")