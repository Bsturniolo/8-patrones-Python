"""Regresiones de desbordamiento y precios modificados después del alta."""

import unittest
from types import SimpleNamespace

from patrones.creacionales.factory import CreadorLibro
from patrones.creacionales.builder import PedidoEstandarBuilder, PedidoExpressBuilder
from patrones.comportamiento.strategy import CarritoCompra, PagoEfectivo
from patrones.comportamiento.chain import ValidadorFraude
from patrones.estructurales.adapter import AdaptadorDHL, AdaptadorFedEx
from patrones.estructurales.decorator import ProductoConcreto, SeguroProducto
from tests.utilidades import capturar_salida


class TestLimitesNumericos(unittest.TestCase):
    """Evita resultados no finitos y excepciones de conversión sin contexto."""

    def test_precio_entero_fuera_de_rango_se_rechaza_con_value_error(self) -> None:
        for crear in (CreadorLibro().crear_producto, ProductoConcreto):
            with self.subTest(crear=crear), self.assertRaises(ValueError):
                crear('X', 10 ** 400)

    def test_fraude_rechaza_entero_fuera_de_rango_sin_excepcion(self) -> None:
        for total in (10 ** 400, -(10 ** 400)):
            resultado, _ = capturar_salida(lambda: ValidadorFraude().validar({'total': total}))
            self.assertFalse(resultado)

    def test_conversion_de_peso_no_puede_desbordar(self) -> None:
        for tipo in (AdaptadorDHL, AdaptadorFedEx):
            for peso in (1e308, 10 ** 400):
                with self.subTest(tipo=tipo, peso=peso), self.assertRaises(ValueError):
                    tipo().calcular_costo(peso, '1428')

    def test_checkout_rechaza_suma_infinita_sin_vaciar_carrito(self) -> None:
        carrito = CarritoCompra()
        for _ in range(2):
            capturar_salida(lambda: carrito.agregar_producto(
                CreadorLibro().crear_producto('X', 1e308)))
        estrategia = PagoEfectivo()
        carrito.set_estrategia_pago(estrategia)
        with self.assertRaises(ValueError):
            capturar_salida(carrito.checkout)
        self.assertEqual(len(carrito._productos), 2)
        self.assertIs(carrito._estrategia_pago, estrategia)

    def test_carrito_revalida_precio_externo_al_calcular(self) -> None:
        for precio, error in ((float('nan'), ValueError), (-1, ValueError), ('10', TypeError)):
            with self.subTest(precio=precio):
                producto = SimpleNamespace(nombre='X', precio=10, mostrar_info=lambda: None)
                carrito = CarritoCompra()
                capturar_salida(lambda: carrito.agregar_producto(producto))
                producto.precio = precio
                with self.assertRaises(error):
                    carrito.calcular_total()
                producto.precio = 20
                self.assertEqual(carrito.calcular_total(), 20)

    def test_pedido_revalida_precio_externo_al_calcular(self) -> None:
        for tipo in (PedidoEstandarBuilder, PedidoExpressBuilder):
            for precio, error in ((float('nan'), ValueError), (-1, ValueError), (True, TypeError)):
                with self.subTest(tipo=tipo, precio=precio):
                    producto = SimpleNamespace(nombre='X', precio=10)
                    builder = tipo()
                    capturar_salida(lambda: builder.agregar_producto(producto))
                    pedido = builder.build()
                    producto.precio = precio
                    with self.assertRaises(error):
                        pedido.calcular_total()

    def test_pedido_rechaza_total_infinito(self) -> None:
        builder = PedidoEstandarBuilder()
        for _ in range(2):
            capturar_salida(lambda: builder.agregar_producto(
                CreadorLibro().crear_producto('X', 1e308)))
        with self.assertRaises(ValueError):
            builder.build().calcular_total()

    def test_seguro_rechaza_precio_resultante_infinito(self) -> None:
        producto = SeguroProducto(ProductoConcreto('X', 1.79e308))
        with self.assertRaises(ValueError):
            _ = producto.precio

    def test_fedex_rechaza_tarifa_infinita_con_conversion_finita(self) -> None:
        with self.assertRaises(ValueError):
            AdaptadorFedEx().calcular_costo(7e307, '1428')

    def test_valores_grandes_representables_siguen_funcionando(self) -> None:
        self.assertEqual(CreadorLibro().crear_producto('X', 10 ** 100).precio, 10 ** 100)
        self.assertEqual(AdaptadorDHL().calcular_costo(1, 'Salta'), 11)
        self.assertEqual(AdaptadorFedEx().calcular_costo(1, '1428'), 5.15)
        self.assertEqual(SeguroProducto(ProductoConcreto('X', 100)).precio, 102)

    def test_altas_rechazan_entero_fuera_de_rango_sin_modificar_estado(self) -> None:
        for tipo in (CarritoCompra, PedidoEstandarBuilder, PedidoExpressBuilder):
            with self.subTest(tipo=tipo):
                destino = tipo()
                producto = SimpleNamespace(nombre='X', precio=10 ** 400, mostrar_info=lambda: None)
                with self.assertRaises(ValueError):
                    destino.agregar_producto(producto)
                if isinstance(destino, CarritoCompra):
                    self.assertEqual(destino.calcular_total(), 0)
                else:
                    self.assertEqual(destino.build()._items, [])

    def test_pedido_se_recupera_al_corregir_precio_externo(self) -> None:
        for tipo, esperado in ((PedidoEstandarBuilder, 25), (PedidoExpressBuilder, 35)):
            producto = SimpleNamespace(nombre='X', precio=10)
            builder = tipo()
            capturar_salida(lambda: builder.agregar_producto(producto))
            pedido = builder.build()
            producto.precio = float('inf')
            with self.assertRaises(ValueError):
                pedido.calcular_total()
            producto.precio = 20
            self.assertEqual(pedido.calcular_total(), esperado)
