"""
Módulo que implementa el patrón Chain of Responsibility para validar pedidos.

El patrón Chain of Responsibility (Cadena de Responsabilidad) permite pasar
solicitudes a lo largo de una cadena de manejadores. Cada manejador decide si
procesa la solicitud o la pasa al siguiente eslabón de la cadena.

Analogía: es como un proceso de aprobación de crédito. Tu solicitud primero pasa
por el analista de riesgo, luego por el gerente de sucursal, luego por gerencia
central. Cada uno puede aprobar, rechazar o escalar. Si uno rechaza, los demás
no necesitan revisar.

Problema que resuelve:
    Validar un pedido requiere múltiples controles (stock, pago, dirección,
    antifraude). Sin Chain of Responsibility, el código de checkout tendría un
    método largo con ifs anidados acoplados a cada validación. Con este patrón,
    cada validación es una clase independiente y reutilizable, y la cadena se
    configura dinámicamente en tiempo de ejecución.

Clases:
    ValidadorPedido: Interfaz abstracta del manejador (ABC).
    ValidadorStock: Verifica que el pedido contenga al menos un producto.
    ValidadorPago: Verifica que el método de pago sea aceptado por la tienda.
    ValidadorDireccion: Verifica que la dirección de envío sea válida.
    ValidadorFraude: Verifica que el monto no supere el límite antifraude.

El pedido se representa como un dict con las siguientes claves:
    - "productos" (list): Lista de productos en el pedido.
    - "metodo_pago" (str): Método de pago utilizado ("tarjeta", "efectivo", "paypal").
    - "direccion_envio" (str): Dirección de entrega del pedido.
    - "total" (float): Monto total del pedido.

Uso:
    # Construir la cadena enlazando los validadores
    validador_stock = ValidadorStock()
    validador_pago  = ValidadorPago()
    validador_dir   = ValidadorDireccion()
    validador_fraude= ValidadorFraude()

    validador_stock \\
        .set_siguiente(validador_pago) \\
        .set_siguiente(validador_dir) \\
        .set_siguiente(validador_fraude)

    pedido = {
        "productos": ["Laptop", "Libro"],
        "metodo_pago": "tarjeta",
        "direccion_envio": "Av. Corrientes 1234, Buenos Aires",
        "total": 950.00,
    }
    aprobado = validador_stock.validar(pedido)
    print("Pedido aprobado" if aprobado else "Pedido rechazado")
"""

from abc import ABC, abstractmethod
from patrones._numeros import es_finito
from typing import Dict, Any, Optional


class ValidadorPedido(ABC):
    """Interfaz abstracta del manejador en la cadena de responsabilidad.

    Define la estructura base para todos los validadores: cada uno guarda
    referencia al siguiente en la cadena y delega a él si su validación pasa.
    El método set_siguiente() devuelve el validador recibido, permitiendo
    encadenar llamadas fluidas: a.set_siguiente(b).set_siguiente(c).

    Attributes:
        _siguiente (ValidadorPedido): El siguiente validador en la cadena, o None.
    """

    def __init__(self) -> None:
        """Inicializa el validador sin sucesor en la cadena."""
        self._siguiente: Optional["ValidadorPedido"] = None

    def set_siguiente(self, validador: "ValidadorPedido") -> "ValidadorPedido":
        """Establece el siguiente validador en la cadena y lo devuelve.

        Devolver el validador recibido permite encadenar llamadas:
            a.set_siguiente(b).set_siguiente(c).set_siguiente(d)

        Args:
            validador (ValidadorPedido): El siguiente manejador en la cadena.

        Returns:
            ValidadorPedido: El mismo validador recibido (para encadenamiento fluido).

        Raises:
            ValueError: Si enlazarlo formaría un ciclo (la validación no terminaría nunca).
        """
        actual = validador
        while actual is not None:
            if actual is self:
                raise ValueError("No se puede enlazar el validador: formaría un ciclo")
            actual = actual._siguiente
        self._siguiente = validador
        return validador

    def _pasar_al_siguiente(self, pedido: Dict[str, Any]) -> bool:
        """Pasa el pedido al siguiente validador si existe; si no, aprueba.

        Este método es utilizado internamente por las subclases al final de
        una validación exitosa. Si no hay siguiente en la cadena, significa
        que todos los validadores pasaron y el pedido está aprobado.

        Args:
            pedido (dict): Datos del pedido a validar.

        Returns:
            bool: True si el resto de la cadena aprueba (o si no hay más), False si no.
        """
        if self._siguiente:
            return self._siguiente.validar(pedido)
        return True

    @abstractmethod
    def validar(self, pedido: Dict[str, Any]) -> bool:
        """Valida el pedido y decide si continúa o detiene la cadena.

        Cada subclase implementa su regla de validación. Si la validación falla,
        debe imprimir el motivo y devolver False sin llamar al siguiente.
        Si pasa, debe llamar a self._pasar_al_siguiente(pedido).

        Args:
            pedido (dict): Diccionario con datos del pedido:
                - "productos" (list): Productos en el pedido.
                - "metodo_pago" (str): Método de pago.
                - "direccion_envio" (str): Dirección de entrega.
                - "total" (float): Monto total del pedido.

        Returns:
            bool: True si el pedido pasa esta validación y todas las siguientes.
        """
        pass


