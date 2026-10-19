"""Tests del patrón Builder (Pedido, builders concretos y DirectorPedido)."""

import unittest

from patrones.creacionales.builder import (
    DirectorPedido,
    Pedido,
    PedidoEstandarBuilder,
    PedidoExpressBuilder,
)
from patrones.creacionales.factory import CreadorLibro, CreadorElectronico
from tests.utilidades import capturar_salida


class TestPedidoBuilders(unittest.TestCase):
    """Verifica la construcción paso a paso de pedidos."""

    def setUp(self) -> None:
        self.libro = CreadorLibro("Autor").crear_producto("Libro", 100.0)

    def test_builder_estandar_aplica_costo_y_etiqueta_por_defecto(self) -> None:
        builder = PedidoEstandarBuilder()
        capturar_salida(lambda: builder.agregar_producto(self.libro))
        pedido = builder.build()
        self.assertEqual(pedido._tipo_envio, PedidoEstandarBuilder.TIPO_ENVIO)
        self.assertEqual(pedido.calcular_total(), 105.0)

    def test_builder_express_aplica_su_costo(self) -> None:
        builder = PedidoExpressBuilder()
        capturar_salida(lambda: builder.agregar_producto(self.libro))
        self.assertEqual(builder.build().calcular_total(), 115.0)

    def test_build_aplica_las_constantes_del_builder(self) -> None:
        # HU-011/HU-012: build() aplica TIPO_ENVIO y COSTO_ENVIO del builder,
        # aunque antes se haya llamado a set_tipo_envio().
        builder = PedidoEstandarBuilder()
        builder.set_tipo_envio("Retiro en sucursal")
        pedido = builder.build()
        self.assertEqual(pedido._tipo_envio, PedidoEstandarBuilder.TIPO_ENVIO)
        self.assertEqual(pedido._costo_envio, PedidoEstandarBuilder.COSTO_ENVIO)

    def test_build_resetea_el_builder_para_reutilizarlo(self) -> None:
        builder = PedidoExpressBuilder()
        capturar_salida(lambda: builder.agregar_producto(self.libro))
        builder.build()
        segundo = builder.build()
        self.assertEqual(segundo._items, [])
        self.assertEqual(segundo._tipo_envio, PedidoExpressBuilder.TIPO_ENVIO)

    def test_pedido_con_envoltura_y_seguro(self) -> None:
        builder = PedidoEstandarBuilder()
        capturar_salida(lambda: builder.agregar_producto(self.libro))
        builder.set_envoltura_regalo("Feliz cumple")
        builder.set_seguro()
        # 100 + 5 envío + 5 envoltura + 3 seguro (3% de 100)
        self.assertEqual(builder.build().calcular_total(), 113.0)

    def test_pedido_vacio_tiene_total_cero(self) -> None:
        self.assertEqual(Pedido().calcular_total(), 0.0)


class TestDirectorPedido(unittest.TestCase):
    """Verifica las secuencias predefinidas del director."""

    def setUp(self) -> None:
        self.telefono = CreadorElectronico(12).crear_producto("iPhone", 999.99)

    def test_pedido_regalo_express(self) -> None:
        director = DirectorPedido(PedidoEstandarBuilder())
        director.set_builder(PedidoExpressBuilder())
        pedido, _ = capturar_salida(
            lambda: director.construir_pedido_regalo([self.telefono], "Calle 742", "Hola")
        )
        self.assertTrue(pedido._incluye_envoltura)
        self.assertTrue(pedido._incluye_seguro)
        self.assertEqual(pedido._nota_regalo, "Hola")
        self.assertEqual(pedido.calcular_total(), 1049.99)

    def test_pedido_simple_sin_extras(self) -> None:
        director = DirectorPedido(PedidoEstandarBuilder())
        pedido, _ = capturar_salida(
            lambda: director.construir_pedido_simple([self.telefono], "Calle 742")
        )
        self.assertFalse(pedido._incluye_envoltura)
        self.assertFalse(pedido._incluye_seguro)
        self.assertEqual(pedido._direccion_envio, "Calle 742")


if __name__ == "__main__":
    unittest.main()
