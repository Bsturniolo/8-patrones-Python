"""
Módulo que implementa el patrón Adapter para sistemas de envío.

El patrón Adapter (también llamado Wrapper) convierte la interfaz de una clase
en otra interfaz que el cliente espera. Permite que clases con interfaces
incompatibles trabajen juntas sin modificar su código fuente.

Problema que resuelve:
    La tienda quiere integrar dos transportistas (DHL y FedEx), pero cada uno
    tiene su propia API con nombres de métodos distintos y unidades distintas:
    - DHL usa gramos y devuelve "2-3 días" como cadena de texto.
    - FedEx usa libras y códigos postales de 4 dígitos.
    Sin el Adapter, el código del carrito/checkout tendría que conocer los detalles
    de cada transportista y tendría lógica condicional para cada uno.

Solución con Adapter:
    Se define una interfaz unificada (SistemaEnvio) y se crean adaptadores que
    traducen las llamadas a esa interfaz hacia la API específica de cada sistema.
    El código cliente solo conoce SistemaEnvio — los detalles quedan encapsulados.

Clases:
    SistemaEnvio: Interfaz objetivo unificada (ABC).
    SistemaLegadoDHL: Sistema DHL existente con interfaz incompatible (adaptado).
    SistemaLegadoFedEx: Sistema FedEx existente con interfaz incompatible (adaptado).
    AdaptadorDHL: Adapter que traduce SistemaEnvio → SistemaLegadoDHL.
    AdaptadorFedEx: Adapter que traduce SistemaEnvio → SistemaLegadoFedEx.

Uso:
    # El cliente solo conoce SistemaEnvio — no sabe qué transportista usa
    def cotizar_envio(sistema: SistemaEnvio, peso_kg, destino):
        costo = sistema.calcular_costo(peso_kg, destino)
        dias  = sistema.estimar_dias(destino)
        print(f"Costo: ${costo:.2f} | Entrega estimada: {dias} días")

    cotizar_envio(AdaptadorDHL(),   2.5, "Buenos Aires")
    cotizar_envio(AdaptadorFedEx(), 2.5, "1428")
"""

import unicodedata
from patrones._numeros import es_finito
from abc import ABC, abstractmethod


def _normalizar_ciudad(ciudad: str) -> str:
    """Normaliza un nombre de ciudad: minúsculas, sin espacios extremos ni tildes.

    Args:
        ciudad (str): Nombre de ciudad tal como lo escribió el cliente.

    Returns:
        str: Nombre normalizado (por ejemplo, "  Córdoba " → "cordoba").
    """
    descompuesto = unicodedata.normalize("NFKD", ciudad.strip().lower())
    return "".join(c for c in descompuesto if not unicodedata.combining(c))


# =============================================================================
# INTERFAZ OBJETIVO: lo que el cliente (tienda) espera
# =============================================================================

class SistemaEnvio(ABC):
    """Interfaz unificada para todos los sistemas de envío de la tienda.

    Define el contrato que todos los adaptadores deben cumplir.
    El código cliente (checkout, carrito) solo trabaja contra esta interfaz
    y desconoce qué transportista concreto está siendo utilizado.
    """

    @abstractmethod
    def calcular_costo(self, peso_kg: float, destino: str) -> float:
        """Calcula el costo del envío en dólares.

        Args:
            peso_kg (float): Peso del paquete en kilogramos.
            destino (str): Ciudad o código postal de destino.

        Returns:
            float: Costo del envío en dólares.
        """
        pass

    @abstractmethod
    def estimar_dias(self, destino: str) -> int:
        """Estima los días hábiles para la entrega.

        Args:
            destino (str): Ciudad o código postal de destino.

        Returns:
            int: Cantidad de días hábiles estimados para la entrega.
        """
        pass

    @abstractmethod
    def crear_envio(self, pedido_id: str, destino: str) -> str:
        """Registra el envío y devuelve el número de seguimiento.

        Args:
            pedido_id (str): Identificador único del pedido en la tienda.
            destino (str): Ciudad o código postal de destino.

        Returns:
            str: Número o código de seguimiento del envío.
        """
        pass


# =============================================================================
# SISTEMAS LEGADOS (ADAPTADOS): interfaces incompatibles preexistentes
# =============================================================================

