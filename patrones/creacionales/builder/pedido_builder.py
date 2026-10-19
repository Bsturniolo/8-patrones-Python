"""
Módulo que implementa el patrón Builder para la construcción de pedidos.

El patrón Builder permite construir objetos complejos paso a paso. A diferencia
de un constructor con muchos parámetros, el builder expone métodos individuales
para cada parte del objeto, y devuelve el resultado final en build().

Analogía: es como armar una hamburguesa en una cadena de comida rápida — el
cliente elige exactamente qué ingredientes quiere y en qué orden; el cocinero
(builder) ensambla la hamburguesa (pedido) sin que el cliente sepa cómo.

Clases:
    PedidoBuilder: Interfaz abstracta del builder.
    PedidoEstandarBuilder: Construye pedidos con envío estándar ($5.00, 5 días).
    PedidoExpressBuilder: Construye pedidos con envío express ($15.00, 1 día).
    DirectorPedido: Orquesta el builder para crear pedidos predefinidos.

Uso:
    builder = PedidoEstandarBuilder()
    director = DirectorPedido(builder)

    # Pedido simple
    pedido = director.construir_pedido_simple([libro, laptop], "Av. 9 de Julio 100")
    pedido.mostrar_resumen()

    # Pedido de regalo (incluye envoltura + seguro)
    pedido_regalo = director.construir_pedido_regalo(
        [iphone], "Calle Falsa 123", "Feliz cumpleaños!"
    )
    pedido_regalo.mostrar_resumen()
"""

from abc import ABC, abstractmethod
from patrones._numeros import es_finito
from typing import Any, List
from patrones.creacionales.builder.pedido import Pedido


class PedidoBuilder(ABC):
    """Interfaz abstracta que define los pasos para construir un Pedido.

    Cada método configura una parte del pedido. El orden de llamada es flexible;
    la clase DirectorPedido define secuencias predefinidas de construcción.

    Las subclases concretas implementan los detalles de cada tipo de envío
    (costos, tiempos estimados, restricciones).
    """

    @abstractmethod
    def agregar_producto(self, producto: Any) -> None:
        """Agrega un producto al pedido.

        Args:
            producto: Objeto con propiedades `nombre` y `precio` (duck typing).
        """
        pass

    @abstractmethod
    def set_direccion(self, direccion: str) -> None:
        """Establece la dirección de envío del pedido.

        Args:
            direccion (str): Dirección completa de entrega.
        """
        pass

    @abstractmethod
    def set_tipo_envio(self, tipo: str) -> None:
        """Configura el tipo de envío.

        Args:
            tipo (str): Tipo de envío ("estándar" o "express").
        """
        pass

    @abstractmethod
    def set_envoltura_regalo(self, nota: str) -> None:
        """Agrega envoltura de regalo con nota personalizada.

        Args:
            nota (str): Mensaje de regalo para incluir en el paquete.
        """
        pass

    @abstractmethod
    def set_seguro(self) -> None:
        """Activa el seguro del pedido (3% del subtotal de productos)."""
        pass

    @abstractmethod
    def build(self) -> Pedido:
        """Finaliza la construcción y devuelve el Pedido configurado.

        Returns:
            Pedido: El objeto Pedido completamente configurado.
        """
        pass


class PedidoEstandarBuilder(PedidoBuilder):
    """Builder concreto para pedidos con envío estándar.

    Configura el pedido con envío estándar: costo $5.00 y 5 días hábiles.
    Es la opción más económica para pedidos sin urgencia.

    Attributes:
        _pedido (Pedido): La instancia del pedido en construcción.
    """

    COSTO_ENVIO = 5.00
    TIPO_ENVIO = "Estándar (5 días hábiles)"

    def __init__(self) -> None:
        """Inicializa el builder creando un nuevo Pedido vacío."""
        self._pedido = Pedido()

    def agregar_producto(self, producto: Any) -> None:
        """Agrega un producto al pedido.

        Args:
            producto: Objeto con propiedades `nombre` y `precio`.
                El precio debe ser int o float finito, no negativo y distinto de bool.

        Raises:
            TypeError: Si faltan atributos o el tipo del precio es inválido.
            ValueError: Si el precio es negativo, no finito o no representable como float.

        La validación ocurre antes de modificar el pedido.
        """
        try:
            nombre, precio = producto.nombre, producto.precio
        except AttributeError as error:
            raise TypeError("El producto debe exponer nombre y precio") from error
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser un número")
        if not es_finito(precio) or precio < 0:
            raise ValueError("El precio debe ser finito y no negativo")
        mensaje = f"  Producto agregado: {nombre} (${precio:.2f})"
        self._pedido._items.append(producto)
        print(mensaje)

    def set_direccion(self, direccion: str) -> None:
        """Establece la dirección de envío.

        Args:
            direccion (str): Dirección completa de entrega.
        """
        self._pedido._direccion_envio = direccion

    def set_tipo_envio(self, tipo: str) -> None:
        """Asigna la etiqueta del tipo de envío y el costo estándar.

        Nota: build() vuelve a aplicar TIPO_ENVIO y COSTO_ENVIO (HU-011), por
        lo que la etiqueta asignada aquí se reemplaza al construir el pedido.

        Args:
            tipo (str): Etiqueta del tipo de envío.
        """
        self._pedido._tipo_envio = tipo
        self._pedido._costo_envio = self.COSTO_ENVIO

    def set_envoltura_regalo(self, nota: str) -> None:
        """Activa la envoltura de regalo y guarda la nota personalizada.

        Args:
            nota (str): Mensaje de regalo para incluir en el paquete.
        """
        self._pedido._incluye_envoltura = True
        self._pedido._nota_regalo = nota

    def set_seguro(self) -> None:
        """Activa el seguro del pedido (3% del subtotal)."""
        self._pedido._incluye_seguro = True

    def build(self) -> Pedido:
        """Aplica TIPO_ENVIO y COSTO_ENVIO estándar y devuelve el pedido terminado.

        Returns:
            Pedido: El pedido con envío estándar configurado.
        """
        self._pedido._tipo_envio = self.TIPO_ENVIO
        self._pedido._costo_envio = self.COSTO_ENVIO
        pedido_terminado = self._pedido
        self._pedido = Pedido()   # reset para reutilización del builder
        return pedido_terminado


