"""Medicion de tiempos: fuerza bruta vs divide y venceras."""

import os
import random
import statistics
import time
from collections.abc import Callable

import matplotlib.pyplot as plt

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo

SEMILLA = 42
TAMANOS = [10, 50, 100, 500, 1000, 2000, 4000, 8000]


def repeticiones_para(n: int) -> int:
    """Devuelve cuantas veces repetir la fuerza bruta segun el tamano.

    Args:
        n: tamano de la entrada.

    Returns:
        Numero de repeticiones: mas para tamanos pequenos, donde el
        tiempo es tan corto que el ruido pesa mas.
    """
    if n <= 100:
        return 200
    if n <= 1000:
        return 20
    return 3


def medir(funcion: Callable[..., object], *args: object) -> float:
    """Mide el tiempo de una sola llamada con perf_counter.

    Args:
        funcion: funcion a cronometrar.
        *args: argumentos de la funcion.

    Returns:
        Tiempo transcurrido en segundos.
    """
    inicio = time.perf_counter()
    funcion(*args)
    return time.perf_counter() - inicio


def mediana_de_tiempos(
    funcion: Callable[..., object], repeticiones: int, *args: object
) -> float:
    """Repite la medicion y devuelve la mediana, en segundos.

    Args:
        funcion: funcion a cronometrar.
        repeticiones: cuantas veces medir.
        *args: argumentos de la funcion.

    Returns:
        Mediana de los tiempos medidos, en segundos.
    """
    tiempos = [medir(funcion, *args) for _ in range(repeticiones)]
    return statistics.median(tiempos)


def ejecutar_experimento() -> tuple[list[float], list[float]]:
    """Corre el experimento para todos los tamanos.

    Returns:
        Dos listas de tiempos en milisegundos, una por algoritmo, en el
        mismo orden que TAMANOS.
    """
    random.seed(SEMILLA)
    tiempos_fb = []
    tiempos_dc = []

    for n in TAMANOS:
        # Los datos se generan fuera del cronometro.
        datos = [random.randint(-100, 100) for _ in range(n)]
        reps = repeticiones_para(n)

        t_fb = mediana_de_tiempos(
            subarreglo_fuerza_bruta, reps, datos
        )
        t_dc = mediana_de_tiempos(
            subarreglo_maximo, 21, datos, 0, n - 1
        )

        # Verificacion: ambos deben dar la misma suma.
        suma_fb = subarreglo_fuerza_bruta(datos)[2]
        suma_dc = subarreglo_maximo(datos, 0, n - 1)[2]
        assert suma_fb == suma_dc, f"Sumas distintas en n={n}"

        tiempos_fb.append(t_fb * 1000)
        tiempos_dc.append(t_dc * 1000)

        print(
            f"n={n:>5}  fuerza bruta={t_fb * 1000:>10.4f} ms  "
            f"divide y venceras={t_dc * 1000:>9.4f} ms"
        )

    return tiempos_fb, tiempos_dc


def graficar(
    tiempos_fb: list[float], tiempos_dc: list[float]
) -> None:
    """Genera las graficas de tiempo vs tamano y las guarda como PNG.

    Args:
        tiempos_fb: tiempos de la fuerza bruta en milisegundos.
        tiempos_dc: tiempos de divide y venceras en milisegundos.
    """
    carpeta = os.path.join(os.path.dirname(__file__), "graficas")
    os.makedirs(carpeta, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(TAMANOS, tiempos_fb, marker="o", label="Fuerza bruta")
    plt.plot(TAMANOS, tiempos_dc, marker="s", label="Divide y venceras")
    plt.title("Subarreglo maximo: tiempo de ejecucion vs tamano de entrada")
    plt.xlabel("Tamano de la entrada n (numero de dias)")
    plt.ylabel("Tiempo de ejecucion (milisegundos)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, "tiempo_vs_n.png"), dpi=150)

    plt.figure(figsize=(8, 5))
    plt.loglog(TAMANOS, tiempos_fb, marker="o", label="Fuerza bruta")
    plt.loglog(TAMANOS, tiempos_dc, marker="s", label="Divide y venceras")
    plt.title("Tiempo vs tamano (escala logaritmica)")
    plt.xlabel("Tamano de la entrada n (numero de dias, escala log)")
    plt.ylabel("Tiempo de ejecucion (milisegundos, escala log)")
    plt.legend()
    plt.grid(True, which="both")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta, "tiempo_vs_n_log.png"), dpi=150)

    plt.close("all")


if __name__ == "__main__":
    fb, dc = ejecutar_experimento()
    graficar(fb, dc)
    print("Graficas guardadas en la carpeta graficas/")
