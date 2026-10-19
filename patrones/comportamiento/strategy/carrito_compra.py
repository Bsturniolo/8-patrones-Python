"""
Patrón Strategy - Contexto (Carrito de Compras).

En el patrón Strategy, el "contexto" es la clase que UTILIZA las estrategias
sin conocer su implementación interna. En este caso, CarritoCompra delega
el procesamiento del pago a cualquier objeto que implemente EstrategiaPago.

Relación con el patrón:
    - CarritoCompra = Contexto (usa la estrategia).
    - EstrategiaPago = Interfaz de estrategia (contrato).
    - PagoTarjeta/PagoEfectivo/PagoPayPal = Estrategias concretas.

Flujo de uso:
    1. Crear un carrito: carrito = CarritoCompra()
    2. Agregar productos: carrito.agregar_producto(producto)
    3. Elegir forma de pago: carrito.set_estrategia_pago(PagoTarjeta(...))
    4. Finalizar compra: carrito.checkout()
    5. Tras el checkout, el carrito se vacía automáticamente.

Ejemplo de uso:
    >>> from patrones.comportamiento.strategy.estrategia_pago import PagoEfectivo
    >>> from patrones.creacionales.factory import CreadorLibro
    >>> libro = CreadorLibro("George Orwell").crear_producto("1984", 15.99)
    >>> carrito = CarritoCompra()
    >>> carrito.agregar_producto(libro)
    Producto agregado al carrito: 1984
    >>> carrito.set_estrategia_pago(PagoEfectivo())
    >>> carrito.checkout()
    <BLANKLINE>
    === CHECKOUT ===
    Productos en el carrito:
    Libro: 1984 | Autor: George Orwell | Precio: $15.99
    Total: $15.99
    Pagando $15.99 en efectivo. Se aplicó 5% descuento.
    Total a pagar: $15.19
    ¡Compra completada!
    <BLANKLINE>
"""

from patrones._numeros import es_finito
from typing import Any

from patrones.comportamiento.strategy.estrategia_pago import EstrategiaPago


class CarritoCompra:
    """Carrito de compras que utiliza el patrón Strategy para el pago.

    El carrito acumula productos y, al momento del checkout, delega
    el procesamiento del pago a la estrategia configurada.

    Atributos:
        _productos (list): Lista de productos agregados al carrito.
        _estrategia_pago (EstrategiaPago | None): Método de pago seleccionado.
    """

    def __init__(self) -> None:
        """Inicializa un carrito vacío sin método de pago seleccionado."""
        self._productos = []
        self._estrategia_pago = None

    def agregar_producto(self, producto: Any) -> None:
        """Agrega un producto al carrito.

        Args:
            producto: Objeto con nombre, precio y método mostrar_info().
                El precio debe ser int o float finito, no negativo y distinto de bool.

        Raises:
            TypeError: Si falta el contrato del producto o el tipo de precio es inválido.
            ValueError: Si el precio es negativo, no finito o no representable como float.

        La validación ocurre antes de modificar el carrito.
        """
        if not callable(getattr(producto, "mostrar_info", None)):
            raise TypeError("El producto debe implementar mostrar_info()")
        try:
            nombre = producto.nombre
            precio = producto.precio
        except AttributeError as error:
            raise TypeError("El producto debe exponer nombre y precio") from error
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser un número")
        if not es_finito(precio) or precio < 0:
            raise ValueError("El precio debe ser finito y no negativo")
        mensaje = f"Producto agregado al carrito: {nombre}"
        self._productos.append(producto)
        print(mensaje)

    def set_estrategia_pago(self, estrategia_pago: EstrategiaPago) -> None:
        """Establece o cambia el método de pago del carrito.

        Este es el método clave del patrón Strategy: permite cambiar
        el comportamiento de pago en tiempo de ejecución sin modificar
        la clase CarritoCompra.

        Args:
            estrategia_pago (EstrategiaPago): La estrategia de pago a usar.

        Raises:
            TypeError: Si el objeto no es una instancia de EstrategiaPago.
        """
        if not isinstance(estrategia_pago, EstrategiaPago):
            raise TypeError(
                f"La estrategia debe ser una instancia de EstrategiaPago, "
                f"se recibió {type(estrategia_pago).__name__}"
            )
        self._estrategia_pago = estrategia_pago

    def calcular_total(self) -> float:
        """Calcula la suma de los precios de todos los productos.

        Returns:
            float: Total redondeado a 2 decimales; float no representa todos
                los valores decimales exactamente.

        Raises:
            TypeError: Si un producto externo cambió su precio a un tipo inválido.
            ValueError: Si un precio o el total es negativo, no finito o fuera de rango.
        """
        total = 0.0
        for producto in self._productos:
            precio = producto.precio
            if not isinstance(precio, (int, float)) or isinstance(precio, bool):
                raise TypeError("El precio debe ser un número")
            if not es_finito(precio) or precio < 0:
                raise ValueError("El precio debe ser finito y no negativo")
            total += precio
        if not es_finito(total):
            raise ValueError("El total del carrito excede el rango numérico")
        return round(total, 2)

    def checkout(self) -> None:
        """Finaliza la compra: muestra resumen, calcula total y procesa el pago.

        Validaciones antes de proceder:
            1. El carrito no debe estar vacío.
            2. Debe haber un método de pago seleccionado.
            3. Se revalidan precios y total antes de invocar la estrategia.

        Los productos externos se conservan por referencia. Si cambian sus precios,
        calcular_total() los comprueba de nuevo. Los errores previos al pago o del
        propio pago se propagan conservando el carrito para un reintento.

        Flujo exitoso:
            - Muestra todos los productos con mostrar_info().
            - Calcula el total con calcular_total().
            - Delega el pago a self._estrategia_pago.pagar(total).
            - Vacía el carrito y resetea la estrategia de pago.
        """
        if not self._productos:
            print("El carrito está vacío")
            return

        if self._estrategia_pago is None:
            print("Debe seleccionar un método de pago")
            return

        total = self.calcular_total()
        print("\n=== CHECKOUT ===")
        print("Productos en el carrito:")
        for producto in self._productos:
            producto.mostrar_info()
        print(f"Total: ${total:.2f}")
        self._estrategia_pago.pagar(total)
        print("¡Compra completada!\n")
        self._productos = []
        self._estrategia_pago = None
