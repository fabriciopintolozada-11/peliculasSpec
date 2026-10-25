# Tareas 001: Catálogo de películas (MVP)

Basado en `spec.md` y `plan.md`. Cada tarea debe tardar entre 15 y 30 minutos. Las tareas van en orden de dependencia: no empieces una sin haber cerrado las anteriores de las que depende.

Convención: "Cubre" indica los RF, RN o RNF de la spec. Las tareas de infraestructura o de principios de la constitución indican el principio.

## Fase 0: Puesta en marcha

- [ ] **T00 Confirmar supuestos del plan.** Revisar la sección 9 de `plan.md` con el responsable del producto y marcar cada punto como confirmado o cambiado.
  - Cubre: todos los RF y RNF de la spec.
  - Hecho cuando: cada uno de los 11 puntos de la sección 9 tiene la palabra "confirmado" o la decisión nueva escrita en el plan.

- [ ] **T01 Declarar dependencias.** Crear `requirements.txt` con Flask fijado a una versión exacta, y `requirements-dev.txt` con pytest fijado a una versión exacta.
  - Cubre: principio 1 de la constitución.
  - Hecho cuando: `pip install -r requirements-dev.txt` termina sin errores en un entorno limpio.

- [x] **T02 Crear la estructura de carpetas.** Crear `pelis_cat/__init__.py`, `tests/`, `templates/` y `data/`.
  - Cubre: plan sección 1.
  - Hecho cuando: `pytest` se ejecuta sin errores de importación (aunque reporte cero pruebas).

- [ ] **T03 Crear el catálogo de ejemplo.** Crear `data/movies.json` con las tres películas del plan sección 2: una activa con tilde ("Amélie"), una activa en inglés ("The Matrix") y una inactiva.
  - Cubre: RN-02 (la película inactiva existe en los datos).
  - Hecho cuando: el archivo es JSON válido y contiene al menos una película con `active: false`.

## Fase 1: Normalización de texto

- [ ] **T04 Escribir pruebas de normalización.** Crear `tests/test_text.py` con casos de mayúsculas, tildes, espacios al inicio y al final, espacios internos múltiples y texto vacío o solo espacios.
  - Cubre: RF-02.
  - Hecho cuando: el archivo tiene al menos un caso por cada tipo de entrada listado y los nombres de prueba citan `RF-02`.

- [ ] **T05 Implementar `normalizar` en `text.py`.** Pasar a minúsculas, quitar tildes, recortar espacios y colapsar espacios internos.
  - Cubre: RF-02.
  - Hecho cuando: `tests/test_text.py` pasa en verde.

## Fase 2: Modelo y almacenamiento

- [ ] **T06 Crear el modelo de película y validar el precio.** Crear `pelis_cat/models.py` con la estructura de película y la validación de precio mayor que cero.
  - Cubre: RN-01.
  - Hecho cuando: una prueba confirma que un precio de cero y uno negativo producen error, y que un precio de 9.99 se acepta.

- [ ] **T07 Leer el catálogo desde el archivo JSON.** Crear `pelis_cat/storage.py` con una función que lee `data/movies.json` y devuelve una lista de películas. Si el archivo no existe o el JSON no es válido, debe lanzar un error con mensaje claro.
  - Cubre: RN-01, RN-02, RF-01 (datos de entrada).
  - Hecho cuando: `tests/test_storage.py` verifica que se cargan tres películas del ejemplo, y que un archivo inexistente lanza error.

## Fase 3: Lógica del catálogo

- [ ] **T08 Filtrar películas activas.** Implementar `películas_activas` en `catalog.py` y probarla en `tests/test_catalog.py`.
  - Cubre: RF-01, RN-02.
  - Hecho cuando: una prueba confirma que una película con `active: false` no aparece en el resultado, y que sigue presente en la lista original.

- [ ] **T09 Ordenar por título.** Implementar la clave de orden y el orden A a Z, con desempate por año y por id, en `catalog.py`.
  - Cubre: RF-01.
  - Hecho cuando: una prueba ordena cuatro títulos con y sin tilde, y otra confirma que dos películas con el mismo título se muestran ambas, ordenadas por año.

- [ ] **T10 Buscar por título.** Implementar `buscar_por_titulo` usando `normalizar` de `text.py`.
  - Cubre: RF-02.
  - Hecho cuando: las pruebas confirman que "amelie" encuentra "Amélie", que un texto vacío o solo con espacios devuelve todas las películas, y que sin coincidencias devuelve una lista vacía.

- [ ] **T11 Filtrar por género y listar géneros.** Implementar `filtrar_por_género` y `géneros_disponibles` en `catalog.py`.
  - Cubre: RF-03.
  - Hecho cuando: las pruebas confirman que un género devuelve solo sus películas, que quitar el filtro devuelve todas, y que la lista de géneros no incluye géneros de películas inactivas.

