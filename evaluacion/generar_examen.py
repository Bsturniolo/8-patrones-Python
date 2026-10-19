"""Genera el examen autónomo y su clave docente con biblioteca estándar."""
import html
from pathlib import Path


def opcion(texto, correcta, *distractores):
    """Define un inciso de selección única."""
    return (texto, str(correcta), [str(correcta)] + list(distractores))


def numero(texto, correcta):
    """Define un inciso numérico sin unidades."""
    return (texto, str(correcta), None)


PREGUNTAS = []


def pregunta(tema, titulo, contexto, codigo, a, b, explicacion):
    """Registra un caso con dos incisos y su fundamentación."""
    PREGUNTAS.append((tema, titulo, contexto, codigo, [a, b], explicacion))


pregunta('Singleton', 'Una conexión compartida',
 'Se ejecuta en un proceso nuevo. Considerá solo el resultado del print final.',
 'db1 = DatabaseConnection.get_instance()\ndb2 = DatabaseConnection()\nprint(db1 is db2)',
 opcion('Resultado del print:', 'True', 'False', 'None', 'TypeError'),
 numero('Cantidad de mensajes «Conexión a BD creada»:', 1),
 '__new__ reutiliza la instancia y la bandera _initialized evita repetir la inicialización.')
pregunta('Singleton', 'Dónde se controla la identidad',
 'Completá las responsabilidades de los métodos de DatabaseConnection.',
 'class DatabaseConnection:\n    def (1)(cls):\n        # crea o devuelve la única instancia\n        ...\n    def __init__(self):\n        # comprueba la bandera (2)\n        ...',
 opcion('Hueco (1):', '__new__', '__repr__', 'query', '__del__'),
 opcion('Hueco (2):', '_initialized', '_clientes', '_siguiente', '_productos'),
 'Python puede invocar __init__ cada vez que se llama al constructor, aunque __new__ devuelva el mismo objeto.')
pregunta('Singleton', 'Qué hace realmente query',
 'El equipo quiere ejecutar una consulta en la demostración del TP.',
 'db = DatabaseConnection.get_instance()\nr = db.query("SELECT * FROM productos")',
 opcion('La implementación de query:', 'Imprime el SQL como simulación', 'Abre una conexión MySQL real', 'Retorna filas de SQLite', 'Crea la tabla productos'),
 opcion('Valor de r:', 'None', '[]', 'True', 'Un cursor de base de datos'),
 'El TP no se conecta a una base real: query usa print y no contiene un return de resultados.')
pregunta('Factory Method', 'Crear sin elegir por cadenas',
 'Completá el uso de la API actual para crear un libro de Ana.',
 'creador = (1)("Ana")\np = creador.crear_producto("Patrones", 20.0)\nprint(p.(2))',
 opcion('Hueco (1):', 'CreadorLibro', 'ProductoFactory', 'CreadorProducto', 'Libro'),
 opcion('Hueco (2), para leer el precio:', 'precio', 'get_precio()', 'precio()', '_autor'),
 'CreadorLibro decide crear un Libro. El precio se expone mediante una propiedad de solo lectura.')
pregunta('Factory Method', 'Registrar un electrónico',
 'Se crea y muestra un producto en una sola operación.',
 'p = CreadorElectronico(24).registrar_producto("Tablet", 300.0)',
 opcion('Clase concreta de p:', 'Electronico', 'CreadorElectronico', 'ProductoFactory', 'Pedido'),
 opcion('Acción de registrar_producto además de crear:', 'Invoca mostrar_info() y devuelve el producto', 'Lo agrega al carrito automáticamente', 'Lo guarda en MySQL', 'Retorna únicamente el precio'),
 'La operación del creador usa el factory method y luego trabaja con la interfaz Producto; no conoce la clase concreta.')
pregunta('Factory Method', 'Un nuevo producto del catálogo',
 'Se incorpora Ropa, con su propio mostrar_info(), sin cambiar los creadores existentes.',
 'class Ropa((1)):\n    def mostrar_info(self): ...\n\nclass CreadorRopa((2)):\n    def crear_producto(self, nombre, precio):\n        return Ropa(nombre, precio)',
 opcion('Base (1):', 'Producto', 'CreadorProducto', 'PedidoBuilder', 'Observer'),
 opcion('Base (2):', 'CreadorProducto', 'Libro', 'CarritoCompra', 'ComponenteProducto'),
 'Se extienden el producto y el creador. La decisión de construcción queda en la nueva subclase, sin agregar un if central.')
pregunta('Builder', 'Pedido estándar simple',
 'El builder es nuevo. El libro cuesta 100 y no se agregan extras.',
 'p = CreadorLibro().crear_producto("TP", 100.0)\nd = DirectorPedido(PedidoEstandarBuilder())\npedido = d.construir_pedido_simple([p], "Calle Falsa 123")\ntotal = pedido.calcular_total()',
 numero('Costo de envío estándar:', 5), numero('Valor de total:', 105),
 'El pedido simple suma el subtotal de productos y el envío estándar de $5.')
