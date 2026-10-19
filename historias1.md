# Historias de Usuario - Sistema E-Commerce con Patrones de Diseño

**Proyecto:** Patrones de Diseño en Python
**Equipo:** Desarrollo Los Cortez
**Fecha:** Marzo 2026
**Versión:** 3.0 (8 patrones GoF implementados — propiedades, type hints, __repr__)

---

## Roles del Sistema

| Rol | Descripcion |
|-----|-------------|
| **Desarrollador** | Programador que construye y mantiene el sistema aplicando patrones de diseño |
| **Comprador** | Usuario final que navega productos, arma su carrito y realiza compras |
| **Administrador de tienda** | Responsable de gestionar la tienda, publicar ofertas y manejar suscriptores |
| **Cliente suscrito** | Comprador que se suscribio a notificaciones de una tienda |
| **Estudiante / Evaluador** | Persona que estudia o evalua la implementacion de los patrones |

---

## EPICA 1: Gestion de Conexion a Base de Datos (Patron Singleton)

> **Objetivo:** Garantizar una unica conexion a la base de datos durante toda la ejecucion, evitando consumo de recursos y conflictos de acceso concurrente.
>
> **Patron aplicado:** Singleton
>
> **Archivos involucrados:** `patrones/creacionales/singleton/database_connection.py`

---

### HU-001: Crear una unica instancia de conexion a base de datos

**Como** desarrollador del sistema,
**quiero** que la clase `DatabaseConnection` permita crear una sola instancia durante toda la ejecucion,
**para** evitar que multiples partes del codigo abran conexiones duplicadas que consuman recursos innecesariamente.

**Criterios de Aceptacion:**

1. La clase `DatabaseConnection` sobreescribe `__new__(cls) -> "DatabaseConnection"` para interceptar la creacion del objeto antes de que Python lo inicialice.
2. Existe una variable de clase `_instance` (inicializada en `None`) que almacena la referencia a la unica instancia.
3. Si `_instance` es `None`, se crea una nueva instancia usando `super().__new__(cls)` y se asigna a `_instance`.
4. Si `_instance` ya existe, `__new__()` retorna la instancia existente sin crear otra.
5. Al verificar `db1 = DatabaseConnection()` y `db2 = DatabaseConnection()`, la expresion `db1 is db2` retorna `True`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `DatabaseConnection` |
| Metodo clave | `__new__(cls) -> "DatabaseConnection"` |
| Variable de control | `_instance` (variable de clase) |
| Archivo | `patrones/creacionales/singleton/database_connection.py` |

**Definicion de Hecho:**
- [x] `__new__()` implementado y controla la creacion.
- [x] `db1 is db2` retorna `True` en todos los flujos.
- [x] No se crean objetos duplicados en memoria.

---

### HU-002: Prevenir la reinicializacion de la conexion

**Como** desarrollador del sistema,
**quiero** que los datos de conexion no se reinicialicen aunque se invoque el constructor multiples veces,
**para** proteger la configuracion de la conexion y evitar perdida de estado.

**Criterios de Aceptacion:**

1. Existe un flag `_initialized: bool` que se establece en `False` al crear el objeto en `__new__()`.
2. El metodo `__init__(self) -> None` verifica `if not self._initialized` antes de ejecutar la logica de configuracion.
3. La cadena `_connection_string` se asigna como `"mysql://localhost:3306/midb"` solo en la primera inicializacion.
4. El mensaje `"Conexión a BD creada: ..."` se imprime exactamente **una vez**, sin importar cuantas instancias se soliciten.
5. Tras la primera inicializacion, `_initialized` se establece en `True` y llamadas posteriores no tienen efecto.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Flag de control | `_initialized: bool` |
| Atributo protegido | `_connection_string: str` |
| Firma | `__init__(self) -> None` |
| Archivo | `patrones/creacionales/singleton/database_connection.py` |

**Definicion de Hecho:**
- [x] Flag `_initialized` controla la inicializacion unica.
- [x] Mensaje de creacion aparece solo una vez.

---

### HU-003: Acceder a la conexion mediante punto de acceso global

**Como** desarrollador del sistema,
**quiero** obtener la instancia de conexion a traves del metodo estatico `get_instance()`,
**para** acceder a la conexion desde cualquier modulo sin instanciar directamente la clase.

**Criterios de Aceptacion:**

1. El metodo `get_instance()` esta decorado con `@staticmethod` y tiene firma `-> "DatabaseConnection"`.
2. Internamente delega a `DatabaseConnection()`, activando el mecanismo `__new__()`.
3. Llamadas consecutivas siempre retornan la misma instancia.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Metodo | `get_instance() -> "DatabaseConnection"` (estatico) |
| Implementacion | `return DatabaseConnection()` |
| Archivo | `patrones/creacionales/singleton/database_connection.py` |

**Definicion de Hecho:**
- [x] Metodo estatico implementado con tipo de retorno anotado.
- [x] Delega a `__new__()` sin duplicar logica.
- [x] Siempre retorna la misma instancia.

---

### HU-004: Ejecutar consultas SQL sobre la conexion unica

**Como** desarrollador del sistema,
**quiero** ejecutar consultas SQL a traves del metodo `query()` de la conexion Singleton,
**para** simular operaciones de base de datos asegurando que siempre usen la misma conexion.

**Criterios de Aceptacion:**

1. El metodo `query(self, sql: str) -> None` recibe el parametro `sql` con type hint.
2. Imprime en consola: `"Ejecutando query: {sql}"`.
3. Se invoca sobre la instancia obtenida con `get_instance()`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firma | `query(self, sql: str) -> None` |
| Salida esperada | `Ejecutando query: SELECT * FROM usuarios` |
| Archivo | `patrones/creacionales/singleton/database_connection.py` |

**Definicion de Hecho:**
- [x] Metodo funcional con type hints y salida por consola.
- [x] Comprobado con al menos una consulta de ejemplo.

---

## EPICA 2: Catalogo de Productos (Patron Factory Method)

> **Objetivo:** Delegar en subclases creadoras la decision de que tipo de producto instanciar, desacoplando el codigo cliente de las clases concretas y permitiendo agregar tipos nuevos sin modificar el codigo existente.
>
> **Patron aplicado:** Factory Method
>
> **Archivos involucrados:** `patrones/creacionales/factory/producto.py`, `patrones/creacionales/factory/creador_producto.py`

---

### HU-005: Definir interfaz comun para todos los productos

**Como** desarrollador del sistema,
**quiero** que exista una clase abstracta `Producto` que defina la estructura base de todos los productos,
**para** garantizar que cualquier tipo de producto comparta una interfaz comun y exponga sus datos mediante propiedades Python.

**Criterios de Aceptacion:**

1. La clase `Producto` hereda de `ABC` (modulo `abc`).
2. El constructor tiene firma `__init__(self, nombre: str, precio: float) -> None`.
3. Declara el metodo abstracto `mostrar_info(self) -> None` decorado con `@abstractmethod`.
4. Expone `nombre` como `@property` que retorna `self._nombre` (tipo `str`).
5. Expone `precio` como `@property` que retorna `self._precio` (tipo `float`).
6. Intentar instanciar `Producto()` directamente lanza `TypeError`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Producto(ABC)` |
| Atributos protegidos | `_nombre: str`, `_precio: float` |
| Metodo abstracto | `mostrar_info(self) -> None` |
| Propiedades | `nombre -> str`, `precio -> float` |
| Archivo | `patrones/creacionales/factory/producto.py` |

**Definicion de Hecho:**
- [x] Clase abstracta con ABC, `@abstractmethod` y type hints.
- [x] Propiedades `nombre` y `precio` retornan valores correctos.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-006: Registrar productos de tipo Libro

**Como** comprador en la tienda en linea,
**quiero** que el sistema soporte productos de tipo Libro con titulo, precio y autor,
**para** disponer de un catalogo de libros con toda su informacion relevante.

**Criterios de Aceptacion:**

1. La clase `Libro` hereda de `Producto` con constructor `__init__(self, nombre: str, precio: float, autor: str) -> None`.
2. Invoca `super().__init__(nombre, precio)` y almacena `_autor: str`.
3. `mostrar_info(self) -> None` imprime: `"Libro: {nombre} | Autor: {autor} | Precio: ${precio:.2f}"`.
4. Las propiedades heredadas `nombre` y `precio` retornan los valores correctos.
5. Implementa `__repr__(self) -> str` retornando `"Libro(nombre=..., precio=..., autor=...)"` para facilitar la depuracion.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Libro(Producto)` |
| Atributo adicional | `_autor: str` |
| `__repr__` | `Libro(nombre='Don Quijote', precio=19.99, autor='Cervantes')` |
| Salida `mostrar_info()` | `Libro: Don Quijote \| Autor: Cervantes \| Precio: $19.99` |
| Archivo | `patrones/creacionales/factory/producto.py` |