class ValidadorStock(ValidadorPedido):
    """Valida que el pedido contenga al menos un producto.

    Es el primer eslabón recomendado de la cadena, ya que un pedido sin
    productos no tiene sentido procesar con los demás validadores.
    """

    def validar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica que la lista de productos no esté vacía.

        Args:
            pedido (dict): Datos del pedido a validar.

        Returns:
            bool: True si hay una lista no vacía; False si el tipo es inválido
                o el pedido está vacío.
        """
        if not isinstance(pedido, dict):
            print("  [Pedido] RECHAZADO: se requiere un diccionario.")
            return False
        productos = pedido.get("productos") or []
        if not isinstance(productos, list) or not productos:
            print("  [Stock] RECHAZADO: el pedido no contiene productos.")
            return False
        print(f"  [Stock] OK: {len(productos)} producto(s) en el pedido.")
        return self._pasar_al_siguiente(pedido)


class ValidadorPago(ValidadorPedido):
    """Valida que el método de pago sea aceptado por la tienda.

    Los métodos aceptados son: "tarjeta", "efectivo" y "paypal".
    La comparación es insensible a mayúsculas.
    """

    METODOS_ACEPTADOS = {"tarjeta", "efectivo", "paypal"}

    def validar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica que el método de pago esté en la lista de aceptados.

        Args:
            pedido (dict): Datos del pedido a validar.

        Returns:
            bool: True si el método es aceptado; False si es inválido o falta.
        """
        if not isinstance(pedido, dict):
            print("  [Pedido] RECHAZADO: se requiere un diccionario.")
            return False
        metodo = pedido.get("metodo_pago")
        metodo = metodo.strip().lower() if isinstance(metodo, str) else ""
        if metodo not in self.METODOS_ACEPTADOS:
            # sorted(): un set no garantiza orden entre ejecuciones
            print(f"  [Pago] RECHAZADO: método '{metodo}' no está habilitado. "
                  f"Aceptados: {', '.join(sorted(self.METODOS_ACEPTADOS))}.")
            return False
        print(f"  [Pago] OK: método '{metodo}' aceptado.")
        return self._pasar_al_siguiente(pedido)


class ValidadorDireccion(ValidadorPedido):
    """Valida que la dirección de envío esté completa y sea suficientemente larga.

    Requiere que la dirección tenga al menos 10 caracteres (sin espacios
    al inicio o final), lo que filtra direcciones incompletas o vacías.
    """

    LONGITUD_MINIMA = 10

    def validar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica que la dirección de envío cumpla con la longitud mínima.

        Args:
            pedido (dict): Datos del pedido a validar.

        Returns:
            bool: True si la dirección es válida; False si está vacía o es muy corta.
        """
        if not isinstance(pedido, dict):
            print("  [Pedido] RECHAZADO: se requiere un diccionario.")
            return False
        direccion = pedido.get("direccion_envio")
        direccion = direccion.strip() if isinstance(direccion, str) else ""
        if len(direccion) < self.LONGITUD_MINIMA:
            print(f"  [Dirección] RECHAZADO: dirección incompleta "
                  f"(mínimo {self.LONGITUD_MINIMA} caracteres).")
            return False
        print(f"  [Dirección] OK: '{direccion}'.")
        return self._pasar_al_siguiente(pedido)


class ValidadorFraude(ValidadorPedido):
    """Valida que el monto total del pedido no supere el límite antifraude.

    Pedidos con montos excesivamente altos son señal de posible fraude o
    error. El límite predeterminado es $5.000. Este validador se recomienda
    como último eslabón de la cadena.
    """

    MONTO_MAXIMO = 5000.00

    def validar(self, pedido: Dict[str, Any]) -> bool:
        """Verifica que el total del pedido no supere el límite antifraude.

        Args:
            pedido (dict): Datos del pedido a validar.

        Returns:
            bool: True si el monto es aceptable; False si no es numérico,
                no es finito, es negativo o supera el límite.
                Un total ausente equivale a cero según HU-039.
        """
        if not isinstance(pedido, dict):
            print("  [Pedido] RECHAZADO: se requiere un diccionario.")
            return False
        total = pedido.get("total", 0)
        # bool es subclase de int en Python: se excluye explícitamente
        if not isinstance(total, (int, float)) or isinstance(total, bool):
            print(f"  [Antifraude] RECHAZADO: total inválido ({total!r}).")
            return False
        if not es_finito(total):
            print("  [Antifraude] RECHAZADO: el total debe ser finito.")
            return False
        if total < 0:
            print(f"  [Antifraude] RECHAZADO: total negativo ${total:.2f}.")
            return False
        if total > self.MONTO_MAXIMO:
            print(f"  [Antifraude] RECHAZADO: total ${total:.2f} supera el límite "
                  f"de ${self.MONTO_MAXIMO:.2f}.")
            return False
        print(f"  [Antifraude] OK: total ${total:.2f} dentro del límite permitido.")
        return self._pasar_al_siguiente(pedido)
