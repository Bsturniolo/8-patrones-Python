# Guía docente — Examen aplicado al TP de patrones

## Análisis del formato de referencia

El HTML de Spring Boot contiene 40 casos Cloze: un escenario, código y varios incisos de selección única o respuesta numérica. Las preguntas 21–40 elevan la dificultad con diagnóstico y consecuencias de implementación. Incluye corrección por pregunta y explicación. El archivo recibido no contiene un exportador XML; esta entrega reproduce su experiencia HTML, no un paquete de importación Moodle.

La adaptación mantiene 40 casos, dos niveles y opciones mezcladas; uniforma a dos incisos por pregunta para equilibrar la puntuación. Se basa en las clases y reglas actuales de patrones/, README.md e historias1.md, no en APIs hipotéticas. La clave se revela sin rellenar las respuestas del alumno ni inflar su puntaje.

## Administración y puntuación

- Duración sugerida: 90 minutos; ajustar según el grupo.
- 80 incisos, 1 punto por acierto, 0 por error u omisión. Nota = aciertos / 8.
- No se fija una nota mínima de aprobación: queda a criterio docente.
- Cinco preguntas por patrón (10 puntos cada uno).
- Importes sin unidades; se admite punto o coma decimal, sin separadores de miles.
- HTML autocorregible para práctica o evaluación con consulta de soluciones autorizada; la clave está incluida en el archivo.
- Las respuestas solo permanecen mientras la página está abierta, sin persistencia ni envío de datos.

## Cobertura

| Patrón | Preguntas |
|---|---|
| Singleton | 1, 2, 3, 21, 22 |
| Factory Method | 4, 5, 6, 23, 24 |
| Builder | 7, 8, 9, 25, 26 |
| Decorator | 10, 11, 12, 27, 28 |
| Adapter | 13, 14, 29, 30, 37 |
| Observer | 15, 16, 31, 32, 38 |
| Strategy | 17, 18, 33, 34, 39 |
| Chain of Responsibility | 19, 20, 35, 36, 40 |

## Clave razonada

### 1. Una conexión compartida · Singleton

**a) True · b) 1**

__new__ reutiliza la instancia y la bandera _initialized evita repetir la inicialización.

### 2. Dónde se controla la identidad · Singleton

**a) __new__ · b) _initialized**

Python puede invocar __init__ cada vez que se llama al constructor, aunque __new__ devuelva el mismo objeto.

### 3. Qué hace realmente query · Singleton

**a) Imprime el SQL como simulación · b) None**

El TP no se conecta a una base real: query usa print y no contiene un return de resultados.

### 4. Crear sin elegir por cadenas · Factory Method

**a) CreadorLibro · b) precio**

CreadorLibro decide crear un Libro. El precio se expone mediante una propiedad de solo lectura.

### 5. Registrar un electrónico · Factory Method

**a) Electronico · b) Invoca mostrar_info() y devuelve el producto**

La operación del creador usa el factory method y luego trabaja con la interfaz Producto; no conoce la clase concreta.

### 6. Un nuevo producto del catálogo · Factory Method

**a) Producto · b) CreadorProducto**

Se extienden el producto y el creador. La decisión de construcción queda en la nueva subclase, sin agregar un if central.

### 7. Pedido estándar simple · Builder

**a) 5 · b) 105**

El pedido simple suma el subtotal de productos y el envío estándar de $5.

### 8. Regalo con seguro · Builder

**a) 3 · b) 113**

Builder aplica 3% al subtotal: 100 + 5 de envío + 5 de envoltura + 3 de seguro = 113. No usa el 2% de Decorator.

### 9. Cambiar la modalidad de construcción · Builder

**a) set_builder · b) 115**

set_builder reemplaza el constructor que utiliza el director. El builder express cobra $15 de envío.

### 10. Envolver un producto · Decorator

**a) 15 · b) 10**

El decorador envuelve el componente y suma $5 al consultar su precio. No cambia el precio del objeto base.

### 11. Servicios acumulados · Decorator

**a) 102 · b) 131.99**

El seguro agrega 2% al precio actual y la garantía extendida suma $29.99.

### 12. El contrato del componente · Decorator

**a) ComponenteProducto · b) Propiedades**

ComponenteProducto define ambas propiedades abstractas. Los componentes concretos y decoradores las implementan.

### 13. Cotizar DHL desde kilogramos · Adapter

**a) 23 · b) 2**

2.5 kg equivalen a 2500 g. La tarifa es 3 + 20. El adaptador extrae 2 de «2-3 días hábiles».

### 14. Un cliente, dos transportistas · Adapter

**a) SistemaEnvio · b) Ciudad en DHL y código postal en FedEx**

Adapter unifica las operaciones, pero este TP conserva la diferencia semántica del destino; no implementa geocodificación.

### 15. Evitar suscripciones repetidas · Observer

**a) 1 · b) 1**

Tienda detecta que el mismo cliente ya está en la lista y no lo vuelve a agregar.

### 16. Agregar otro tipo de observador · Observer

**a) Observer · b) actualizar**

Tienda invoca actualizar(mensaje) y exige que el suscriptor sea una instancia de Observer.

### 17. Pagar en efectivo · Strategy

**a) 95 · b) Productos vacíos y estrategia None**

PagoEfectivo descuenta 5%. Tras pagar correctamente, checkout reinicia tanto los productos como la estrategia.

### 18. Cambiar el algoritmo de pago · Strategy

**a) PagoPayPal · b) Contexto**

