"""Tests del patrón Singleton (DatabaseConnection)."""

import contextlib
import io
import threading
import time
import unittest

from patrones.creacionales.singleton import DatabaseConnection
from tests.utilidades import capturar_salida


class SalidaLenta(io.StringIO):
    """Stream que demora cada escritura para forzar la intercalación de hilos."""

    def write(self, texto: str) -> int:
        time.sleep(0.02)
        return super().write(texto)


class TestDatabaseConnection(unittest.TestCase):
    """Verifica la unicidad de la instancia y la no reinicialización."""

    def setUp(self) -> None:
        """Resetea el Singleton para que cada test arranque limpio."""
        DatabaseConnection._instance = None

    def test_get_instance_devuelve_siempre_el_mismo_objeto(self) -> None:
        (db1, db2), _ = capturar_salida(
            lambda: (DatabaseConnection.get_instance(), DatabaseConnection.get_instance())
        )
        self.assertIs(db1, db2)

    def test_constructor_directo_tambien_devuelve_la_misma_instancia(self) -> None:
        (db1, db2), _ = capturar_salida(
            lambda: (DatabaseConnection(), DatabaseConnection.get_instance())
        )
        self.assertIs(db1, db2)

    def test_la_conexion_se_inicializa_una_sola_vez(self) -> None:
        _, salida = capturar_salida(
            lambda: [DatabaseConnection.get_instance() for _ in range(3)]
        )
        self.assertEqual(salida.count("Conexión a BD creada"), 1)

    def test_acceso_concurrente_inicializa_una_sola_vez(self) -> None:
        # Épica 1: evitar "conflictos de acceso concurrente" (historias1.md)
        cantidad_hilos = 8
        barrera = threading.Barrier(cantidad_hilos, timeout=5)
        instancias = []

        def tarea() -> None:
            barrera.wait()
            instancias.append(DatabaseConnection.get_instance())

        salida = SalidaLenta()
        with contextlib.redirect_stdout(salida):
            hilos = [threading.Thread(target=tarea, daemon=True) for _ in range(cantidad_hilos)]
            for hilo in hilos:
                hilo.start()
            for hilo in hilos:
                hilo.join(timeout=5)

        self.assertFalse(any(hilo.is_alive() for hilo in hilos), "Hilos bloqueados")

        self.assertEqual(salida.getvalue().count("Conexión a BD creada"), 1)
        self.assertEqual(len(instancias), cantidad_hilos)
        self.assertTrue(all(instancia is instancias[0] for instancia in instancias))

    def test_query_imprime_la_consulta(self) -> None:
        db, _ = capturar_salida(DatabaseConnection.get_instance)
        _, salida = capturar_salida(lambda: db.query("SELECT 1"))
        self.assertIn("Ejecutando query: SELECT 1", salida)


if __name__ == "__main__":
    unittest.main()
