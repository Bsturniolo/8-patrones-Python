# Patrones de Diseño en Python

Proyecto educativo que implementa ocho patrones de diseño clásicos del libro *Gang of Four* aplicados a un sistema de comercio electrónico simulado. Todo el código está escrito en Python usando únicamente la biblioteca estándar (sin dependencias externas).

**Equipo:** Desarrollo Los Cortez
**Asignatura:** Metodología de Sistemas 2
**Python:** 3.6+

---

## Introducción

Este proyecto simula el núcleo de una tienda en línea con el objetivo de mostrar, en un contexto real y comprensible, cómo los patrones de diseño resuelven problemas concretos de arquitectura de software.

Los ocho patrones están agrupados según la clasificación GoF:

**Creacionales** — controlan cómo se crean los objetos:
1. **Singleton** — una única conexión a la base de datos compartida durante toda la ejecución.
2. **Factory Method** — cada creador concreto (subclase) decide qué producto instanciar (libros y electrónicos), sin exponer las clases concretas al código que los usa.
3. **Builder** — construcción paso a paso de pedidos complejos con opciones variables (envío, envoltura, seguro), sin constructores con decenas de parámetros.

**Estructurales** — definen cómo se componen los objetos:
4. **Decorator** — agrega servicios opcionales a productos (envoltura de regalo, seguro, garantía extendida) apilándolos dinámicamente en tiempo de ejecución.
5. **Adapter** — unifica la integración con dos transportistas (DHL y FedEx) que tienen APIs completamente distintas bajo una interfaz común.

**De comportamiento** — definen cómo interactúan los objetos:
6. **Observer** — notifica automáticamente a todos los clientes suscritos cuando la tienda publica una nueva oferta.
7. **Strategy** — permite elegir el método de pago (tarjeta, efectivo, PayPal) en tiempo de ejecución sin modificar el carrito.
8. **Chain of Responsibility** — valida un pedido a través de una cadena de controles (stock, pago, dirección, antifraude) donde cada eslabón puede aprobar o rechazar.

Cada patrón vive en su propio subpaquete dentro de `patrones/`. Siete patrones emplean interfaces abstractas (ABC) y clases concretas; Singleton controla directamente la creación de su única instancia.

---

## Patrones Implementados

| # | Categoría | Patrón | Propósito en el proyecto | Clases principales |
|---|-----------|--------|--------------------------|-------------------|
| 1 | Creacional | **Singleton** | Una única conexión a la BD en toda la app | `DatabaseConnection` |
| 2 | Creacional | **Factory Method** | Cada creador concreto decide qué tipo de producto crear | `CreadorProducto`, `CreadorLibro`, `CreadorElectronico`, `Libro`, `Electronico` |
| 3 | Creacional | **Builder** | Construir pedidos complejos paso a paso | `PedidoEstandarBuilder`, `PedidoExpressBuilder`, `DirectorPedido` |
| 4 | Estructural | **Decorator** | Apilar servicios opcionales sobre productos | `ProductoConcreto`, `EnvolturaRegalo`, `SeguroProducto`, `GarantiaExtendida` |
| 5 | Estructural | **Adapter** | Integrar sistemas de envío con APIs incompatibles | `AdaptadorDHL`, `AdaptadorFedEx` |
| 6 | Comportamiento | **Observer** | Notificar a clientes suscritos ante nuevas ofertas | `Tienda`, `Cliente` |
| 7 | Comportamiento | **Strategy** | Elegir el método de pago en tiempo de ejecución | `CarritoCompra`, `PagoTarjeta`, `PagoEfectivo`, `PagoPayPal` |
| 8 | Comportamiento | **Chain of Responsibility** | Validar pedidos en cadena de responsabilidad | `ValidadorStock`, `ValidadorPago`, `ValidadorDireccion`, `ValidadorFraude` |

---

## Estructura del Proyecto

```
Python8-main/
├── main.py                              # Punto de entrada — demo de los 8 patrones
├── requirements.txt                     # Sin dependencias externas
├── historias1.md                        # Historias de usuario (40 HU, 9 épicas)
├── tests/                               # Suite unittest: un archivo por patrón + main + convenciones
└── patrones/                            # Paquete principal
    ├── __init__.py
    ├── _numeros.py                        # Validación del rango numérico compartida
    ├── creacionales/
    │   ├── __init__.py
    │   ├── singleton/
    │   │   ├── __init__.py              # Re-exporta: DatabaseConnection
    │   │   └── database_connection.py
    │   ├── factory/
    │   │   ├── __init__.py              # Re-exporta: Producto, Libro, Electronico, Creador*
    │   │   ├── producto.py
    │   │   └── creador_producto.py
    │   └── builder/
    │       ├── __init__.py              # Re-exporta: Pedido, PedidoBuilder, Pedido*Builder, DirectorPedido
    │       ├── pedido.py
    │       └── pedido_builder.py
    ├── estructurales/
    │   ├── __init__.py
    │   ├── decorator/
    │   │   ├── __init__.py              # Re-exporta: ComponenteProducto, ProductoConcreto, Decorador*, servicios
    │   │   └── decorador_producto.py
    │   └── adapter/
    │       ├── __init__.py              # Re-exporta: SistemaEnvio, SistemaLegado*, Adaptador*
    │       └── adaptador_envio.py
    └── comportamiento/
        ├── __init__.py
        ├── observer/
        │   ├── __init__.py              # Re-exporta: Observer, Cliente, Tienda
        │   ├── observer.py
        │   └── tienda.py
        ├── strategy/
        │   ├── __init__.py              # Re-exporta: EstrategiaPago, Pago*, CarritoCompra
        │   ├── estrategia_pago.py
        │   └── carrito_compra.py
        └── chain/
            ├── __init__.py              # Re-exporta: ValidadorPedido, Validador*
            └── validador_pedido.py
```