pregunta('Builder', 'Regalo con seguro',
 'El builder es nuevo. El director activa envoltura y seguro del pedido.',
 'p = CreadorLibro().crear_producto("TP", 100.0)\nd = DirectorPedido(PedidoEstandarBuilder())\npedido = d.construir_pedido_regalo([p], "Calle Falsa 123", "¡Felicitaciones!")',
 numero('Importe del seguro del pedido:', 3), numero('Total del pedido:', 113),
 'Builder aplica 3% al subtotal: 100 + 5 de envío + 5 de envoltura + 3 de seguro = 113. No usa el 2% de Decorator.')
pregunta('Builder', 'Cambiar la modalidad de construcción',
 'El director ya existe; ahora se necesita envío express para un libro de $100.',
 'd = DirectorPedido(PedidoEstandarBuilder())\nd.(1)(PedidoExpressBuilder())\npedido = d.construir_pedido_simple([libro_de_100], "Calle Falsa 123")',
 opcion('Hueco (1):', 'set_builder', 'set_estrategia_pago', 'set_siguiente', 'suscribir'),
 numero('Total express sin extras:', 115),
 'set_builder reemplaza el constructor que utiliza el director. El builder express cobra $15 de envío.')
pregunta('Decorator', 'Envolver un producto',
 'Se ofrece envoltura para un producto de $10.',
 'base = ProductoConcreto("Libro", 10.0)\nregalo = EnvolturaRegalo(base)',
 numero('regalo.precio:', 15), numero('base.precio después de decorar:', 10),
 'El decorador envuelve el componente y suma $5 al consultar su precio. No cambia el precio del objeto base.')
pregunta('Decorator', 'Servicios acumulados',
 'Calculá los resultados usando las reglas del TP.',
 'p = ProductoConcreto("Laptop", 100.0)\np = SeguroProducto(p)\ncon_seguro = p.precio\np = GarantiaExtendida(p)',
 numero('con_seguro:', 102), numero('Precio final con garantía:', 131.99),
 'El seguro agrega 2% al precio actual y la garantía extendida suma $29.99.')
pregunta('Decorator', 'El contrato del componente',
 'Un cliente trabaja con productos simples o decorados mediante el mismo contrato.',
 'def mostrar(p):\n    print(p.descripcion)\n    print(p.precio)',
 opcion('Interfaz común:', 'ComponenteProducto', 'CreadorProducto', 'EstrategiaPago', 'SistemaEnvio'),
 opcion('En las clases del TP, descripcion y precio son:', 'Propiedades', 'Métodos que requieren ()', 'Variables globales', 'Métodos estáticos'),
 'ComponenteProducto define ambas propiedades abstractas. Los componentes concretos y decoradores las implementan.')
pregunta('Adapter', 'Cotizar DHL desde kilogramos',
 'DHL legado cobra 3 + gramos × 0.008. La interfaz del adaptador recibe kilogramos.',
 'a = AdaptadorDHL()\ncosto = a.calcular_costo(2.5, "Buenos Aires")\ndias = a.estimar_dias("Buenos Aires")',
 numero('costo:', 23), numero('dias:', 2),
 '2.5 kg equivalen a 2500 g. La tarifa es 3 + 20. El adaptador extrae 2 de «2-3 días hábiles».')
pregunta('Adapter', 'Un cliente, dos transportistas',
 'Se quiere invocar el mismo conjunto de métodos para DHL y FedEx.',
 'def cotizar(sistema, peso, destino):\n    return sistema.calcular_costo(peso, destino)',
 opcion('Contrato que implementan ambos adaptadores:', 'SistemaEnvio', 'SistemaLegadoDHL', 'PedidoBuilder', 'Producto'),
 opcion('Significado de destino según el TP:', 'Ciudad en DHL y código postal en FedEx', 'Ciudad en ambos', 'Código postal en ambos', 'Siempre un objeto Pedido'),
 'Adapter unifica las operaciones, pero este TP conserva la diferencia semántica del destino; no implementa geocodificación.')
pregunta('Observer', 'Evitar suscripciones repetidas',
 'Se intenta suscribir dos veces el mismo objeto.',
 't = Tienda("Cortez")\nc = Cliente("Ana")\nt.suscribir(c)\nt.suscribir(c)\nt.nueva_oferta("Libros al 20%")',
 numero('Clientes en t._clientes:', 1), numero('Llamadas a c.actualizar por esa oferta:', 1),
 'Tienda detecta que el mismo cliente ya está en la lista y no lo vuelve a agregar.')
pregunta('Observer', 'Agregar otro tipo de observador',
 'Completá el contrato para recibir los mensajes publicados por Tienda.',
 'class PanelOfertas((1)):\n    def (2)(self, mensaje):\n        print("PANEL:", mensaje)',
 opcion('Base (1):', 'Observer', 'Tienda', 'EstrategiaPago', 'ValidadorPedido'),
 opcion('Método (2):', 'actualizar', 'pagar', 'crear_producto', 'build'),
 'Tienda invoca actualizar(mensaje) y exige que el suscriptor sea una instancia de Observer.')
