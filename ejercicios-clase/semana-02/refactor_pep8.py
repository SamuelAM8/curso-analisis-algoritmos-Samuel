def calcular_promedio(lista_numeros: list[int]) -> float:
    """Calcula el promedio de una lista de números.

    Args:
        lista_numeros: Lista de números enteros.

    Returns:
        El promedio de los números de la lista.
    """
    suma_total = 0

    for numero in lista_numeros:
        suma_total = suma_total + numero

    return suma_total / len(lista_numeros)


def main() -> None:
    """Punto de entrada principal del programa."""
    lista_numeros = [1, 2, 3, 4, 5]
    promedio = calcular_promedio(lista_numeros)
    print(promedio)


if __name__ == "__main__":
    main()