El contexto mantiene una referencia a la estrategia actual; la segunda asignación reemplaza la primera.

### 19. Enlazar validadores · Chain of Responsibility

**a) b · b) Stock → Pago → Dirección**

set_siguiente devuelve el manejador recibido; por eso la siguiente llamada enlaza desde b y no desde a.

### 20. Cortar un pedido vacío · Chain of Responsibility

**a) False · b) 0**

Stock rechaza la lista vacía y devuelve False sin delegar. No se evalúan los manejadores posteriores.

### 21. Inicializar una sola vez · Singleton

**a) True · b) 2**

Controlar la identidad no evita invocar __init__. La bandera protege los efectos de inicialización, no la identidad.

### 22. Creación concurrente · Singleton

**a) Otro hilo pudo crear la instancia mientras este esperaba · b) El proceso de Python actual**

El segundo chequeo evita crear otra instancia tras esperar el bloqueo. Las variables de clase no comparten objetos entre procesos.

### 23. Polimorfismo del creador · Factory Method

**a) Libro, Electronico · b) La implementación de crear_producto de cada subclase**

registrar_producto reutiliza un flujo común y despacha crear_producto polimórficamente.

### 24. Contrato de precios y propiedades · Factory Method

**a) ValueError · b) AttributeError**

El constructor rechaza precios negativos. La propiedad precio no declara setter: asignarle un valor produce AttributeError.

### 25. Reutilizar sin mezclar pedidos · Builder

**a) 15 · b) 5**

build devuelve el pedido anterior y crea otro vacío. El segundo build aplica igualmente el envío de $5; no conserva los productos del primero.

### 26. La etiqueta personalizada · Builder

**a) Express (1 día hábil) · b) 15**

Según el contrato del TP, build vuelve a aplicar TIPO_ENVIO y COSTO_ENVIO del builder. set_tipo_envio no cambia esa política.

### 27. El orden cambia el precio · Decorator

**a) 107.1 · b) 107**

En a, el seguro grava 105: 105 × 1.02 = 107.10. En b, primero se asegura 100 y luego se suman 5: 107.00.

### 28. Un envoltorio sin recargo · Decorator

**a) Se crea un decorador que delega · b) 10**

DecoradorProducto implementa las dos propiedades abstractas. Por eso es instanciable y delega sin sumar recargos.

### 29. FedEx y las unidades · Adapter

**a) 5.15 · b) 3**

Un kilogramo se convierte en 2.205 libras y cuesta 5.15. El código 5000 no empieza con 1, por lo que demora 3 días.

### 30. Redondeo y normalización · Adapter

**a) 3.02 · b) 2**

1.9 gramos se redondean a 2, no se truncan a 1. La comparación de ciudades normaliza espacios extremos, mayúsculas y tildes.

### 31. Desuscripción durante el aviso · Observer

**a) Sí · b) 1**

Se recorre una copia de la lista. Quitar a Ana de la lista original no desplaza a Luis en la copia que se está recorriendo.

### 32. Mismo nombre, objetos distintos · Observer

**a) 2 · b) Informa que el cliente no está suscrito**

Los tres Cliente son objetos distintos. La prevención de duplicados no deduplica nombres; desuscribir un objeto ausente solo informa.

### 33. Un pago que falla · Strategy

**a) Se conservan para reintentar · b) Sigue siendo PagoFallido**

El reinicio ocurre después de pagar. Si pagar lanza una excepción, esa parte de checkout no se ejecuta.

### 34. Una clase con pagar no basta · Strategy

**a) TypeError · b) Heredar de EstrategiaPago e implementar pagar**

El setter valida isinstance(estrategia, EstrategiaPago). La compatibilidad aquí es nominal y no solo duck typing.

### 35. El límite antifraude · Chain of Responsibility

**a) True · b) False**

Se rechazan totales mayores que 5000; el límite exacto está permitido. Al terminar una cadena válida se devuelve True.

### 36. Evitar un ciclo · Chain of Responsibility

**a) Lanza ValueError · b) Evitar una delegación que pueda no terminar**

set_siguiente recorre la cadena propuesta antes de asignar el enlace y rechaza si encuentra al propio manejador.

### 37. Identificar responsabilidades al extender · Adapter

**a) SistemaEnvio · b) Dentro del adaptador nuevo**

El adaptador implementa la interfaz esperada y encapsula la traducción. El cliente conserva la llamada uniforme calcular_costo.

### 38. El contrato de suscripción · Observer

**a) TypeError · b) Informa la ausencia sin lanzar ValueError**

suscribir exige Observer. desuscribir comprueba pertenencia antes de remove, de modo que una baja inexistente no rompe la ejecución.

### 39. Integración entre patrones · Strategy

**a) TypeError antes de agregarlo · b) nombre, precio y mostrar_info() invocable**

Decorator usa descripcion y precio, mientras que el carrito requiere nombre, precio y mostrar_info. Los patrones están separados; haría falta una adaptación explícita.

### 40. No confundir controles con integración · Chain of Responsibility

**a) Que productos sea una lista no vacía · b) No; habría que integrarla explícitamente**

Stock simula una regla sobre la estructura del pedido. CarritoCompra no invoca los validadores: main demuestra los patrones sin conectar automáticamente todos sus flujos.

## Mantenimiento

Regenerar ambos documentos con `python evaluacion/generar_examen.py` desde la raíz del proyecto. Validar el corrector con `node evaluacion/prueba_correccion.cjs`. Node solo se utiliza para esa prueba; el alumno únicamente necesita un navegador.