class PedidoExpressBuilder(PedidoBuilder):
    """Builder concreto para pedidos con envío express.

    Configura el pedido con envío express: costo $15.00 y entrega en 1 día hábil.
    Ideal para pedidos urgentes o regalos de último momento.

    Attributes:
        _pedido (Pedido): La instancia del pedido en construcción.
    """

    COSTO_ENVIO = 15.00
    TIPO_ENVIO = "Express (1 día hábil)"

    def __init__(self) -> None:
        """Inicializa el builder creando un nuevo Pedido vacío."""
        self._pedido = Pedido()

    def agregar_producto(self, producto: Any) -> None:
        """Agrega un producto al pedido.

        Args:
            producto: Objeto con propiedades `nombre` y `precio`.
                El precio debe ser int o float finito, no negativo y distinto de bool.

        Raises:
            TypeError: Si faltan atributos o el tipo del precio es inválido.
            ValueError: Si el precio es negativo, no finito o no representable como float.

        La validación ocurre antes de modificar el pedido.
        """
        try:
            nombre, precio = producto.nombre, producto.precio
        except AttributeError as error:
            raise TypeError("El producto debe exponer nombre y precio") from error
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise TypeError("El precio debe ser un número")
        if not es_finito(precio) or precio < 0:
            raise ValueError("El precio debe ser finito y no negativo")
        mensaje = f"  Producto agregado: {nombre} (${precio:.2f})"
        self._pedido._items.append(producto)
        print(mensaje)

    def set_direccion(self, direccion: str) -> None:
        """Establece la dirección de envío.

        Args:
            direccion (str): Dirección completa de entrega.
        """
        self._pedido._direccion_envio = direccion

    def set_tipo_envio(self, tipo: str) -> None:
        """Asigna la etiqueta del tipo de envío y el costo express.

        Nota: build() vuelve a aplicar TIPO_ENVIO y COSTO_ENVIO (HU-012), por
        lo que la etiqueta asignada aquí se reemplaza al construir el pedido.

        Args:
            tipo (str): Etiqueta del tipo de envío.
        """
        self._pedido._tipo_envio = tipo
        self._pedido._costo_envio = self.COSTO_ENVIO

    def set_envoltura_regalo(self, nota: str) -> None:
        """Activa la envoltura de regalo y guarda la nota personalizada.

        Args:
            nota (str): Mensaje de regalo para incluir en el paquete.
        """
        self._pedido._incluye_envoltura = True
        self._pedido._nota_regalo = nota

    def set_seguro(self) -> None:
        """Activa el seguro del pedido (3% del subtotal)."""
        self._pedido._incluye_seguro = True

    def build(self) -> Pedido:
        """Aplica TIPO_ENVIO y COSTO_ENVIO express y devuelve el pedido terminado.

        Returns:
            Pedido: El pedido con envío express configurado.
        """
        self._pedido._tipo_envio = self.TIPO_ENVIO
        self._pedido._costo_envio = self.COSTO_ENVIO
        pedido_terminado = self._pedido
        self._pedido = Pedido()   # reset para reutilización del builder
        return pedido_terminado


class DirectorPedido:
    """Director que orquesta el builder para crear pedidos predefinidos.

    El Director conoce la secuencia de pasos necesaria para construir tipos
    comunes de pedidos, evitando que el cliente tenga que invocar cada paso
    manualmente. El cliente solo elige qué builder usar.

    Attributes:
        _builder (PedidoBuilder): El builder concreto que se orquesta.
    """

    def __init__(self, builder: "PedidoBuilder") -> None:
        """Inicializa el director con un builder concreto.

        Args:
            builder (PedidoBuilder): Instancia del builder a utilizar.
        """
        self._builder = builder

    def set_builder(self, builder: "PedidoBuilder") -> None:
        """Reemplaza el builder en uso, permitiendo reutilizar el director.

        Args:
            builder (PedidoBuilder): Nuevo builder a utilizar.
        """
        self._builder = builder

    def construir_pedido_simple(self, productos: List, direccion: str) -> Pedido:
        """Construye un pedido con la modalidad del builder seleccionado.

        Usa el estado actual del builder. Para un pedido sin extras ni productos
        previos, debe recibirse un builder nuevo o reiniciado mediante build().

        Args:
            productos (list): Lista de productos (con propiedades nombre y precio).
            direccion (str): Dirección de entrega.

        Returns:
            Pedido: Pedido con productos y dirección, sin envoltura ni seguro.
        """
        for producto in productos:
            self._builder.agregar_producto(producto)
        self._builder.set_direccion(direccion)
        return self._builder.build()

    def construir_pedido_regalo(self, productos: List, direccion: str, nota: str) -> Pedido:
        """Construye un pedido de regalo con envoltura y seguro incluidos.

        Args:
            productos (list): Lista de productos (con propiedades nombre y precio).
            direccion (str): Dirección de entrega.
            nota (str): Mensaje de regalo personalizado.

        Returns:
            Pedido: Pedido con envoltura de regalo y seguro activados.
        """
        for producto in productos:
            self._builder.agregar_producto(producto)
        self._builder.set_direccion(direccion)
        self._builder.set_envoltura_regalo(nota)
        self._builder.set_seguro()
        return self._builder.build()
