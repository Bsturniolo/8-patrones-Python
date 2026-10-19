# AGENTS.md

This file provides guidance to Codex (claude.ai/code) when working with code in this repository.

## Project Overview

Educational Python project (Equipo: Desarrollo Los Cortez) demonstrating eight GoF design patterns through a simulated e-commerce scenario. Uses only the Python standard library — no external dependencies. Keep changes focused on the educational purpose of the repository.

The system models eight concrete problems grouped by GoF category:

- **Creacionales**: shared DB connection (Singleton), product creation delegated to creator subclasses (Factory Method), step-by-step order construction (Builder)
- **Estructurales**: optional product services stacked at runtime (Decorator), unified shipping API over incompatible systems (Adapter)
- **Comportamiento**: customer notification system (Observer), interchangeable payment methods (Strategy), multi-step order validation (Chain of Responsibility)

Seven patterns use an abstract base class (ABC) and concrete implementations; Singleton directly controls instance creation. Each pattern lives in its own subpackage nested under one of three category packages inside `patrones/`.

## Running the Project

```bash
python main.py
```

Quick sanity checks for individual patterns:

```bash
# Singleton — verifica que dos llamadas devuelven el mismo objeto
python -c "from patrones.creacionales.singleton import DatabaseConnection; db1 = DatabaseConnection.get_instance(); db2 = DatabaseConnection.get_instance(); print('OK' if db1 is db2 else 'FAIL')"

# Factory Method — verifica que el creador concreto crea el producto y se accede por propiedad
python -c "from patrones.creacionales.factory import CreadorLibro; p = CreadorLibro('Autor').crear_producto('Test', 10.0); print('OK' if p.nombre == 'Test' else 'FAIL')"

# Factory Method — verifica que cada creador concreto decide la clase del producto
python -c "from patrones.creacionales.factory import CreadorLibro, CreadorElectronico, Libro, Electronico; t = [type(c.crear_producto('X', 1.0)) for c in (CreadorLibro(), CreadorElectronico())]; print('OK' if t == [Libro, Electronico] else 'FAIL')"

# Builder — verifica que el director inicializa el builder correctamente
python -c "from patrones.creacionales.builder import PedidoEstandarBuilder, DirectorPedido; b = PedidoEstandarBuilder(); DirectorPedido(b); print('Builder OK')"

# Decorator — verifica apilamiento de precio: base $10 + envoltura $5 = $15
python -c "
from patrones.estructurales.decorator import ProductoConcreto, EnvolturaRegalo
p = EnvolturaRegalo(ProductoConcreto('X', 10.0))
print('Decorator OK' if p.precio == 15.0 else 'FAIL')
"

# Adapter — verifica que el adaptador DHL devuelve un costo mayor que 0
python -c "
from patrones.estructurales.adapter import AdaptadorDHL
a = AdaptadorDHL()
print('Adapter OK' if a.calcular_costo(2.0, 'Buenos Aires') > 0 else 'FAIL')
"

# Observer — verifica suscripción y rechazo de duplicados
python -c "
from patrones.comportamiento.observer import Cliente, Tienda
t = Tienda('Test'); c = Cliente('Ana')
t.suscribir(c); t.suscribir(c)
print('OK' if len(t._clientes) == 1 else 'FAIL')
"

# Strategy — verifica checkout y reset del carrito
python -c "
from patrones.creacionales.factory import CreadorLibro
from patrones.comportamiento.strategy import CarritoCompra, PagoEfectivo
c = CarritoCompra(); c.set_estrategia_pago(PagoEfectivo())
c.agregar_producto(CreadorLibro('Autor').crear_producto('Test', 10.0))
c.checkout()
print('OK' if c._productos == [] else 'FAIL')
"

# Chain — verifica que un pedido válido pasa toda la cadena
python -c "
from patrones.comportamiento.chain import ValidadorStock, ValidadorPago, ValidadorDireccion, ValidadorFraude
v = ValidadorStock()
v.set_siguiente(ValidadorPago()).set_siguiente(ValidadorDireccion()).set_siguiente(ValidadorFraude())
r = v.validar({'productos': ['x'], 'metodo_pago': 'tarjeta', 'direccion_envio': 'Calle Falsa 123', 'total': 100})
print('Chain OK' if r else 'FAIL')
"
```

Test suite (stdlib `unittest`, no external dependencies) lives in `tests/`: one file per pattern, a smoke test for `main.py` (HU-040 criteria), `test_convenciones.py` and `test_doctests.py`:

