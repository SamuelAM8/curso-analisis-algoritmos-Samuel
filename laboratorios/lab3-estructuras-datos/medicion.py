"""Medicion de busquedas: lista enlazada vs tabla hash."""
import os
import random
import time

import matplotlib.pyplot as plt

from estructuras import ListaEnlazada, TablaHash

SEMILLA = 2026
CARPETA = "graficas"
REPETICIONES = 5
BUSQUEDAS = 200
MUESTRA_VERIFICACION = 100
VALORES_N = [100, 500, 1_000, 5_000, 20_000, 50_000, 100_000]
N_FIJO = 20_000
VALORES_ALFA = [0.25, 0.5, 1, 2, 4, 10]
ESTADOS = ("en bodega", "en reparto", "entregado")


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def es_primo(x: int) -> bool:
    """Indica si un entero es primo (division por tentativa).

    Args:
        x: entero a evaluar.

    Returns:
        True si x es primo.
    """
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    divisor = 3
    while divisor * divisor <= x:
        if x % divisor == 0:
            return False
        divisor += 2
    return True


def primo_cercano(x: int) -> int:
    """Devuelve el primo mas pequeno mayor o igual que x.

    Args:
        x: valor de partida.

    Returns:
        El primer primo mayor o igual que x.
    """
    while not es_primo(x):
        x += 1
    return x


def generar_guias(n: int, semilla: int) -> list[int]:
    """Genera n guias distintas de diez digitos con semilla fija.

    Args:
        n: cantidad de guias.
        semilla: semilla del generador.

    Returns:
        Lista de n guias distintas.
    """
    azar = random.Random(semilla)
    return azar.sample(range(10**9, 10**10), n)


def construir(
    guias: list[int], m: int
) -> tuple[ListaEnlazada, TablaHash]:
    """Construye lista y tabla con las mismas guias (sin cronometrar).

    Args:
        guias: guias a almacenar.
        m: numero de casillas de la tabla.

    Returns:
        La lista y la tabla ya pobladas.
    """
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for i, guia in enumerate(guias):
        estado = ESTADOS[i % len(ESTADOS)]
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    return lista, tabla


def verificar(
    lista: ListaEnlazada, tabla: TablaHash, guias: list[int]
) -> None:
    """Comprueba que lista y tabla devuelven lo mismo en una muestra.

    Args:
        lista: lista poblada.
        tabla: tabla poblada.
        guias: guias almacenadas.

    Raises:
        AssertionError: si alguna respuesta difiere o es None.
    """
    azar = random.Random(SEMILLA)
    muestra = azar.sample(guias, min(MUESTRA_VERIFICACION, len(guias)))
    for guia in muestra:
        respuesta = lista.buscar(guia)
        assert respuesta is not None
        assert respuesta == tabla.buscar(guia)


def medir(
    estructura: ListaEnlazada | TablaHash, consultas: list[int]
) -> float:
    """Mide el tiempo medio por busqueda, en microsegundos.

    Solo se cronometra el ciclo de busquedas. Se repite la medicion
    y se promedian las repeticiones.

    Args:
        estructura: lista o tabla donde buscar.
        consultas: guias a buscar.

    Returns:
        Microsegundos por busqueda.
    """
    tiempos: list[float] = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for guia in consultas:
            estructura.buscar(guia)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) / len(consultas))
    return sum(tiempos) / len(tiempos) * 1e6


def experimento_a() -> tuple[list[float], list[float]]:
    """Experimento A: lista frente a tabla, busquedas infructuosas.

    Returns:
        Tiempos medios de la lista y de la tabla para cada n.
    """
    t_lista: list[float] = []
    t_tabla: list[float] = []
    print("\nExperimento A: tiempo vs n (busquedas infructuosas)")
    print(f"{'n':>8} {'m':>8} {'alfa':>7} {'lista (us)':>12} "
          f"{'tabla (us)':>11}")
    for n in VALORES_N:
        m = primo_cercano(n // 2)
        guias = generar_guias(n, SEMILLA + n)
        lista, tabla = construir(guias, m)
        verificar(lista, tabla, guias)
        consultas = generar_guias_inexistentes(set(guias), BUSQUEDAS)
        tl = medir(lista, consultas)
        tt = medir(tabla, consultas)
        t_lista.append(tl)
        t_tabla.append(tt)
        print(f"{n:>8} {m:>8} {tabla.factor_carga():>7.2f} "
              f"{tl:>12.3f} {tt:>11.3f}")
    return t_lista, t_tabla


def experimento_b() -> tuple[list[float], list[float]]:
    """Experimento B: efecto del factor de carga con n fijo.

    Returns:
        Los alfa reales y el tiempo medio de busqueda para cada uno.
    """
    guias = generar_guias(N_FIJO, SEMILLA)
    consultas = generar_guias_inexistentes(set(guias), BUSQUEDAS)
    alfas: list[float] = []
    tiempos: list[float] = []
    print(f"\nExperimento B: tiempo vs alfa (n = {N_FIJO})")
    print(f"{'alfa meta':>10} {'m':>8} {'alfa real':>10} "
          f"{'tabla (us)':>11}")
    for alfa in VALORES_ALFA:
        m = primo_cercano(round(N_FIJO / alfa))
        lista, tabla = construir(guias, m)
        verificar(lista, tabla, guias)
        real = tabla.factor_carga()
        tiempo = medir(tabla, consultas)
        alfas.append(real)
        tiempos.append(tiempo)
        print(f"{alfa:>10} {m:>8} {real:>10.3f} {tiempo:>11.3f}")
    return alfas, tiempos


def graficar_a(t_lista: list[float], t_tabla: list[float]) -> None:
    """Guarda graficas/lista_vs_tabla.png.

    Args:
        t_lista: tiempos de la lista para cada n.
        t_tabla: tiempos de la tabla para cada n.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(VALORES_N, t_lista, "o-", label="Lista enlazada")
    plt.plot(VALORES_N, t_tabla, "s-", label="Tabla hash")
    plt.title("Tiempo de busqueda infructuosa: lista vs tabla hash")
    plt.xlabel("Numero de guias n (guias)")
    plt.ylabel("Tiempo medio por busqueda (microsegundos)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(CARPETA, "lista_vs_tabla.png"), dpi=150,
                bbox_inches="tight")
    plt.close()


def graficar_b(alfas: list[float], tiempos: list[float]) -> None:
    """Guarda graficas/tiempo_vs_alfa.png.

    Args:
        alfas: factores de carga reales.
        tiempos: tiempos medios de busqueda para cada alfa.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(alfas, tiempos, "o-", label="Tabla hash (infructuosa)")
    plt.title(f"Tiempo de busqueda vs factor de carga (n = {N_FIJO})")
    plt.xlabel("Factor de carga alfa = n / m (adimensional)")
    plt.ylabel("Tiempo medio por busqueda (microsegundos)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(CARPETA, "tiempo_vs_alfa.png"), dpi=150,
                bbox_inches="tight")
    plt.close()


def main() -> None:
    """Ejecuta ambos experimentos y guarda las graficas."""
    os.makedirs(CARPETA, exist_ok=True)
    t_lista, t_tabla = experimento_a()
    graficar_a(t_lista, t_tabla)
    alfas, tiempos = experimento_b()
    graficar_b(alfas, tiempos)
    print("\nGraficas guardadas en", CARPETA)


if __name__ == "__main__":
    main()