pregunta('Strategy', 'Pagar en efectivo',
 'El carrito contiene un único libro de $100. La compra finaliza sin errores.',
 'c = CarritoCompra()\nc.agregar_producto(CreadorLibro().crear_producto("TP", 100.0))\nc.set_estrategia_pago(PagoEfectivo())\nc.checkout()',
 numero('Importe final anunciado por PagoEfectivo:', 95),
 opcion('Estado después de checkout:', 'Productos vacíos y estrategia None', 'Productos vacíos y PagoEfectivo conservado', 'Productos y estrategia conservados', 'El carrito se convierte en Pedido'),
 'PagoEfectivo descuenta 5%. Tras pagar correctamente, checkout reinicia tanto los productos como la estrategia.')
pregunta('Strategy', 'Cambiar el algoritmo de pago',
 'El carrito tiene productos válidos y se selecciona un método dos veces antes del checkout.',
 'c.set_estrategia_pago(PagoEfectivo())\nc.set_estrategia_pago(PagoPayPal("ana@example.com"))\nc.checkout()',
 opcion('Estrategia ejecutada:', 'PagoPayPal', 'PagoEfectivo', 'Las dos', 'Ninguna: no se puede cambiar'),
 opcion('Rol de CarritoCompra:', 'Contexto', 'Estrategia concreta', 'Adaptado legado', 'Producto del Builder'),
 'El contexto mantiene una referencia a la estrategia actual; la segunda asignación reemplaza la primera.')
pregunta('Chain of Responsibility', 'Enlazar validadores',
 'Se construye la cadena por medio de llamadas fluidas.',
 'a = ValidadorStock()\nb = ValidadorPago()\nc = ValidadorDireccion()\nr = a.set_siguiente(b)\nr.set_siguiente(c)',
 opcion('r es el mismo objeto que:', 'b', 'a', 'c', 'None'),
 opcion('Orden resultante:', 'Stock → Pago → Dirección', 'Stock → Dirección → Pago', 'Pago → Stock → Dirección', 'Stock → Dirección; Pago queda fuera'),
 'set_siguiente devuelve el manejador recibido; por eso la siguiente llamada enlaza desde b y no desde a.')
pregunta('Chain of Responsibility', 'Cortar un pedido vacío',
 'Se inicia la validación desde stock.',
 'stock = ValidadorStock()\nstock.set_siguiente(ValidadorPago())\nr = stock.validar({"productos": [], "metodo_pago": "tarjeta"})',
 opcion('Valor de r:', 'False', 'True', 'None', 'TypeError'),
 numero('Veces que se ejecuta ValidadorPago.validar:', 0),
 'Stock rechaza la lista vacía y devuelve False sin delegar. No se evalúan los manejadores posteriores.')

# Nivel 2: diagnóstico, límites e interacción entre objetos.
pregunta('Singleton', 'Inicializar una sola vez',
 'Un compañero elimina la comprobación de _initialized de __init__, pero conserva __new__.',
 'db1 = DatabaseConnection()\ndb2 = DatabaseConnection()\n# Variante propuesta: __init__ imprime siempre el mensaje de creación.',
 opcion('En esa variante, db1 is db2:', 'True', 'False', 'None', 'Depende del SQL'),
 numero('Mensajes de creación en esa variante, con dos llamadas secuenciales:', 2),
 'Controlar la identidad no evita invocar __init__. La bandera protege los efectos de inicialización, no la identidad.')
pregunta('Singleton', 'Creación concurrente',
 'Dos hilos intentan obtener la conexión por primera vez. Analizá la implementación actual.',
 'if cls._instance is None:\n    with cls._lock:\n        if cls._instance is None:\n            cls._instance = super().__new__(cls)',
 opcion('Razón de repetir el chequeo dentro del lock:', 'Otro hilo pudo crear la instancia mientras este esperaba', 'El lock borra la instancia', 'Evita usar __init__', 'Abre dos conexiones en paralelo'),
 opcion('Alcance real de esta instancia compartida:', 'El proceso de Python actual', 'Todos los procesos del sistema', 'Todos los equipos de la red', 'La base de datos remota'),
 'El segundo chequeo evita crear otra instancia tras esperar el bloqueo. Las variables de clase no comparten objetos entre procesos.')
pregunta('Factory Method', 'Polimorfismo del creador',
 'Se ejecuta la misma operación para dos creadores distintos.',
 'creadores = [CreadorLibro("Ana"), CreadorElectronico(24)]\nproductos = [c.registrar_producto("X", 10.0) for c in creadores]',
 opcion('Tipos de productos, en orden:', 'Libro, Electronico', 'Producto, Producto', 'CreadorLibro, CreadorElectronico', 'Libro, Libro'),
 opcion('Quién decide la clase concreta:', 'La implementación de crear_producto de cada subclase', 'registrar_producto mediante un if por nombre', 'El precio recibido', 'El módulo main mediante una conexión SQL'),
 'registrar_producto reutiliza un flujo común y despacha crear_producto polimórficamente.')