Cada subpaquete de patrón expone sus clases públicas mediante `__init__.py` y `__all__`. Los imports públicos usan la ruta de tres niveles; `_numeros.py` es un módulo interno compartido:

```python
from patrones.creacionales.singleton import DatabaseConnection
from patrones.estructurales.adapter import AdaptadorDHL
from patrones.comportamiento.chain import ValidadorStock
```

---

## Requisitos y Ejecución

**Requisitos:**
- Python 3.6 o superior
- Sin dependencias externas (solo biblioteca estándar de Python)

**Ejecutar la demo completa:**

```bash
python main.py
```

**Verificar patrones individualmente:**

```bash
# Singleton — confirma que dos llamadas devuelven el mismo objeto
python -c "from patrones.creacionales.singleton import DatabaseConnection; db1 = DatabaseConnection.get_instance(); db2 = DatabaseConnection.get_instance(); print('Singleton OK' if db1 is db2 else 'ERROR')"

# Factory Method — el creador concreto crea un libro y se accede a su nombre como propiedad
python -c "from patrones.creacionales.factory import CreadorLibro; p = CreadorLibro('Autor').crear_producto('Test', 10.0); print('Factory Method OK' if p.nombre == 'Test' else 'ERROR')"

# Builder — construye un pedido estándar simple
python -c "
from patrones.creacionales.builder import PedidoEstandarBuilder, DirectorPedido
from patrones.creacionales.factory import CreadorLibro
b = PedidoEstandarBuilder(); d = DirectorPedido(b)
p = d.construir_pedido_simple([CreadorLibro('A').crear_producto('X', 10.0)], 'Calle Falsa 123')
print('Builder OK' if p.calcular_total() > 0 else 'ERROR')
"

# Decorator — verifica apilamiento de precio: base \$10 + envoltura \$5 = \$15
python -c "
from patrones.estructurales.decorator import ProductoConcreto, EnvolturaRegalo
p = EnvolturaRegalo(ProductoConcreto('X', 10.0))
print('Decorator OK' if p.precio == 15.0 else 'ERROR')
"

# Adapter — verifica que el adaptador DHL devuelve un costo mayor que 0
python -c "
from patrones.estructurales.adapter import AdaptadorDHL
a = AdaptadorDHL()
print('Adapter OK' if a.calcular_costo(2.0, 'Buenos Aires') > 0 else 'ERROR')
"

# Observer — suscribe un cliente dos veces y verifica que no se duplique
python -c "
from patrones.comportamiento.observer import Cliente, Tienda
t = Tienda('Test'); c = Cliente('Ana')
t.suscribir(c); t.suscribir(c)
print('Observer OK' if len(t._clientes) == 1 else 'ERROR')
"

# Strategy — hace checkout y verifica que el carrito quede vacío
python -c "
from patrones.creacionales.factory import CreadorLibro
from patrones.comportamiento.strategy import CarritoCompra, PagoEfectivo
c = CarritoCompra(); c.set_estrategia_pago(PagoEfectivo())
c.agregar_producto(CreadorLibro('Autor').crear_producto('Test', 10.0))
c.checkout()
print('Strategy OK' if c._productos == [] else 'ERROR')
"

# Chain — verifica que un pedido válido pasa toda la cadena
python -c "
from patrones.comportamiento.chain import ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude
v = ValidadorStock()
v.set_siguiente(ValidadorPago()).set_siguiente(ValidadorDireccion()).set_siguiente(ValidadorFraude())
r = v.validar({'productos': ['x'], 'metodo_pago': 'tarjeta', 'direccion_envio': 'Calle Falsa 123', 'total': 100})
print('Chain OK' if r else 'ERROR')
"
```

**Ejecutar la suite de tests** (`unittest`, biblioteca estándar):

```bash
python -m unittest discover -s tests -t .
```

Incluye un archivo de tests por patrón, un test de humo de `main.py` (criterios de HU-040),
un test de convenciones (líneas de hasta 100 caracteres, type hints en todas las firmas e
imports sin usar) y `test_doctests.py`, que ejecuta los ejemplos `>>>` de los docstrings.

---

## Contratos de entrada y manejo de errores

- Los precios aceptan `int` o `float` no negativos representables como float finito;
  `bool` se rechaza. Los enteros fuera de ese rango producen `ValueError`.
  Un tipo incorrecto produce `TypeError`; un valor negativo o no finito produce `ValueError`.