**Definicion de Hecho:**
- [x] Herencia correcta con `super().__init__()`.
- [x] `mostrar_info()` produce el formato exacto.
- [x] `__repr__` implementado y util para depuracion.

---

### HU-007: Registrar productos de tipo Electronico

**Como** comprador en la tienda en linea,
**quiero** que el sistema soporte productos electronicos con nombre, precio y garantia en meses,
**para** conocer la cobertura de garantia de cada dispositivo antes de comprarlo.

**Criterios de Aceptacion:**

1. La clase `Electronico` hereda de `Producto` con constructor `__init__(self, nombre: str, precio: float, garantia_meses: int) -> None`.
2. Invoca `super().__init__(nombre, precio)` y almacena `_garantia_meses: int`.
3. `mostrar_info(self) -> None` imprime: `"Electrónico: {nombre} | Garantía: {garantia_meses} meses | Precio: ${precio:.2f}"`.
4. Las propiedades heredadas `nombre` y `precio` retornan los valores correctos.
5. Implementa `__repr__(self) -> str` retornando `"Electronico(nombre=..., precio=..., garantia=Xm)"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Electronico(Producto)` |
| Atributo adicional | `_garantia_meses: int` |
| `__repr__` | `Electronico(nombre='Laptop HP', precio=899.99, garantia=24m)` |
| Salida `mostrar_info()` | `Electrónico: Laptop HP \| Garantía: 24 meses \| Precio: $899.99` |
| Archivo | `patrones/creacionales/factory/producto.py` |

**Definicion de Hecho:**
- [x] Herencia correcta con `super().__init__()`.
- [x] `mostrar_info()` produce el formato exacto.
- [x] `__repr__` implementado con sufijo `m` para meses.

---

### HU-008: Crear productos mediante creadores (Factory Method)

**Como** desarrollador del sistema,
**quiero** que cada tipo de producto tenga su propio creador que decida que clase concreta instanciar,
**para** que el codigo cliente trabaje solo contra las abstracciones y agregar un tipo nuevo no obligue a modificar el codigo existente.

**Criterios de Aceptacion:**

1. `CreadorProducto` hereda de `ABC` y declara el factory method abstracto `crear_producto(self, nombre: str, precio: float) -> Producto`.
2. `CreadorProducto` implementa `registrar_producto(self, nombre: str, precio: float) -> Producto`, que invoca `crear_producto()`, llama a `mostrar_info()` sobre el resultado y lo retorna, sin conocer la clase concreta.
3. `CreadorLibro(CreadorProducto)` recibe `autor: str = "Autor Desconocido"` en su constructor y su `crear_producto()` retorna un `Libro`.
4. `CreadorElectronico(CreadorProducto)` recibe `garantia_meses: int = 12` en su constructor y su `crear_producto()` retorna un `Electronico`.
5. No es posible instanciar `CreadorProducto` ni una subclase que no implemente `crear_producto()` (lanza `TypeError`).
6. Agregar un tipo de producto nuevo requiere solo una subclase de `Producto` y una de `CreadorProducto`, sin modificar las existentes.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Creador abstracto | `CreadorProducto(ABC)` |
| Factory method | `crear_producto(nombre, precio) -> Producto` (`@abstractmethod`) |
| Operacion del creador | `registrar_producto(nombre, precio) -> Producto` |
| Creadores concretos | `CreadorLibro(autor)`, `CreadorElectronico(garantia_meses)` |
| Archivo | `patrones/creacionales/factory/creador_producto.py` |

**Definicion de Hecho:**
- [x] Cada creador concreto retorna su producto concreto con type hints.
- [x] `registrar_producto()` funciona con cualquier creador, incluso uno nuevo.
- [x] Instanciacion directa del creador abstracto lanza `TypeError`.

---

## EPICA 3: Construccion de Pedidos Complejos (Patron Builder)

> **Objetivo:** Construir pedidos con multiples opciones configurables (tipo de envio, envoltura, seguro) paso a paso, sin requerir un constructor con multiples parametros ni combinaciones de subclases.
>
> **Patron aplicado:** Builder
>
> **Archivos involucrados:** `patrones/creacionales/builder/pedido.py`, `patrones/creacionales/builder/pedido_builder.py`

---

### HU-009: Representar el pedido como objeto complejo

**Como** desarrollador del sistema,
**quiero** que exista una clase `Pedido` que agrupe todos los datos de un pedido,
**para** tener un objeto resultado bien definido que el builder construya paso a paso.

**Criterios de Aceptacion:**

1. `Pedido` se inicializa con `__init__(self) -> None` con todos los atributos en estado neutro.
2. Atributos anotados: `_items: List`, `_direccion_envio: Optional[str]`, `_tipo_envio: Optional[str]`, `_costo_envio: float`, `_incluye_envoltura: bool`, `_nota_regalo: Optional[str]`, `_incluye_seguro: bool`.
3. Constantes de clase: `COSTO_ENVOLTURA = 5.00` y `COSTO_SEGURO_PORCENTAJE = 0.03`.
4. `calcular_total(self) -> float` suma precios de items (via propiedad `precio`) mas cargos adicionales, redondeado a 2 decimales.
5. `mostrar_resumen(self) -> None` imprime todos los detalles del pedido incluyendo nombre/precio de items via propiedades.
6. `__repr__(self) -> str` retorna representacion tecnica con lista de nombres, tipo de envio y total.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Pedido` |
| Imports | `from typing import List, Optional` |
| Costo envoltura | `COSTO_ENVOLTURA = 5.00` |
| Costo seguro | `COSTO_SEGURO_PORCENTAJE = 0.03` (3% del subtotal) |
| Acceso a productos | Via propiedad `p.precio` y `p.nombre` (duck typing) |
| Archivo | `patrones/creacionales/builder/pedido.py` |

**Definicion de Hecho:**
- [x] Atributos con type annotations (`Optional`, `List`).
- [x] `calcular_total()` usa `p.precio` (propiedad, no getter).
- [x] `__repr__` implementado para depuracion.

---

### HU-010: Definir interfaz abstracta del builder

**Como** desarrollador del sistema,
**quiero** una clase abstracta `PedidoBuilder` que defina los pasos de construccion del pedido,
**para** garantizar que todos los builders concretos implementen los mismos pasos.

**Criterios de Aceptacion:**

1. `PedidoBuilder` hereda de `ABC` y declara 6 metodos abstractos con `@abstractmethod`.
2. Metodos: `agregar_producto(producto)`, `set_direccion(direccion: str)`, `set_tipo_envio(tipo: str)`, `set_envoltura_regalo(nota: str)`, `set_seguro()`, `build() -> Pedido`.
3. La docstring de `agregar_producto` especifica duck typing: objeto con propiedades `nombre` y `precio`.
4. No es posible instanciar `PedidoBuilder` directamente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PedidoBuilder(ABC)` |
| Metodos abstractos | 6 pasos de construccion |
| Duck typing | productos con propiedades `nombre` y `precio` |
| Archivo | `patrones/creacionales/builder/pedido_builder.py` |

**Definicion de Hecho:**
- [x] 6 metodos abstractos con `@abstractmethod`.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-011: Construir pedidos con envio estandar

**Como** comprador en la tienda en linea,
**quiero** crear pedidos con envio estandar (costo $5.00, 5 dias habiles),
**para** elegir la opcion mas economica cuando no hay urgencia de entrega.

