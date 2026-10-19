"""
Patrón Singleton - Conexión única a la base de datos.

El patrón Singleton garantiza que una clase tenga **una sola instancia** en toda
la aplicación y proporciona un punto de acceso global a ella.

Problema que resuelve:
    En un sistema real, abrir múltiples conexiones a la base de datos consume
    recursos innecesariamente y puede causar conflictos. El Singleton asegura
    que todas las partes del sistema compartan la misma conexión.

Cómo funciona en Python:
    1. Se sobreescribe __new__() para controlar la creación del objeto.
    2. Una variable de clase (_instance) guarda la referencia a la única instancia.
    3. Un flag (_initialized) evita que __init__() reinicialice los datos.

Ejemplo de uso:
    >>> db1 = DatabaseConnection.get_instance()
    Conexión a BD creada: mysql://localhost:3306/midb
    >>> db2 = DatabaseConnection.get_instance()  # ya existe: no se vuelve a crear
    >>> db1 is db2  # ambas variables apuntan al mismo objeto
    True

Acceso concurrente:
    Sin protección, dos hilos podrían ver _instance en None (o _initialized en
    False) al mismo tiempo y crear/inicializar la conexión dos veces. Un Lock de
    clase serializa la creación ("double-checked locking") y la inicialización.
"""

import threading


class DatabaseConnection:
    """Clase que implementa el patrón Singleton para gestionar una conexión a BD.

    Atributos de clase:
        _instance: Referencia a la única instancia de la clase (None si no existe).
        _lock (threading.Lock): Protege la creación e inicialización entre hilos.

    Atributos de instancia:
        _initialized (bool): Flag que previene reinicialización del objeto.
        _connection_string (str): URL de conexión simulada a la base de datos.
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseConnection":
        """Controla la creación del objeto. Si ya existe una instancia, la retorna.

        Este método se ejecuta ANTES que __init__(). Es el responsable de crear
        (o no) el objeto en memoria. Se verifica _instance dos veces: afuera del
        lock (rápido, caso común) y adentro (seguro frente a otros hilos).

        Returns:
            DatabaseConnection: La única instancia de la clase.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Inicializa la conexión solo la primera vez.

        Gracias al flag _initialized, aunque Python llame a __init__() cada vez
        que se invoca DatabaseConnection(), la lógica de configuración se ejecuta
        una sola vez. El lock evita que dos hilos pasen el chequeo a la vez.
        """
        with self._lock:
            if not self._initialized:
                self._connection_string = "mysql://localhost:3306/midb"
                print(f"Conexión a BD creada: {self._connection_string}")
                self._initialized = True

    @staticmethod
    def get_instance() -> "DatabaseConnection":
        """Punto de acceso global a la instancia Singleton.

        Delega la creación/obtención al mecanismo __new__(), que garantiza
        que siempre se retorne la misma instancia.

        Returns:
            DatabaseConnection: La única instancia de la clase.
        """
        return DatabaseConnection()

    def query(self, sql: str) -> None:
        """Simula la ejecución de una consulta SQL.

        Args:
            sql (str): La consulta SQL a ejecutar.
        """
        print(f"Ejecutando query: {sql}")
