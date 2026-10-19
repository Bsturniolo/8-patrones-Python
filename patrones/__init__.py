"""
Paquete principal de patrones de diseño.

Organizado en tres categorías GoF, cada una con sus subpaquetes:

Patrones Creacionales  (patrones.creacionales.*):
    - creacionales.singleton  → DatabaseConnection
    - creacionales.factory    → Producto, Libro, Electronico, Creador* (Factory Method)
    - creacionales.builder    → Pedido, PedidoBuilder, Pedido*Builder, DirectorPedido

Patrones Estructurales  (patrones.estructurales.*):
    - estructurales.decorator → ComponenteProducto, ProductoConcreto, Decorador*, servicios
    - estructurales.adapter   → SistemaEnvio, SistemaLegado*, Adaptador*

Patrones de Comportamiento  (patrones.comportamiento.*):
    - comportamiento.observer → Observer, Cliente, Tienda
    - comportamiento.strategy → EstrategiaPago, Pago*, CarritoCompra
    - comportamiento.chain    → ValidadorPedido, Validador*
"""
