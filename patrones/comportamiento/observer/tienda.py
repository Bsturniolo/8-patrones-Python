"""
Patrón Observer - Sujeto observable (Tienda).

La Tienda actúa como el "sujeto" o "publicador" en el patrón Observer.
Mantiene una lista de observadores (clientes suscritos) y los notifica
cuando ocurre un evento relevante (nueva oferta).

Flujo del patrón:
    1. Los clientes se suscriben con suscribir().
    2. La tienda publica una oferta con nueva_oferta().
    3. Internamente se llama a notificar_clientes(), que recorre la lista
       y llama a actualizar() en cada cliente suscrito.
    4. Los clientes pueden desuscribirse con desuscribir().

Validaciones implementadas:
    - Solo se aceptan objetos que hereden de Observer (isinstance).
    - No se permiten suscripciones duplicadas.
    - desuscribir() verifica que el cliente exista antes de eliminarlo.

Ejemplo de uso:
    >>> from patrones.comportamiento.observer.observer import Cliente
    >>> tienda = Tienda("MiTienda")
    >>> cliente = Cliente("Ana")
    >>> tienda.suscribir(cliente)
    Cliente suscrito a la tienda MiTienda
    >>> tienda.nueva_oferta("20% en todo")
    <BLANKLINE>
    ¡Nueva oferta en MiTienda!
    <BLANKLINE>
    --- Notificando a 1 clientes ---
    Cliente Ana recibió notificación: Nueva oferta: 20% en todo
"""

from typing import List
from patrones.comportamiento.observer.observer import Observer


class Tienda:
    """Sujeto observable que notifica ofertas a sus clientes suscritos.

    Atributos:
        _nombre (str): Nombre de la tienda.
        _clientes (list): Lista de observadores (clientes) suscritos.
    """

    def __init__(self, nombre: str) -> None:
        """Inicializa la tienda con su nombre y una lista vacía de clientes.

        Args:
            nombre (str): Nombre de la tienda.
        """
        self._nombre = nombre
        self._clientes: List[Observer] = []

    def suscribir(self, cliente: Observer) -> None:
        """Agrega un cliente a la lista de suscriptores.

        Validaciones:
            - El cliente debe ser una instancia de Observer (TypeError si no).
            - No se permiten suscripciones duplicadas del mismo cliente.

        Args:
            cliente (Observer): El cliente que desea suscribirse.

        Raises:
            TypeError: Si el objeto no es una instancia de Observer.
        """
        if not isinstance(cliente, Observer):
            raise TypeError("El objeto debe ser una instancia de Observer")
        if cliente in self._clientes:
            print(f"Cliente ya está suscrito a la tienda {self._nombre}")
            return
        self._clientes.append(cliente)
        print(f"Cliente suscrito a la tienda {self._nombre}")

    def desuscribir(self, cliente: Observer) -> None:
        """Elimina un cliente de la lista de suscriptores.

        Si el cliente no está suscrito, muestra un mensaje informativo
        en lugar de lanzar una excepción.

        Args:
            cliente (Observer): El cliente que desea desuscribirse.
        """
        if cliente not in self._clientes:
            print(f"Cliente no está suscrito a la tienda {self._nombre}")
            return
        self._clientes.remove(cliente)
        print(f"Cliente desuscrito de la tienda {self._nombre}")

    def notificar_clientes(self, mensaje: str) -> None:
        """Envía un mensaje a todos los clientes suscritos.

        Recorre una copia de la lista _clientes y llama al método actualizar()
        de cada observador. Se itera sobre una copia porque un observador
        podría desuscribirse dentro de actualizar(); modificar la lista
        mientras se la recorre haría que se saltee al siguiente cliente.

        Args:
            mensaje (str): El mensaje a enviar a todos los suscriptores.
        """
        print(f"\n--- Notificando a {len(self._clientes)} clientes ---")
        for cliente in list(self._clientes):
            cliente.actualizar(mensaje)

    def nueva_oferta(self, descripcion: str) -> None:
        """Publica una nueva oferta y notifica a todos los suscriptores.

        Este es el método que dispara todo el mecanismo del Observer:
        crea el mensaje y delega a notificar_clientes().

        Args:
            descripcion (str): Descripción de la oferta.
        """
        print(f"\n¡Nueva oferta en {self._nombre}!")
        self.notificar_clientes(f"Nueva oferta: {descripcion}")
