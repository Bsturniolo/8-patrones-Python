"""Comprueba respuestas ejecutables del examen contra el código real del TP."""
import contextlib
import io
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generar_examen import PREGUNTAS
from patrones.creacionales.singleton import DatabaseConnection
from patrones.creacionales.factory import CreadorLibro, CreadorElectronico
from patrones.creacionales.builder import (
    DirectorPedido, PedidoEstandarBuilder, PedidoExpressBuilder,
)
from patrones.estructurales.decorator import (
    ProductoConcreto, DecoradorProducto, EnvolturaRegalo,
    SeguroProducto, GarantiaExtendida,
)
from patrones.estructurales.adapter import AdaptadorDHL, AdaptadorFedEx
from patrones.comportamiento.observer import Tienda, Cliente
from patrones.comportamiento.strategy import CarritoCompra, PagoEfectivo, EstrategiaPago
from patrones.comportamiento.chain import (
    ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude,
)


def respuesta(n, inciso, actual):
    """Compara un valor calculado con la clave incluida en el banco."""
    esperada = PREGUNTAS[n - 1][4][inciso][1]
    opciones = PREGUNTAS[n - 1][4][inciso][2]
    if opciones is None:
        assert float(esperada) == actual, (n, inciso, esperada, actual)
    else:
        assert esperada == str(actual), (n, inciso, esperada, actual)


def error(tipo, accion):
    """Verifica una excepción esperada sin ocultar errores de otro tipo."""
    try:
        accion()
    except tipo:
        return
    raise AssertionError('No se produjo {}'.format(tipo.__name__))


def verificar():
    """Ejecuta casos representativos de todos los patrones y valida el banco."""
    assert len(PREGUNTAS) == 40
    assert set(Counter(q[0] for q in PREGUNTAS).values()) == {5}
    for q in PREGUNTAS:
        assert len(q[4]) == 2
        for _, correcta, opciones in q[4]:
            if opciones:
                assert len(opciones) == len(set(opciones))
                assert opciones.count(correcta) == 1

    DatabaseConnection._instance = None
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        a, b = DatabaseConnection.get_instance(), DatabaseConnection()
    respuesta(1, 0, a is b)
    respuesta(1, 1, salida.getvalue().count('Conexión a BD creada'))
    respuesta(3, 1, a.query('SELECT * FROM productos'))
    respuesta(5, 0, type(CreadorElectronico(24).registrar_producto('Tablet', 300)).__name__)
    p = CreadorLibro().crear_producto('TP', 100)
    d = DirectorPedido(PedidoEstandarBuilder())
    respuesta(7, 0, PedidoEstandarBuilder.COSTO_ENVIO)
    respuesta(7, 1, d.construir_pedido_simple([p], 'Calle Falsa 123').calcular_total())
    respuesta(8, 1, d.construir_pedido_regalo([p], 'Calle Falsa 123', 'Hola').calcular_total())
    d.set_builder(PedidoExpressBuilder())
    respuesta(9, 1, d.construir_pedido_simple([p], 'Calle Falsa 123').calcular_total())
    base = ProductoConcreto('Libro', 10)
    respuesta(10, 0, EnvolturaRegalo(base).precio)
    respuesta(10, 1, base.precio)
    seguro = SeguroProducto(ProductoConcreto('Laptop', 100))
    respuesta(11, 0, seguro.precio)
    respuesta(11, 1, GarantiaExtendida(seguro).precio)
    respuesta(13, 0, AdaptadorDHL().calcular_costo(2.5, 'Buenos Aires'))
    respuesta(13, 1, AdaptadorDHL().estimar_dias('Buenos Aires'))
    t, c = Tienda('Cortez'), Cliente('Ana')
    t.suscribir(c)
    t.suscribir(c)
    respuesta(15, 0, len(t._clientes))
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        t.nueva_oferta('Libros al 20%')
    respuesta(15, 1, salida.getvalue().count('recibió notificación'))
    carrito = CarritoCompra()
    carrito.agregar_producto(p)
    carrito.set_estrategia_pago(PagoEfectivo())
    salida = io.StringIO()
    with contextlib.redirect_stdout(salida):
        carrito.checkout()
    assert 'Total a pagar: $95.00' in salida.getvalue()
    assert carrito._productos == [] and carrito._estrategia_pago is None
    a, b, c = ValidadorStock(), ValidadorPago(), ValidadorDireccion()
    r = a.set_siguiente(b)
    assert r is b
    r.set_siguiente(c)
    assert a._siguiente is b and b._siguiente is c
    respuesta(20, 0, a.validar({'productos': [], 'metodo_pago': 'tarjeta'}))
    productos = [x.registrar_producto('X', 10) for x in (CreadorLibro(), CreadorElectronico())]
    respuesta(23, 0, ', '.join(type(x).__name__ for x in productos))
    error(ValueError, lambda: CreadorLibro().crear_producto('X', -1))
    error(AttributeError, lambda: setattr(p, 'precio', 20))
    b = PedidoEstandarBuilder()
    b.agregar_producto(CreadorLibro().crear_producto('X', 10))
    respuesta(25, 0, b.build().calcular_total())
    respuesta(25, 1, b.build().calcular_total())
    b = PedidoExpressBuilder()
    b.set_tipo_envio('Retiro local')
    pedido = b.build()
    respuesta(26, 0, pedido._tipo_envio)
    respuesta(26, 1, pedido.calcular_total())
    base = ProductoConcreto('X', 100)
    respuesta(27, 0, SeguroProducto(EnvolturaRegalo(base)).precio)
    respuesta(27, 1, EnvolturaRegalo(SeguroProducto(base)).precio)
    respuesta(28, 1, DecoradorProducto(ProductoConcreto('X', 10)).precio)
    respuesta(29, 0, AdaptadorFedEx().calcular_costo(1, '1428'))
    respuesta(29, 1, AdaptadorFedEx().estimar_dias('5000'))
    respuesta(30, 0, AdaptadorDHL().calcular_costo(.0019, 'Córdoba'))
    respuesta(30, 1, AdaptadorDHL().estimar_dias('  CÓRDOBA  '))
    t = Tienda('Cortez')
    t.suscribir(Cliente('Ana'))
    t.suscribir(Cliente('Ana'))
    t.desuscribir(Cliente('Ana'))
    respuesta(32, 0, len(t._clientes))

    class PagoFallido(EstrategiaPago):
        """Estrategia que reproduce el fallo planteado en la pregunta 33."""
        def pagar(self, monto):
            """Interrumpe el checkout antes del reinicio."""
            raise RuntimeError('Servicio no disponible')

    carrito.agregar_producto(p)
    fallido = PagoFallido()
    carrito.set_estrategia_pago(fallido)
    error(RuntimeError, carrito.checkout)
    assert carrito._productos == [p] and carrito._estrategia_pago is fallido
    error(TypeError, lambda: carrito.set_estrategia_pago(object()))
    respuesta(35, 0, ValidadorFraude().validar({'total': 5000}))
    respuesta(35, 1, ValidadorFraude().validar({'total': 5000.01}))
    a, b = ValidadorStock(), ValidadorPago()
    a.set_siguiente(b)
    error(ValueError, lambda: b.set_siguiente(a))
    error(TypeError, lambda: t.suscribir(object()))
    error(TypeError, lambda: carrito.agregar_producto(EnvolturaRegalo(base)))
    assert ValidadorStock().validar({'productos': ['X']}) is True


if __name__ == '__main__':
    with contextlib.redirect_stdout(io.StringIO()):
        verificar()
    print('Banco validado: 40 preguntas, 5 por patrón; claves ejecutables comprobadas.')