pregunta('Factory Method', 'Contrato de precios y propiedades',
 'Evaluá las dos líneas de manera independiente.',
 '# Caso A\nCreadorLibro().crear_producto("X", -1.0)\n# Caso B\np = CreadorLibro().crear_producto("X", 10.0)\np.precio = 20.0',
 opcion('Caso A:', 'ValueError', 'Crea el producto', 'TypeError', 'Retorna None'),
 opcion('Caso B:', 'AttributeError', 'Actualiza el precio', 'Crea otro producto', 'Devuelve False'),
 'El constructor rechaza precios negativos. La propiedad precio no declara setter: asignarle un valor produce AttributeError.')
pregunta('Builder', 'Reutilizar sin mezclar pedidos',
 'El mismo builder produce dos pedidos consecutivos.',
 'b = PedidoEstandarBuilder()\nb.agregar_producto(CreadorLibro().crear_producto("X", 10.0))\np1 = b.build()\np2 = b.build()',
 numero('p1.calcular_total():', 15), numero('p2.calcular_total():', 5),
 'build devuelve el pedido anterior y crea otro vacío. El segundo build aplica igualmente el envío de $5; no conserva los productos del primero.')
pregunta('Builder', 'La etiqueta personalizada',
 'Se configura una etiqueta antes de construir, sin agregar productos.',
 'b = PedidoExpressBuilder()\nb.set_tipo_envio("Retiro local")\np = b.build()',
 opcion('Etiqueta final del pedido:', 'Express (1 día hábil)', 'Retiro local', 'Estándar (5 días hábiles)', 'None'),
 numero('p.calcular_total():', 15),
 'Según el contrato del TP, build vuelve a aplicar TIPO_ENVIO y COSTO_ENVIO del builder. set_tipo_envio no cambia esa política.')
pregunta('Decorator', 'El orden cambia el precio',
 'Ambas expresiones parten de un producto de $100.',
 'base = ProductoConcreto("X", 100.0)\na = SeguroProducto(EnvolturaRegalo(base))\nb = EnvolturaRegalo(SeguroProducto(base))',
 numero('a.precio:', 107.10), numero('b.precio:', 107),
 'En a, el seguro grava 105: 105 × 1.02 = 107.10. En b, primero se asegura 100 y luego se suman 5: 107.00.')
pregunta('Decorator', 'Un envoltorio sin recargo',
 'Se instancia directamente la clase base del decorador del TP.',
 'base = ProductoConcreto("X", 10.0)\nd = DecoradorProducto(base)',
 opcion('Resultado de la construcción:', 'Se crea un decorador que delega', 'TypeError por clase abstracta', 'Se crea un Libro', 'ValueError por faltar seguro'),
 numero('d.precio:', 10),
 'DecoradorProducto implementa las dos propiedades abstractas. Por eso es instanciable y delega sin sumar recargos.')
pregunta('Adapter', 'FedEx y las unidades',
 'La conversión es round(kg × 2.205, 3). La tarifa es round(2.50 + libras × 1.20, 2).',
 'a = AdaptadorFedEx()\ncosto = a.calcular_costo(1.0, "1428")\ndias = a.estimar_dias("5000")',
 numero('costo:', 5.15), numero('dias:', 3),
 'Un kilogramo se convierte en 2.205 libras y cuesta 5.15. El código 5000 no empieza con 1, por lo que demora 3 días.')
pregunta('Adapter', 'Redondeo y normalización',
 'Se cotiza un paquete liviano y se estima una ciudad escrita con espacios y tilde.',
 'a = AdaptadorDHL()\ncosto = a.calcular_costo(0.0019, "Córdoba")\ndias = a.estimar_dias("  CÓRDOBA  ")',
 numero('costo:', 3.02), numero('dias:', 2),
 '1.9 gramos se redondean a 2, no se truncan a 1. La comparación de ciudades normaliza espacios extremos, mayúsculas y tildes.')
pregunta('Observer', 'Desuscripción durante el aviso',
 'Ana y Luis están suscritos en ese orden. Durante actualizar, Ana se desuscribe; ninguno lanza excepciones.',
 '# Implementación actual de Tienda\nfor cliente in list(self._clientes):\n    cliente.actualizar(mensaje)',
 opcion('¿Luis recibe ese mismo aviso?', 'Sí', 'No', 'Solo si se suscribe otra vez', 'Solo si se usa un hilo'),
 numero('Suscriptores restantes tras el aviso:', 1),
 'Se recorre una copia de la lista. Quitar a Ana de la lista original no desplaza a Luis en la copia que se está recorriendo.')
