"""Regresiones de validación y conservación del estado ante entradas inválidas."""

import unittest
from types import SimpleNamespace

from patrones.comportamiento.chain import (
    ValidadorStock, ValidadorFraude, ValidadorPago, ValidadorDireccion,
)
from patrones.comportamiento.strategy import CarritoCompra, PagoEfectivo
from patrones.creacionales.builder import PedidoEstandarBuilder, PedidoExpressBuilder
from patrones.creacionales.factory import CreadorLibro
from patrones.estructurales.adapter import AdaptadorDHL, AdaptadorFedEx
from patrones.estructurales.decorator import ProductoConcreto
from tests.utilidades import capturar_salida


class TestRegresionesValidacion(unittest.TestCase):
    """Comprueba los errores reproducidos durante la auditoría."""

    def test_stock_rechaza_cadena_en_lugar_de_lista(self) -> None:
        resultado, _ = capturar_salida(lambda: ValidadorStock().validar({'productos': 'x'}))
        self.assertFalse(resultado)

    def test_fraude_rechaza_nan(self) -> None:
        resultado, _ = capturar_salida(lambda: ValidadorFraude().validar({'total': float('nan')}))
        self.assertFalse(resultado)

    def test_productos_rechazan_precio_nan(self) -> None:
        for crear in (CreadorLibro().crear_producto, ProductoConcreto):
            with self.subTest(crear=crear), self.assertRaises(ValueError):
                crear('X', float('nan'))

    def test_carrito_rechaza_producto_sin_contrato_completo(self) -> None:
        carrito = CarritoCompra()
        with self.assertRaises(TypeError):
            capturar_salida(lambda: carrito.agregar_producto(SimpleNamespace(nombre='X', precio=10)))
        self.assertEqual(carrito.calcular_total(), 0)

    def test_alta_fallida_no_contamina_carrito(self) -> None:
        carrito = CarritoCompra()
        try:
            carrito.agregar_producto(object())
        except (AttributeError, TypeError):
            pass
        self.assertEqual(carrito._productos, [])

    def test_alta_fallida_no_contamina_builders(self) -> None:
        for tipo in (PedidoEstandarBuilder, PedidoExpressBuilder):
            with self.subTest(builder=tipo):
                builder = tipo()
                try:
                    builder.agregar_producto(object())
                except (AttributeError, TypeError):
                    pass
                self.assertEqual(builder.build()._items, [])

    def test_adaptadores_rechazan_peso_negativo(self) -> None:
        for adaptador, destino in ((AdaptadorDHL(), 'Salta'), (AdaptadorFedEx(), '1428')):
            with self.subTest(adaptador=adaptador), self.assertRaises(ValueError):
                adaptador.calcular_costo(-1, destino)

    def test_stock_rechaza_tipos_incorrectos_sin_excepcion(self) -> None:
        for valor in (1, True, {'x': 1}, ('x',), None, []):
            with self.subTest(valor=valor):
                resultado, _ = capturar_salida(
                    lambda: ValidadorStock().validar({'productos': valor})
                )
                self.assertFalse(resultado)

    def test_validadores_rechazan_pedido_que_no_es_diccionario(self) -> None:
        for tipo in (ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude):
            for pedido in (None, [], 'pedido'):
                with self.subTest(tipo=tipo, pedido=pedido):
                    resultado, _ = capturar_salida(lambda: tipo().validar(pedido))
                    self.assertFalse(resultado)

    def test_cadena_rechaza_nan_y_stock_invalido(self) -> None:
        cadena = ValidadorStock()
        cadena.set_siguiente(ValidadorPago()).set_siguiente(ValidadorDireccion()) \
            .set_siguiente(ValidadorFraude())
        for cambios in ({'productos': 'x'}, {'total': float('nan')}):
            pedido = dict(productos=['X'], metodo_pago='tarjeta',
                          direccion_envio='Calle Falsa 123', total=100)
            pedido.update(cambios)
            resultado, _ = capturar_salida(lambda: cadena.validar(pedido))
            self.assertFalse(resultado)

    def test_fraude_rechaza_no_finitos_y_conserva_limites(self) -> None:
        for total, esperado in ((float('inf'), False), (float('-inf'), False),
                                (True, False), (0, True), (5000, True), (5000.01, False)):
            with self.subTest(total=total):
                resultado, _ = capturar_salida(lambda: ValidadorFraude().validar({'total': total}))
                self.assertEqual(resultado, esperado)
        resultado, _ = capturar_salida(lambda: ValidadorFraude().validar({}))
        self.assertTrue(resultado)  # HU-039: total ausente equivale a cero.

    def test_productos_rechazan_tipos_de_precio_incorrectos(self) -> None:
        for crear in (CreadorLibro().crear_producto, ProductoConcreto):
            for precio in (True, '10', None):
                with self.subTest(crear=crear, precio=precio), self.assertRaises(TypeError):
                    crear('X', precio)

    def test_productos_rechazan_infinitos_y_aceptan_cero(self) -> None:
        for crear in (CreadorLibro().crear_producto, ProductoConcreto):
            for precio in (float('inf'), float('-inf')):
                with self.subTest(precio=precio), self.assertRaises(ValueError):
                    crear('X', precio)
            self.assertEqual(crear('Gratis', 0).precio, 0)

    def test_altas_invalidas_preservan_productos_anteriores(self) -> None:
        for tipo in (CarritoCompra, PedidoEstandarBuilder, PedidoExpressBuilder):
            for precio, error in ((float('nan'), ValueError), (-1, ValueError),
                                  ('10', TypeError), (True, TypeError)):
                with self.subTest(tipo=tipo, precio=precio):
                    destino = tipo()
                    valido = CreadorLibro().crear_producto('Libro', 10)
                    capturar_salida(lambda: destino.agregar_producto(valido))
                    invalido = SimpleNamespace(nombre='X', precio=precio, mostrar_info=lambda: None)
                    with self.assertRaises(error):
                        capturar_salida(lambda: destino.agregar_producto(invalido))
                    if isinstance(destino, CarritoCompra):
                        self.assertEqual(destino.calcular_total(), 10)
                    else:
                        self.assertEqual(destino.build()._items, [valido])

    def test_carrito_admite_producto_ajeno_con_contrato_completo(self) -> None:
        carrito = CarritoCompra()
        producto = SimpleNamespace(nombre='Revista', precio=20,
                                   mostrar_info=lambda: print('Revista de prueba'))
        capturar_salida(lambda: carrito.agregar_producto(producto))
        carrito.set_estrategia_pago(PagoEfectivo())
        _, salida = capturar_salida(carrito.checkout)
        self.assertIn('Revista de prueba', salida)
        self.assertIn('Total a pagar: $19.00', salida)
        self.assertEqual(carrito.calcular_total(), 0)

    def test_builders_admiten_producto_ajeno_con_nombre_y_precio(self) -> None:
        for tipo, total in ((PedidoEstandarBuilder, 25), (PedidoExpressBuilder, 35)):
            builder = tipo()
            capturar_salida(lambda: builder.agregar_producto(SimpleNamespace(nombre='X', precio=20)))
            self.assertEqual(builder.build().calcular_total(), total)

    def test_adaptadores_rechazan_peso_cero_y_no_finito(self) -> None:
        for adaptador in (AdaptadorDHL(), AdaptadorFedEx()):
            for peso in (0, float('nan'), float('inf'), float('-inf')):
                with self.subTest(adaptador=adaptador, peso=peso), self.assertRaises(ValueError):
                    adaptador.calcular_costo(peso, '1428')

    def test_adaptadores_rechazan_tipo_de_peso_incorrecto(self) -> None:
        for adaptador in (AdaptadorDHL(), AdaptadorFedEx()):
            for peso in (True, '1', None):
                with self.subTest(adaptador=adaptador, peso=peso), self.assertRaises(TypeError):
                    adaptador.calcular_costo(peso, '1428')


if __name__ == '__main__':
    unittest.main()
