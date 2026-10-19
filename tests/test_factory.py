"""Tests del patrón Factory Method (Producto, creadores abstracto y concretos)."""

import unittest

import patrones.creacionales.factory as paquete_factory
from patrones.creacionales.factory import (
    CreadorElectronico,
    CreadorLibro,
    CreadorProducto,
    Electronico,
    Libro,
    Producto,
)
from tests.utilidades import capturar_salida


class Revista(Producto):
    """Producto nuevo definido solo en el test para verificar la extensibilidad."""

    def mostrar_info(self) -> None:
        print(f"Revista: {self._nombre} | Precio: ${self._precio:.2f}")


class CreadorRevista(CreadorProducto):
    """Creador concreto nuevo: extiende el sistema sin modificar el existente."""

    def crear_producto(self, nombre: str, precio: float) -> Revista:
        return Revista(nombre, precio)


class TestCreadorProducto(unittest.TestCase):
    """Verifica el creador abstracto y su operación basada en el factory method."""

    def test_creador_abstracto_no_se_puede_instanciar(self) -> None:
        with self.assertRaises(TypeError):
            CreadorProducto()

    def test_subclase_sin_factory_method_no_se_puede_instanciar(self) -> None:
        class CreadorIncompleto(CreadorProducto):
            pass

        with self.assertRaises(TypeError):
            CreadorIncompleto()

    def test_registrar_producto_crea_muestra_y_devuelve_el_producto(self) -> None:
        producto, salida = capturar_salida(
            lambda: CreadorLibro("Orwell").registrar_producto("1984", 15.99)
        )
        self.assertIsInstance(producto, Libro)
        self.assertEqual(salida.strip(), "Libro: 1984 | Autor: Orwell | Precio: $15.99")

    def test_registrar_producto_funciona_con_creadores_nuevos_sin_cambios(self) -> None:
        producto, salida = capturar_salida(
            lambda: CreadorRevista().registrar_producto("Billiken", 3.5)
        )
        self.assertIsInstance(producto, Revista)
        self.assertEqual(salida.strip(), "Revista: Billiken | Precio: $3.50")

    def test_cada_creador_concreto_decide_la_clase_del_producto(self) -> None:
        creadores = [CreadorLibro(), CreadorElectronico()]
        tipos = [type(creador.crear_producto("X", 1.0)) for creador in creadores]
        self.assertEqual(tipos, [Libro, Electronico])

    def test_la_simple_factory_anterior_ya_no_existe(self) -> None:
        self.assertFalse(hasattr(paquete_factory, "ProductoFactory"))


class TestCreadorLibro(unittest.TestCase):
    """Verifica el creador concreto de libros."""

    def test_crea_libro_con_el_autor_configurado(self) -> None:
        libro = CreadorLibro("Cervantes").crear_producto("Don Quijote", 19.99)
        self.assertIsInstance(libro, Libro)
        self.assertEqual(libro.nombre, "Don Quijote")
        self.assertEqual(libro.precio, 19.99)
        self.assertEqual(
            repr(libro), "Libro(nombre='Don Quijote', precio=19.99, autor='Cervantes')"
        )

    def test_autor_por_defecto_es_autor_desconocido(self) -> None:
        libro = CreadorLibro().crear_producto("X", 1.0)
        self.assertIn("autor='Autor Desconocido'", repr(libro))

    def test_un_creador_puede_producir_varios_productos_independientes(self) -> None:
        creador = CreadorLibro("Borges")
        primero = creador.crear_producto("Ficciones", 10.0)
        segundo = creador.crear_producto("El Aleph", 12.0)
        self.assertIsNot(primero, segundo)
        self.assertEqual([primero.nombre, segundo.nombre], ["Ficciones", "El Aleph"])


class TestCreadorElectronico(unittest.TestCase):
    """Verifica el creador concreto de electrónicos."""

    def test_crea_electronico_con_la_garantia_configurada(self) -> None:
        laptop = CreadorElectronico(24).crear_producto("Laptop HP", 899.99)
        self.assertIsInstance(laptop, Electronico)
        self.assertEqual(
            repr(laptop), "Electronico(nombre='Laptop HP', precio=899.99, garantia=24m)"
        )

    def test_garantia_por_defecto_es_12_meses(self) -> None:
        self.assertIn("garantia=12m", repr(CreadorElectronico().crear_producto("X", 1.0)))


class TestProducto(unittest.TestCase):
    """Verifica la clase abstracta Producto y las validaciones comunes."""

    def test_producto_abstracto_no_se_puede_instanciar(self) -> None:
        with self.assertRaises(TypeError):
            Producto("X", 1.0)

    def test_precio_negativo_lanza_value_error(self) -> None:
        with self.assertRaises(ValueError):
            CreadorLibro().crear_producto("X", -5.0)

    def test_precio_cero_es_valido(self) -> None:
        self.assertEqual(CreadorElectronico().crear_producto("X", 0).precio, 0)

    def test_precio_es_de_solo_lectura(self) -> None:
        libro = CreadorLibro().crear_producto("X", 10.0)
        with self.assertRaises(AttributeError):
            libro.precio = 1.0

    def test_mostrar_info_formatea_precio_con_dos_decimales(self) -> None:
        _, salida_libro = capturar_salida(CreadorLibro("A").crear_producto("X", 10).mostrar_info)
        _, salida_laptop = capturar_salida(
            CreadorElectronico(24).crear_producto("Y", 899.5).mostrar_info
        )
        self.assertIn("Precio: $10.00", salida_libro)
        self.assertIn("Precio: $899.50", salida_laptop)


if __name__ == "__main__":
    unittest.main()