pregunta('Observer', 'Mismo nombre, objetos distintos',
 'Cliente no redefine la igualdad por nombre.',
 't = Tienda("Cortez")\nt.suscribir(Cliente("Ana"))\nt.suscribir(Cliente("Ana"))\nt.desuscribir(Cliente("Ana"))',
 numero('Cantidad final de suscriptores:', 2),
 opcion('Resultado de desuscribir:', 'Informa que el cliente no está suscrito', 'Elimina ambos clientes llamados Ana', 'Elimina al primero', 'Lanza ValueError'),
 'Los tres Cliente son objetos distintos. La prevención de duplicados no deduplica nombres; desuscribir un objeto ausente solo informa.')
pregunta('Strategy', 'Un pago que falla',
 'El carrito tiene un producto válido. Se captura la excepción fuera de checkout.',
 'class PagoFallido(EstrategiaPago):\n    def pagar(self, monto):\n        raise RuntimeError("Servicio no disponible")\n\nc.set_estrategia_pago(PagoFallido())\ntry:\n    c.checkout()\nexcept RuntimeError:\n    pass',
 opcion('Estado de los productos tras el error:', 'Se conservan para reintentar', 'Se eliminan', 'Se duplican', 'Se convierten en decoradores'),
 opcion('Estado de la estrategia:', 'Sigue siendo PagoFallido', 'None', 'PagoEfectivo automáticamente', 'PagoPayPal automáticamente'),
 'El reinicio ocurre después de pagar. Si pagar lanza una excepción, esa parte de checkout no se ejecuta.')
pregunta('Strategy', 'Una clase con pagar no basta',
 'Se intenta inyectar un objeto que no hereda de la interfaz del TP.',
 'class PagoNuevo:\n    def pagar(self, monto):\n        print(monto)\n\nCarritoCompra().set_estrategia_pago(PagoNuevo())',
 opcion('Resultado actual:', 'TypeError', 'Se acepta por tener pagar', 'Se cobra cero', 'Se selecciona PagoEfectivo'),
 opcion('Cambio mínimo para cumplir el contrato:', 'Heredar de EstrategiaPago e implementar pagar', 'Renombrar pagar a actualizar', 'Heredar de Producto', 'Agregar un atributo precio'),
 'El setter valida isinstance(estrategia, EstrategiaPago). La compatibilidad aquí es nominal y no solo duck typing.')
pregunta('Chain of Responsibility', 'El límite antifraude',
 'El validador se usa solo, sin sucesor. Cada llamada es independiente.',
 'v = ValidadorFraude()\na = v.validar({"total": 5000.0})\nb = v.validar({"total": 5000.01})',
 opcion('Valor de a:', 'True', 'False', 'None', 'ValueError'),
 opcion('Valor de b:', 'False', 'True', 'None', 'ValueError'),
 'Se rechazan totales mayores que 5000; el límite exacto está permitido. Al terminar una cadena válida se devuelve True.')
pregunta('Chain of Responsibility', 'Evitar un ciclo',
 'Se intenta cerrar la cadena para que vuelva al principio.',
 'a = ValidadorStock()\nb = ValidadorPago()\na.set_siguiente(b)\nb.set_siguiente(a)',
 opcion('Última llamada:', 'Lanza ValueError', 'Acepta el ciclo', 'Devuelve False', 'Elimina a de la cadena'),
 opcion('Motivo de la protección:', 'Evitar una delegación que pueda no terminar', 'Impedir más de dos validadores', 'Obligar a usar un Singleton', 'Garantizar un pago real'),
 'set_siguiente recorre la cadena propuesta antes de asignar el enlace y rechaza si encuentra al propio manejador.')
pregunta('Adapter', 'Identificar responsabilidades al extender',
 'Se incorpora un transportista legado nuevo que ofrece cotizar_onzas(peso, zona).',
 'class AdaptadorNuevo((1)):\n    def calcular_costo(self, peso_kg, destino):\n        # convierte kg a onzas y delega al legado\n        ...\n    def estimar_dias(self, destino): ...\n    def crear_envio(self, pedido_id, destino): ...',
 opcion('Base (1):', 'SistemaEnvio', 'SistemaLegadoDHL', 'DecoradorProducto', 'CreadorProducto'),
 opcion('Lugar de la conversión kg → onzas:', 'Dentro del adaptador nuevo', 'En todos los clientes que cotizan', 'En Producto.precio', 'En Tienda.suscribir'),
 'El adaptador implementa la interfaz esperada y encapsula la traducción. El cliente conserva la llamada uniforme calcular_costo.')
pregunta('Observer', 'El contrato de suscripción',
 'Las llamadas se evalúan por separado con una tienda vacía.',
 '# A\nt.suscribir(object())\n# B\nt.desuscribir(Cliente("Ausente"))',
 opcion('Caso A:', 'TypeError', 'Se agrega el objeto', 'Retorna un Observer', 'Notifica a todos'),
 opcion('Caso B:', 'Informa la ausencia sin lanzar ValueError', 'Lanza ValueError', 'Suscribe al cliente', 'Borra la tienda'),
 'suscribir exige Observer. desuscribir comprueba pertenencia antes de remove, de modo que una baja inexistente no rompe la ejecución.')