- El carrito requiere `nombre`, `precio` y un método invocable `mostrar_info()`.
  Los builders requieren `nombre` y `precio`. No es necesario heredar de `Producto`.
  Las altas inválidas se rechazan antes de modificar las colecciones.
- Ambos adaptadores requieren peso numérico finito mayor que cero, excluyendo `bool`.
  Peso, conversiones y tarifa deben permanecer en el rango finito de float; si se
  desbordan se lanza `ValueError`.
- Carrito y Pedido conservan referencias a los productos externos y revalidan sus
  precios al calcular. Una suma no finita produce `ValueError` antes del pago.
  `SeguroProducto` también rechaza el desbordamiento del precio resultante.
- Los validadores rechazan pedidos que no sean diccionarios. Stock requiere una lista
  no vacía y antifraude rechaza `NaN`, infinitos, booleanos, negativos y montos excesivos.
  Un total ausente equivale a cero, como establece HU-039.
- Si la estrategia de pago lanza una excepción, el carrito conserva sus productos y
  estrategia para permitir un reintento. Las estrategias incluidas son simulaciones.

`tests/test_regresiones_validacion.py` cubre entradas inválidas y conservación del estado.
`tests/test_limites_numericos.py` cubre desbordamientos y cambios de precios externos.
`tests/test_documentacion.py` ejecuta los ejemplos Python de este README y compara
la salida completa publicada con `main.py`.
La ejecución se verificó en Python 3.12.10. La compatibilidad objetivo con Python 3.6+
se conserva en la sintaxis, pero no se ejecutó una matriz de versiones.

## Descripción Detallada de Cada Patrón

---

### 1. Singleton — `patrones/creacionales/singleton/`

**Problema que resuelve:** Garantizar que exista una única instancia de un objeto costoso de crear (como una conexión a base de datos) y proveer un punto de acceso global a esa instancia.

**Diagrama de clases:**

```
┌────────────────────────────────┐
│       DatabaseConnection       │
├────────────────────────────────┤
│ - _instance: cls (class var)   │
│ - _lock: threading.Lock (cls)  │
│ - _initialized: bool           │
│ - _connection_string: str      │
├────────────────────────────────┤
│ + __new__(cls) -> self         │  ← controla la creación
│ + __init__(self) -> None       │  ← inicialización efectiva única
│ + get_instance() -> self       │  ← punto de acceso público
│ + query(sql: str) -> None      │
└────────────────────────────────┘
```

**Uso:**

```python
from patrones.creacionales.singleton import DatabaseConnection

db1 = DatabaseConnection.get_instance()
db2 = DatabaseConnection.get_instance()

print(db1 is db2)      # True — misma instancia
db1.query("SELECT * FROM usuarios")
```

**Implementación Python:**

Esta implementación de Singleton sobrescribe `__new__`, ya que es el método que crea el objeto antes de que `__init__` lo inicialice. Como Python llama a `__init__` siempre —incluso cuando `__new__` devuelve una instancia existente— se usa un flag `_initialized` para evitar la re-inicialización. Un `threading.Lock` de clase protege ambos pasos frente a hilos concurrentes ("double-checked locking"):

```python
import threading

class DatabaseConnection:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseConnection":
        if cls._instance is None:                 # chequeo rápido, sin lock
            with cls._lock:
                if cls._instance is None:         # chequeo seguro, con lock
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        with self._lock:
            if not self._initialized:
                self._connection_string = "mysql://localhost:3306/midb"
                print(f"Conexión a BD creada: {self._connection_string}")
                self._initialized = True
```

---

### 2. Factory Method — `patrones/creacionales/factory/`

**Problema que resuelve:** Crear productos de distintos tipos sin que el código que los usa conozca las clases concretas, y poder agregar tipos nuevos sin modificar el código existente.

**Cómo lo resuelve:** El creador abstracto `CreadorProducto` declara el *factory method* `crear_producto()`. Cada subclase (creador concreto) lo sobreescribe y decide qué producto instanciar. La operación `registrar_producto()` vive en el creador abstracto y usa el factory method sin saber qué clase concreta recibe.

**Diferencia con una Simple Factory:** en una Simple Factory una sola clase elige el producto con un `if/elif` según un string, y cada tipo nuevo obliga a modificarla. En Factory Method, agregar un tipo nuevo es agregar un creador nuevo (principio abierto/cerrado).

**Diagrama de clases:**

```
┌──────────────────────────────────────────┐        ┌──────────────────┐
│        CreadorProducto  (ABC)            │ crea   │  Producto  (ABC) │
│──────────────────────────────────────────│ ─────▶ │──────────────────│
│ + crear_producto(nombre, precio)         │        │ @property nombre │
│       -> Producto   ← @abstractmethod    │        │ @property precio │
│ + registrar_producto(nombre, precio)     │        │ + mostrar_info() │
│       -> Producto   ← usa el factory     │        └────────┬─────────┘
│                       method             │                 │
└───────────────────┬──────────────────────┘        ┌────────┴─────────┐
          ┌─────────┴──────────┐                    │                  │
┌─────────┴─────────┐ ┌────────┴───────────┐ ┌──────┴──────┐ ┌─────────┴────────┐
│   CreadorLibro    │ │ CreadorElectronico │ │    Libro    │ │   Electronico    │
│───────────────────│ │────────────────────│ │─────────────│ │──────────────────│
│ # _autor          │ │ # _garantia_meses  │ │ # _autor    │ │ # _garantia_meses│
│ crear_producto()  │ │ crear_producto()   │ │ mostrar_info│ │ mostrar_info()   │
│   -> Libro        │ │   -> Electronico   │ │ __repr__()  │ │ __repr__()       │
└───────────────────┘ └────────────────────┘ └─────────────┘ └──────────────────┘
```