class SistemaLegadoDHL:
    """Sistema DHL con su API propietaria incompatible con la interfaz de la tienda.

    Este es el sistema "adaptado" (Adaptee). Usa gramos en lugar de kilogramos,
    devuelve tiempos de entrega como cadenas de texto ("2-3 días") y tiene
    nombres de métodos específicos de DHL.

    En un proyecto real, esta clase representaría un SDK o librería de terceros
    que no podemos (o no queremos) modificar.
    """

    def calcular_tarifa_dhl(self, gramos: int, ciudad_destino: str) -> float:
        """Calcula la tarifa DHL en base a gramos y ciudad de destino.

        Args:
            gramos (int): Peso del paquete en gramos.
            ciudad_destino (str): Ciudad de destino del envío.

        Returns:
            float: Tarifa de envío DHL en dólares.
        """
        # Tarifa simulada: $0.008 por gramo + $3.00 base
        return round(3.00 + gramos * 0.008, 2)

    def tiempo_entrega_dhl(self, ciudad: str) -> str:
        """Devuelve el tiempo de entrega como cadena de texto.

        Args:
            ciudad (str): Ciudad de destino.

        Returns:
            str: Tiempo estimado en formato "X-Y días hábiles".
        """
        # Simulación: ciudades capitales 2-3 días, resto 4-5 días
        ciudades_principales = ["buenos aires", "cordoba", "rosario", "mendoza"]
        if _normalizar_ciudad(ciudad) in ciudades_principales:
            return "2-3 días hábiles"
        return "4-5 días hábiles"

    def generar_guia(self, id_orden: str, ciudad: str) -> str:
        """Genera y registra la guía de envío DHL.

        Args:
            id_orden (str): Número de orden de la tienda.
            ciudad (str): Ciudad de destino.

        Returns:
            str: Número de guía DHL generado.
        """
        guia = f"DHL-{id_orden.upper()}-{ciudad[:3].upper()}"
        print(f"  [DHL] Guía generada: {guia} con destino a {ciudad}")
        return guia


class SistemaLegadoFedEx:
    """Sistema FedEx con su API propietaria incompatible con la interfaz de la tienda.

    Este es el segundo "adaptado" (Adaptee). Usa libras en lugar de kilogramos,
    trabaja con códigos postales numéricos de 4 dígitos, y devuelve los días
    como enteros directamente.

    En un proyecto real, representaría otro SDK de terceros con su propia forma
    de trabajar, completamente diferente a DHL.
    """

    def obtener_precio_fedex(self, libras: float, codigo_postal: str) -> float:
        """Calcula el precio de envío FedEx en base a libras y código postal.

        Args:
            libras (float): Peso del paquete en libras.
            codigo_postal (str): Código postal de 4 dígitos del destino.

        Returns:
            float: Precio de envío FedEx en dólares.
        """
        # Tarifa simulada: $1.20 por libra + $2.50 base
        return round(2.50 + libras * 1.20, 2)

    def dias_habiles(self, codigo_postal: str) -> int:
        """Devuelve la cantidad de días hábiles para la entrega.

        Args:
            codigo_postal (str): Código postal de destino (4 dígitos).

        Returns:
            int: Días hábiles estimados para la entrega.
        """
        # Simulación: códigos que empiezan con 1 son zona rápida (2 días)
        if codigo_postal.startswith("1"):
            return 2
        return 3

    def registrar_paquete(self, num_orden: str, codigo_postal: str) -> str:
        """Registra el paquete en el sistema FedEx y devuelve el tracking.

        Args:
            num_orden (str): Número de orden de la tienda.
            codigo_postal (str): Código postal de destino.

        Returns:
            str: Número de tracking FedEx.
        """
        tracking = f"FX{num_orden.upper()}{codigo_postal}"
        print(f"  [FedEx] Tracking generado: {tracking} | CP destino: {codigo_postal}")
        return tracking


# =============================================================================
# ADAPTADORES: traducen la interfaz objetivo a la API de cada sistema legado
# =============================================================================