pregunta('Strategy', 'Integración entre patrones',
 'Se intenta usar directamente un componente decorado en CarritoCompra.',
 'p = EnvolturaRegalo(ProductoConcreto("Libro", 10.0))\nc = CarritoCompra()\nc.agregar_producto(p)',
 opcion('Resultado en el código actual:', 'TypeError antes de agregarlo', 'Se agrega y se paga automáticamente', 'Se agrega con precio cero', 'Se convierte automáticamente en Libro'),
 opcion('Contrato completo requerido por el carrito:', 'nombre, precio y mostrar_info() invocable', 'Solo descripcion y precio', 'Solo heredar de Observer', 'Solo implementar build()'),
 'Decorator usa descripcion y precio, mientras que el carrito requiere nombre, precio y mostrar_info. Los patrones están separados; haría falta una adaptación explícita.')
pregunta('Chain of Responsibility', 'No confundir controles con integración',
 'Analizá el código actual, sin suponer conexiones adicionales entre los patrones.',
 'v = ValidadorStock()\nr = v.validar({"productos": ["X"]})\n# En otra parte del programa:\nc = CarritoCompra()',
 opcion('Qué verifica ese ValidadorStock:', 'Que productos sea una lista no vacía', 'Que haya unidades reales en una base de datos', 'Que el pago haya sido autorizado', 'Que X sea una instancia de Producto'),
 opcion('¿checkout ejecuta automáticamente esta cadena?', 'No; habría que integrarla explícitamente', 'Sí, siempre', 'Solo cuando se paga con PayPal', 'Solo con pedidos express'),
 'Stock simula una regla sobre la estructura del pedido. CarritoCompra no invoca los validadores: main demuestra los patrones sin conectar automáticamente todos sus flujos.')


CSS = '''
:root{color-scheme:light dark;--bg:#f3f5f8;--card:#fff;--ink:#18283d;--muted:#526279;--line:#cad3df;--accent:#175ca6;--code:#eef2f7}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
main{max-width:960px;margin:auto;padding:32px 20px 70px}h1{font-size:clamp(1.8rem,5vw,2.7rem);line-height:1.15;margin:12px 0}h2{font-size:1.2rem;margin:0}p{margin:12px 0}.intro,.q{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:24px;margin:20px 0}.kicker,.tema{color:var(--muted);font-size:.9rem}.kicker{font-weight:700;letter-spacing:.08em}.nav{display:flex;flex-wrap:wrap;gap:7px;margin:20px 0}.nav a{display:grid;place-items:center;width:38px;height:38px;border:1px solid var(--line);border-radius:7px;color:var(--accent);text-decoration:none;background:var(--card)}.q{scroll-margin-top:16px}.q header{display:flex;gap:14px;align-items:center}.n{background:var(--accent);color:white;border-radius:50%;min-width:38px;height:38px;display:grid;place-items:center;font-weight:bold}pre{background:var(--code);padding:18px;border-radius:8px;overflow:auto;line-height:1.6;font-size:.88rem}code{font-family:Consolas,monospace}.inciso{padding:12px 0;border-bottom:1px solid var(--line)}label{display:block;margin-bottom:7px;font-weight:600}select,input{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--muted);border-radius:6px;padding:9px;max-width:100%}select{width:100%}.num{width:150px}.feedback{display:block;font-size:.9rem;margin-top:5px}.acc{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-top:18px}button{font:inherit;cursor:pointer;border:1px solid var(--accent);border-radius:7px;padding:8px 14px;background:var(--card);color:var(--accent)}button.primary{background:var(--accent);color:#fff}.exp{padding:14px;background:var(--code);border-radius:8px;margin-top:16px}.ok{outline:2px solid #21804b}.bad{outline:2px solid #c0392b}:focus-visible{outline:3px solid #d28a00;outline-offset:3px}.score{font-weight:bold}.note{color:var(--muted);font-size:.92rem}#global{font-weight:bold}footer{color:var(--muted)}
@media(prefers-color-scheme:dark){:root{--bg:#101925;--card:#182536;--ink:#e7edf5;--muted:#b1c0d4;--line:#40546d;--accent:#75b9ff;--code:#101c2c}.n,button.primary{color:#101925}}
@media(max-width:520px){main{padding:16px 12px}.intro,.q{padding:17px}pre{padding:12px;font-size:.8rem}}
@media print{body{background:white;color:black}main{max-width:none;padding:0}.nav,.acc,#global,.note-interactive{display:none}.q{break-inside:avoid;border-color:#888}.exp[hidden]{display:none}select{appearance:none}pre{white-space:pre-wrap}.intro,.q{box-shadow:none}}
'''

