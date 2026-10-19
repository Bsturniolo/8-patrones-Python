"""Subpaquete: Patrón Factory Method (Creacional)."""
from patrones.creacionales.factory.producto import Producto, Libro, Electronico
from patrones.creacionales.factory.creador_producto import (
    CreadorProducto,
    CreadorLibro,
    CreadorElectronico,
)
__all__ = [
    "Producto",
    "Libro",
    "Electronico",
    "CreadorProducto",
    "CreadorLibro",
    "CreadorElectronico",
]
