
"""Pruebas funcionales para la lista enlazada y la tabla hash."""

import random

from estructuras import ListaEnlazada, TablaHash


# 1. Busqueda exitosa e infructuosa.
lista = ListaEnlazada()
tabla = TablaHash(7)

datos_prueba = [
    (10, "en bodega"),
    (24, "en reparto"),
    (17, "entregado"),
]

for guia, estado in datos_prueba:
    lista.insertar(guia, estado)
    tabla.insertar(guia, estado)

assert lista.buscar(24) == "en reparto"
assert lista.buscar(99) is None

assert tabla.buscar(24) == "en reparto"
assert tabla.buscar(99) is None


# 2. Colision forzada con m = 7.
assert tabla.hash(10) == 3
assert tabla.hash(24) == 3
assert tabla.hash(17) == 3

assert tabla.casillas[3].tamano == 3

assert tabla.buscar(10) == "en bodega"
assert tabla.buscar(24) == "en reparto"
assert tabla.buscar(17) == "entregado"


# 3. Factor de carga.
assert tabla.factor_carga() == 3 / 7
assert tabla.tamano == 3


# 4. Veinticinco colecciones aleatorias.
random.seed(42)

ESTADOS = ("en bodega", "en reparto", "entregado")
TAMANOS_TABLA = (7, 101, 1009)
CANTIDAD_COLECCIONES = 25
CANTIDAD_INEXISTENTES = 10

for _ in range(CANTIDAD_COLECCIONES):
    cantidad = random.randint(1, 500)
    guias = random.sample(range(10**9, 10**10), cantidad)

    datos = [
        (guia, random.choice(ESTADOS))
        for guia in guias
    ]

    lista = ListaEnlazada()
    tabla = TablaHash(random.choice(TAMANOS_TABLA))

    for guia, estado in datos:
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)

    # Ambas estructuras deben contener la misma cantidad de elementos.
    assert lista.tamano == cantidad
    assert tabla.tamano == cantidad
    assert lista.tamano == tabla.tamano

    # Las guias existentes deben devolver el estado correcto.
    for guia, estado in datos:
        assert lista.buscar(guia) == estado
        assert tabla.buscar(guia) == estado
        assert lista.buscar(guia) == tabla.buscar(guia)

    # Generar guias inexistentes, sin repetirlas entre si.
    inexistentes: list[int] = []

    while len(inexistentes) < CANTIDAD_INEXISTENTES:
        candidato = random.randint(10**9, 10**10 - 1)

        existe_en_datos = any(
            candidato == guia for guia, _ in datos
        )
        existe_en_inexistentes = candidato in inexistentes

        if not existe_en_datos and not existe_en_inexistentes:
            inexistentes.append(candidato)

    # Ambas estructuras deben indicar que las guias no existen.
    for guia in inexistentes:
        assert lista.buscar(guia) is None
        assert tabla.buscar(guia) is None


print("Todas las pruebas pasaron.")