**Uso:**

```python
from patrones.creacionales.factory import CreadorLibro, CreadorElectronico

creador_libros = CreadorLibro("García Márquez")       # autor por defecto: "Autor Desconocido"
creador_electronicos = CreadorElectronico(24)         # garantía por defecto: 12 meses

libro = creador_libros.crear_producto("Cien Años de Soledad", 25.99)
print(libro.nombre)    # "Cien Años de Soledad"  — acceso por propiedad, no getter

# registrar_producto() usa el factory method y muestra el producto
laptop = creador_electronicos.registrar_producto("Laptop HP", 899.99)
# Electrónico: Laptop HP | Garantía: 24 meses | Precio: $899.99
print(repr(laptop))    # Electronico(nombre='Laptop HP', precio=899.99, garantia=24m)
```

**Extender con un tipo nuevo** (sin modificar ninguna clase existente):

```python
from patrones.creacionales.factory import CreadorProducto, Producto

class Revista(Producto):                        # 1) producto nuevo
    def mostrar_info(self) -> None:
        print(f"Revista: {self.nombre} | Precio: ${self.precio:.2f}")

class CreadorRevista(CreadorProducto):          # 2) creador nuevo
    def crear_producto(self, nombre: str, precio: float) -> Revista:
        return Revista(nombre, precio)

CreadorRevista().registrar_producto("Billiken", 3.5)   # Revista: Billiken | Precio: $3.50
```

---

### 3. Builder — `patrones/creacionales/builder/`

**Problema que resuelve:** Construir objetos complejos (pedidos con múltiples opciones) paso a paso sin que el cliente tenga que conocer ni gestionar cada detalle de construcción.

**Diagrama de clases:**

```
┌───────────────────────┐       ┌──────────────────────────┐
│    DirectorPedido     │uses   │      PedidoBuilder       │ (ABC)
│───────────────────────│──────►│──────────────────────────│
│ - _builder            │       │ + agregar_producto()     │
│───────────────────────│       │ + set_direccion()        │
│ + set_builder()       │       │ + set_tipo_envio()       │
│ + construir_pedido_   │       │ + set_envoltura_regalo() │
│   simple() -> Pedido  │       │ + set_seguro()           │
│ + construir_pedido_   │       │ + build() -> Pedido      │
│   regalo() -> Pedido  │       └──────────┬───────────────┘
└───────────────────────┘                  │
                              ┌────────────┴───────────────┐
                              │                            │
                  ┌───────────┴──────┐       ┌────────────┴──────┐
                  │ PedidoEstandar   │       │  PedidoExpress    │
                  │ Builder          │       │  Builder          │
                  │ (5 días, $5.00)  │       │ (1 día, $15.00)   │
                  └──────────────────┘       └───────────────────┘
```

**Uso:**

```python
from patrones.creacionales.builder import PedidoEstandarBuilder, PedidoExpressBuilder, DirectorPedido
from patrones.creacionales.factory import CreadorLibro, CreadorElectronico

libro = CreadorLibro("García Márquez").crear_producto("Cien Años de Soledad", 25.99)
laptop = CreadorElectronico(24).crear_producto("Laptop HP", 899.99)
telefono = CreadorElectronico(12).crear_producto("iPhone 15", 999.99)

builder = PedidoEstandarBuilder()
director = DirectorPedido(builder)

# Pedido simple: el director ejecuta solo los pasos necesarios
pedido = director.construir_pedido_simple([libro, laptop], "Av. Corrientes 1234")
pedido.mostrar_resumen()

# Cambiar a express en tiempo de ejecución sin recrear el director
director.set_builder(PedidoExpressBuilder())
pedido_regalo = director.construir_pedido_regalo([telefono], "Calle Falsa 742", "¡Feliz cumpleaños!")
pedido_regalo.mostrar_resumen()
```

---

### 4. Decorator — `patrones/estructurales/decorator/`

**Problema que resuelve:** Agregar responsabilidades a un objeto dinámicamente en tiempo de ejecución, sin crear una subclase para cada combinación posible de servicios.

**Diagrama de clases:**