- [ ] **T12 Combinar búsqueda, filtro y estados.** Implementar `vista_catálogo` con los tres estados: vacío, sin coincidencias y correcto.
  - Cubre: RF-01, RF-02, RF-03, RF-04.
  - Hecho cuando: las pruebas cubren un catálogo sin películas activas aunque haya búsqueda, una búsqueda sin coincidencias, un género sin películas, y una combinación de texto y género que sí tiene resultados.

- [ ] **T13 Obtener el detalle de una película.** Implementar `detalle` en `catalog.py`.
  - Cubre: RF-05.
  - Hecho cuando: las pruebas confirman que una película activa se devuelve, y que una inactiva y un id inexistente devuelven el estado de no disponible.

## Fase 4: Textos y verificación de arquitectura

- [ ] **T14 Centralizar los textos del visitante.** Crear `pelis_cat/messages.py` con los cuatro textos: "No hay películas disponibles por ahora", "No se encontraron películas para tu búsqueda", "La película no está disponible" y "Volver al catálogo".
  - Cubre: RF-01, RF-02, RF-03, RF-04, RF-05 (mensajes).
  - Hecho cuando: cada texto aparece una sola vez en el archivo, con las tildes exactas de la spec.

- [ ] **T15 Verificar las reglas de arquitectura.** Crear `tests/test_architecture.py` que revise el código fuente.
  - Cubre: principios 3, 5 y 6 de la constitución.
  - Hecho cuando: la prueba falla si `catalog.py` o `text.py` importan `flask`, `storage` o `web`; si un texto del visitante aparece fuera de `messages.py`; o si un archivo distinto de `storage.py` abre archivos. Se verifica rompiendo la regla a propósito una vez.

## Fase 5: Interfaz web

- [ ] **T16 Ruta del catálogo sin filtros.** Crear `pelis_cat/web.py` con la ruta `/` que llama a `vista_catálogo` sin parámetros y pasa el resultado a la plantilla. Crear `templates/catalog.html` con la lista de películas.
  - Cubre: RF-01, RNF-01.
  - Hecho cuando: una prueba con el cliente de Flask recibe 200 y solo ve las películas activas, sin pedir inicio de sesión.

- [ ] **T17 Búsqueda y filtro en la página del catálogo.** Añadir a `/` la lectura de los parámetros `q` y `genero`, el formulario de búsqueda, el selector de género con `géneros_disponibles`, y el mensaje según el estado.
  - Cubre: RF-02, RF-03, RF-04.
  - Hecho cuando: las pruebas de `/?q=amelie`, `/?genero=Comedia` y `/?q=%20%20` (solo espacios, equivale a búsqueda vacía) devuelven las películas esperadas.

- [ ] **T18 Mensajes en la página del catálogo.** Mostrar en `catalog.html` el texto de `messages.py` que corresponde a cada estado.
  - Cubre: RF-01, RF-02, RF-03, RF-04.
  - Hecho cuando: una prueba de `/` con un catálogo sin películas activas muestra "No hay películas disponibles por ahora", y una búsqueda sin coincidencias muestra "No se encontraron películas para tu búsqueda".

- [ ] **T19 Ruta de detalle.** Añadir a `web.py` la ruta `/peliculas/<id>` y crear `templates/detail.html`.
  - Cubre: RF-05.
  - Hecho cuando: una prueba recibe 200 con título, año, género, precio y sinopsis para una película activa.

- [ ] **T20 Detalle no disponible.** Responder 404 con el mensaje de no disponible y un enlace a `/` cuando la película está inactiva o no existe.
  - Cubre: RF-05.
  - Hecho cuando: las pruebas confirman el código 404, el texto "La película no está disponible" y un enlace que apunta a `/`.

- [ ] **T21 Diseño adaptable a móvil.** Añadir la etiqueta de viewport y un diseño que se ajuste en pantallas pequeñas a `catalog.html` y `detail.html`.
  - Cubre: RNF-02.
  - Hecho cuando: la página se ve completa, sin desplazamiento horizontal, en una ventana de escritorio y en una de móvil (la verificación es manual).

## Fase 6: Cierre

- [ ] **T22 Verificar cobertura de requisitos.** Revisar que cada RF, RN y RNF aparece en al menos un nombre de prueba.
  - Cubre: todos los RF-01 a RF-05, RN-01, RN-02, RNF-01 y RNF-02.
  - Hecho cuando: buscar cada ID en `tests/` devuelve al menos una coincidencia; RNF-02 se marca como verificado manualmente.

- [ ] **T23 Citar IDs en el código.** Revisar que cada función pública de `catalog.py`, `text.py`, `storage.py` y `web.py` cita su RF o RN en un comentario en inglés.
  - Cubre: principio 2 de la constitución.
  - Hecho cuando: ninguna función pública queda sin ID citado.

- [ ] **T24 Ejecutar la suite completa.** Ejecutar `pytest` desde la raíz del proyecto.
  - Cubre: principio 4 de la constitución.
  - Hecho cuando: `pytest` termina en verde y el resultado se pega en el PR.
