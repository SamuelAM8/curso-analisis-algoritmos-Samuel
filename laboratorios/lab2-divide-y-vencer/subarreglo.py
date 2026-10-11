"""Subarreglo maximo: fuerza bruta y divide y venceras."""


def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).

    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.

    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    n = len(valores)
    mejor_inicio = 0
    mejor_fin = 0
    mejor_suma = valores[0]

    for i in range(n):
        suma = 0
        for j in range(i, n):
            suma += valores[j]  # acumula en vez de recalcular
            if suma > mejor_suma:
                mejor_suma = suma
                mejor_inicio = i
                mejor_fin = j

    return (mejor_inicio, mejor_fin, mejor_suma)


def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    # Barrido hacia la izquierda: parte de medio y retrocede hasta inicio.
    mejor_izq = float("-inf")
    indice_izq = medio
    suma = 0
    for k in range(medio, inicio - 1, -1):
        suma += valores[k]
        if suma > mejor_izq:
            mejor_izq = suma
            indice_izq = k

    # Barrido hacia la derecha: parte de medio + 1 y avanza hasta fin.
    mejor_der = float("-inf")
    indice_der = medio + 1
    suma = 0
    for k in range(medio + 1, fin + 1):
        suma += valores[k]
        if suma > mejor_der:
            mejor_der = suma
            indice_der = k

    return (indice_izq, indice_der, mejor_izq + mejor_der)


def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    if inicio == fin:
        return (inicio, fin, valores[inicio])

    medio = (inicio + fin) // 2
    izquierdo = subarreglo_maximo(valores, inicio, medio)
    derecho = subarreglo_maximo(valores, medio + 1, fin)
    cruzado = suma_cruzada(valores, inicio, medio, fin)

    if izquierdo[2] >= derecho[2] and izquierdo[2] >= cruzado[2]:
        return izquierdo
    if derecho[2] >= cruzado[2]:
        return derecho
    return cruzado
