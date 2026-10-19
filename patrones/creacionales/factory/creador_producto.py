"""
Patrón Factory Method - Creadores de productos.

El patrón Factory Method (GoF) define una interfaz para crear un objeto, pero
deja que las SUBCLASES decidan qué clase concreta instanciar. Así, el código
del creador trabaja contra la abstracción Producto y nunca nombra a Libro ni
a Electronico.

Participantes del patrón en este módulo:
    - Producto (en producto.py): interfaz de los objetos que se crean.
    - Libro / Electronico (en producto.py): productos concretos.
    - CreadorProducto: creador abstracto. Declara el factory method
      crear_producto() y una operación propia (registrar_producto()) que lo usa.
    - CreadorLibro / CreadorElectronico: creadores concretos. Sobreescriben
      crear_producto() para devolver su producto concreto.

Diferencia con una "Simple Factory":
    En una Simple Factory, UNA clase decide con un if/elif qué producto crear;
    agregar un tipo nuevo obliga a modificarla. En Factory Method la decisión
    está repartida en subclases: agregar un tipo nuevo es agregar un creador
    nuevo, sin tocar el código existente (principio abierto/cerrado).

Ejemplo de uso:
    >>> creador = CreadorLibro("George Orwell")
    >>> libro = creador.crear_producto("1984", 15.99)
    >>> libro.nombre
    '1984'
    >>> producto = CreadorElectronico(24).registrar_producto("Laptop", 899.99)
    Electrónico: Laptop | Garantía: 24 meses | Precio: $899.99
"""

from abc import ABC, abstractmethod

from patrones.creacionales.factory.producto import Producto, Libro, Electronico


class CreadorProducto(ABC):
    """Creador abstracto del patrón Factory Method.

    Declara el factory method crear_producto(), que cada subclase implementa
    devolviendo su producto concreto. También ofrece registrar_producto(), una
    operación que usa el factory method sin conocer la clase concreta creada.
    """

    @abstractmethod
    def crear_producto(self, nombre: str, precio: float) -> Producto:
        """Factory method: crea el producto concreto que corresponde al creador.

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.

        Returns:
            Producto: Instancia del producto concreto.
        """
        pass

    def registrar_producto(self, nombre: str, precio: float) -> Producto:
        """Crea un producto mediante el factory method y muestra su información.

        Este método no sabe qué producto concreto se crea: delega esa decisión
        a crear_producto() y luego usa el resultado solo a través de la
        interfaz Producto (mostrar_info() es polimórfico).

        Args:
            nombre (str): Nombre del producto.
            precio (float): Precio del producto.

        Returns:
            Producto: El producto creado y mostrado.
        """
        producto = self.crear_producto(nombre, precio)
        producto.mostrar_info()
        return producto


class CreadorLibro(CreadorProducto):
    """Creador concreto que produce instancias de Libro.

    Atributos:
        _autor (str): Autor asignado a los libros que crea este creador.
    """

    def __init__(self, autor: str = "Autor Desconocido") -> None:
        """Inicializa el creador con el autor de los libros que va a crear.

        Args:
            autor (str): Nombre del autor. Por defecto, "Autor Desconocido".
        """
        self._autor = autor

    def crear_producto(self, nombre: str, precio: float) -> Libro:
        """Crea un Libro con el autor configurado en este creador.

        Args:
            nombre (str): Título del libro.
            precio (float): Precio del libro.

        Returns:
            Libro: Nueva instancia de Libro.
        """
        return Libro(nombre, precio, self._autor)


class CreadorElectronico(CreadorProducto):
    """Creador concreto que produce instancias de Electronico.

    Atributos:
        _garantia_meses (int): Meses de garantía de los electrónicos que crea.
    """

    def __init__(self, garantia_meses: int = 12) -> None:
        """Inicializa el creador con la garantía de los electrónicos que va a crear.

        Args:
            garantia_meses (int): Meses de garantía. Por defecto, 12.
        """
        self._garantia_meses = garantia_meses

    def crear_producto(self, nombre: str, precio: float) -> Electronico:
        """Crea un Electronico con la garantía configurada en este creador.

        Args:
            nombre (str): Nombre del dispositivo.
            precio (float): Precio del dispositivo.

        Returns:
            Electronico: Nueva instancia de Electronico.
        """
        return Electronico(nombre, precio, self._garantia_meses)
