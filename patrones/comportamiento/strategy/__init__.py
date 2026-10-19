"""Subpaquete: Patrón Strategy (Comportamiento)."""
from patrones.comportamiento.strategy.estrategia_pago import (
    EstrategiaPago, PagoTarjeta, PagoEfectivo, PagoPayPal,
)
from patrones.comportamiento.strategy.carrito_compra import CarritoCompra
__all__ = ["EstrategiaPago", "PagoTarjeta", "PagoEfectivo", "PagoPayPal", "CarritoCompra"]