JS = '''
function esCorrecta(value, answer, numeric) {
  const cleaned = value.trim().replace(',', '.');
  if (!numeric) return value === answer;
  if (!/^[+-]?(?:\\d+(?:\\.\\d*)?|\\.\\d+)$/.test(cleaned)) return false;
  const n = Number(cleaned);
  return Number.isFinite(n) && Math.abs(n - Number(answer)) < 1e-9;
}
// INTERFAZ
const preguntas = [...document.querySelectorAll('.q')];
function totalizar() {
  let puntos = 0, revisadas = 0;
  for (const q of preguntas) {
    if (q.dataset.score !== undefined) {
      puntos += Number(q.dataset.score);
      revisadas++;
    }
  }
  document.querySelector('#global').textContent =
    `${puntos} / 80 incisos correctos · ${revisadas} / 40 preguntas corregidas · Nota: ${(puntos / 8).toFixed(2)} / 10`;
}
function corregir(q) {
  let puntos = 0;
  for (const field of q.querySelectorAll('[data-answer]')) {
    const bien = esCorrecta(field.value, field.dataset.answer, field.tagName === 'INPUT');
    field.classList.toggle('ok', bien);
    field.classList.toggle('bad', !bien);
    field.setAttribute('aria-invalid', String(!bien));
    field.parentElement.querySelector('.feedback').textContent =
      bien ? 'Correcto.' : (field.value.trim() ? 'Incorrecto.' : 'Sin responder.');
    if (bien) puntos++;
  }
  q.dataset.score = puntos;
  q.querySelector('.score').textContent = `${puntos} / 2`;
  totalizar();
}
function revelar(q) {
  q.querySelector('.exp').hidden = false;
  q.querySelector('.ver').setAttribute('aria-expanded', 'true');
}
for (const q of preguntas) {
  for (const select of q.querySelectorAll('select')) {
    const options = [...select.options].slice(1);
    for (let i = options.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [options[i], options[j]] = [options[j], options[i]];
    }
    select.append(...options);
    select.value = '';
  }
  q.querySelector('.corr').addEventListener('click', () => corregir(q));
  q.querySelector('.ver').addEventListener('click', () => revelar(q));
  q.addEventListener('input', () => {
    delete q.dataset.score;
    q.querySelector('.score').textContent = 'Respuesta modificada: volver a corregir.';
    for (const field of q.querySelectorAll('[data-answer]')) {
      field.classList.remove('ok', 'bad');
      field.removeAttribute('aria-invalid');
      field.parentElement.querySelector('.feedback').textContent = '';
    }
    totalizar();
  });
}
document.querySelector('#corregir-todo').addEventListener('click', () => preguntas.forEach(corregir));
totalizar();
'''


