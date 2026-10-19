"""
Patrón Strategy - Estrategias de pago.

El patrón Strategy permite definir una familia de algoritmos (en este caso,
formas de pago), encapsular cada uno en una clase y hacerlos intercambiables
en tiempo de ejecución.

Este módulo define:
    - EstrategiaPago: Interfaz abstracta que toda forma de pago debe cumplir.
    - PagoTarjeta: Pago con tarjeta de crédito/débito (muestra solo últimos 4 dígitos).
    - PagoEfectivo: Pago en efectivo con 5% de descuento.
    - PagoPayPal: Pago digital mediante cuenta de correo.

Ventajas del patrón Strategy:
    1. Se pueden agregar nuevas formas de pago sin modificar el carrito.
    2. El carrito no sabe NI necesita saber cómo funciona cada método de pago.
    3. El método de pago se puede cambiar dinámicamente antes del checkout.

Ejemplo de uso:
    >>> estrategia = PagoTarjeta("4532-1234-5678-9012")
    >>> estrategia.pagar(100.0)
    Pagando $100.00 con tarjeta terminada en 9012
"""

from abc import ABC, abstractmethod


class EstrategiaPago(ABC):
    """Interfaz abstracta para las estrategias de pago.

    Toda nueva forma de pago debe heredar de esta clase e implementar
    el método pagar(). Esto garantiza que el CarritoCompra pueda usar
    cualquier estrategia sin conocer su implementación interna.
    """

    @abstractmethod
    def pagar(self, monto: float) -> None:
        """Procesa el pago por el monto indicado.

        Args:
            monto (float): Monto total a pagar.
        """
        pass


class PagoTarjeta(EstrategiaPago):
    """Estrategia de pago con tarjeta de crédito/débito.

    Por seguridad, solo muestra los últimos 4 dígitos del número de tarjeta
    al procesar el pago.

    Atributos:
        _numero_tarjeta (str): Número completo de la tarjeta.
    """

    def __init__(self, numero_tarjeta: str) -> None:
        """Inicializa la estrategia con el número de tarjeta.

        Args:
            numero_tarjeta (str): Número de la tarjeta (ej: "4532-1234-5678-9012").
        """
        self._numero_tarjeta = numero_tarjeta

    def pagar(self, monto: float) -> None:
        """Procesa el pago con tarjeta, mostrando solo los últimos 4 dígitos.

        Args:
            monto (float): Monto total a pagar.
        """
        ultimos_digitos = self._numero_tarjeta[-4:]
        print(f"Pagando ${monto:.2f} con tarjeta terminada en {ultimos_digitos}")


class PagoEfectivo(EstrategiaPago):
    """Estrategia de pago en efectivo con descuento del 5%.

    Al pagar en efectivo se aplica automáticamente un descuento del 5%
    sobre el monto total. Se usa round() para redondear a dos decimales;
    esto no convierte float en aritmética decimal exacta.
    """

    def pagar(self, monto: float) -> None:
        """Procesa el pago en efectivo aplicando 5% de descuento.

        Args:
            monto (float): Monto total antes del descuento.
        """
        total_con_descuento = round(monto * 0.95, 2)
        print(f"Pagando ${monto:.2f} en efectivo. Se aplicó 5% descuento.")
        print(f"Total a pagar: ${total_con_descuento:.2f}")


class PagoPayPal(EstrategiaPago):
    """Estrategia de pago con PayPal.

    Utiliza el correo electrónico del usuario como identificador
    de la cuenta de PayPal.

    Atributos:
        _email (str): Correo electrónico de la cuenta PayPal.
    """

    def __init__(self, email: str) -> None:
        """Inicializa la estrategia con el email de PayPal.

        Args:
            email (str): Correo electrónico asociado a la cuenta PayPal.
        """
        self._email = email

    def pagar(self, monto: float) -> None:
        """Procesa el pago a través de PayPal.

        Args:
            monto (float): Monto total a pagar.
        """
        print(f"Pagando ${monto:.2f} con PayPal desde la cuenta: {self._email}")