**Criterios de Aceptacion:**

1. `PedidoEstandarBuilder` implementa todos los pasos abstractos de `PedidoBuilder`.
2. Constantes de clase: `COSTO_ENVIO = 5.00`, `TIPO_ENVIO = "Estándar (5 días hábiles)"`.
3. `agregar_producto(producto)` imprime `"  Producto agregado: {producto.nombre} (${producto.precio:.2f})"` accediendo via **propiedades**.
4. `build(self) -> Pedido` aplica `TIPO_ENVIO` y `COSTO_ENVIO`, guarda el pedido terminado, hace `self._pedido = Pedido()` y retorna el anterior para permitir reutilizacion.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PedidoEstandarBuilder(PedidoBuilder)` |
| Costo envio | `COSTO_ENVIO = 5.00` |
| Reset en build | `self._pedido = Pedido()` antes de retornar el pedido terminado |
| Acceso a producto | `producto.nombre`, `producto.precio` (propiedades) |
| Archivo | `patrones/creacionales/builder/pedido_builder.py` |

**Definicion de Hecho:**
- [x] Implementa todos los pasos abstractos.
- [x] `build()` resetea el pedido interno para reutilizacion.
- [x] Accede a productos via propiedades (no getters).

---

### HU-012: Construir pedidos con envio express

**Como** comprador en la tienda en linea,
**quiero** crear pedidos con envio express (costo $15.00, 1 dia habil),
**para** recibir mis compras urgentes o regalos de ultimo momento al dia siguiente.

**Criterios de Aceptacion:**

1. `PedidoExpressBuilder` implementa todos los pasos abstractos con las mismas firmas que `PedidoEstandarBuilder`.
2. Constantes de clase: `COSTO_ENVIO = 15.00`, `TIPO_ENVIO = "Express (1 día hábil)"`.
3. `build(self) -> Pedido` aplica las constantes express y resetea `self._pedido = Pedido()`.
4. El comportamiento de `agregar_producto`, `set_envoltura_regalo` y `set_seguro` es identico al builder estandar.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PedidoExpressBuilder(PedidoBuilder)` |
| Costo envio | `COSTO_ENVIO = 15.00` |
| Tipo envio | `"Express (1 día hábil)"` |
| Archivo | `patrones/creacionales/builder/pedido_builder.py` |

**Definicion de Hecho:**
- [x] Constantes express correctas.
- [x] `build()` resetea correctamente el builder.

---

### HU-013: Orquestar la construccion de pedidos con el Director

**Como** desarrollador del sistema,
**quiero** un `DirectorPedido` que defina secuencias de construccion predefinidas,
**para** que el codigo cliente no tenga que invocar cada paso manualmente.

**Criterios de Aceptacion:**

1. `DirectorPedido` tiene constructor `__init__(self, builder: "PedidoBuilder") -> None`.
2. `set_builder(self, builder: "PedidoBuilder") -> None` permite cambiar el builder en tiempo de ejecucion sin recrear el director.
3. `construir_pedido_simple(self, productos: List, direccion: str) -> Pedido` itera productos, setea direccion y llama `build()`.
4. `construir_pedido_regalo(self, productos: List, direccion: str, nota: str) -> Pedido` ademas activa envoltura y seguro.
5. Devuelve siempre una instancia de `Pedido` completamente configurada.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `DirectorPedido` |
| Import | `from typing import List` |
| Tipos de construccion | `construir_pedido_simple`, `construir_pedido_regalo` |
| Patron | Director orquesta; builder ensambla; cliente elige builder |
| Archivo | `patrones/creacionales/builder/pedido_builder.py` |

**Definicion de Hecho:**
- [x] `set_builder()` permite cambiar builder sin recrear director.
- [x] Pedido simple: sin envoltura ni seguro.
- [x] Pedido regalo: con envoltura + seguro activados.

---

## EPICA 4: Servicios Opcionales en Productos (Patron Decorator)

> **Objetivo:** Agregar responsabilidades opcionales (envoltura, seguro, garantia extendida) a un producto en tiempo de ejecucion, sin crear una subclase por cada combinacion posible.
>
> **Patron aplicado:** Decorator
>
> **Archivos involucrados:** `patrones/estructurales/decorator/decorador_producto.py`

---

### HU-014: Definir interfaz abstracta de componente con propiedades

**Como** desarrollador del sistema,
**quiero** una interfaz abstracta `ComponenteProducto` que defina `descripcion` y `precio` como propiedades abstractas,
**para** que tanto el componente base como todos los decoradores sean intercambiables y usen el idioma Python de propiedades.

**Criterios de Aceptacion:**

1. `ComponenteProducto` hereda de `ABC`.
2. Declara `descripcion` como `@property @abstractmethod` con retorno `-> str`.
3. Declara `precio` como `@property @abstractmethod` con retorno `-> float`.
4. Toda subclase debe conservar el contrato de ambas propiedades. `@abstractmethod` exige sobrescribir los miembros abstractos, pero no verifica que la sobrescritura siga siendo una propiedad.
5. No es posible instanciar `ComponenteProducto` directamente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `ComponenteProducto(ABC)` |
| Propiedades abstractas | `descripcion -> str`, `precio -> float` |
| Idioma | `@property @abstractmethod` (no metodos `get_*`) |
| Archivo | `patrones/estructurales/decorator/decorador_producto.py` |

**Definicion de Hecho:**
- [x] Dos propiedades abstractas declaradas con `@property @abstractmethod`.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-015: Implementar componente base concreto

**Como** desarrollador del sistema,
**quiero** una clase `ProductoConcreto` que sea el punto de partida de la cadena de decoradores,
**para** tener un componente base que devuelva nombre y precio originales sin ningun cargo adicional.

**Criterios de Aceptacion:**

