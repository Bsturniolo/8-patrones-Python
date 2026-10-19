"""Tests del patrón Adapter (sistemas de envío DHL y FedEx)."""

import unittest

from patrones.estructurales.adapter import AdaptadorDHL, AdaptadorFedEx, SistemaEnvio
from tests.utilidades import capturar_salida


class TestAdaptadorDHL(unittest.TestCase):
    """Verifica la traducción kg→gramos y el parseo de días de DHL."""

    def setUp(self) -> None:
        self.adaptador = AdaptadorDHL()

    def test_implementa_la_interfaz_unificada(self) -> None:
        self.assertIsInstance(self.adaptador, SistemaEnvio)

    def test_calcular_costo_convierte_kg_a_gramos(self) -> None:
        # 2.5 kg = 2500 g -> 3.00 + 2500 * 0.008 = 23.00
        self.assertEqual(self.adaptador.calcular_costo(2.5, "Buenos Aires"), 23.0)

    def test_calcular_costo_redondea_gramos_en_vez_de_truncar(self) -> None:
        # 0.0019 kg = 1.9 g -> 2 g -> 3.00 + 0.016 = 3.02 (truncando daría 3.01)
        self.assertEqual(self.adaptador.calcular_costo(0.0019, "Mendoza"), 3.02)

    def test_estimar_dias_ciudad_principal(self) -> None:
        self.assertEqual(self.adaptador.estimar_dias("Buenos Aires"), 2)

    def test_estimar_dias_ciudad_secundaria(self) -> None:
        self.assertEqual(self.adaptador.estimar_dias("Salta"), 4)

    def test_estimar_dias_ignora_tildes_y_espacios(self) -> None:
        self.assertEqual(self.adaptador.estimar_dias("Cordoba"), 2)
        self.assertEqual(self.adaptador.estimar_dias("  CÓRDOBA "), 2)

    def test_crear_envio_genera_guia(self) -> None:
        guia, _ = capturar_salida(
            lambda: self.adaptador.crear_envio("ped-001", "Buenos Aires")
        )
        self.assertEqual(guia, "DHL-PED-001-BUE")


class TestAdaptadorFedEx(unittest.TestCase):
    """Verifica la traducción kg→libras y el uso de código postal de FedEx."""

    def setUp(self) -> None:
        self.adaptador = AdaptadorFedEx()

    def test_calcular_costo_convierte_kg_a_libras(self) -> None:
        # 2.5 kg = 5.5125 lb -> 2.50 + 5.5125 * 1.20 = 9.115 -> 9.12 aprox.
        self.assertAlmostEqual(self.adaptador.calcular_costo(2.5, "1428"), 9.12, places=2)

    def test_estimar_dias_segun_codigo_postal(self) -> None:
        self.assertEqual(self.adaptador.estimar_dias("1428"), 2)
        self.assertEqual(self.adaptador.estimar_dias("5000"), 3)

    def test_crear_envio_genera_tracking(self) -> None:
        tracking, _ = capturar_salida(lambda: self.adaptador.crear_envio("ped-001", "1428"))
        self.assertEqual(tracking, "FXPED-0011428")


if __name__ == "__main__":
    unittest.main()
