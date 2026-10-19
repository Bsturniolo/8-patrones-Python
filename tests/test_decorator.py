"""Tests del patrón Decorator (servicios opcionales sobre productos)."""

import unittest

from patrones.estructurales.decorator import (
    ComponenteProducto,
    EnvolturaRegalo,
    GarantiaExtendida,
    ProductoConcreto,
    SeguroProducto,
)


class TestDecoradores(unittest.TestCase):
    """Verifica el apilamiento de precio y descripción."""

    def test_producto_base_sin_decorar(self) -> None:
        producto = ProductoConcreto("X", 10.0)
        self.assertEqual(producto.descripcion, "X")
        self.assertEqual(producto.precio, 10.0)

    def test_envoltura_suma_costo_fijo(self) -> None:
        self.assertEqual(EnvolturaRegalo(ProductoConcreto("X", 10.0)).precio, 15.0)

    def test_seguro_se_calcula_sobre_el_precio_ya_decorado(self) -> None:
        producto = SeguroProducto(EnvolturaRegalo(ProductoConcreto("X", 95.0)))
        self.assertEqual(producto.precio, 102.0)  # (95 + 5) * 1.02

    def test_apilado_completo_coincide_con_el_ejemplo_documentado(self) -> None:
        producto = GarantiaExtendida(
            SeguroProducto(EnvolturaRegalo(ProductoConcreto("Laptop HP", 899.99)))
        )
        self.assertEqual(producto.precio, 953.08)
        self.assertEqual(
            producto.descripcion,
            "Laptop HP + Envoltura de regalo + Seguro del producto"
            " + Garantía extendida (2 años)",
        )

    def test_docstring_del_modulo_documenta_el_precio_real(self) -> None:
        import patrones.estructurales.decorator.decorador_producto as modulo
        self.assertIn("953.08", modulo.__doc__)
        self.assertNotIn("953.88", modulo.__doc__)

    def test_un_decorador_puede_aplicarse_dos_veces(self) -> None:
        doble = EnvolturaRegalo(EnvolturaRegalo(ProductoConcreto("X", 10.0)))
        self.assertEqual(doble.precio, 20.0)

    def test_componente_abstracto_no_se_puede_instanciar(self) -> None:
        with self.assertRaises(TypeError):
            ComponenteProducto()

    def test_precio_base_negativo_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            ProductoConcreto("X", -1.0)


if __name__ == "__main__":
    unittest.main()
