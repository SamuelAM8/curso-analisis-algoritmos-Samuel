
"""Implementacion de lista enlazada y tabla hash para guias de envio."""


class Nodo:
    """Representa un nodo de una lista enlazada."""

    def __init__(self, guia: int, estado: str) -> None:
        """Inicializa un nodo con una guia y su estado.

        Args:
            guia: Numero de guia del envio.
            estado: Estado actual del envio.
        """
        self.guia = guia
        self.estado = estado
        self.siguiente: Nodo | None = None


class ListaEnlazada:
    """Lista simplemente enlazada con insercion al inicio."""

    def __init__(self) -> None:
        """Inicializa una lista enlazada vacia."""
        self.cabeza: Nodo | None = None
        self.tamano = 0

    def insertar(self, guia: int, estado: str) -> None:
        """Inserta una guia al inicio de la lista.

        Args:
            guia: Numero de guia del envio.
            estado: Estado actual del envio.
        """
        nuevo = Nodo(guia, estado)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo
        self.tamano += 1

    def buscar(self, guia: int) -> str | None:
        """Busca una guia recorriendo la lista iterativamente.

        Args:
            guia: Numero de guia que se desea buscar.

        Returns:
            El estado del envio si existe, o None si no se encuentra.
        """
        actual = self.cabeza

        while actual is not None:
            if actual.guia == guia:
                return actual.estado
            actual = actual.siguiente

        return None


class TablaHash:
    """Tabla hash con encadenamiento y metodo de division."""

    def __init__(self, m: int) -> None:
        """Inicializa una tabla hash con m casillas vacias.

        Args:
            m: Numero de casillas de la tabla.

        Raises:
            ValueError: Si el numero de casillas no es positivo.
        """
        if m <= 0:
            raise ValueError("El numero de casillas debe ser positivo.")

        self.m = m
        self.casillas: list[ListaEnlazada] = [
            ListaEnlazada() for _ in range(m)
        ]
        self.tamano = 0

    def hash(self, guia: int) -> int:
        """Calcula el indice de una guia mediante el metodo de division.

        Args:
            guia: Numero de guia del envio.

        Returns:
            El indice de la casilla, entre 0 y m - 1.
        """
        return guia % self.m

    def insertar(self, guia: int, estado: str) -> None:
        """Inserta una guia en la lista de su casilla correspondiente.

        Args:
            guia: Numero de guia del envio.
            estado: Estado actual del envio.
        """
        indice = self.hash(guia)
        self.casillas[indice].insertar(guia, estado)
        self.tamano += 1

    def buscar(self, guia: int) -> str | None:
        """Busca una guia unicamente en su casilla correspondiente.

        Args:
            guia: Numero de guia que se desea buscar.

        Returns:
            El estado del envio si existe, o None si no se encuentra.
        """
        indice = self.hash(guia)
        return self.casillas[indice].buscar(guia)

    def factor_carga(self) -> float:
        """Calcula el factor de carga de la tabla hash.

        Returns:
            La cantidad de elementos dividida entre el numero de casillas.
        """
        return self.tamano / self.m