def generar():
    """Escribe HTML sin recursos externos y guía de respuestas en Markdown."""
    escape = html.escape
    partes = ['<!doctype html><html lang="es"><head><meta charset="utf-8">',
              '<meta name="viewport" content="width=device-width,initial-scale=1">',
              '<title>Examen aplicado · Patrones de diseño · Los Cortez</title>',
              '<style>' + CSS + '</style></head><body><main>',
              '<div class="intro"><div class="kicker">DESARROLLO LOS CORTEZ · TP PYTHON</div>',
              '<h1>Patrones en acción</h1><p>Examen aplicado: 40 preguntas Cloze sobre los ocho patrones del TP.</p>',
              '<p><strong>1–20:</strong> aplicación y lectura de código. <strong>21–40:</strong> diagnóstico y diseño.</p>',
              '<p>Tiempo sugerido: 90 minutos. Dos incisos por pregunta: 80 puntos. Nota sobre 10 = aciertos ÷ 8. Sin penalización por error.</p>',
              '<p>Los fragmentos son independientes. Suponé importadas las clases desde sus subpaquetes de patrones; las variables preexistentes se describen en cada enunciado. Los huecos (1) y (2) se completan mentalmente antes de ejecutar.</p>',
              '<p>Importes en dólares, sin símbolo ni separador de miles. Se acepta punto o coma decimal. Cuando se pregunta por un print o valor concreto, ignorá los demás mensajes de diagnóstico.</p>',
              '<p class="note note-interactive">Opciones mezcladas al abrir. Corregir evalúa tus respuestas; Ver respuestas muestra la clave sin cambiarlas ni sumar puntos. Las respuestas no se guardan al cerrar o recargar.</p>',
              '<noscript>Activá JavaScript para usar el corrector. La guía docente contiene las respuestas.</noscript></div>',
              '<nav class="nav" aria-label="Ir a una pregunta">']
    partes.extend('<a href="#q{0}" aria-label="Pregunta {0}">{0}</a>'.format(i) for i in range(1, 41))
    partes.append('</nav><div class="acc"><button class="primary" id="corregir-todo">Corregir todo</button><p id="global" role="status" aria-live="polite"></p></div>')
    guia = ['# Guía docente — Examen aplicado al TP de patrones', '',
            '## Análisis del formato de referencia', '',
            'El HTML de Spring Boot contiene 40 casos Cloze: un escenario, código y varios incisos de selección única o respuesta numérica. Las preguntas 21–40 elevan la dificultad con diagnóstico y consecuencias de implementación. Incluye corrección por pregunta y explicación. El archivo recibido no contiene un exportador XML; esta entrega reproduce su experiencia HTML, no un paquete de importación Moodle.', '',
            'La adaptación mantiene 40 casos, dos niveles y opciones mezcladas; uniforma a dos incisos por pregunta para equilibrar la puntuación. Se basa en las clases y reglas actuales de patrones/, README.md e historias1.md, no en APIs hipotéticas. La clave se revela sin rellenar las respuestas del alumno ni inflar su puntaje.', '',
            '## Administración y puntuación', '',
            '- Duración sugerida: 90 minutos; ajustar según el grupo.',
            '- 80 incisos, 1 punto por acierto, 0 por error u omisión. Nota = aciertos / 8.',
            '- No se fija una nota mínima de aprobación: queda a criterio docente.',
            '- Cinco preguntas por patrón (10 puntos cada uno).',
            '- Importes sin unidades; se admite punto o coma decimal, sin separadores de miles.',
            '- HTML autocorregible para práctica o evaluación con consulta de soluciones autorizada; la clave está incluida en el archivo.',
            '- Las respuestas solo permanecen mientras la página está abierta, sin persistencia ni envío de datos.', '',
            '## Cobertura', '', '| Patrón | Preguntas |', '|---|---|']
    for tema in dict.fromkeys(q[0] for q in PREGUNTAS):
        ids = [str(i) for i, q in enumerate(PREGUNTAS, 1) if q[0] == tema]
        guia.append('| {} | {} |'.format(tema, ', '.join(ids)))
    guia.extend(['', '## Clave razonada', ''])
    for i, (tema, titulo, contexto, codigo, incisos, explicacion) in enumerate(PREGUNTAS, 1):
        nivel = 1 if i <= 20 else 2
        partes.append('<section class="q" id="q{}"><header><span class="n">{}</span><div><h2>{}</h2><span class="tema">{} · Nivel {}</span></div></header><p>{}</p><pre><code>{}</code></pre>'.format(i, i, escape(titulo), escape(tema), nivel, escape(contexto), escape(codigo)))
        claves = []
        for j, (texto, respuesta, opciones) in enumerate(incisos):
            letra = 'ab'[j]
            fid = 'q{}-{}'.format(i, letra)
            partes.append('<div class="inciso"><label for="{}">{}) {}</label>'.format(fid, letra, escape(texto)))
            atributos = 'id="{}" data-answer="{}" aria-describedby="{}-fb"'.format(fid, escape(respuesta, quote=True), fid)
            if opciones:
                partes.append('<select {}><option value="">Elegir…</option>'.format(atributos))
                for valor in opciones:
                    partes.append('<option value="{}">{}</option>'.format(escape(valor, quote=True), escape(valor)))
                partes.append('</select>')
            else:
                partes.append('<input class="num" {} inputmode="decimal" autocomplete="off" placeholder="?">'.format(atributos))
            partes.append('<span class="feedback" id="{}-fb"></span></div>'.format(fid))
            claves.append('{}) {}'.format(letra, respuesta))
        partes.append('<div class="acc"><button class="corr primary" aria-label="Corregir pregunta {0}">Corregir</button><button class="ver" aria-label="Ver respuestas de pregunta {0}" aria-expanded="false" aria-controls="exp{0}">Ver respuestas</button><span class="score" role="status" aria-live="polite"></span></div>'.format(i))
        partes.append('<div class="exp" id="exp{}" hidden><strong>Respuestas:</strong> {}<p><strong>Explicación.</strong> {}</p></div></section>'.format(i, escape(' · '.join(claves)), escape(explicacion)))
        guia.extend(['### {}. {} · {}'.format(i, titulo, tema), '', '**{}**'.format(' · '.join(claves)), '', explicacion, ''])
    partes.append('<footer>Basado en el TP Python de ocho patrones GoF. Edición: 19/10/2026. Simulaciones locales: no hay pagos, inventario ni transportistas reales.</footer></main><script type="module">' + JS + '</script></body></html>')
    destino = Path(__file__).resolve().parent
    (destino / 'examen_patrones.html').write_text('\n'.join(partes), encoding='utf-8')
    guia.extend(['## Mantenimiento', '',
                 'Regenerar ambos documentos con `python evaluacion/generar_examen.py` desde la raíz del proyecto. Validar el corrector con `node evaluacion/prueba_correccion.cjs`. Node solo se utiliza para esa prueba; el alumno únicamente necesita un navegador.', ''])
    (destino / 'guia_docente.md').write_text('\n'.join(guia), encoding='utf-8')


if __name__ == '__main__':
    generar()
