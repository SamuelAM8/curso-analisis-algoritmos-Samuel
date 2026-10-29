import random

from estructuras import ListaEnlazada, TablaHash

# --- 1. Busqueda exitosa e infructuosa ---
lista = ListaEnlazada()
tabla = TablaHash(7)
for guia, estado in ((10, "en bodega"), (24, "en reparto"),
                     (17, "entregado")):
    lista.insertar(guia, estado)
    tabla.insertar(guia, estado)

assert lista.buscar(24) == "en reparto"
assert lista.buscar(99) is None
assert tabla.buscar(24) == "en reparto"
assert tabla.buscar(99) is None

# --- 2. Colision forzada con m = 7 ---
assert 10 % 7 == 24 % 7 == 17 % 7 == 3
assert tabla.casillas[3].tamano == 3
assert tabla.buscar(10) == "en bodega"
assert tabla.buscar(24) == "en reparto"
assert tabla.buscar(17) == "entregado"

# --- 3. Factor de carga ---
assert tabla.factor_carga() == 3 / 7

# --- 4. Veinticinco colecciones aleatorias ---
random.seed(42)
ESTADOS = ("en bodega", "en reparto", "entregado")
for _ in range(25):
    k = random.randint(1, 500)
    guias = random.sample(range(10**9, 10**10), k)
    estados = {g: random.choice(ESTADOS) for g in guias}

    lista = ListaEnlazada()
    tabla = TablaHash(random.choice([7, 101, 1009]))
    for g in guias:
        lista.insertar(g, estados[g])
        tabla.insertar(g, estados[g])

    assert tabla.tamano == lista.tamano == k

    for g in guias:
        assert lista.buscar(g) == tabla.buscar(g) == estados[g]

    existentes = set(guias)
    inexistentes: list[int] = []
    while len(inexistentes) < 10:
        candidato = random.randint(10**9, 10**10 - 1)
        if candidato not in existentes:
            inexistentes.append(candidato)
    for g in inexistentes:
        assert lista.buscar(g) is None
        assert tabla.buscar(g) is None

print("Todas las pruebas pasaron")