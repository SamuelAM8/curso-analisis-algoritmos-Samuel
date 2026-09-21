"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1."""


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    lista = datos.copy()
    comparaciones = 0

    for i in range(1, len(lista)):
        clave = lista[i]
        j = i - 1
        # Mientras haya un elemento anterior y sea mayor que la clave,
        # se cuenta la comparacion entre elementos y se desplaza.
        while j >= 0:
            comparaciones += 1
            if lista[j] < clave:
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break
        lista[j + 1] = clave

    return lista, comparaciones


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    lista = datos.copy()
    comparaciones = 0

    def _merge_sort(sub: list[int]) -> list[int]:
        """Divide la sublista por la mitad, la ordena y combina las mitades.

        Args:
            sub: sublista a ordenar.

        Returns:
            Una lista nueva con los elementos de sub, de mayor a menor.
        """
        nonlocal comparaciones
        if len(sub) <= 1:
            return sub

        medio = len(sub) // 2
        izquierda = _merge_sort(sub[:medio])
        derecha = _merge_sort(sub[medio:])

        return _merge(izquierda, derecha)

    def _merge(izquierda: list[int], derecha: list[int]) -> list[int]:
        """Mezcla dos listas ya ordenadas de mayor a menor en una sola.

        Args:
            izquierda: primera lista, ordenada de mayor a menor.
            derecha: segunda lista, ordenada de mayor a menor.

        Returns:
            Una lista nueva con todos los elementos, de mayor a menor.
        """
        nonlocal comparaciones
        resultado = []
        i = j = 0

        while i < len(izquierda) and j < len(derecha):
            comparaciones += 1
            if izquierda[i] >= derecha[j]:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

        # Los residuos no requieren comparacion entre elementos:
        # ya estan ordenados entre si.
        resultado.extend(izquierda[i:])
        resultado.extend(derecha[j:])
        return resultado

    lista_ordenada = _merge_sort(lista)
    return lista_ordenada, comparaciones