```bash
python -m unittest discover -s tests -t .
```

`tests/utilidades.py` provides `capturar_salida()` to capture `print()` output. `tests/test_convenciones.py` enforces lines ≤ 100 chars, type hints on every signature and no unused imports in `main.py` and `patrones/`. `tests/test_doctests.py` runs every `>>>` docstring example in `patrones/` (resetting the Singleton first), so docstring examples must show the exact output. Singleton tests reset `DatabaseConnection._instance = None` in `setUp()` for isolation. No build step, no linter configured. Target Python 3.6+.

## Architecture

`main.py` is the entry point — imports from `patrones` and demos each pattern in sequence inside `main()`. Products created in the Factory section (`libro1`, `laptop`, etc.) are deliberately reused in the Builder and Strategy sections to show realistic inter-pattern integration.

The `patrones/` package is organised into **three category packages**, each containing the relevant pattern subpackages with their own `__init__.py` re-exports:

```
patrones/
├── __init__.py
├── _numeros.py                     # Shared finite-float range check
├── creacionales/
│   ├── __init__.py
│   ├── singleton/
│   │   ├── __init__.py              # re-exports DatabaseConnection
│   │   └── database_connection.py
│   ├── factory/
│   │   ├── __init__.py              # re-exports Producto, Libro, Electronico, Creador*
│   │   ├── producto.py
│   │   └── creador_producto.py
│   └── builder/
│       ├── __init__.py              # re-exports Pedido, PedidoBuilder, Pedido*Builder, DirectorPedido
│       ├── pedido.py
│       └── pedido_builder.py
├── estructurales/
│   ├── __init__.py
│   ├── decorator/
│   │   ├── __init__.py              # re-exports ComponenteProducto, ProductoConcreto, Decorador*, servicios
│   │   └── decorador_producto.py
│   └── adapter/
│       ├── __init__.py              # re-exports SistemaEnvio, SistemaLegado*, Adaptador*
│       └── adaptador_envio.py
└── comportamiento/
    ├── __init__.py
    ├── observer/
    │   ├── __init__.py              # re-exports Observer, Cliente, Tienda
    │   ├── observer.py
    │   └── tienda.py
    ├── strategy/
    │   ├── __init__.py              # re-exports EstrategiaPago, Pago*, CarritoCompra
    │   ├── estrategia_pago.py
    │   └── carrito_compra.py
    └── chain/
        ├── __init__.py              # re-exports ValidadorPedido, Validador*
        └── validador_pedido.py
```

| Category | Pattern | Subpackage path | Key Classes |
|----------|---------|-----------------|-------------|
| Creacional | Singleton | `creacionales.singleton` | `DatabaseConnection` — `__new__` + `_initialized` flag prevent re-init |
| Creacional | Factory Method | `creacionales.factory` | Abstract `Producto` → `Libro`, `Electronico`; abstract creator `CreadorProducto` (factory method `crear_producto()`) → `CreadorLibro`, `CreadorElectronico` |
| Creacional | Builder | `creacionales.builder` | `Pedido` (product); abstract `PedidoBuilder` → `PedidoEstandarBuilder`, `PedidoExpressBuilder`; `DirectorPedido` orchestrates sequences |
| Estructural | Decorator | `estructurales.decorator` | Abstract `ComponenteProducto` → `ProductoConcreto`; instantiable base `DecoradorProducto` → `EnvolturaRegalo`, `SeguroProducto`, `GarantiaExtendida` |
| Estructural | Adapter | `estructurales.adapter` | Abstract `SistemaEnvio` (target); `SistemaLegadoDHL`, `SistemaLegadoFedEx` (adaptees); `AdaptadorDHL`, `AdaptadorFedEx` wrap adaptees |
| Comportamiento | Observer | `comportamiento.observer` | Abstract `Observer` → `Cliente`; `Tienda` validates `isinstance`, rejects duplicates, handles missing subscriber gracefully |
| Comportamiento | Strategy | `comportamiento.strategy` | Abstract `EstrategiaPago` → `PagoTarjeta`, `PagoEfectivo`, `PagoPayPal`; `CarritoCompra` resets after checkout |
| Comportamiento | Chain | `comportamiento.chain` | Abstract `ValidadorPedido` → `ValidadorStock`, `ValidadorPago`, `ValidadorDireccion`, `ValidadorFraude`; `set_siguiente()` returns next handler for fluent chaining |

