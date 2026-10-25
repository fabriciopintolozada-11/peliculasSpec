# Especificación 001: Catálogo de películas (MVP)

Estado: borrador para revisión.
Origen: `README.md` (RF-01 a RF-03 y RN-02) y las decisiones tomadas en la fase de aclaración.

## 1. Contexto y objetivo

Hoy no hay forma de explorar las películas que se venden. Esta funcionalidad permite a cualquier visitante ver el catálogo, buscarlo, filtrarlo por género y consultar el detalle de cada película.

Es la base de la compra, que se especificará en una funcionalidad posterior. Sin un catálogo consultable, ningún cliente puede decidir qué comprar.

## 2. Usuarios

- **Visitante:** persona sin cuenta. Usa todo el catálogo sin iniciar sesión.
- **Administrador:** no interactúa con esta funcionalidad. Su única influencia es que las películas dadas de baja dejan de aparecer.

## 3. Historias de usuario

- **HU-01:** Como visitante, quiero ver la lista de películas disponibles, para saber qué hay a la venta.
- **HU-02:** Como visitante, quiero buscar películas por título, para encontrar una película concreta.
- **HU-03:** Como visitante, quiero filtrar por género, para explorar películas de mi interés.
- **HU-04:** Como visitante, quiero ver el detalle de una película, para decidir si me interesa.

## 4. Requisitos funcionales

### RF-01 Listado del catálogo

- El sistema deberá mostrar cada película activa con su título, año, género, precio y sinopsis.
- Cuando el visitante abra el catálogo, el sistema deberá mostrar las películas en orden alfabético por título, de A a Z.
- El sistema no deberá mostrar películas dadas de baja al cargar el catálogo.
- Si no hay películas activas, entonces el sistema deberá mostrar el mensaje "No hay películas disponibles por ahora", incluso si el visitante ha escrito una búsqueda o seleccionado un género.

### RF-02 Búsqueda por título

- Cuando el visitante escriba un texto en la búsqueda, el sistema deberá mostrar solo las películas activas cuyo título contenga ese texto.
- La búsqueda deberá ignorar mayúsculas y tildes. Por ejemplo, "amelie" deberá encontrar "Amélie".
- Si el texto de búsqueda está vacío o solo tiene espacios, entonces el sistema deberá mostrar el catálogo completo.
- Si hay películas activas pero ninguna coincide con la búsqueda, entonces el sistema deberá mostrar el mensaje "No se encontraron películas para tu búsqueda".

### RF-03 Filtro por género

- Cuando el visitante seleccione un género, el sistema deberá mostrar solo las películas activas de ese género.
- Cuando el visitante quite el filtro de género, el sistema deberá volver a mostrar las películas según la búsqueda vigente.
- Si hay películas activas pero el género seleccionado no tiene ninguna, entonces el sistema deberá mostrar el mensaje "No se encontraron películas para tu búsqueda".

### RF-04 Combinación de búsqueda y filtro

- Mientras haya un texto de búsqueda y un género seleccionados, el sistema deberá mostrar solo las películas que cumplan ambos criterios.
- El sistema deberá mantener el orden alfabético de RF-01 en los resultados de búsqueda y filtro.
- Si hay películas activas pero ninguna cumple ambos criterios, entonces el sistema deberá mostrar el mensaje "No se encontraron películas para tu búsqueda".

### RF-05 Detalle de película

- Cuando el visitante seleccione una película activa, el sistema deberá mostrar su título, año, género, precio y sinopsis.
- Si el visitante intenta abrir una película que no existe o que está dada de baja, entonces el sistema deberá mostrar el mensaje "La película no está disponible" y un enlace para volver al catálogo.

## 5. Trazabilidad con el README

| Requisito de esta especificación | Requisito del README |
|---|---|
| RF-01 Listado | RF-01, RN-02 |
| RF-02 Búsqueda | RF-02 |
| RF-03 Filtro por género | RF-02 |
| RF-04 Combinación | RF-02 |
| RF-05 Detalle | RF-03 |

## 6. Requisitos no funcionales

- **RNF-01 Acceso público:** el catálogo, la búsqueda, el filtro y el detalle deberán estar disponibles sin iniciar sesión.
- **RNF-02 Usabilidad:** la lista, la búsqueda y el filtro deberán ser utilizables tanto en pantallas de escritorio como de móvil.

## 7. Casos límite

- Dos películas activas con el mismo título se muestran ambas.
- Una película que se da de baja mientras el visitante navega el catálogo puede seguir visible en la lista hasta que el catálogo se vuelva a cargar. Al intentar abrir su detalle, se aplica RF-05 y se muestra como no disponible.
- Si el visitante abre el detalle de una película y después cambia la búsqueda o el filtro, el sistema no deberá cambiar la película que está viendo.

## 8. Fuera de alcance

- Carrito, compra y pago.
- Registro e inicio de sesión.
- Administración del catálogo (alta, edición, baja).
- Historial de compras.
- Reseñas, valoraciones y recomendaciones.
- Streaming o descarga de películas.
- Múltiples idiomas y monedas.

## 9. Criterios de finalización

- Cada criterio de RF-01 a RF-05 y de RNF-01 se verifica con al menos una prueba automatizada. RNF-02 se verifica mediante revisión manual en pantallas de escritorio y de móvil.
- Cada regla de RF-01 a RF-05 se revisa contra el README para confirmar que no hay contradicciones.
- Todas las dudas de la sección 10 están resueltas o aceptadas de forma explícita por el responsable del producto.

## 10. Dudas abiertas

- [NECESITA ACLARACIÓN] ¿Los géneros del filtro son una lista fija o se toman de los géneros de las películas activas?
- [NECESITA ACLARACIÓN] ¿La búsqueda debe incluir también la sinopsis, o solo el título?
- [NECESITA ACLARACIÓN] ¿Cómo se ordenan dos películas con el mismo título? Propuesta: por año, de menor a mayor.
- [NECESITA ACLARACIÓN] ¿Cuál es el formato y la moneda del precio?
- [NECESITA ACLARACIÓN] ¿Hace falta paginación, o se muestran todas las películas en una sola lista?
- [NECESITA ACLARACIÓN] ¿La letra "ñ" debe tratarse como "n" en la búsqueda?
- [NECESITA ACLARACIÓN] ¿Cuál es el tiempo de respuesta aceptable para mostrar el catálogo?
