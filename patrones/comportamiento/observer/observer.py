"""
Patrón Observer - Interfaz del observador y observador concreto.

El patrón Observer define una relación uno-a-muchos entre objetos: cuando un
objeto (el "sujeto") cambia de estado, todos sus dependientes (los "observadores")
son notificados automáticamente.

Este módulo define:
    - Observer: Interfaz abstracta que todo observador debe implementar.
    - Cliente: Observador concreto que representa a un cliente de la tienda.

Analogía:
    Es como suscribirse a un canal de YouTube. Cuando el canal sube un video
    (nueva oferta), todos los suscriptores (clientes) reciben la notificación.
    Si te desuscribes, dejas de recibir avisos.

Ejemplo de uso:
    >>> cliente = Cliente("Juan")
    >>> cliente.actualizar("50% de descuento")
    Cliente Juan recibió notificación: 50% de descuento
    >>> cliente.nombre
    'Juan'
"""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Interfaz abstracta que define el contrato para los observadores.

    Todo objeto que quiera recibir notificaciones de un sujeto observable
    debe heredar de esta clase e implementar el método actualizar().
    """

    @abstractmethod
    def actualizar(self, mensaje: str) -> None:
        """Recibe una notificación del sujeto observable.

        Args:
            mensaje: El contenido de la notificación.
        """
        pass


class Cliente(Observer):
    """Observador concreto que representa un cliente de la tienda.

    Implementa el método actualizar() para recibir y mostrar las
    notificaciones enviadas por la tienda.

    Atributos:
        _nombre (str): Nombre del cliente.
    """

    def __init__(self, nombre: str) -> None:
        """Inicializa un cliente con su nombre.

        Args:
            nombre: Nombre del cliente.
        """
        self._nombre = nombre

    def actualizar(self, mensaje: str) -> None:
        """Recibe y muestra una notificación de la tienda.

        Args:
            mensaje: Contenido de la notificación recibida.
        """
        print(f"Cliente {self._nombre} recibió notificación: {mensaje}")

    @property
    def nombre(self) -> str:
        """Nombre del cliente (solo lectura)."""
        return self._nombre

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return f"Cliente({self._nombre!r})"