Public pattern imports use the three-level path; internal numeric checks use patrones._numeros: `from patrones.<categoria>.<patron> import <Clase>`, e.g.:
```python
from patrones.creacionales.singleton import DatabaseConnection
from patrones.estructurales.adapter import AdaptadorDHL
from patrones.comportamiento.chain import ValidadorStock
```

## Key Implementation Details

- **Singleton**: `get_instance()` simply calls `DatabaseConnection()` — `__new__` handles the guard. The `_initialized` flag in `__init__` prevents re-execution since Python always calls `__init__` after `__new__`. A class-level `threading.Lock` (`_lock`) makes creation (double-checked locking in `__new__`) and initialization (`__init__`) thread-safe.
- **Factory Method** (GoF): `CreadorProducto` (ABC) declares the abstract factory method `crear_producto(nombre, precio) -> Producto` and the operation `registrar_producto(nombre, precio)`, which calls the factory method, prints via `mostrar_info()` and returns the product without knowing its concrete class. Concrete creators decide the class: `CreadorLibro(autor="Autor Desconocido")` → `Libro`, `CreadorElectronico(garantia_meses=12)` → `Electronico` (defaults carried over from the former HU-008). The former Simple Factory (`ProductoFactory`, string-based `crear_producto(tipo, ...)`) was removed. `Producto.__init__` (and `ProductoConcreto` in Decorator) raise `ValueError` for negative prices. `mostrar_info()` formats prices with `:.2f`.
- **Builder**: `build()` always applies the builder's `TIPO_ENVIO` and `COSTO_ENVIO` (HU-011/HU-012), so a label set via `set_tipo_envio()` is overwritten. `build()` resets `self._pedido = Pedido()` after returning, allowing builder reuse. `DirectorPedido.set_builder()` swaps the builder at runtime without recreating the director. Standard and Express builders duplicate their step implementations on purpose (HU-012 requires both to subclass `PedidoBuilder` directly).
- **Decorator**: `ComponenteProducto` defines `descripcion` and `precio` as `@property @abstractmethod` — subclasses should preserve the property contract; ABC does not enforce descriptor types. `SeguroProducto` computes 2% of `self._componente.precio` (already-decorated price, not base). `round(..., 2)` rounds to two decimals without guaranteeing exact decimal arithmetic.
- **Adapter**: `AdaptadorDHL.calcular_costo()` converts kg → gramos with `round()` (not truncation). `AdaptadorDHL.estimar_dias()` parses `"2-3 días hábiles"` by splitting on `"-"` and taking `[0]`; city matching ignores case, leading/trailing spaces and accents. `AdaptadorFedEx` converts kg → libras using `* 2.205`. Per spec, `destino` is a city for DHL and a postal code for FedEx.
- **Observer — Tienda.suscribir()**: validates `isinstance(cliente, Observer)` raising `TypeError("El objeto debe ser una instancia de Observer")` (exact message from HU-024), short-circuits on duplicate without error.
- **Observer — Tienda.desuscribir()**: checks `if cliente not in self._clientes` before `remove()` to avoid `ValueError`.
- **Observer — Tienda.notificar_clientes()**: iterates over a copy (`list(self._clientes)`) so an observer unsubscribing inside `actualizar()` does not make the loop skip the next one.
- **Strategy — PagoEfectivo.pagar()**: uses `round(monto * 0.95, 2)` to round to two decimals. All strategies print amounts with `:.2f`.
- **Strategy — CarritoCompra**: `set_estrategia_pago()` raises `TypeError` if the object is not an `EstrategiaPago`. `calcular_total()` rounds to 2 decimals. `checkout()` guards empty cart and `None` strategy; clears `_productos` and `_estrategia_pago` after purchase.
- **Chain**: `set_siguiente()` returns the handler it receives enabling fluent chaining: `a.set_siguiente(b).set_siguiente(c)`, and raises `ValueError` if the link would create a cycle. `_pasar_al_siguiente()` returns `True` at chain end (no next = approved). Validators return `False` for non-dict requests and invalid fields. Stock requires a nonempty list; Fraude rejects negative, non-finite or non-numeric totals, while a missing total defaults to zero (HU-039); `ValidadorPago` lists accepted methods with `sorted()` for deterministic output. The `pedido` dict keys: `"productos"`, `"metodo_pago"`, `"direccion_envio"`, `"total"`.