class AdaptadorDHL(SistemaEnvio):
    """Adapter que hace compatible SistemaLegadoDHL con la interfaz SistemaEnvio.

    Traduce las llamadas de la interfaz unificada a las llamadas específicas
    de DHL, realizando conversiones de unidades donde es necesario:
    - Kilogramos → Gramos (*1000)
    - "2-3 días hábiles" → 2 (extrae el primer número del string)

    Attributes:
        _dhl (SistemaLegadoDHL): Instancia del sistema DHL legado.
    """

    def __init__(self) -> None:
        """Inicializa el adaptador creando la instancia del sistema DHL."""
        self._dhl = SistemaLegadoDHL()

    def calcular_costo(self, peso_kg: float, destino: str) -> float:
        """Traduce peso en kg a gramos y delega al sistema DHL.

        Args:
            peso_kg (float): Peso del paquete en kilogramos.
            destino (str): Ciudad de destino.

        Returns:
            float: Costo del envío según tarifa DHL.

        Raises:
            TypeError: Si el peso no es int o float, o es bool.
            ValueError: Si el peso no es positivo o el peso/conversión/tarifa
                excede el rango finito representable como float.
        """
        if not isinstance(peso_kg, (int, float)) or isinstance(peso_kg, bool):
            raise TypeError("El peso debe ser un número")
        if not es_finito(peso_kg) or peso_kg <= 0:
            raise ValueError("El peso debe ser finito y mayor que cero")
        # round() en vez de int(): int() trunca y subfactura (1.9 g → 1 g)
        gramos_sin_redondear = peso_kg * 1000
        if not es_finito(gramos_sin_redondear):
            raise ValueError("La conversión del peso excede el rango numérico")
        gramos = int(round(gramos_sin_redondear))
        return self._dhl.calcular_tarifa_dhl(gramos, destino)

    def estimar_dias(self, destino: str) -> int:
        """Obtiene el tiempo de DHL y extrae el mínimo de días como entero.

        Args:
            destino (str): Ciudad de destino.

        Returns:
            int: Estimado mínimo de días hábiles para la entrega.
        """
        tiempo_str = self._dhl.tiempo_entrega_dhl(destino)
        # Parsea "2-3 días hábiles" → 2
        return int(tiempo_str.split("-")[0])

    def crear_envio(self, pedido_id: str, destino: str) -> str:
        """Delega directamente la creación de guía al sistema DHL.

        Args:
            pedido_id (str): Identificador del pedido.
            destino (str): Ciudad de destino.

        Returns:
            str: Número de guía DHL.
        """
        return self._dhl.generar_guia(pedido_id, destino)


class AdaptadorFedEx(SistemaEnvio):
    """Adapter que hace compatible SistemaLegadoFedEx con la interfaz SistemaEnvio.

    Traduce las llamadas de la interfaz unificada a las llamadas específicas
    de FedEx, realizando conversiones de unidades donde es necesario:
    - Kilogramos → Libras (*2.205)
    - La ciudad/destino se interpreta como código postal para FedEx

    Attributes:
        _fedex (SistemaLegadoFedEx): Instancia del sistema FedEx legado.
    """

    KG_A_LIBRAS = 2.205

    def __init__(self) -> None:
        """Inicializa el adaptador creando la instancia del sistema FedEx."""
        self._fedex = SistemaLegadoFedEx()

    def calcular_costo(self, peso_kg: float, destino: str) -> float:
        """Traduce peso en kg a libras y delega al sistema FedEx.

        Args:
            peso_kg (float): Peso del paquete en kilogramos.
            destino (str): Código postal de destino (FedEx usa códigos postales).

        Returns:
            float: Costo del envío según tarifa FedEx.

        Raises:
            TypeError: Si el peso no es int o float, o es bool.
            ValueError: Si el peso no es positivo o el peso/conversión/tarifa
                excede el rango finito representable como float.
        """
        if not isinstance(peso_kg, (int, float)) or isinstance(peso_kg, bool):
            raise TypeError("El peso debe ser un número")
        if not es_finito(peso_kg) or peso_kg <= 0:
            raise ValueError("El peso debe ser finito y mayor que cero")
        libras = round(peso_kg * self.KG_A_LIBRAS, 3)
        if not es_finito(libras):
            raise ValueError("La conversión del peso excede el rango numérico")
        costo = self._fedex.obtener_precio_fedex(libras, destino)
        if not es_finito(costo):
            raise ValueError("La tarifa excede el rango numérico")
        return costo

    def estimar_dias(self, destino: str) -> int:
        """Delega directamente la estimación de días al sistema FedEx.

        Args:
            destino (str): Código postal de destino.

        Returns:
            int: Días hábiles estimados para la entrega.
        """
        return self._fedex.dias_habiles(destino)

    def crear_envio(self, pedido_id: str, destino: str) -> str:
        """Delega el registro del paquete al sistema FedEx.

        Args:
            pedido_id (str): Identificador del pedido.
            destino (str): Código postal de destino.

        Returns:
            str: Número de tracking FedEx.
        """
        return self._fedex.registrar_paquete(pedido_id, destino)
