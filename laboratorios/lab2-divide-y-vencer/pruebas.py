import random

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo, suma_cruzada


def divide(serie):
    return subarreglo_maximo(serie, 0, len(serie) - 1)


# 1. Serie de ocho días (suma 17)
serie = [-3, 5, -2, 8, -6, 3, 9, -4]
assert subarreglo_fuerza_bruta(serie)[2] == 17
assert divide(serie)[2] == 17

assert suma_cruzada(serie, 0, 3, 7)[2] == 17
# El cruzado debe tomar un elemento de cada lado aunque sean negativos
assert suma_cruzada([-4, -1, -2, -9], 0, 1, 3)[2] == -3

# 2. Un solo elemento
assert subarreglo_fuerza_bruta([7])[2] == 7
assert divide([7])[2] == 7
assert subarreglo_fuerza_bruta([-7])[2] == -7
assert divide([-7])[2] == -7

# 3. Todos negativos: gana el menos negativo
negativos = [-8, -3, -6, -2, -5]
assert subarreglo_fuerza_bruta(negativos)[2] == -2
assert divide(negativos)[2] == -2

# 4. Todos positivos: gana la serie completa
positivos = [4, 1, 7, 3, 2]
assert subarreglo_fuerza_bruta(positivos)[2] == 17
assert divide(positivos)[2] == 17

# 5. Caso cruzado: el mejor tramo (índices 2..5) cruza el punto medio
cruzada = [1, -5, 4, 3, 2, 5, -6, 1]
assert subarreglo_fuerza_bruta(cruzada)[2] == 14
assert divide(cruzada)[2] == 14
assert suma_cruzada(cruzada, 0, 3, 7)[2] == 14

# 6. Los índices devueltos coinciden con la suma declarada
ini, fin, suma = divide(serie)
assert sum(serie[ini:fin + 1]) == suma

# 7. La función no modifica la lista recibida
copia = list(serie)
divide(serie)
subarreglo_fuerza_bruta(serie)
assert serie == copia

# 8. Listas aleatorias: ambas funciones deben dar la misma suma
random.seed(42)  # reproducible
for _ in range(200):
    n = random.randint(1, 60)
    lista = [random.randint(-50, 50) for _ in range(n)]
    esperado = subarreglo_fuerza_bruta(lista)[2]
    obtenido = divide(lista)
    assert obtenido[2] == esperado, f"Falla en {lista}"
    assert sum(lista[obtenido[0]:obtenido[1] + 1]) == obtenido[2]

print("Todas las pruebas pasaron")
