"""Subpaquete: Patrón Adapter (Estructural)."""
from patrones.estructurales.adapter.adaptador_envio import (
    SistemaEnvio,
    SistemaLegadoDHL,
    SistemaLegadoFedEx,
    AdaptadorDHL,
    AdaptadorFedEx,
)
__all__ = [
    "SistemaEnvio",
    "SistemaLegadoDHL",
    "SistemaLegadoFedEx",
    "AdaptadorDHL",
    "AdaptadorFedEx",
]