1. `ProductoConcreto` hereda de `ComponenteProducto` con constructor `__init__(self, nombre: str, precio: float) -> None`.
2. Propiedad `descripcion -> str` retorna `self._nombre`.
3. Propiedad `precio -> float` retorna `self._precio`.
4. Implementa `__repr__(self) -> str` retornando `"ProductoConcreto('nombre', precio)"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `ProductoConcreto(ComponenteProducto)` |
| `__repr__` | `ProductoConcreto('Laptop HP', 899.99)` |
| Archivo | `patrones/estructurales/decorator/decorador_producto.py` |

**Definicion de Hecho:**
- [x] Implementa ambas propiedades abstractas.
- [x] `__repr__` implementado para depuracion.

---

### HU-016: Crear decorador base con delegacion

**Como** desarrollador del sistema,
**quiero** una clase `DecoradorProducto` que envuelva un `ComponenteProducto` y delegue a el por defecto,
**para** que los decoradores concretos solo sobreescriban lo que modifican, sin duplicar logica.

**Criterios de Aceptacion:**

1. `DecoradorProducto` hereda de `ComponenteProducto` con constructor `__init__(self, componente: ComponenteProducto) -> None`.
2. Propiedad `descripcion -> str` delega a `self._componente.descripcion`.
3. Propiedad `precio -> float` delega a `self._componente.precio`.
4. Las subclases solo necesitan sobreescribir la propiedad que modifican. La base es instanciable porque implementa ambas propiedades abstractas.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `DecoradorProducto(ComponenteProducto)` |
| Delegacion | `self._componente.descripcion` / `self._componente.precio` |
| Archivo | `patrones/estructurales/decorator/decorador_producto.py` |

**Definicion de Hecho:**
- [x] Delegacion implementada en ambas propiedades.
- [x] Subclases solo sobreescriben lo que cambian.

---

### HU-017: Agregar servicios opcionales apilables al producto

**Como** comprador en la tienda en linea,
**quiero** agregar envoltura de regalo, seguro y garantia extendida a mis productos de forma independiente y combinable,
**para** personalizar mi pedido sin que el sistema necesite una clase separada por cada combinacion.

**Criterios de Aceptacion:**

1. `EnvolturaRegalo(DecoradorProducto)` — constante `COSTO = 5.00`. Propiedad `precio -> float` retorna `round(self._componente.precio + self.COSTO, 2)`. Agrega `" + Envoltura de regalo"` a la descripcion.
2. `SeguroProducto(DecoradorProducto)` — constante `PORCENTAJE = 0.02`. Propiedad `precio -> float` retorna `round(self._componente.precio * (1 + self.PORCENTAJE), 2)`. El 2% se calcula sobre el **precio ya decorado** (no el base). Agrega `" + Seguro del producto"`.
3. `GarantiaExtendida(DecoradorProducto)` — constante `COSTO = 29.99`. Propiedad `precio -> float` retorna `round(self._componente.precio + self.COSTO, 2)`. Agrega `" + Garantía extendida (2 años)"`.
4. Se pueden apilar los 3 decoradores en cualquier orden sobre el mismo producto.
5. `round(..., 2)` se usa en todos los decoradores para precision monetaria.

**Datos Tecnicos:**

| Decorador | Cargo | Calculo |
|-----------|-------|---------|
| `EnvolturaRegalo` | +$5.00 fijo | `componente.precio + 5.00` |
| `SeguroProducto` | +2% variable | `componente.precio * 1.02` |
| `GarantiaExtendida` | +$29.99 fijo | `componente.precio + 29.99` |

| Elemento | Detalle |
|----------|---------|
| Archivo | `patrones/estructurales/decorator/decorador_producto.py` |
| Ejemplo apilado | Base $899.99 → +regalo → +seguro → +garantia = $953.08 |

**Definicion de Hecho:**
- [x] Tres decoradores concretos con `@property` para `descripcion` y `precio`.
- [x] `SeguroProducto` aplica el porcentaje sobre el precio ya decorado.
- [x] `round()` aplicado en los tres decoradores para precision monetaria.

---

## EPICA 5: Integracion de Sistemas de Envio (Patron Adapter)

> **Objetivo:** Integrar los sistemas de envio de DHL y FedEx, que tienen APIs propietarias incompatibles, bajo una interfaz unificada para que el codigo cliente use siempre los mismos metodos.
>
> **Patron aplicado:** Adapter (Object Adapter)
>
> **Archivos involucrados:** `patrones/estructurales/adapter/adaptador_envio.py`

---

### HU-018: Definir interfaz unificada de envio

**Como** desarrollador del sistema,
**quiero** una interfaz abstracta `SistemaEnvio` que todos los adaptadores implementen,
**para** que el codigo del carrito pueda calcular costos y crear envios sin saber que transportista esta usando.

**Criterios de Aceptacion:**

1. `SistemaEnvio` hereda de `ABC` y declara 3 metodos abstractos con type hints.
2. `calcular_costo(self, peso_kg: float, destino: str) -> float` — retorna costo en dolares.
3. `estimar_dias(self, destino: str) -> int` — retorna dias habiles estimados.
4. `crear_envio(self, pedido_id: str, destino: str) -> str` — retorna numero de guia/tracking.
5. No es posible instanciar `SistemaEnvio` directamente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `SistemaEnvio(ABC)` |
| Metodos | 3 abstractos con type hints completos |
| Archivo | `patrones/estructurales/adapter/adaptador_envio.py` |

**Definicion de Hecho:**
- [x] 3 metodos abstractos con firmas tipadas.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-019: Integrar el sistema de envio DHL

**Como** administrador de la tienda,
**quiero** usar el sistema DHL a traves del adaptador `AdaptadorDHL` con la misma interfaz que cualquier transportista,
**para** calcular tarifas y generar guias DHL sin que el codigo cliente conozca la API propietaria de DHL.

**Criterios de Aceptacion:**

1. `SistemaLegadoDHL` representa la API original de DHL con sus metodos propietarios:
   - `calcular_tarifa_dhl(gramos: int, ciudad_destino: str) -> float` (usa gramos, no kg)
   - `tiempo_entrega_dhl(ciudad: str) -> str` (retorna `"2-3 días hábiles"` como cadena)
   - `generar_guia(id_orden: str, ciudad: str) -> str`
2. `AdaptadorDHL` hereda de `SistemaEnvio` e implementa los 3 metodos:
   - `calcular_costo`: convierte `int(round(peso_kg * 1000))` → gramos (redondea, no trunca) y delega a `calcular_tarifa_dhl`.
   - `estimar_dias`: parsea `"2-3 días hábiles"` con `.split("-")[0]` → retorna `int`.
   - `crear_envio`: delega directamente a `generar_guia`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Adaptado | `SistemaLegadoDHL` |
| Conversion | kg × 1000 → gramos |
| Parseo tiempo | `"2-3 días hábiles".split("-")[0]` → `2` |
| Archivo | `patrones/estructurales/adapter/adaptador_envio.py` |

**Definicion de Hecho:**
- [x] Conversion de kg a gramos correcta.
- [x] Parseo de string de tiempo retorna el minimo como `int`.

---

### HU-020: Integrar el sistema de envio FedEx

**Como** administrador de la tienda,
**quiero** usar el sistema FedEx a traves del adaptador `AdaptadorFedEx` con la misma interfaz que DHL,
**para** cambiar o comparar transportistas sin modificar el codigo del carrito.

**Criterios de Aceptacion:**

1. `SistemaLegadoFedEx` representa la API de FedEx con metodos propietarios tipados:
   - `obtener_precio_fedex(libras: float, codigo_postal: str) -> float`
   - `dias_habiles(codigo_postal: str) -> int`
   - `registrar_paquete(num_orden: str, codigo_postal: str) -> str`
2. `AdaptadorFedEx` hereda de `SistemaEnvio` con constante de clase `KG_A_LIBRAS = 2.205`.
3. `calcular_costo`: convierte `round(peso_kg * 2.205, 3)` → libras y delega a `obtener_precio_fedex`.
4. `estimar_dias`: delega directamente a `dias_habiles`.
5. `crear_envio`: delega directamente a `registrar_paquete`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Adaptado | `SistemaLegadoFedEx` |
| Constante | `KG_A_LIBRAS = 2.205` (como constante de clase) |
| Conversion | `peso_kg * 2.205` → libras |
| Archivo | `patrones/estructurales/adapter/adaptador_envio.py` |

**Definicion de Hecho:**
- [x] Constante de conversion definida como atributo de clase.
- [x] Conversion kg → libras correcta con `round(..., 3)`.

---

### HU-021: Usar los adaptadores de forma transparente

**Como** desarrollador del sistema,
**quiero** que el codigo cliente use `AdaptadorDHL` y `AdaptadorFedEx` a traves de la interfaz `SistemaEnvio` sin saber cual transportista esta detras,
**para** demostrar que el patron Adapter desacopla la tienda de los sistemas de envio externos.

**Criterios de Aceptacion:**

1. Una funcion cliente recibe un `SistemaEnvio` generico y llama a `calcular_costo`, `estimar_dias` y `crear_envio` indistintamente.
2. El mismo codigo funciona con `AdaptadorDHL()` y con `AdaptadorFedEx()` sin cambios.
3. DHL recibe ciudad como destino; FedEx recibe codigo postal — el adaptador gestiona la diferencia.
4. Ambos adaptadores se demuestran en `main.py` en la seccion del Patron Adapter.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Demostracion en `main.py` | Seccion `>>> 7. PATRON ADAPTER <<<` |
| Entrada DHL | `peso_kg=2.5, destino="Buenos Aires"` |
| Entrada FedEx | `peso_kg=2.5, destino="1428"` (codigo postal) |
| Archivo | `patrones/estructurales/adapter/adaptador_envio.py` |

**Definicion de Hecho:**
- [x] Misma funcion cliente opera sobre ambos adaptadores.
- [x] Ambos transportistas demostrados en `main.py`.

---

## EPICA 6: Sistema de Notificaciones (Patron Observer)

> **Objetivo:** Implementar un mecanismo de suscripcion/publicacion donde la tienda notifique automaticamente a todos los clientes suscritos sobre nuevas ofertas.
>
> **Patron aplicado:** Observer (Publicador/Suscriptor)
>
> **Archivos involucrados:** `patrones/comportamiento/observer/observer.py`, `patrones/comportamiento/observer/tienda.py`

---

### HU-022: Definir contrato para observadores

**Como** desarrollador del sistema,
**quiero** que exista una interfaz abstracta `Observer` con el metodo `actualizar(mensaje: str) -> None`,
**para** establecer un contrato estandar con type hints que cualquier tipo de suscriptor debe cumplir.

**Criterios de Aceptacion:**

1. La clase `Observer` hereda de `ABC`.
2. Declara `actualizar(self, mensaje: str) -> None` con `@abstractmethod` y type hints.
3. No es posible instanciar `Observer` directamente (lanza `TypeError`).
4. Cualquier clase que herede de `Observer` debe implementar `actualizar()`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Observer(ABC)` |
| Firma abstracta | `actualizar(self, mensaje: str) -> None` |
| Archivo | `patrones/comportamiento/observer/observer.py` |