## Code Conventions

- Classes: `CamelCase`. Methods/variables: `snake_case`. Protected attributes: `_single_underscore`.
- Abstract interfaces use `abc.ABC` + `@abstractmethod`. The only `@staticmethod` is the Singleton access point `DatabaseConnection.get_instance()`; the Factory Method uses instance methods overridden by creator subclasses.
- All output is via `print()` to stdout — no real DB, network, or file I/O.
- Keep lines under ~100 chars. Use f-strings for formatting.
- All code, output, and documentation is in Spanish.
- Every module, class, and method has a Google-style docstring (Args/Returns/Raises sections); properties and `__repr__` use one-line docstrings. Maintain this when adding new code.
- Type hints are present on all method signatures (`param: type`, `-> return`). Use `from typing import List, Optional, Dict, Any` for complex types (Python 3.6 compatibility).
- Domain objects expose read-only data via `@property` (Python idiom) — not Java-style `get_*()` methods. `Producto` exposes `nombre`/`precio`; `ComponenteProducto` exposes `descripcion`/`precio`; `Cliente` exposes `nombre`.
- Key domain classes implement `__repr__` for debugging: `Libro`, `Electronico`, `ProductoConcreto`, `Cliente`, `Pedido`.

## Fuentes de verdad

- `historias1.md` contiene las 40 historias de usuario (9 épicas) con criterios de aceptación exactos (firmas, constantes, mensajes de salida). Es la **especificación**: ante una duda de comportamiento, consultarla antes de cambiar código. Ejemplos de reglas que parecen inconsistencias pero están especificadas: el seguro del `Pedido` (Builder) es 3% del subtotal y el `SeguroProducto` (Decorator) es 2% del precio decorado; DHL recibe ciudad y FedEx código postal como `destino`.
- `README.md` está actualizado (8 patrones, rutas de 3 niveles, propiedades, salida completa real de `main.py`). Si cambia la salida de `main.py`, regenerar la sección "Salida Completa del Programa".

## Extending the Project

Follow the existing idiom for each pattern category:

- **New product type**: subclass `Producto` (ABC in `creacionales.factory`) implementing `mostrar_info()`, plus a new creator subclassing `CreadorProducto` that overrides `crear_producto()`. Existing creators are not modified.
- **New payment method**: subclass `EstrategiaPago` (ABC in `comportamiento.strategy`), implement `pagar(monto: float) -> None`, inject via `set_estrategia_pago`.
- **New observer**: subclass `Observer` (ABC in `comportamiento.observer`), implement `actualizar(mensaje)`.
- **New order builder**: subclass `PedidoBuilder` (ABC in `creacionales.builder`), implement all abstract steps.
- **New product decorator**: subclass `DecoradorProducto` (in `estructurales.decorator`), override the `descripcion` and `precio` properties adding surcharge on top of `self._componente.precio`.
- **New shipping system**: create an adaptee class, then subclass `SistemaEnvio` (ABC in `estructurales.adapter`) to wrap it.
- **New validation rule**: subclass `ValidadorPedido` (ABC in `comportamiento.chain`), implement `validar(pedido)` calling `self._pasar_al_siguiente(pedido)` on success.

New patterns should be placed in the appropriate category directory (`creacionales/`, `estructurales/`, or `comportamiento/`) following the same subpackage structure. Patterns are intentionally decoupled — avoid importing across category packages except in `main.py`.

## Validation contracts after robustness fixes

- Prices must be nonnegative int/float values representable as finite float; bool is rejected. Invalid types
  raise TypeError, negative or non-finite values raise ValueError.
- CarritoCompra requires nombre, precio and callable mostrar_info(); builders require
  nombre and precio. Validate before appending so rejected inputs preserve state.
- Adapter weights must be finite positive int/float values (excluding bool).
- Chain validators reject non-dict requests. Stock requires a nonempty list.
  Fraude rejects non-finite totals; missing total remains zero per HU-039.
- Regression cases live in tests/test_regresiones_validacion.py.

- CarritoCompra and Pedido revalidate current product prices when calculating totals;
  external products are held by reference. Non-finite totals raise ValueError.
- patrones/_numeros.py safely rejects integers outside the float range. Adapters and
  SeguroProducto also reject arithmetic overflow with ValueError.
- tests/test_limites_numericos.py covers those limits. tests/test_documentacion.py
  executes README Python examples and compares its complete output with main.py.
