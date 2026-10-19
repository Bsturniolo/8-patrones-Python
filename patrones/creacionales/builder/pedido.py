"""
Módulo que define la clase Pedido para el patrón Builder.

El patrón Builder separa la construcción de un objeto complejo de su representación,
de modo que el mismo proceso de construcción pueda crear diferentes representaciones.

La clase Pedido es el **producto final** que el Builder construye paso a paso.
Un pedido puede contener múltiples productos, una dirección de envío, tipo de envío,
envoltura de regalo y seguro. Todos estos atributos son opcionales y se asignan
progresivamente a través del builder.

Clases:
    Pedido: Objeto complejo resultante del proceso de construcción.

Uso:
    # Uso habitual: obtenerlo llamando a builder.build()
    builder = PedidoEstandarBuilder()
    builder.agregar_producto(producto)
    builder.set_direccion("Av. Corrientes 1234, Buenos Aires")
    pedido = builder.build()
    pedido.mostrar_resumen()
"""

from typing import List, Optional

from patrones._numeros import es_finito


class Pedido:
    """Representa un pedido complejo construido paso a paso mediante el patrón Builder.

    Un pedido agrupa productos, dirección y opciones de envío, envoltura de regalo
    y seguro. Habitualmente se obtiene mediante un PedidoBuilder concreto;
    también puede instanciarse directamente como pedido vacío.

    Attributes:
        _items (list): Lista de productos (con propiedades nombre y precio).
        _direccion_envio (str): Dirección de destino del pedido.
        _tipo_envio (str): Modalidad de envío ("estándar" o "express").
        _costo_envio (float): Costo del envío según la modalidad.
        _incluye_envoltura (bool): Indica si incluye envoltura de regalo.
        _nota_regalo (str): Mensaje personalizado para la envoltura.
        _incluye_seguro (bool): Indica si incluye seguro del pedido.
    """

    # Costos fijos asociados a los servicios adicionales
    COSTO_ENVOLTURA = 5.00
    COSTO_SEGURO_PORCENTAJE = 0.03   # 3% del subtotal de productos

    def __init__(self) -> None:
        """Inicializa un Pedido vacío con todos los atributos en estado neutro."""
        self._items: List = []
        self._direccion_envio: Optional[str] = None
        self._tipo_envio: Optional[str] = None
        self._costo_envio: float = 0.0
        self._incluye_envoltura: bool = False
        self._nota_regalo: Optional[str] = None
        self._incluye_seguro: bool = False

    def calcular_total(self) -> float:
        """Calcula el total del pedido sumando productos y cargos adicionales.

        Returns:
            float: Total del pedido redondeado a 2 decimales.

        Raises:
            TypeError: Si un precio externo ya no es int o float, o es bool.
            ValueError: Si un precio o el total es negativo, no finito o fuera de rango.
        """
        subtotal = 0.0
        for producto in self._items:
            precio = producto.precio
            if not isinstance(precio, (int, float)) or isinstance(precio, bool):
                raise TypeError("El precio debe ser un número")
            if not es_finito(precio) or precio < 0:
                raise ValueError("El precio debe ser finito y no negativo")
            subtotal += precio
        total = subtotal + self._costo_envio
        if self._incluye_envoltura:
            total += self.COSTO_ENVOLTURA
        if self._incluye_seguro:
            total += round(subtotal * self.COSTO_SEGURO_PORCENTAJE, 2)
        if not es_finito(total):
            raise ValueError("El total del pedido excede el rango numérico")
        return round(total, 2)

    def mostrar_resumen(self) -> None:
        """Imprime el resumen completo del pedido con todos sus detalles."""
        print("=== RESUMEN DEL PEDIDO ===")

        print("Productos:")
        for producto in self._items:
            print(f"  - {producto.nombre} | ${producto.precio:.2f}")

        subtotal = sum(p.precio for p in self._items)
        print(f"Subtotal productos: ${subtotal:.2f}")

        print(f"Tipo de envío: {self._tipo_envio} (${self._costo_envio:.2f})")
        print(f"Dirección: {self._direccion_envio}")

        if self._incluye_envoltura:
            print(f"Envoltura de regalo: Sí (+${self.COSTO_ENVOLTURA:.2f})")
            if self._nota_regalo:
                print(f"  Nota: \"{self._nota_regalo}\"")

        if self._incluye_seguro:
            costo_seguro = round(subtotal * self.COSTO_SEGURO_PORCENTAJE, 2)
            print(f"Seguro del pedido: Sí (+${costo_seguro:.2f})")

        print(f"TOTAL: ${self.calcular_total():.2f}")
        print("==========================")

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        nombres = [p.nombre for p in self._items]
        return (
            f"Pedido(items={nombres!r}, tipo_envio={self._tipo_envio!r}, "
            f"total={self.calcular_total():.2f})"
        )