**Definicion de Hecho:**
- [x] Interfaz abstracta con type hints implementada.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-023: Crear clientes que reciben notificaciones

**Como** cliente de la tienda en linea,
**quiero** registrarme como observador con mi nombre y recibir notificaciones personalizadas,
**para** estar informado de las ofertas que me interesan.

**Criterios de Aceptacion:**

1. `Cliente` hereda de `Observer` con constructor `__init__(self, nombre: str) -> None`.
2. Implementa `actualizar(self, mensaje: str) -> None` imprimiendo: `"Cliente {nombre} recibió notificación: {mensaje}"`.
3. Expone `nombre` como `@property -> str` que retorna `self._nombre`.
4. Implementa `__repr__(self) -> str` retornando `"Cliente('nombre')"` para depuracion.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Cliente(Observer)` |
| Propiedad | `nombre -> str` |
| `__repr__` | `Cliente('Juan Perez')` |
| Salida notificacion | `Cliente Juan Perez recibió notificación: Nueva oferta: 50% descuento` |
| Archivo | `patrones/comportamiento/observer/observer.py` |

**Definicion de Hecho:**
- [x] Implementa `actualizar()` con nombre personalizado.
- [x] Propiedad `nombre` expuesta (no getter `get_nombre()`).
- [x] `__repr__` implementado.

---

### HU-024: Suscribir clientes a la tienda con validaciones

**Como** administrador de la tienda,
**quiero** que los clientes puedan suscribirse al sistema de notificaciones con validacion de tipo y sin duplicados,
**para** mantener una lista de suscriptores limpia y evitar errores en tiempo de notificacion.

**Criterios de Aceptacion:**

1. `Tienda` tiene constructor `__init__(self, nombre: str) -> None` y mantiene lista `_clientes: list`.
2. `suscribir(self, cliente: Observer) -> None` valida `isinstance(cliente, Observer)`.
3. Si **no es** `Observer`, lanza `TypeError` con mensaje: `"El objeto debe ser una instancia de Observer"`.
4. Si **ya esta suscrito**, imprime `"Cliente ya está suscrito a la tienda {nombre}"` sin agregarlo nuevamente.
5. Si pasa ambas validaciones, agrega e imprime `"Cliente suscrito a la tienda {nombre}"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `Tienda` |
| Import | `from typing import List` |
| Firma | `suscribir(self, cliente: Observer) -> None` |
| Validacion 1 | `isinstance(cliente, Observer)` → `TypeError` |
| Validacion 2 | `cliente in self._clientes` → rechazo silencioso |
| Archivo | `patrones/comportamiento/observer/tienda.py` |

**Definicion de Hecho:**
- [x] Valida tipo `Observer` con type hint en la firma.
- [x] Rechaza duplicados con mensaje informativo.

---

### HU-025: Desuscribir clientes de la tienda de forma segura

**Como** cliente suscrito,
**quiero** cancelar mi suscripcion a las notificaciones sin que el sistema falle,
**para** dejar de recibir alertas cuando ya no me interesen las ofertas.

**Criterios de Aceptacion:**

1. `desuscribir(self, cliente: Observer) -> None` verifica existencia antes de eliminar.
2. Si **no esta suscrito**, imprime `"Cliente no está suscrito a la tienda {nombre}"` sin lanzar excepcion.
3. Si **esta suscrito**, elimina con `list.remove()` e imprime `"Cliente desuscrito de la tienda {nombre}"`.
4. Tras desuscribirse, el cliente no recibe notificaciones posteriores.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firma | `desuscribir(self, cliente: Observer) -> None` |
| Verificacion | `if cliente not in self._clientes` (evita `ValueError`) |
| Archivo | `patrones/comportamiento/observer/tienda.py` |

**Definicion de Hecho:**
- [x] No lanza `ValueError` al desuscribir un cliente no suscrito.
- [x] Cliente desuscrito no recibe mas notificaciones.

---

### HU-026: Publicar ofertas y notificar automaticamente a suscriptores

**Como** administrador de la tienda,
**quiero** publicar una nueva oferta y que todos los clientes suscritos sean notificados automaticamente,
**para** maximizar el alcance de las promociones sin contactar a cada cliente individualmente.

**Criterios de Aceptacion:**

1. `nueva_oferta(self, descripcion: str) -> None` imprime `"¡Nueva oferta en {nombre_tienda}!"` y delega a `notificar_clientes()`.
2. `notificar_clientes(self, mensaje: str) -> None` imprime `"--- Notificando a {N} clientes ---"` y llama `actualizar(mensaje)` en cada suscriptor.
3. Si hay 3 suscritos, los 3 reciben la notificacion. Si uno se desuscribio, solo 2 la reciben.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firmas | `nueva_oferta(self, descripcion: str) -> None`, `notificar_clientes(self, mensaje: str) -> None` |
| Iteracion | `for cliente in list(self._clientes): cliente.actualizar(mensaje)` |
| Archivo | `patrones/comportamiento/observer/tienda.py` |

**Definicion de Hecho:**
- [x] Todos los suscritos reciben la notificacion.
- [x] Conteo de clientes notificados es correcto.

---

## EPICA 7: Carrito de Compras y Metodos de Pago (Patron Strategy)

> **Objetivo:** Permitir que los compradores agreguen productos a un carrito y seleccionen dinamicamente entre diferentes metodos de pago al momento del checkout, sin que el carrito conozca los detalles internos de cada metodo.
>
> **Patron aplicado:** Strategy
>
> **Archivos involucrados:** `patrones/comportamiento/strategy/estrategia_pago.py`, `patrones/comportamiento/strategy/carrito_compra.py`

---

### HU-027: Definir interfaz de estrategia de pago

**Como** desarrollador del sistema,
**quiero** una interfaz abstracta `EstrategiaPago` que defina el contrato para todos los metodos de pago,
**para** poder agregar nuevas formas de pago en el futuro sin modificar el carrito ni el flujo de checkout.

**Criterios de Aceptacion:**

1. `EstrategiaPago` hereda de `ABC` y declara `pagar(self, monto: float) -> None` con `@abstractmethod` y type hints.
2. No es posible instanciar `EstrategiaPago` directamente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `EstrategiaPago(ABC)` |
| Firma abstracta | `pagar(self, monto: float) -> None` |
| Archivo | `patrones/comportamiento/strategy/estrategia_pago.py` |

**Definicion de Hecho:**
- [x] Interfaz abstracta con type hints implementada.
- [x] Instanciacion directa lanza `TypeError`.

---

### HU-028: Pagar con tarjeta mostrando solo los ultimos 4 digitos

**Como** comprador en la tienda en linea,
**quiero** pagar con tarjeta de credito/debito y que el sistema solo muestre los ultimos 4 digitos,
**para** realizar transacciones electronicas sin exponer mi numero completo de tarjeta.

**Criterios de Aceptacion:**

1. `PagoTarjeta(EstrategiaPago)` con constructor `__init__(self, numero_tarjeta: str) -> None`.
2. `pagar(self, monto: float) -> None` extrae `self._numero_tarjeta[-4:]` y nunca muestra el numero completo.
3. Imprime: `"Pagando ${monto:.2f} con tarjeta terminada en {ultimos_4}"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoTarjeta(EstrategiaPago)` |
| Seguridad | Slicing `[-4:]` oculta datos sensibles |
| Salida | `Pagando $925.98 con tarjeta terminada en 9012` |
| Archivo | `patrones/comportamiento/strategy/estrategia_pago.py` |