```
┌──────────────────────────┐
│   ComponenteProducto     │  (ABC)
│──────────────────────────│
│ @property descripcion    │  ← @abstractmethod
│ @property precio         │  ← @abstractmethod
└──────────────┬───────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───┴──────────┐  ┌───────┴──────────────┐
│ Producto     │  │  DecoradorProducto   │  (base instanciable, envuelve ComponenteProducto)
│ Concreto     │  │──────────────────────│
│──────────────│  │ - _componente        │
│ __repr__()   │  │ @property descripcion│  ← delega a _componente
└──────────────┘  │ @property precio     │  ← delega a _componente
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────┴──┐  ┌────────┴──┐  ┌───────┴──────────┐
     │ Envoltura │  │  Seguro   │  │   Garantia       │
     │ Regalo    │  │ Producto  │  │   Extendida      │
     │ (+$5.00)  │  │ (+2%)     │  │   (+$29.99)      │
     └───────────┘  └───────────┘  └──────────────────┘
```

**Uso:**

```python
from patrones.estructurales.decorator import (
    ProductoConcreto, EnvolturaRegalo, SeguroProducto, GarantiaExtendida
)

base         = ProductoConcreto("Laptop HP", 899.99)
con_envoltura = EnvolturaRegalo(base)         # $904.99
con_seguro    = SeguroProducto(con_envoltura) # $923.09  (2% sobre precio ya decorado)
con_garantia  = GarantiaExtendida(con_seguro) # $953.08

print(con_garantia.descripcion)
# Laptop HP + Envoltura de regalo + Seguro del producto + Garantía extendida (2 años)
print(f"${con_garantia.precio:.2f}")  # $953.08
```

**Nota clave:** `descripcion` y `precio` son `@property` (no métodos). `SeguroProducto` calcula el 2% sobre `self._componente.precio` — el precio ya-decorado, no el base.

---

### 5. Adapter — `patrones/estructurales/adapter/`

**Problema que resuelve:** Integrar sistemas externos con APIs incompatibles (DHL y FedEx) bajo una interfaz unificada, sin modificar los sistemas originales.

**Diagrama de clases:**

```
┌───────────────────────────┐
│       SistemaEnvio        │  (ABC — interfaz objetivo)
│───────────────────────────│
│ + calcular_costo(         │
│     peso_kg, destino)     │  ← @abstractmethod
│ + estimar_dias(destino)   │  ← @abstractmethod
│ + crear_envio(            │
│     pedido_id, destino)   │  ← @abstractmethod
└───────────┬───────────────┘
            │
   ┌────────┴────────┐
   │                 │
┌──┴──────────┐  ┌───┴───────────┐
│ Adaptador   │  │  Adaptador    │
│    DHL      │  │   FedEx       │
│─────────────│  │───────────────│
│ _dhl        │  │ _fedex        │
│ kg→gramos   │  │ kg→libras     │
│ parsea str  │  │ usa cod postal│
└──────┬──────┘  └───────┬───────┘
       │                 │
┌──────┴──────┐  ┌───────┴───────┐
│ SistemaLeg  │  │ SistemaLeg    │
│  adoDHL     │  │  adoFedEx     │
│ (adaptado)  │  │ (adaptado)    │
└─────────────┘  └───────────────┘
```

**Uso:**

```python
from patrones.estructurales.adapter import AdaptadorDHL, AdaptadorFedEx

# El cliente usa SIEMPRE la misma interfaz — no sabe qué transportista hay detrás
def cotizar(sistema, peso_kg, destino):
    print(f"Costo: ${sistema.calcular_costo(peso_kg, destino):.2f}")
    print(f"Días: {sistema.estimar_dias(destino)}")
    print(f"Guía: {sistema.crear_envio('PED-001', destino)}")

cotizar(AdaptadorDHL(),   2.5, "Buenos Aires")  # convierte kg→gramos internamente
cotizar(AdaptadorFedEx(), 2.5, "1428")          # convierte kg→libras internamente
```

| Adaptador | Conversión de peso | Formato de destino | Días devueltos |
|-----------|-------------------|-------------------|----------------|
| `AdaptadorDHL` | kg × 1000 → gramos | ciudad | parsea `"2-3 días"` → `2` |
| `AdaptadorFedEx` | kg × 2.205 → libras | código postal 4 dígitos | entero directo |

---

### 6. Observer — `patrones/comportamiento/observer/`

**Problema que resuelve:** Cuando la tienda publica una oferta, notificar automáticamente a todos los clientes suscritos sin que la tienda conozca los detalles de cada uno.

**Diagrama de clases:**

```
┌──────────────────────────┐         ┌───────────────────────────────┐
│         Tienda           │         │          Observer             │ (ABC)
│──────────────────────────│  notif. │───────────────────────────────│
│ - _nombre: str           │────────►│ + actualizar(mensaje: str)    │
│ - _clientes: List        │         └──────────────┬────────────────┘
│──────────────────────────│                        │
│ + suscribir(cliente)     │               ┌────────┴────────┐
│ + desuscribir(cliente)   │               │    Cliente      │
│ + notificar_clientes(msg)│               │─────────────────│
│ + nueva_oferta(desc)     │               │ - _nombre: str  │
└──────────────────────────┘               │ @property nombre│
                                           │ + actualizar()  │
                                           │ + __repr__()    │
                                           └─────────────────┘
```

**Uso:**

