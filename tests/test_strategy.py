"""Tests del patrón Strategy (CarritoCompra y estrategias de pago)."""

import unittest

from patrones.comportamiento.strategy import (
    EstrategiaPago,
    CarritoCompra,
    PagoEfectivo,
    PagoPayPal,
    PagoTarjeta,
)
from patrones.creacionales.factory import CreadorLibro
from tests.utilidades import capturar_salida


class TestEstrategiasPago(unittest.TestCase):
    """Verifica cada estrategia concreta de forma aislada."""

    def test_tarjeta_muestra_solo_ultimos_cuatro_digitos(self) -> None:
        _, salida = capturar_salida(lambda: PagoTarjeta("4532-1234-5678-9012").pagar(100))
        self.assertIn("terminada en 9012", salida)
        self.assertNotIn("4532", salida)

    def test_tarjeta_formatea_monto_con_dos_decimales(self) -> None:
        _, salida = capturar_salida(lambda: PagoTarjeta("1234").pagar(100))
        self.assertIn("Pagando $100.00", salida)

    def test_efectivo_aplica_cinco_por_ciento_de_descuento(self) -> None:
        _, salida = capturar_salida(lambda: PagoEfectivo().pagar(1019.98))
        self.assertIn("Total a pagar: $968.98", salida)

    def test_efectivo_formatea_total_con_dos_decimales(self) -> None:
        _, salida = capturar_salida(lambda: PagoEfectivo().pagar(100))
        self.assertIn("Total a pagar: $95.00", salida)

    def test_paypal_usa_el_email(self) -> None:
        _, salida = capturar_salida(lambda: PagoPayPal("a@b.com").pagar(10))
        self.assertIn("a@b.com", salida)


class TestCarritoCompra(unittest.TestCase):
    """Verifica el contexto que usa las estrategias."""

    def setUp(self) -> None:
        self.carrito = CarritoCompra()

    def _agregar(self, *precios: float) -> None:
        for precio in precios:
            producto = CreadorLibro("Autor").crear_producto("X", precio)
            capturar_salida(lambda: self.carrito.agregar_producto(producto))

    def test_calcular_total_redondea_a_dos_decimales(self) -> None:
        self._agregar(0.1, 0.2)
        self.assertEqual(self.carrito.calcular_total(), 0.3)

    def test_checkout_muestra_total_formateado(self) -> None:
        self._agregar(0.1, 0.2)
        self.carrito.set_estrategia_pago(PagoTarjeta("1234"))
        _, salida = capturar_salida(self.carrito.checkout)
        self.assertIn("Total: $0.30", salida)
        self.assertNotIn("0.30000000000000004", salida)

    def test_checkout_vacia_carrito_y_estrategia(self) -> None:
        self._agregar(10.0)
        self.carrito.set_estrategia_pago(PagoEfectivo())
        capturar_salida(self.carrito.checkout)
        self.assertEqual(self.carrito._productos, [])
        self.assertIsNone(self.carrito._estrategia_pago)

    def test_checkout_con_carrito_vacio_no_paga(self) -> None:
        self.carrito.set_estrategia_pago(PagoEfectivo())
        _, salida = capturar_salida(self.carrito.checkout)
        self.assertIn("El carrito está vacío", salida)

    def test_checkout_sin_estrategia_no_paga(self) -> None:
        self._agregar(10.0)
        _, salida = capturar_salida(self.carrito.checkout)
        self.assertIn("Debe seleccionar un método de pago", salida)
        self.assertEqual(len(self.carrito._productos), 1)

    def test_set_estrategia_rechaza_objetos_que_no_son_estrategia(self) -> None:
        with self.assertRaises(TypeError):
            self.carrito.set_estrategia_pago("efectivo")

    def test_checkout_usa_la_ultima_estrategia_seleccionada(self) -> None:
        self._agregar(20)
        self.carrito.set_estrategia_pago(PagoTarjeta("1234"))
        self.carrito.set_estrategia_pago(PagoEfectivo())
        _, salida = capturar_salida(self.carrito.checkout)
        self.assertIn("Total a pagar: $19.00", salida)
        self.assertNotIn("tarjeta terminada", salida)

    def test_error_de_pago_conserva_carrito_y_permite_reintentar(self) -> None:
        class PagoFallido(EstrategiaPago):
            def pagar(self, monto: float) -> None:
                raise RuntimeError("Pago rechazado")

        self._agregar(10)
        estrategia = PagoFallido()
        self.carrito.set_estrategia_pago(estrategia)
        with self.assertRaises(RuntimeError):
            capturar_salida(self.carrito.checkout)
        self.assertEqual(self.carrito.calcular_total(), 10)
        self.assertIs(self.carrito._estrategia_pago, estrategia)
        self.carrito.set_estrategia_pago(PagoEfectivo())
        _, salida = capturar_salida(self.carrito.checkout)
        self.assertIn("Total a pagar: $9.50", salida)
        self.assertEqual(self.carrito.calcular_total(), 0)


if __name__ == "__main__":
    unittest.main()