**Definicion de Hecho:**
- [x] Solo muestra ultimos 4 digitos.
- [x] Type hints en constructor y `pagar()`.

---

### HU-029: Pagar en efectivo con descuento automatico del 5%

**Como** comprador en la tienda en linea,
**quiero** pagar en efectivo y recibir automaticamente un descuento del 5%,
**para** obtener un beneficio economico por elegir este metodo de pago.

**Criterios de Aceptacion:**

1. `PagoEfectivo(EstrategiaPago)` sin atributos propios.
2. `pagar(self, monto: float) -> None` calcula `round(monto * 0.95, 2)` usando `round()` para precision monetaria.
3. Imprime el monto original y el total con descuento en dos lineas.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoEfectivo(EstrategiaPago)` |
| Calculo | `round(monto * 0.95, 2)` (redondea a dos decimales) |
| Salida | `Total a pagar: $968.98` (no `$968.981`) |
| Archivo | `patrones/comportamiento/strategy/estrategia_pago.py` |

**Definicion de Hecho:**
- [x] `round()` aplicado para precision monetaria.
- [x] Muestra monto original y total con descuento.

---

### HU-030: Pagar con PayPal usando correo electronico

**Como** comprador en la tienda en linea,
**quiero** pagar a traves de PayPal usando mi correo electronico,
**para** realizar pagos digitales rapidos sin compartir datos de mi tarjeta.

**Criterios de Aceptacion:**

1. `PagoPayPal(EstrategiaPago)` con constructor `__init__(self, email: str) -> None`.
2. `pagar(self, monto: float) -> None` imprime: `"Pagando ${monto:.2f} con PayPal desde la cuenta: {email}"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `PagoPayPal(EstrategiaPago)` |
| Atributo | `_email: str` |
| Salida | `Pagando $1899.98 con PayPal desde la cuenta: usuario@email.com` |
| Archivo | `patrones/comportamiento/strategy/estrategia_pago.py` |

**Definicion de Hecho:**
- [x] Email se muestra correctamente.
- [x] Type hints en constructor y `pagar()`.

---

### HU-031: Agregar productos al carrito de compras

**Como** comprador en la tienda en linea,
**quiero** agregar productos de cualquier tipo a mi carrito,
**para** acumular los articulos que deseo comprar antes de pagar.

**Criterios de Aceptacion:**

1. `CarritoCompra` se inicializa con `_productos = []` y `_estrategia_pago = None`.
2. `agregar_producto(self, producto) -> None` anade el producto a la lista.
3. Imprime: `"Producto agregado al carrito: {producto.nombre}"` accediendo via **propiedad** (no `get_nombre()`).
4. Acepta cualquier objeto con `nombre`, `precio` y método invocable `mostrar_info()` (duck typing), coherente con HU-034.
5. Antes de agregar, valida el contrato y que el precio sea `int` o `float` finito y no negativo, excluyendo `bool`. Rechaza tipos incorrectos con `TypeError` y valores negativos/no finitos con `ValueError`, conservando los productos anteriores.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Acceso al nombre | `producto.nombre` (propiedad, no `get_nombre()`) |
| Firma | `agregar_producto(self, producto) -> None` |
| Archivo | `patrones/comportamiento/strategy/carrito_compra.py` |

**Definicion de Hecho:**
- [x] Usa `producto.nombre` via propiedad.
- [x] Acepta `Libro`, `Electronico` u otros productos con propiedad `nombre`.

---

### HU-032: Seleccionar metodo de pago dinamicamente

**Como** comprador en la tienda en linea,
**quiero** elegir o cambiar mi metodo de pago en cualquier momento antes del checkout,
**para** tener flexibilidad sin necesidad de crear un nuevo carrito.

**Criterios de Aceptacion:**

1. `set_estrategia_pago(self, estrategia_pago) -> None` establece la estrategia activa.
2. Se puede cambiar en cualquier momento antes de `checkout()`.
3. Acepta cualquier objeto que herede de `EstrategiaPago`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firma | `set_estrategia_pago(self, estrategia_pago) -> None` |
| Principio | Inyeccion de dependencia en tiempo de ejecucion |
| Archivo | `patrones/comportamiento/strategy/carrito_compra.py` |

**Definicion de Hecho:**
- [x] Estrategia se puede establecer y cambiar.
- [x] Checkout usa la ultima estrategia configurada.

---

### HU-033: Calcular el total del carrito automaticamente

**Como** comprador en la tienda en linea,
**quiero** que el sistema calcule automaticamente el total de mis productos,
**para** conocer el monto exacto antes de confirmar la compra.

**Criterios de Aceptacion:**

1. `calcular_total(self) -> float` recorre los productos, revalida cada **propiedad** `precio`, acumula y redondea a dos decimales. Rechaza precios inválidos y totales no finitos antes del pago.
2. Con carrito vacio retorna `0`.
3. Funciona correctamente con 1 o multiples productos.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firma | `calcular_total(self) -> float` |
| Implementacion | Acumulación de precios revalidados y `round(total, 2)` |
| Acceso precio | Via propiedad `precio` (no `get_precio()`) |
| Archivo | `patrones/comportamiento/strategy/carrito_compra.py` |

**Definicion de Hecho:**
- [x] Usa propiedad `precio` en la suma.
- [x] Carrito vacio retorna `0`.

---

### HU-034: Realizar checkout con resumen, pago y vaciado del carrito

**Como** comprador en la tienda en linea,
**quiero** finalizar mi compra con un checkout que muestre el resumen, procese el pago y vacie el carrito,
**para** completar mi compra de forma clara y que el carrito quede listo para una nueva compra.

**Criterios de Aceptacion:**

1. `checkout(self) -> None` con dos validaciones previas: carrito vacio e `_estrategia_pago is None`.
2. Muestra `"=== CHECKOUT ==="`, lista productos con `mostrar_info()` y muestra `"Total: ${total:.2f}"`.
3. Delega el pago a `self._estrategia_pago.pagar(total)`.
4. Imprime `"¡Compra completada!"` y resetea `_productos = []` y `_estrategia_pago = None`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Firma | `checkout(self) -> None` |
| Post-checkout | Vaciado de `_productos` y `_estrategia_pago` |
| Archivo | `patrones/comportamiento/strategy/carrito_compra.py` |

**Definicion de Hecho:**
- [x] Ambas validaciones funcionan.
- [x] Carrito se vacia despues del checkout exitoso.

---

## EPICA 8: Validacion de Pedidos en Cadena (Patron Chain of Responsibility)

> **Objetivo:** Validar un pedido a traves de multiples controles independientes (stock, pago, direccion, antifraude) de forma encadenada, donde cada validador decide si aprueba y delega al siguiente, o rechaza y detiene la cadena.
>
> **Patron aplicado:** Chain of Responsibility
>
> **Archivos involucrados:** `patrones/comportamiento/chain/validador_pedido.py`

---

### HU-035: Definir interfaz abstracta del validador

**Como** desarrollador del sistema,
**quiero** una clase abstracta `ValidadorPedido` con soporte de encadenamiento fluido,
**para** poder construir la cadena de validacion con la sintaxis `a.set_siguiente(b).set_siguiente(c)`.

**Criterios de Aceptacion:**

1. `ValidadorPedido(ABC)` con constructor `__init__(self) -> None` e inicializa `_siguiente = None`.
2. `set_siguiente(self, validador: "ValidadorPedido") -> "ValidadorPedido"` asigna `_siguiente` y **retorna el validador recibido** para permitir encadenamiento fluido.
3. `_pasar_al_siguiente(self, pedido: Dict[str, Any]) -> bool` retorna `True` si no hay siguiente (fin de cadena = aprobado) o delega al siguiente con `self._siguiente.validar(pedido)`.
4. Declara `validar(self, pedido: Dict[str, Any]) -> bool` como `@abstractmethod`.
5. El `pedido` es un `dict` con claves: `"productos"`, `"metodo_pago"`, `"direccion_envio"`, `"total"`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `ValidadorPedido(ABC)` |
| Import | `from typing import Dict, Any, Optional` |
| Encadenamiento | `set_siguiente()` retorna el handler recibido |
| Fin de cadena | `_pasar_al_siguiente` retorna `True` si no hay siguiente |
| Archivo | `patrones/comportamiento/chain/validador_pedido.py` |