```python
from patrones.comportamiento.observer import Cliente, Tienda

tienda = Tienda("TechStore")
juan   = Cliente("Juan Pérez")
maria  = Cliente("María López")

tienda.suscribir(juan)
tienda.suscribir(maria)
tienda.nueva_oferta("50% descuento en laptops")
# → Juan y María reciben la notificación

tienda.desuscribir(maria)
tienda.nueva_oferta("Black Friday: 70% de descuento")
# → solo Juan recibe la notificación
```

**Validaciones implementadas en `Tienda`:**

| Situación | Comportamiento |
|-----------|---------------|
| `suscribir()` con objeto que no es `Observer` | Lanza `TypeError` |
| `suscribir()` con cliente ya suscrito | Imprime aviso, no duplica |
| `desuscribir()` con cliente no suscrito | Imprime aviso, no lanza excepción |

---

### 7. Strategy — `patrones/comportamiento/strategy/`

**Problema que resuelve:** Elegir el algoritmo de pago en tiempo de ejecución sin modificar el carrito. Cada estrategia encapsula su lógica y es completamente intercambiable.

**Diagrama de clases:**

```
┌──────────────────────────┐       ┌─────────────────────────┐
│      CarritoCompra       │       │     EstrategiaPago      │  (ABC)
│  (Contexto)              │uses   │─────────────────────────│
│──────────────────────────│──────►│ + pagar(monto: float)   │
│ - _productos: List       │       └────────────┬────────────┘
│ - _estrategia_pago       │                    │
│──────────────────────────│       ┌────────────┼────────────┐
│ + agregar_producto(p)    │       │            │            │
│ + set_estrategia_pago(e) │  ┌────┴───┐  ┌────┴────┐  ┌───┴──────┐
│ + calcular_total() float │  │  Pago  │  │  Pago   │  │  Pago    │
│ + checkout() -> None     │  │Tarjeta │  │Efectivo │  │ PayPal   │
└──────────────────────────┘  └────────┘  └─────────┘  └──────────┘
```

**Uso:**

```python
from patrones.comportamiento.strategy import CarritoCompra, PagoTarjeta, PagoEfectivo, PagoPayPal
from patrones.creacionales.factory import CreadorElectronico

laptop = CreadorElectronico(24).crear_producto("Laptop HP", 899.99)

carrito = CarritoCompra()
carrito.agregar_producto(laptop)
carrito.set_estrategia_pago(PagoEfectivo())
carrito.checkout()
# (extracto de la salida)
# Pagando $899.99 en efectivo. Se aplicó 5% descuento.
# Total a pagar: $854.99
```

**Comportamiento de cada estrategia:**

| Estrategia | Constructor | Lógica de pago |
|------------|-------------|----------------|
| `PagoTarjeta` | `numero_tarjeta: str` | Muestra los últimos 4 dígitos (`[-4:]`) |
| `PagoEfectivo` | sin parámetros | Aplica 5% descuento: `round(monto * 0.95, 2)` |
| `PagoPayPal` | `email: str` | Muestra el correo asociado |

`CarritoCompra.checkout()` verifica carrito no vacío y estrategia configurada antes de procesar. Tras el checkout, **el carrito se resetea** (`_productos = []`, `_estrategia_pago = None`).

---

### 8. Chain of Responsibility — `patrones/comportamiento/chain/`

**Problema que resuelve:** Validar un pedido a través de múltiples controles independientes, donde cada uno decide si continúa la cadena o la detiene. Cada regla es una clase aislada y la cadena es configurable en tiempo de ejecución.

**Diagrama de clases:**

```
┌──────────────────────────────┐
│       ValidadorPedido        │  (ABC)
│──────────────────────────────│
│ - _siguiente: Optional[self] │
│──────────────────────────────│
│ + set_siguiente(v) -> v      │  ← permite chaining: a.set_siguiente(b).set_siguiente(c)
│ + validar(pedido: dict) bool │  ← @abstractmethod
│ # _pasar_al_siguiente(p)     │  ← delega al siguiente o retorna True si es el último
└──────────────┬───────────────┘
               │
   ┌───────────┼───────────┬──────────────┐
   │           │           │              │
┌──┴────┐  ┌──┴────┐  ┌───┴──────┐  ┌───┴──────┐
│Valida-│  │Valida-│  │Validador │  │Validador │
│dorSto-│  │dorPago│  │Direccion │  │ Fraude   │
│ck     │  │       │  │          │  │          │
│≥1 prod│  │tarjeta│  │≥10 chars │  │≤$5000    │
│       │  │efect. │  │          │  │          │
│       │  │paypal │  │          │  │          │
└───────┘  └───────┘  └──────────┘  └──────────┘
```

**Uso:**

```python
from patrones.comportamiento.chain import ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude

# Construir la cadena con encadenamiento fluido
validador = ValidadorStock()
validador \
    .set_siguiente(ValidadorPago()) \
    .set_siguiente(ValidadorDireccion()) \
    .set_siguiente(ValidadorFraude())

pedido = {
    "productos": ["Laptop HP", "iPhone 15"],
    "metodo_pago": "tarjeta",
    "direccion_envio": "Av. Santa Fe 3456, Buenos Aires",
    "total": 1899.98,
}
resultado = validador.validar(pedido)
print("APROBADO" if resultado else "RECHAZADO")
```

