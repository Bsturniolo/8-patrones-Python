"""
Módulo que implementa el patrón Decorator para productos de la tienda.

El patrón Decorator permite agregar responsabilidades adicionales a un objeto
dinámicamente, como alternativa flexible a la herencia. Los decoradores envuelven
al componente y extienden su comportamiento sin modificar su clase.

Analogía: es como agregar ingredientes a una pizza. La pizza base tiene un precio;
si agregas mozzarella extra (+$2), el total sube, pero sigue siendo una pizza.
Si además agregas jamón (+$3), el total suma sobre el precio anterior. Cada
"topping" es un decorador que envuelve el componente anterior.

Problema que resuelve sin Decorator:
    Si existieran 3 servicios opcionales (envoltura, seguro, garantía), habría que
    crear 7 subclases para cubrir cada combinación posible. Con Decorator, basta
    con 3 clases y se pueden combinar arbitrariamente en tiempo de ejecución.

Clases:
    ComponenteProducto: Interfaz abstracta base (ABC).
    ProductoConcreto: Componente concreto — el producto base a decorar.
    DecoradorProducto: Decorador base instanciable que envuelve un ComponenteProducto.
    EnvolturaRegalo: Decorador concreto — agrega envoltura de regalo (+$5.00).
    SeguroProducto: Decorador concreto — agrega seguro del producto (+2%).
    GarantiaExtendida: Decorador concreto — agrega garantía extendida de 2 años (+$29.99).

Uso:
    producto = ProductoConcreto("Laptop HP", 899.99)
    producto = EnvolturaRegalo(producto)      # envuelve con regalo
    producto = SeguroProducto(producto)       # agrega seguro sobre el precio actual
    producto = GarantiaExtendida(producto)    # agrega garantía extendida

    print(producto.descripcion)
    # Laptop HP + Envoltura de regalo + Seguro del producto + Garantía extendida (2 años)
    print(producto.precio)
    # 953.08
"""

from abc import ABC, abstractmethod
from patrones._numeros import es_finito


class ComponenteProducto(ABC):
    """Interfaz abstracta que define el contrato para productos y decoradores.

    Tanto el componente base (ProductoConcreto) como todos los decoradores
    implementan esta interfaz, lo que permite que los decoradores sean
    intercambiables con el componente y entre sí.
    """

    @property
    @abstractmethod
    def descripcion(self) -> str:
        """Descripción acumulada del producto con sus servicios.

        Returns:
            Descripción del producto incluyendo todos los decoradores aplicados.
        """
        pass

    @property
    @abstractmethod
    def precio(self) -> float:
        """Precio total del producto con todos sus decoradores.

        Returns:
            Precio acumulado con todos los servicios adicionales.
        """
        pass


class ProductoConcreto(ComponenteProducto):
    """Componente concreto base — el producto sin servicios adicionales.

    Es el punto de partida de la cadena de decoradores. Almacena el nombre
    y precio base del producto que se desea decorar.

    Atributos:
        _nombre (str): Nombre del producto.
        _precio (float): Precio base del producto.
    """

    def __init__(self, nombre: str, precio: float) -> None:
        """Inicializa el producto con nombre y precio base.

        Args:
            nombre: Nombre descriptivo del producto.
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

    @property
    def descripcion(self) -> str:
        """Nombre base del producto, sin decoradores."""
        return self._nombre

    @property
    def precio(self) -> float:
        """Precio base del producto, sin cargos adicionales."""
        return self._precio

    def __repr__(self) -> str:
        """Representación técnica útil para depuración."""
        return f"ProductoConcreto({self._nombre!r}, {self._precio})"


class DecoradorProducto(ComponenteProducto):
    """Decorador base instanciable que envuelve un ComponenteProducto.

    Define la estructura base de todos los decoradores concretos. Mantiene
    una referencia al componente envuelto y delega las operaciones base a él,
    permitiendo que las subclases solo sobreescriban lo que modifican.

    Atributos:
        _componente (ComponenteProducto): El objeto que este decorador envuelve.
    """

    def __init__(self, componente: ComponenteProducto) -> None:
        """Inicializa el decorador envolviendo al componente dado.

        Args:
            componente: El producto (o decorador) a envolver.
        """
        self._componente = componente

    @property
    def descripcion(self) -> str:
        """Delega la descripción al componente envuelto."""
        return self._componente.descripcion

    @property
    def precio(self) -> float:
        """Delega el precio al componente envuelto."""
        return self._componente.precio


class EnvolturaRegalo(DecoradorProducto):
    """Decorador que agrega el servicio de envoltura de regalo al producto.

    Agrega un cargo fijo de $5.00 al precio del componente envuelto e
    incluye la leyenda "+ Envoltura de regalo" en la descripción.

    Atributos:
        COSTO (float): Cargo fijo por el servicio de envoltura.
    """

    COSTO = 5.00

    @property
    def descripcion(self) -> str:
        """Extiende la descripción con la leyenda de envoltura de regalo."""
        return self._componente.descripcion + " + Envoltura de regalo"

    @property
    def precio(self) -> float:
        """Suma el costo de envoltura al precio del componente."""
        return round(self._componente.precio + self.COSTO, 2)


class SeguroProducto(DecoradorProducto):
    """Decorador que agrega seguro al producto (2% sobre el precio actual).

    El cargo es proporcional al precio del componente en ese momento, lo que
    significa que si ya se aplicaron otros decoradores, el seguro se calcula
    sobre el precio ya aumentado.

    Atributos:
        PORCENTAJE (float): Porcentaje del precio que se cobra como seguro (0.02 = 2%).
    """

    PORCENTAJE = 0.02

    @property
    def descripcion(self) -> str:
        """Extiende la descripción con la leyenda del seguro."""
        return self._componente.descripcion + " + Seguro del producto"

    @property
    def precio(self) -> float:
        """Suma el 2% del precio actual; ValueError si el resultado no es finito."""
        precio = round(self._componente.precio * (1 + self.PORCENTAJE), 2)
        if not es_finito(precio):
            raise ValueError("El precio con seguro excede el rango numérico")
        return precio


class GarantiaExtendida(DecoradorProducto):
    """Decorador que agrega garantía extendida de 2 años al producto (+$29.99).

    Aplica un cargo fijo e incluye la leyenda "+ Garantía extendida (2 años)"
    en la descripción. Útil para productos electrónicos de alto valor.

    Atributos:
        COSTO (float): Cargo fijo por la garantía extendida.
    """

    COSTO = 29.99

    @property
    def descripcion(self) -> str:
        """Extiende la descripción con la leyenda de garantía extendida."""
        return self._componente.descripcion + " + Garantía extendida (2 años)"

    @property
    def precio(self) -> float:
        """Suma el costo de la garantía extendida al precio del componente."""
        return round(self._componente.precio + self.COSTO, 2)