**Definicion de Hecho:**
- [x] `set_siguiente()` retorna el validador (habilita encadenamiento fluido).
- [x] `_pasar_al_siguiente()` retorna `True` al final de la cadena.
- [x] Type hints `Dict[str, Any]` en todos los metodos.

---

### HU-036: Validar que el pedido contiene productos

**Como** administrador de la tienda,
**quiero** que el primer validador de la cadena verifique que el pedido contiene al menos un producto,
**para** rechazar pedidos vacios antes de procesar pago u otras validaciones.

**Criterios de Aceptacion:**

1. `ValidadorStock(ValidadorPedido)` implementa `validar(self, pedido: Dict[str, Any]) -> bool`.
2. Requiere un pedido de tipo `dict` y una lista no vacía en `productos`; rechaza campos ausentes, `None` y otros tipos devolviendo `False`.
3. Si esta vacia, imprime `"  [Stock] RECHAZADO: el pedido no contiene productos."` y retorna `False`.
4. Si tiene productos, imprime `"  [Stock] OK: {N} producto(s) en el pedido."` y llama a `self._pasar_al_siguiente(pedido)`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Clase | `ValidadorStock(ValidadorPedido)` |
| Validacion | `if not productos` |
| Archivo | `patrones/comportamiento/chain/validador_pedido.py` |

**Definicion de Hecho:**
- [x] Rechaza pedidos sin productos.
- [x] Delega al siguiente si hay productos.

---

### HU-037: Validar el metodo de pago del pedido

**Como** administrador de la tienda,
**quiero** que el sistema rechace pedidos con metodos de pago no habilitados,
**para** asegurar que solo se procesen pagos con metodos soportados por la tienda.

**Criterios de Aceptacion:**

1. `ValidadorPago(ValidadorPedido)` tiene constante `METODOS_ACEPTADOS = {"tarjeta", "efectivo", "paypal"}`.
2. Normaliza con `.strip().lower()` y verifica `metodo not in self.METODOS_ACEPTADOS`.
3. Si invalido, imprime `"  [Pago] RECHAZADO: método '{metodo}' no está habilitado. Aceptados: {lista}."` y retorna `False`.
4. Si valido, imprime `"  [Pago] OK: método '{metodo}' aceptado."` y delega al siguiente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Constante | `METODOS_ACEPTADOS = {"tarjeta", "efectivo", "paypal"}` |
| Normalizacion | `.lower()` (case-insensitive) |
| Archivo | `patrones/comportamiento/chain/validador_pedido.py` |

**Definicion de Hecho:**
- [x] Constante como `set` para busqueda O(1).
- [x] Comparacion case-insensitive.

---

### HU-038: Validar la direccion de envio del pedido

**Como** administrador de la tienda,
**quiero** que el sistema rechace pedidos con direcciones de envio incompletas,
**para** asegurar que los paquetes puedan ser entregados correctamente.

**Criterios de Aceptacion:**

1. `ValidadorDireccion(ValidadorPedido)` tiene constante `LONGITUD_MINIMA = 10`.
2. Aplica `.strip()` y verifica `len(direccion) < LONGITUD_MINIMA`.
3. Si invalida, imprime `"  [Dirección] RECHAZADO: dirección incompleta (mínimo {N} caracteres)."` y retorna `False`.
4. Si valida, imprime `"  [Dirección] OK: '{direccion}'."` y delega al siguiente.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Constante | `LONGITUD_MINIMA = 10` |
| Normalizacion | `.strip()` elimina espacios externos |
| Archivo | `patrones/comportamiento/chain/validador_pedido.py` |

**Definicion de Hecho:**
- [x] Constante configurable para el minimo de caracteres.
- [x] `.strip()` antes de la validacion.

---

### HU-039: Validar que el monto no supere el limite antifraude

**Como** administrador de la tienda,
**quiero** que el ultimo validador de la cadena rechace pedidos con montos sospechosamente altos,
**para** prevenir posibles fraudes o errores antes de procesar el pago.

**Criterios de Aceptacion:**

1. `ValidadorFraude(ValidadorPedido)` tiene constante `MONTO_MAXIMO = 5000.00`.
2. Obtiene el total con `pedido.get("total", 0)`: ausente equivale a cero. Rechaza tipos distintos de `int`/`float`, booleanos, valores no finitos y negativos devolviendo `False`.
3. Si `total > MONTO_MAXIMO`, imprime `"  [Antifraude] RECHAZADO: total ${total:.2f} supera el límite de ${MONTO_MAXIMO:.2f}."` y retorna `False`.
4. Si dentro del limite, imprime `"  [Antifraude] OK: total ${total:.2f} dentro del limite permitido."` y llama `_pasar_al_siguiente(pedido)`.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Constante | `MONTO_MAXIMO = 5000.00` |
| Formato salida | `:.2f` para valores monetarios |
| Posicion en cadena | Ultimo eslabón recomendado |
| Archivo | `patrones/comportamiento/chain/validador_pedido.py` |

**Definicion de Hecho:**
- [x] Constante configurable para el limite antifraude.
- [x] Rechaza montos superiores a $5000.00.

---

## EPICA 9: Demostracion Integral del Sistema (8 Patrones)

> **Objetivo:** Integrar los 8 patrones en un programa principal ejecutable que demuestre el funcionamiento completo del sistema de e-commerce con inter-operacion entre patrones.
>
> **Archivo involucrado:** `main.py`

---

### HU-040: Ejecutar demostracion completa de los 8 patrones

**Como** estudiante o evaluador del sistema,
**quiero** ejecutar un unico archivo `main.py` que demuestre los 8 patrones en secuencia con secciones claramente delimitadas,
**para** observar el funcionamiento integral del sistema y comprender cada patron en un contexto practico de e-commerce.

**Criterios de Aceptacion:**

1. Se ejecuta con `python main.py` sin errores ni excepciones.
2. Muestra encabezado y pie con separadores `"=" * 50`.
3. **Seccion 1 Singleton:** Crea dos instancias, verifica `db1 is db2` y obtiene `True`, ejecuta una query.
4. **Seccion 2 Factory Method:** Crea 2 libros y 2 electronicos via `CreadorLibro` y `CreadorElectronico` (`registrar_producto()`). Demuestra propiedades `nombre` y `precio`.
5. **Seccion 3 Observer:** 3 clientes suscritos reciben primera oferta; uno se desuscribe; 2 reciben la segunda oferta.
6. **Seccion 4 Strategy:** 3 carritos con metodos de pago diferentes (tarjeta, efectivo, PayPal); cada uno hace checkout completo. Productos reutilizados del paso Factory.
7. **Seccion 5 Builder:** Pedido simple con `PedidoEstandarBuilder`; pedido de regalo con `PedidoExpressBuilder` (envoltura + seguro). Director orquesta ambos.
8. **Seccion 6 Decorator:** Producto base apilado con `EnvolturaRegalo` → `SeguroProducto` → `GarantiaExtendida`; se muestra `descripcion` y `precio` acumulados via propiedades en cada paso.
9. **Seccion 7 Adapter:** Misma funcion cliente cotiza envio con `AdaptadorDHL` y `AdaptadorFedEx` usando la interfaz `SistemaEnvio`.
10. **Seccion 8 Chain:** Cadena `ValidadorStock → ValidadorPago → ValidadorDireccion → ValidadorFraude` evaluada con 3 casos: pedido valido (APROBADO), metodo de pago invalido (RECHAZADO en ValidadorPago), monto excesivo (RECHAZADO en ValidadorFraude).
11. No requiere dependencias externas. Compatible con Python 3.6+.

**Datos Tecnicos:**

