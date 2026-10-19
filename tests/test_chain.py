"""Tests del patrón Chain of Responsibility (validadores de pedido)."""

import unittest

from patrones.comportamiento.chain import (
    ValidadorDireccion,
    ValidadorFraude,
    ValidadorPago,
    ValidadorStock,
)
from tests.utilidades import capturar_salida


def pedido_valido(**cambios):
    """Devuelve un pedido válido, opcionalmente con campos modificados."""
    pedido = {
        "productos": ["Laptop"],
        "metodo_pago": "tarjeta",
        "direccion_envio": "Av. Corrientes 1234, Buenos Aires",
        "total": 100.0,
    }
    pedido.update(cambios)
    return pedido


class TestCadenaCompleta(unittest.TestCase):
    """Verifica el recorrido de la cadena Stock → Pago → Dirección → Fraude."""

    def setUp(self) -> None:
        self.cadena = ValidadorStock()
        self.cadena.set_siguiente(ValidadorPago()) \
            .set_siguiente(ValidadorDireccion()) \
            .set_siguiente(ValidadorFraude())

    def _validar(self, pedido) -> bool:
        resultado, _ = capturar_salida(lambda: self.cadena.validar(pedido))
        return resultado

    def test_pedido_valido_pasa_toda_la_cadena(self) -> None:
        self.assertTrue(self._validar(pedido_valido()))

    def test_rechazo_corta_la_cadena(self) -> None:
        _, salida = capturar_salida(
            lambda: self.cadena.validar(pedido_valido(metodo_pago="bitcoin"))
        )
        self.assertIn("[Pago] RECHAZADO", salida)
        self.assertNotIn("[Dirección]", salida)

    def test_set_siguiente_devuelve_el_validador_recibido(self) -> None:
        a, b = ValidadorStock(), ValidadorPago()
        self.assertIs(a.set_siguiente(b), b)

    def test_cadena_con_ciclo_lanza_value_error(self) -> None:
        a, b = ValidadorStock(), ValidadorPago()
        a.set_siguiente(b)
        with self.assertRaises(ValueError):
            b.set_siguiente(a)

    def test_validador_no_puede_apuntarse_a_si_mismo(self) -> None:
        a = ValidadorStock()
        with self.assertRaises(ValueError):
            a.set_siguiente(a)


class TestValidadoresIndividuales(unittest.TestCase):
    """Verifica cada regla, incluyendo datos faltantes o mal tipados."""

    def _validar(self, validador, pedido) -> bool:
        resultado, _ = capturar_salida(lambda: validador.validar(pedido))
        return resultado

    def test_stock_rechaza_pedido_sin_productos(self) -> None:
        self.assertFalse(self._validar(ValidadorStock(), pedido_valido(productos=[])))
        self.assertFalse(self._validar(ValidadorStock(), pedido_valido(productos=None)))

    def test_pago_es_insensible_a_mayusculas(self) -> None:
        self.assertTrue(self._validar(ValidadorPago(), pedido_valido(metodo_pago="PayPal")))

    def test_pago_rechaza_metodo_none_sin_romper(self) -> None:
        self.assertFalse(self._validar(ValidadorPago(), pedido_valido(metodo_pago=None)))

    def test_pago_rechaza_metodo_faltante(self) -> None:
        pedido = pedido_valido()
        del pedido["metodo_pago"]
        self.assertFalse(self._validar(ValidadorPago(), pedido))

    def test_pago_lista_metodos_aceptados_en_orden_determinista(self) -> None:
        _, salida = capturar_salida(
            lambda: ValidadorPago().validar(pedido_valido(metodo_pago="bitcoin"))
        )
        self.assertIn("Aceptados: efectivo, paypal, tarjeta.", salida)

    def test_direccion_rechaza_direccion_corta(self) -> None:
        validador = ValidadorDireccion()
        self.assertFalse(self._validar(validador, pedido_valido(direccion_envio="Calle 1")))

    def test_direccion_rechaza_none_sin_romper(self) -> None:
        validador = ValidadorDireccion()
        self.assertFalse(self._validar(validador, pedido_valido(direccion_envio=None)))

    def test_fraude_rechaza_total_sobre_el_limite(self) -> None:
        self.assertFalse(self._validar(ValidadorFraude(), pedido_valido(total=9999.99)))

    def test_fraude_acepta_total_en_el_limite(self) -> None:
        self.assertTrue(self._validar(ValidadorFraude(), pedido_valido(total=5000.00)))

    def test_fraude_rechaza_total_negativo(self) -> None:
        self.assertFalse(self._validar(ValidadorFraude(), pedido_valido(total=-100)))

    def test_fraude_rechaza_total_no_numerico_sin_romper(self) -> None:
        self.assertFalse(self._validar(ValidadorFraude(), pedido_valido(total="100")))
        self.assertFalse(self._validar(ValidadorFraude(), pedido_valido(total=None)))


if __name__ == "__main__":
    unittest.main()
