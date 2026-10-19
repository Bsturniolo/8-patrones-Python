"""Tests de humo del punto de entrada main.py (criterios de HU-040)."""

import ast
import os
import re
import unittest

import main
from patrones.creacionales.singleton import DatabaseConnection
from tests.utilidades import capturar_salida

RUTA_MAIN = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
ORDEN_CATEGORIAS = ["creacionales", "estructurales", "comportamiento"]


def ejecutar_demo() -> str:
    """Ejecuta main.main() desde un Singleton limpio y devuelve la salida."""
    DatabaseConnection._instance = None
    _, salida = capturar_salida(main.main)
    return salida


class TestMain(unittest.TestCase):
    """Verifica que la demostración completa cumple HU-040."""

    def test_shebang_esta_en_la_primera_linea(self) -> None:
        with open(RUTA_MAIN, encoding="utf-8") as archivo:
            primera_linea = archivo.readline()
        self.assertTrue(primera_linea.startswith("#!"))

    def test_demo_completa_termina_sin_errores(self) -> None:
        salida = ejecutar_demo()
        for seccion in range(1, 9):
            self.assertIn(">>> {}. PATRÓN".format(seccion), salida)
        self.assertIn("FIN DE LA DEMOSTRACIÓN", salida)

    def test_imports_organizados_en_tres_bloques_por_categoria(self) -> None:
        with open(RUTA_MAIN, encoding="utf-8") as archivo:
            arbol = ast.parse(archivo.read())
        categorias = [
            nodo.module.split(".")[1]
            for nodo in arbol.body
            if isinstance(nodo, ast.ImportFrom) and nodo.module.startswith("patrones.")
        ]
        indices = [ORDEN_CATEGORIAS.index(categoria) for categoria in categorias]
        self.assertEqual(indices, sorted(indices))

    def test_numeracion_del_docstring_coincide_con_las_secciones(self) -> None:
        documentados = {
            int(numero): nombre.upper()
            for numero, nombre in re.findall(r"^\s+(\d)\.\s+(\w+)", main.__doc__, re.M)
        }
        secciones = {
            int(numero): nombre.split()[0]
            for numero, nombre in re.findall(r">>> (\d)\. PATRÓN (.+?) <<<", ejecutar_demo())
        }
        self.assertEqual(len(secciones), 8)
        self.assertEqual(documentados, secciones)

    def test_seccion_factory_demuestra_propiedades_nombre_y_precio(self) -> None:
        salida = ejecutar_demo()
        seccion = salida.split(">>> 2. PATRÓN FACTORY METHOD <<<")[1].split(">>> 3.")[0]
        lineas = [linea for linea in seccion.splitlines() if "Acceso por propiedades" in linea]
        self.assertEqual(len(lineas), 1)
        self.assertIn("Cien Años de Soledad", lineas[0])
        self.assertIn("25.99", lineas[0])


if __name__ == "__main__":
    unittest.main()