| Elemento | Detalle |
|----------|---------|
| Archivo | `main.py` |
| Ejecucion | `python main.py` |
| Secciones | 8 patrones + encabezado/pie |
| Reutilizacion inter-patron | `libro1`, `laptop`, `telefono` usados en Factory, Strategy, Builder |
| Imports | Organizados en 3 bloques: creacionales, estructurales, comportamiento |
| Dependencias | Solo biblioteca estandar de Python (`abc`, `typing`, `threading`, `unicodedata`, `math`) |

**Definicion de Hecho:**
- [x] Ejecucion completa sin errores.
- [x] Los 8 patrones se demuestran en orden.
- [x] Productos del Factory reutilizados en Strategy y Builder.
- [x] Decorator usa propiedades `.descripcion` y `.precio` (no `.get_descripcion()` / `.get_precio()`).

---

## Limites numericos y referencias externas

Los precios y pesos deben ser representables como float finito. Los enteros que
exceden ese rango se rechazan con `ValueError` (o `False` en antifraude).
Las conversiones de envío, tarifa FedEx, total del carrito, total del pedido y
precio con seguro se comprueban también después del cálculo: una entrada finita
no garantiza que la suma o multiplicación resulte finita.

Carrito y Pedido almacenan referencias, no copias de los productos. Revalidan
los precios al calcular; si un producto externo cambia a un valor inválido, se
rechaza el cálculo. El carrito conserva sus productos y estrategia ante ese error.

`patrones/_numeros.py` centraliza la comprobación del rango, sin imports entre
categorías. `tests/test_documentacion.py` comprueba ejemplos y salida del README.

## Precisiones de validacion (revision de robustez)

- HU-005/HU-015: precios `int`/`float` finitos no negativos; `bool` no es un precio.
- HU-010/HU-011/HU-012: los builders comprueban nombre/precio antes de agregar y
  conservan el pedido si la entrada es inválida. Admiten productos por duck typing.
- HU-019/HU-020: los adaptadores requieren peso `int`/`float` finito mayor que cero;
  tipos incorrectos (incluido bool) producen `TypeError`; valores inválidos, `ValueError`.
- HU-031/HU-034: el contrato incluye `mostrar_info()`; un pago que lanza una excepción
  conserva productos y estrategia para reintentar.
- HU-035 a HU-039: entradas que no son diccionarios se rechazan con `False`.
- `round()` redondea resultados, pero no garantiza representación decimal exacta.

## Matriz de Trazabilidad

### Historias de Usuario por Archivo

| Archivo | Historias Relacionadas |
|---------|----------------------|
| `patrones/creacionales/singleton/database_connection.py` | HU-001, HU-002, HU-003, HU-004 |
| `patrones/creacionales/factory/producto.py` | HU-005, HU-006, HU-007 |
| `patrones/creacionales/factory/creador_producto.py` | HU-008 |
| `patrones/creacionales/builder/pedido.py` | HU-009 |
| `patrones/creacionales/builder/pedido_builder.py` | HU-010, HU-011, HU-012, HU-013 |
| `patrones/estructurales/decorator/decorador_producto.py` | HU-014, HU-015, HU-016, HU-017 |
| `patrones/estructurales/adapter/adaptador_envio.py` | HU-018, HU-019, HU-020, HU-021 |
| `patrones/comportamiento/observer/observer.py` | HU-022, HU-023 |
| `patrones/comportamiento/observer/tienda.py` | HU-024, HU-025, HU-026 |
| `patrones/comportamiento/strategy/estrategia_pago.py` | HU-027, HU-028, HU-029, HU-030 |
| `patrones/comportamiento/strategy/carrito_compra.py` | HU-031, HU-032, HU-033, HU-034 |
| `patrones/comportamiento/chain/validador_pedido.py` | HU-035, HU-036, HU-037, HU-038, HU-039 |
| `main.py` | HU-040 |

### Historias de Usuario por Patron y Epica

| Patron GoF | Categoria | Epica | Historias | Cantidad |
|------------|-----------|-------|-----------|----------|
| Singleton | Creacional | Epica 1 | HU-001 a HU-004 | 4 |
| Factory Method | Creacional | Epica 2 | HU-005 a HU-008 | 4 |
| Builder | Creacional | Epica 3 | HU-009 a HU-013 | 5 |
| Decorator | Estructural | Epica 4 | HU-014 a HU-017 | 4 |
| Adapter | Estructural | Epica 5 | HU-018 a HU-021 | 4 |
| Observer | Comportamiento | Epica 6 | HU-022 a HU-026 | 5 |
| Strategy | Comportamiento | Epica 7 | HU-027 a HU-034 | 8 |
| Chain | Comportamiento | Epica 8 | HU-035 a HU-039 | 5 |
| Demo integral | Transversal | Epica 9 | HU-040 | 1 |
| **Total** | | | | **40** |

### Historias por Rol

| Rol | Historias | Cantidad |
|-----|-----------|----------|
| Desarrollador | HU-001, HU-002, HU-003, HU-004, HU-005, HU-008, HU-009, HU-010, HU-013, HU-014, HU-015, HU-016, HU-018, HU-021, HU-022, HU-027, HU-035 | 17 |
| Comprador | HU-006, HU-007, HU-011, HU-012, HU-017, HU-028, HU-029, HU-030, HU-031, HU-032, HU-033, HU-034 | 12 |
| Administrador de tienda | HU-019, HU-020, HU-024, HU-026, HU-036, HU-037, HU-038, HU-039 | 8 |
| Cliente (de la tienda / suscrito) | HU-023, HU-025 | 2 |
| Estudiante / Evaluador | HU-040 | 1 |
| **Total** | | **40** |

### Mejoras tecnicas reflejadas en esta version

| Mejora | Historias impactadas | Descripcion |
|--------|---------------------|-------------|
| `@property` | HU-005, HU-006, HU-007, HU-014, HU-015, HU-023, HU-031, HU-033 | `nombre`, `precio`, `descripcion` expuestos como propiedades Python |
| Type hints | Todas las HUs | Firmas con `param: tipo` y `-> retorno` en todos los metodos |
| `__repr__` | HU-006, HU-007, HU-009, HU-015, HU-023 | `Libro`, `Electronico`, `Pedido`, `ProductoConcreto`, `Cliente` |
| 3-level paths | Todas las HUs | `patrones/<categoria>/<patron>/archivo.py` |
| Thread-safety | HU-001, HU-002 | `threading.Lock` de clase con double-checked locking en `__new__` y lock en `__init__` |
| Validacion de precios | HU-005, HU-015 | `Producto` y `ProductoConcreto` requieren int/float finito no negativo; excluyen bool. Tipo inválido: `TypeError`; valor negativo/no finito: `ValueError` |
| Formato monetario | HU-006, HU-007, HU-028, HU-029, HU-030, HU-034 | Montos impresos con 2 decimales (`:.2f`); `calcular_total()` del carrito redondea a 2 decimales |
| Normalizacion de ciudades | HU-019 | DHL compara ciudades sin distinguir mayusculas, espacios externos ni tildes (`unicodedata`) |
| Notificacion segura | HU-026 | `notificar_clientes()` recorre una copia de la lista: desuscribirse durante la notificacion no saltea a otros |
| Validacion de estrategia | HU-032 | `set_estrategia_pago()` lanza `TypeError` si el objeto no es `EstrategiaPago` |
| Cadena robusta | HU-035 a HU-039 | `set_siguiente()` rechaza ciclos (`ValueError`); los validadores rechazan pedidos que no son dict y campos inválidos; Stock exige lista no vacía; Fraude rechaza totales no finitos o negativos, pero total ausente equivale a cero por HU-039; `ValidadorPago` lista los metodos con `sorted()` |
| Suite de tests | Todas las HUs | `python -m unittest discover -s tests -t .`: tests por patron, criterios de HU-040, convenciones y doctests |

---

*Documento generado a partir del analisis del codigo fuente implementado.*
*Las marcas de cumplimiento describen la implementación; no sustituyen la ejecución de pruebas en cada versión objetivo de Python.*
*Version 3.0 — refleja la arquitectura con 8 patrones GoF organizados en 3 categorias.*
