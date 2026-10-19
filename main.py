#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demostración de Patrones de Diseño en Python - Sistema de Comercio Electrónico.

Este archivo es el punto de entrada del programa. Ejecuta demostraciones
de los 8 patrones de diseño implementados en el paquete 'patrones/', en el
mismo orden y con la misma numeración que las secciones de la salida:

    1. Singleton  - Una sola conexión a base de datos.        (Creacional)
    2. Factory Method - Subclases deciden qué producto crear. (Creacional)
    3. Observer   - Notificaciones a clientes suscritos.      (Comportamiento)
    4. Strategy   - Formas de pago intercambiables.           (Comportamiento)
    5. Builder    - Construcción paso a paso de pedidos.      (Creacional)
    6. Decorator  - Servicios opcionales sobre productos.     (Estructural)
    7. Adapter    - Sistemas de envío con APIs incompatibles. (Estructural)
    8. Chain of Responsibility - Validación de pedidos.       (Comportamiento)

Ejecución:
    python main.py

Cada sección está claramente separada para que el estudiante pueda
identificar qué patrón se está demostrando y cómo se usa.
"""

# Importaciones organizadas en 3 bloques por categoría GoF (HU-040)

# Patrones creacionales
from patrones.creacionales.singleton import DatabaseConnection
from patrones.creacionales.factory import CreadorProducto, CreadorLibro, CreadorElectronico
from patrones.creacionales.builder import (
    PedidoEstandarBuilder, PedidoExpressBuilder, DirectorPedido,
)

# Patrones estructurales
from patrones.estructurales.decorator import (
    ProductoConcreto, EnvolturaRegalo, SeguroProducto, GarantiaExtendida,
)
from patrones.estructurales.adapter import SistemaEnvio, AdaptadorDHL, AdaptadorFedEx

# Patrones de comportamiento
from patrones.comportamiento.observer import Cliente, Tienda
from patrones.comportamiento.strategy import CarritoCompra, PagoTarjeta, PagoEfectivo, PagoPayPal
from patrones.comportamiento.chain import (
    ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude,
)


def main() -> None:
    """Función principal que demuestra todos los patrones de diseño."""
    print("=" * 50)
    print("DEMOSTRACIÓN DE PATRONES DE DISEÑO EN PYTHON")
    print("=" * 50)
    print()

    # ============================================
    # 1. PATRÓN SINGLETON - Conexión a BD
    # ============================================
    # Demuestra que get_instance() siempre retorna el MISMO objeto.
    # No importa cuántas veces se llame, solo existe una conexión.
    print(">>> 1. PATRÓN SINGLETON <<<")
    db1 = DatabaseConnection.get_instance()
    db2 = DatabaseConnection.get_instance()

    # 'is' compara identidad (misma posición en memoria), no igualdad de valor
    print(f"¿Son la misma instancia? {db1 is db2}")
    db1.query("SELECT * FROM usuarios")
    print()

    # ============================================
    # 2. PATRÓN FACTORY METHOD - Crear productos
    # ============================================
    # Cada creador concreto (subclase de CreadorProducto) decide qué clase
    # instanciar en su factory method crear_producto(). registrar_producto()
    # es código del creador abstracto: usa el factory method y muestra el
    # producto sin saber si es un Libro o un Electronico.
    print(">>> 2. PATRÓN FACTORY METHOD <<<")
    creador_garcia_marquez: CreadorProducto = CreadorLibro("Gabriel García Márquez")
    creador_cervantes: CreadorProducto = CreadorLibro("Miguel de Cervantes")
    creador_garantia_24: CreadorProducto = CreadorElectronico(24)
    creador_garantia_12: CreadorProducto = CreadorElectronico(12)

    libro1 = creador_garcia_marquez.registrar_producto("Cien Años de Soledad", 25.99)
    libro2 = creador_cervantes.registrar_producto("Don Quijote", 19.99)
    laptop = creador_garantia_24.registrar_producto("Laptop HP", 899.99)
    telefono = creador_garantia_12.registrar_producto("iPhone 15", 999.99)

    # Los datos se leen mediante propiedades (@property), no con getters get_*()
    print(f"Acceso por propiedades -> nombre: {libro1.nombre} | precio: ${libro1.precio:.2f}")
    print()

    # ============================================
    # 3. PATRÓN OBSERVER - Sistema de notificaciones
    # ============================================
    # Los clientes se suscriben a la tienda. Cuando hay una oferta,
    # todos los suscritos reciben la notificación automáticamente.
    print(">>> 3. PATRÓN OBSERVER <<<")
    tienda = Tienda("TechStore")

    cliente1 = Cliente("Juan Pérez")
    cliente2 = Cliente("María López")
    cliente3 = Cliente("Carlos Gómez")

    # Suscribir 3 clientes -> los 3 recibirán la primera oferta
    tienda.suscribir(cliente1)
    tienda.suscribir(cliente2)
    tienda.suscribir(cliente3)

    tienda.nueva_oferta("50% descuento en laptops")

    # Desuscribir a María -> solo Juan y Carlos recibirán la siguiente oferta
    print()
    tienda.desuscribir(cliente2)
    print()

    tienda.nueva_oferta("Black Friday: Todo al 70% de descuento")
    print()

    # ============================================
    # 4. PATRÓN STRATEGY - Diferentes formas de pago
    # ============================================
    # Cada carrito usa una estrategia de pago diferente.
    # El CarritoCompra no sabe cómo funciona cada pago internamente;
    # solo llama a pagar() y la estrategia se encarga del resto.
    print(">>> 4. PATRÓN STRATEGY <<<")

    # Carrito 1 - Pago con tarjeta (muestra solo últimos 4 dígitos)
    carrito1 = CarritoCompra()
    carrito1.agregar_producto(libro1)
    carrito1.agregar_producto(laptop)
    carrito1.set_estrategia_pago(PagoTarjeta("4532-1234-5678-9012"))
    carrito1.checkout()

    # Carrito 2 - Pago en efectivo (aplica 5% de descuento automáticamente)
    carrito2 = CarritoCompra()
    carrito2.agregar_producto(telefono)
    carrito2.agregar_producto(libro2)
    carrito2.set_estrategia_pago(PagoEfectivo())
    carrito2.checkout()

    # Carrito 3 - Pago con PayPal (usa email como identificador)
    carrito3 = CarritoCompra()
    carrito3.agregar_producto(laptop)
    carrito3.agregar_producto(telefono)
    carrito3.set_estrategia_pago(PagoPayPal("usuario@email.com"))
    carrito3.checkout()

    # ============================================
    # 5. PATRÓN BUILDER - Construcción de pedidos
    # ============================================
    # El Builder construye un objeto complejo (Pedido) paso a paso.
    # El Director orquesta la secuencia; el cliente elige el tipo de builder.
    # Ventaja: sin un constructor de 10 parámetros ni combinaciones de subclases.
    print(">>> 5. PATRÓN BUILDER <<<")

    # Pedido estándar simple: el director ejecuta solo los pasos necesarios
    print("-- Pedido estándar simple --")
    builder_estandar = PedidoEstandarBuilder()
    director = DirectorPedido(builder_estandar)
    pedido_simple = director.construir_pedido_simple(
        [libro1, laptop],
        "Av. Corrientes 1234, Buenos Aires"
    )
    pedido_simple.mostrar_resumen()
    print()

    # Pedido de regalo express: el director agrega envoltura + seguro automáticamente
    print("-- Pedido de regalo express --")
    builder_express = PedidoExpressBuilder()
    director.set_builder(builder_express)
    pedido_regalo = director.construir_pedido_regalo(
        [telefono],
        "Calle Falsa 742, Córdoba",
        "¡Feliz cumpleaños! Te mereces lo mejor."
    )
    pedido_regalo.mostrar_resumen()
    print()

    # ============================================
    # 6. PATRÓN DECORATOR - Servicios opcionales
    # ============================================
    # El Decorator agrega responsabilidades a un objeto dinámicamente.
    # Cada decorador "envuelve" al anterior y apila descripción y precio.
    # Ventaja: sin subclasificar cada combinación posible de servicios.
    print(">>> 6. PATRÓN DECORATOR <<<")

    # Producto base sin decoradores
    producto_base = ProductoConcreto("Laptop HP", 899.99)
    print(f"Base:               {producto_base.descripcion}")
    print(f"                    Precio: ${producto_base.precio:.2f}")

    # Agregar envoltura de regalo (+$5.00)
    con_envoltura = EnvolturaRegalo(producto_base)
    print(f"+ EnvolturaRegalo:  {con_envoltura.descripcion}")
    print(f"                    Precio: ${con_envoltura.precio:.2f}")

    # Agregar seguro sobre el precio ya con envoltura (+2%)
    con_seguro = SeguroProducto(con_envoltura)
    print(f"+ SeguroProducto:   {con_seguro.descripcion}")
    print(f"                    Precio: ${con_seguro.precio:.2f}")

    # Agregar garantía extendida de 2 años (+$29.99)
    con_garantia = GarantiaExtendida(con_seguro)
    print(f"+ GarantiaExtendida:{con_garantia.descripcion}")
    print(f"                    Precio: ${con_garantia.precio:.2f}")
    print()

    # ============================================
    # 7. PATRÓN ADAPTER - Sistemas de envío
    # ============================================
    # DHL y FedEx tienen APIs propietarias incompatibles entre sí.
    # El Adapter traduce ambas a una interfaz unificada (SistemaEnvio).
    # El código cliente llama siempre a calcular_costo/estimar_dias/crear_envio
    # sin importar qué transportista está detrás.
    print(">>> 7. PATRÓN ADAPTER <<<")

    # Función cliente que trabaja solo contra la interfaz SistemaEnvio
    def cotizar_y_crear_envio(sistema: SistemaEnvio, nombre_sistema: str, peso_kg: float,
                              destino: str, pedido_id: str) -> None:
        """Demuestra que el cliente usa la misma interfaz para cualquier transportista.

        Args:
            sistema: Cualquier adaptador que implemente SistemaEnvio.
            nombre_sistema: Etiqueta del transportista para la salida.
            peso_kg: Peso del paquete en kilogramos.
            destino: Ciudad (DHL) o código postal (FedEx), según HU-019/HU-020.
            pedido_id: Identificador del pedido en la tienda.
        """
        costo = sistema.calcular_costo(peso_kg, destino)
        dias = sistema.estimar_dias(destino)
        print(f"  [{nombre_sistema}] Costo: ${costo:.2f} | Días estimados: {dias}")
        guia = sistema.crear_envio(pedido_id, destino)
        print(f"  [{nombre_sistema}] Seguimiento: {guia}")

    print("-- Envio via DHL (adaptador convierte kg->gramos, parsea 'X-Y dias') --")
    adaptador_dhl = AdaptadorDHL()
    cotizar_y_crear_envio(adaptador_dhl, "DHL", 2.5, "Buenos Aires", "PED-001")
    print()

    print("-- Envio via FedEx (adaptador convierte kg->libras, usa codigo postal) --")
    adaptador_fedex = AdaptadorFedEx()
    cotizar_y_crear_envio(adaptador_fedex, "FedEx", 2.5, "1428", "PED-001")
    print()

    # ============================================
    # 8. PATRÓN CHAIN OF RESPONSIBILITY - Validación
    # ============================================
    # La solicitud (pedido) pasa por una cadena de validadores.
    # Cada uno decide si aprueba y pasa al siguiente, o rechaza y detiene la cadena.
    # Ventaja: cada regla es independiente, reutilizable y la cadena es configurable.
    print(">>> 8. PATRÓN CHAIN OF RESPONSIBILITY <<<")

    # Construir la cadena: Stock → Pago → Dirección → Antifraude
    validador_stock = ValidadorStock()
    validador_stock \
        .set_siguiente(ValidadorPago()) \
        .set_siguiente(ValidadorDireccion()) \
        .set_siguiente(ValidadorFraude())

    # Caso 1: pedido válido — debe pasar toda la cadena
    pedido_valido = {
        "productos": ["Laptop HP", "iPhone 15"],
        "metodo_pago": "tarjeta",
        "direccion_envio": "Av. Santa Fe 3456, Buenos Aires",
        "total": 1899.98,
    }
    print("-- Pedido válido --")
    resultado = validador_stock.validar(pedido_valido)
    print(f"  Resultado: {'APROBADO' if resultado else 'RECHAZADO'}")
    print()

    # Caso 2: pedido con método de pago inválido — debe fallar en ValidadorPago
    pedido_pago_invalido = {
        "productos": ["Libro"],
        "metodo_pago": "bitcoin",
        "direccion_envio": "Calle Falsa 742, Córdoba",
        "total": 25.99,
    }
    print("-- Pedido con método de pago no habilitado --")
    resultado2 = validador_stock.validar(pedido_pago_invalido)
    print(f"  Resultado: {'APROBADO' if resultado2 else 'RECHAZADO'}")
    print()

    # Caso 3: pedido con monto sospechoso — debe fallar en ValidadorFraude
    pedido_fraude = {
        "productos": ["Producto caro"],
        "metodo_pago": "paypal",
        "direccion_envio": "Av. Corrientes 9999, Buenos Aires",
        "total": 9999.99,
    }
    print("-- Pedido con monto que supera el límite antifraude --")
    resultado3 = validador_stock.validar(pedido_fraude)
    print(f"  Resultado: {'APROBADO' if resultado3 else 'RECHAZADO'}")
    print()

    print("=" * 50)
    print("FIN DE LA DEMOSTRACIÓN")
    print("=" * 50)


# Este bloque asegura que main() solo se ejecute cuando el archivo
# se ejecuta directamente (python main.py), no cuando se importa como módulo.
if __name__ == "__main__":
    main()