**Validadores disponibles:**

| Clase | Regla | Falla cuando |
|-------|-------|-------------|
| `ValidadorStock` | Lista no vacía | `productos` falta, está vacío o no es lista |
| `ValidadorPago` | Método aceptado | no es `"tarjeta"`, `"efectivo"` ni `"paypal"` |
| `ValidadorDireccion` | Dirección con ≥ 10 caracteres | dirección muy corta o vacía |
| `ValidadorFraude` | Total numérico finito entre 0 y $5000 | Tipo inválido, bool, no finito, fuera de rango, negativo o mayor al límite; ausente equivale a 0 |

---

## Integración entre Patrones

`main.py` demuestra cómo los ocho patrones coexisten en un escenario realista. Los productos creados por **Factory Method** se reutilizan directamente en **Builder** y **Strategy**, y **Chain** valida diccionarios de ejemplo independientes. Decorator y Adapter también tienen demostraciones propias; el checkout no los ejecuta automáticamente:

```
main.py
  │
  ├── Singleton ──── Una conexión DB compartida en toda la ejecución
  │
  ├── Factory Method  CreadorLibro / CreadorElectronico crean: libro1, libro2, laptop, telefono
  │        └───────── Los mismos objetos se reutilizan en Builder y Strategy
  │
  ├── Observer ────── Tienda notifica a 3 clientes → desuscribe 1 → notifica a 2
  │
  ├── Strategy ─────  carrito1 (libro1 + laptop)      → PagoTarjeta
  │                   carrito2 (telefono + libro2)    → PagoEfectivo
  │                   carrito3 (laptop + telefono)    → PagoPayPal
  │
  ├── Builder ──────  director + PedidoEstandarBuilder → pedido simple
  │                   director + PedidoExpressBuilder  → pedido regalo
  │
  ├── Decorator ────  ProductoConcreto → EnvolturaRegalo → SeguroProducto → GarantiaExtendida
  │
  ├── Adapter ──────  AdaptadorDHL   → misma interfaz SistemaEnvio
  │                   AdaptadorFedEx → misma interfaz SistemaEnvio
  │
  └── Chain ─────────  Stock → Pago → Dirección → Antifraude
                        pedido válido    → APROBADO
                        pago inválido    → RECHAZADO en ValidadorPago
                        monto sospechoso → RECHAZADO en ValidadorFraude
```

---

## Características de Python Utilizadas

| Característica | Dónde se usa |
|----------------|-------------|
| `__new__` + `_initialized` | Singleton — controla instancia única sin re-inicialización |
| `abc.ABC` + `@abstractmethod` | Todos salvo Singleton — define miembros abstractos |
| `@property @abstractmethod` | Decorator — declara propiedades abstractas; las subclases deben conservar ese contrato |
| `@property` | Factory Method, Decorator, Observer — acceso a datos sin getters explícitos |
| `__repr__` | `Libro`, `Electronico`, `ProductoConcreto`, `Cliente`, `Pedido` — representación para depuración |
| `@staticmethod` | `DatabaseConnection.get_instance()` — punto de acceso global sin instancia previa |
| Herencia + sobreescritura | Factory Method — cada creador concreto sobreescribe `crear_producto()` |
| `isinstance()` | `Tienda.suscribir()` — validación de tipo en runtime |
| `round(x, 2)` | `PagoEfectivo`, decoradores — redondea a dos decimales; no garantiza aritmética decimal exacta |
| `from typing import ...` | Type hints en todas las firmas — compatible con Python 3.6+ |
| f-strings | Toda la capa de presentación (`print`) |
| `__all__` en `__init__.py` | Declara la API pública de cada subpaquete |

---

## Salida Completa del Programa

