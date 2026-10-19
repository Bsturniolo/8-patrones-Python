"""Tests del patrón Observer (Tienda y Cliente)."""

import unittest

from patrones.comportamiento.observer import Cliente, Observer, Tienda
from tests.utilidades import capturar_salida


class ObservadorEspia(Observer):
    """Observador de prueba que registra los mensajes recibidos."""

    def __init__(self) -> None:
        self.mensajes = []

    def actualizar(self, mensaje: str) -> None:
        self.mensajes.append(mensaje)


class ObservadorQueSeDesuscribe(ObservadorEspia):
    """Observador que se desuscribe de la tienda al recibir el primer aviso."""

    def __init__(self, tienda: Tienda) -> None:
        super().__init__()
        self._tienda = tienda

    def actualizar(self, mensaje: str) -> None:
        super().actualizar(mensaje)
        self._tienda.desuscribir(self)


class TestTienda(unittest.TestCase):
    """Verifica suscripción, desuscripción y notificación."""

    def setUp(self) -> None:
        self.tienda = Tienda("Test")

    def test_notifica_a_todos_los_suscritos(self) -> None:
        a, b = ObservadorEspia(), ObservadorEspia()
        capturar_salida(lambda: (self.tienda.suscribir(a), self.tienda.suscribir(b)))
        capturar_salida(lambda: self.tienda.nueva_oferta("20% off"))
        self.assertEqual(a.mensajes, ["Nueva oferta: 20% off"])
        self.assertEqual(b.mensajes, ["Nueva oferta: 20% off"])

    def test_no_notifica_a_desuscritos(self) -> None:
        a = ObservadorEspia()
        capturar_salida(lambda: (self.tienda.suscribir(a), self.tienda.desuscribir(a)))
        capturar_salida(lambda: self.tienda.nueva_oferta("x"))
        self.assertEqual(a.mensajes, [])

    def test_rechaza_suscripcion_duplicada(self) -> None:
        cliente = Cliente("Ana")
        capturar_salida(lambda: (self.tienda.suscribir(cliente), self.tienda.suscribir(cliente)))
        self.assertEqual(len(self.tienda._clientes), 1)

    def test_rechaza_objetos_que_no_son_observer(self) -> None:
        with self.assertRaises(TypeError) as contexto:
            self.tienda.suscribir("no soy observer")
        # Mensaje exacto exigido por HU-024 (historias1.md)
        self.assertEqual(str(contexto.exception), "El objeto debe ser una instancia de Observer")

    def test_desuscribir_inexistente_no_lanza_error(self) -> None:
        _, salida = capturar_salida(lambda: self.tienda.desuscribir(Cliente("Ana")))
        self.assertIn("no está suscrito", salida)

    def test_desuscribirse_durante_la_notificacion_no_saltea_a_otros(self) -> None:
        que_se_va = ObservadorQueSeDesuscribe(self.tienda)
        siguiente = ObservadorEspia()
        capturar_salida(
            lambda: (self.tienda.suscribir(que_se_va), self.tienda.suscribir(siguiente))
        )
        capturar_salida(lambda: self.tienda.nueva_oferta("oferta"))
        self.assertEqual(que_se_va.mensajes, ["Nueva oferta: oferta"])
        self.assertEqual(siguiente.mensajes, ["Nueva oferta: oferta"])
        self.assertEqual(self.tienda._clientes, [siguiente])


class TestCliente(unittest.TestCase):
    """Verifica el observador concreto."""

    def test_actualizar_imprime_el_mensaje(self) -> None:
        _, salida = capturar_salida(lambda: Cliente("Ana").actualizar("hola"))
        self.assertEqual(salida.strip(), "Cliente Ana recibió notificación: hola")

    def test_nombre_y_repr(self) -> None:
        cliente = Cliente("Ana")
        self.assertEqual(cliente.nombre, "Ana")
        self.assertEqual(repr(cliente), "Cliente('Ana')")


if __name__ == "__main__":
    unittest.main()
