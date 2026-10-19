"""
Patrón Factory Method - Productos (interfaz y productos concretos).

En el patrón Factory Method, los creadores (ver creador_producto.py) devuelven
objetos que cumplen la interfaz Producto; cada creador concreto decide qué
producto concreto instanciar, y el código cliente solo trabaja contra Producto.

Este módulo define:
    - Producto: Clase abstracta base que establece la interfaz común.
    - Libro: Producto concreto que representa un libro con autor.
    - Electronico: Producto concreto que representa un dispositivo con garantía.

Concepto clave - Clase Abstracta (ABC):
    Una clase abstracta NO se puede instanciar directamente. Sirve como
    "contrato" que obliga a las subclases a implementar ciertos métodos.
    En Python se logra heredando de ABC y usando @abstractmethod.

Ejemplo de uso:
    >>> libro = Libro("Don Quijote", 19.99, "Cervantes")
    >>> libro.mostrar_info()
    Libro: Don Quijote | Autor: Cervantes | Precio: $19.99
    >>> libro.nombre
    'Don Quijote'
    >>> libro.precio
    19.99
"""

from abc import ABC, abstractmethod
from patrones._numeros import es_finito


class Producto(ABC):
    """Clase abstracta base para todos los productos del sistema.

    Define la interfaz común que deben cumplir todos los productos.
    No se puede instanciar directamente (es abstracta).

    Atributos:
        _nombre (str): Nombre del producto.
        _precio (float): Precio del producto.
    """

    def __init__(self, nombre: str, precio: float) -> None:
        """Inicializa los atributos comunes a todos los productos.

        Args:
            nombre: Nombre del producto.
            precio: Número finito no negativo (int o float, excluyendo bool).

        Raises:
            TypeError: Si el precio no es int o float, o es bool.
            ValueError: Si el precio es negativo, no finito o no representable como float.
        """
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser un número")
        if not es_finito(precio):
            raise ValueError("El precio debe ser finito")
        if precio < 0:
            raise ValueError(f"El precio no puede ser negativo: {precio}")
        self._nombre = nombre
        self._precio = precio

    @abstractmethod
    def mostrar_info(self) -> None:
        """Muestra la información del producto en consola.

        Cada subclase DEBE implementar este método con su propio formato.
        Si no lo implementa, Python lanzará TypeError al intentar instanciarla.
        """
        pass

    @property
    def nombre(self) -> str:
        """Nombre del producto (solo lectura)."""
        return self._nombre

    @property
    def precio(self) -> float:
        """Precio del producto (solo lectura)."""
        return self._precio


class Libro(Producto):
    """Producto concreto que representa un libro.

    Hereda de Producto y agrega el atributo _autor.
    Implementa mostrar_info() con el formato específico para libros.

    Atributos:
        _autor (str): Nombre del autor del libro.
    """

    def __init__(self, nombre: str, precio: float, autor: str) -> None:
        """Inicializa un libro con nombre, precio y autor.

        Args:
            nombre: Título del libro.
            precio: Precio del libro.
            autor: Nombre del autor.
        """
        super().__init__(nombre, precio)
        self._autor = autor

    def mostrar_info(self) -> None:
        """Muestra la información del libro: título, autor y precio."""
        print(f"Libro: {self._nombre} | Autor: {self._autor} | Precio: ${self._precio:.2f}")

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return f"Libro(nombre={self._nombre!r}, precio={self._precio}, autor={self._autor!r})"


class Electronico(Producto):
    """Producto concreto que representa un dispositivo electrónico.

    Hereda de Producto y agrega el atributo _garantia_meses.
    Implementa mostrar_info() con el formato específico para electrónicos.

    Atributos:
        _garantia_meses (int): Duración de la garantía en meses.
    """

    def __init__(self, nombre: str, precio: float, garantia_meses: int) -> None:
        """Inicializa un electrónico con nombre, precio y garantía.

        Args:
            nombre: Nombre del dispositivo.
            precio: Precio del dispositivo.
            garantia_meses: Meses de garantía.
        """
        super().__init__(nombre, precio)
        self._garantia_meses = garantia_meses

    def mostrar_info(self) -> None:
        """Muestra la información del electrónico: nombre, garantía y precio."""
        print(f"Electrónico: {self._nombre} | Garantía: {self._garantia_meses} meses "
              f"| Precio: ${self._precio:.2f}")

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return (f"Electronico(nombre={self._nombre!r}, precio={self._precio}, "
                f"garantia={self._garantia_meses}m)")