```
==================================================
DEMOSTRACIÓN DE PATRONES DE DISEÑO EN PYTHON
==================================================

>>> 1. PATRÓN SINGLETON <<<
Conexión a BD creada: mysql://localhost:3306/midb
¿Son la misma instancia? True
Ejecutando query: SELECT * FROM usuarios

>>> 2. PATRÓN FACTORY METHOD <<<
Libro: Cien Años de Soledad | Autor: Gabriel García Márquez | Precio: $25.99
Libro: Don Quijote | Autor: Miguel de Cervantes | Precio: $19.99
Electrónico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Electrónico: iPhone 15 | Garantía: 12 meses | Precio: $999.99
Acceso por propiedades -> nombre: Cien Años de Soledad | precio: $25.99

>>> 3. PATRÓN OBSERVER <<<
Cliente suscrito a la tienda TechStore
Cliente suscrito a la tienda TechStore
Cliente suscrito a la tienda TechStore

¡Nueva oferta en TechStore!

--- Notificando a 3 clientes ---
Cliente Juan Pérez recibió notificación: Nueva oferta: 50% descuento en laptops
Cliente María López recibió notificación: Nueva oferta: 50% descuento en laptops
Cliente Carlos Gómez recibió notificación: Nueva oferta: 50% descuento en laptops

Cliente desuscrito de la tienda TechStore


¡Nueva oferta en TechStore!

--- Notificando a 2 clientes ---
Cliente Juan Pérez recibió notificación: Nueva oferta: Black Friday: Todo al 70% de descuento
Cliente Carlos Gómez recibió notificación: Nueva oferta: Black Friday: Todo al 70% de descuento

>>> 4. PATRÓN STRATEGY <<<
Producto agregado al carrito: Cien Años de Soledad
Producto agregado al carrito: Laptop HP

=== CHECKOUT ===
Productos en el carrito:
Libro: Cien Años de Soledad | Autor: Gabriel García Márquez | Precio: $25.99
Electrónico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Total: $925.98
Pagando $925.98 con tarjeta terminada en 9012
¡Compra completada!

Producto agregado al carrito: iPhone 15
Producto agregado al carrito: Don Quijote

=== CHECKOUT ===
Productos en el carrito:
Electrónico: iPhone 15 | Garantía: 12 meses | Precio: $999.99
Libro: Don Quijote | Autor: Miguel de Cervantes | Precio: $19.99
Total: $1019.98
Pagando $1019.98 en efectivo. Se aplicó 5% descuento.
Total a pagar: $968.98
¡Compra completada!

Producto agregado al carrito: Laptop HP
Producto agregado al carrito: iPhone 15

=== CHECKOUT ===
Productos en el carrito:
Electrónico: Laptop HP | Garantía: 24 meses | Precio: $899.99
Electrónico: iPhone 15 | Garantía: 12 meses | Precio: $999.99
Total: $1899.98
Pagando $1899.98 con PayPal desde la cuenta: usuario@email.com
¡Compra completada!

>>> 5. PATRÓN BUILDER <<<
-- Pedido estándar simple --
  Producto agregado: Cien Años de Soledad ($25.99)
  Producto agregado: Laptop HP ($899.99)
=== RESUMEN DEL PEDIDO ===
Productos:
  - Cien Años de Soledad | $25.99
  - Laptop HP | $899.99
Subtotal productos: $925.98
Tipo de envío: Estándar (5 días hábiles) ($5.00)
Dirección: Av. Corrientes 1234, Buenos Aires
TOTAL: $930.98
==========================

-- Pedido de regalo express --
  Producto agregado: iPhone 15 ($999.99)
=== RESUMEN DEL PEDIDO ===
Productos:
  - iPhone 15 | $999.99
Subtotal productos: $999.99
Tipo de envío: Express (1 día hábil) ($15.00)
Dirección: Calle Falsa 742, Córdoba
Envoltura de regalo: Sí (+$5.00)
  Nota: "¡Feliz cumpleaños! Te mereces lo mejor."
Seguro del pedido: Sí (+$30.00)
TOTAL: $1049.99
==========================

>>> 6. PATRÓN DECORATOR <<<
Base:               Laptop HP
                    Precio: $899.99
+ EnvolturaRegalo:  Laptop HP + Envoltura de regalo
                    Precio: $904.99
+ SeguroProducto:   Laptop HP + Envoltura de regalo + Seguro del producto
                    Precio: $923.09
+ GarantiaExtendida:Laptop HP + Envoltura de regalo + Seguro del producto + Garantía extendida (2 años)
                    Precio: $953.08

>>> 7. PATRÓN ADAPTER <<<
-- Envio via DHL (adaptador convierte kg->gramos, parsea 'X-Y dias') --
  [DHL] Costo: $23.00 | Días estimados: 2
  [DHL] Guía generada: DHL-PED-001-BUE con destino a Buenos Aires
  [DHL] Seguimiento: DHL-PED-001-BUE

-- Envio via FedEx (adaptador convierte kg->libras, usa codigo postal) --
  [FedEx] Costo: $9.12 | Días estimados: 2
  [FedEx] Tracking generado: FXPED-0011428 | CP destino: 1428
  [FedEx] Seguimiento: FXPED-0011428

>>> 8. PATRÓN CHAIN OF RESPONSIBILITY <<<
-- Pedido válido --
  [Stock] OK: 2 producto(s) en el pedido.
  [Pago] OK: método 'tarjeta' aceptado.
  [Dirección] OK: 'Av. Santa Fe 3456, Buenos Aires'.
  [Antifraude] OK: total $1899.98 dentro del límite permitido.
  Resultado: APROBADO

-- Pedido con método de pago no habilitado --
  [Stock] OK: 1 producto(s) en el pedido.
  [Pago] RECHAZADO: método 'bitcoin' no está habilitado. Aceptados: efectivo, paypal, tarjeta.
  Resultado: RECHAZADO

-- Pedido con monto que supera el límite antifraude --
  [Stock] OK: 1 producto(s) en el pedido.
  [Pago] OK: método 'paypal' aceptado.
  [Dirección] OK: 'Av. Corrientes 9999, Buenos Aires'.
  [Antifraude] RECHAZADO: total $9999.99 supera el límite de $5000.00.
  Resultado: RECHAZADO

==================================================
FIN DE LA DEMOSTRACIÓN
==================================================
```

---

## Licencia

Proyecto educativo — uso libre para aprendizaje y estudio.
