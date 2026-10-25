# Plan 001: Catálogo de películas (MVP)

Estado: borrador para revisión.
Basado en: `docs/constitution.md` y `specs/001-pelis-mvp/spec.md`.

Este plan define cómo se construye el catálogo. Los requisitos que cubre están en la spec; aquí se referencian por ID y no se repiten.

## 0. Conformidad con la constitución

| Principio | Cómo lo cumple este plan |
|---|---|
| 1. Stack simple | Python estándar más dos dependencias justificadas en la sección 4 (Flask y pytest). |
| 2. La spec manda | Cada módulo, función y prueba cita el ID de RF o RNF que cubre (sección 7). |
| 3. Lógica separada | El módulo `catalog` no importa Flask, `print` ni `input`. Solo recibe datos y devuelve resultados. |
| 4. Tests obligatorios | Cada RF y RN tiene al menos una prueba; `pytest` debe pasar antes de fusionar. |
| 5. Persistencia aislada | Solo `storage` abre el archivo JSON. El resto recibe listas de películas. |
| 6. Idioma | Código, nombres y comentarios en inglés. Textos para el visitante en español, solo en `messages`. |

**Nota de conformidad pendiente:** la constitución pide que los requisitos vivan en `README.md`. Los IDs RF-01 a RF-05 y RNF-01 y RNF-02 de la spec 001 aún no están allí. Este plan los usa tal como están en la spec; la decisión de cómo registrarlos queda en la sección 9.

## 1. Estructura de módulos

Nombre del paquete: `pelis_cat`. Todos los nombres de archivo están en inglés (principio 6).

```
peliculasSPEC/
├── data/
│   └── movies.json          # catálogo de ejemplo (datos, no código)
├── pelis_cat/
│   ├── __init__.py
│   ├── catalog.py           # lógica pura: activas, búsqueda, filtro, orden, detalle
│   ├── text.py              # normalización de texto (minúsculas, sin tildes, espacios)
│   ├── models.py            # estructura de una película y validación de precio
│   ├── storage.py           # única lectura del archivo JSON
│   ├── messages.py          # todos los textos en español para el visitante
│   └── web.py               # rutas HTTP y plantillas; llama a catalog
├── templates/
│   ├── catalog.html         # lista, búsqueda, filtro
│   └── detail.html          # detalle y mensaje de no disponible
├── tests/
│   ├── test_text.py
│   ├── test_catalog.py
│   ├── test_storage.py
│   ├── test_web.py
│   └── test_architecture.py # verifica el principio 3 y el principio 6
├── requirements.txt
└── requirements-dev.txt
```

Responsabilidades:

- **`catalog.py`:** todas las reglas de RF-01 a RF-05. Recibe una lista de películas y parámetros; devuelve una lista o un estado. No sabe de HTTP ni de archivos.
- **`text.py`:** una sola función de normalización que usan la búsqueda y el orden. Así ambos se comportan igual con tildes y mayúsculas.
- **`models.py`:** representa una película y valida RN-01 (precio mayor que cero) al cargarla.
- **`storage.py`:** lee `data/movies.json` y entrega objetos `models`. Es el único módulo que toca el disco (principio 5).
- **`messages.py`:** cuatro textos del visitante, con su clave. Ningún otro archivo contiene texto para el visitante.
- **`web.py`:** traduce parámetros de la URL a llamadas de `catalog` y pasa el resultado a la plantilla. No contiene reglas de negocio.

## 2. Modelo de datos (JSON)

Archivo: `data/movies.json`. Es de solo lectura en este MVP; la administración del catálogo está fuera de alcance.

Ejemplo:

```json
{
  "movies": [
    {
      "id": "m-001",
      "title": "Amélie",
      "year": 2001,
      "genre": "Comedia",
      "price": 9.99,
      "synopsis": "Una joven decide cambiar la vida de quienes la rodean.",
      "active": true
    },
    {
      "id": "m-002",
      "title": "The Matrix",
      "year": 1999,
      "genre": "Ciencia ficción",
      "price": 12.5,
      "synopsis": "Un programador descubre la verdad detrás de la realidad.",
      "active": true
    },
    {
      "id": "m-003",
      "title": "Película retirada",
      "year": 1990,
      "genre": "Drama",
      "price": 7.0,
      "synopsis": "Ejemplo de película dada de baja.",
      "active": false
    }
  ]
}
```

Reglas del modelo:

| Campo | Tipo | Regla | Fuente |
|---|---|---|---|
| `id` | texto, único | Identifica la película en la URL. No se repite. | RF-05 |
| `title` | texto, no vacío | Base de la búsqueda y del orden. | RF-01, RF-02 |
| `year` | entero | Se muestra; no interviene en el orden principal. | RF-01 |
| `genre` | texto, no vacío | Usado por el filtro. | RF-03 |
| `price` | número con dos decimales | Debe ser mayor que cero (RN-01). Moneda pendiente (sección 9). | RF-01, RF-05 |
| `synopsis` | texto | Puede ser vacío; se muestra tal cual. | RF-01, RF-05 |
| `active` | booleano | `false` oculta la película del catálogo; no la borra (RN-02). | RF-01, RF-05 |

Los géneros del filtro se calculan a partir de las películas activas (supuesto, ver sección 9).

## 3. Algoritmos en pseudocódigo

### 3.1 Normalizar texto (RF-02, RF-01)

```
función normalizar(texto):
    texto ← convertir a minúsculas
    texto ← descomponer caracteres acentuados y quitar las marcas de tilde
    texto ← quitar espacios al inicio y al final
    texto ← reemplazar cada secuencia de espacios por un solo espacio
    devolver texto
```

Pendiente: si la "ñ" debe tratarse como "n" (sección 9). Hasta confirmarlo, la "ñ" se conserva como letra distinta.

### 3.2 Películas activas (RF-01, RN-02)

```
función películas_activas(películas):
    devolver [p para p en películas si p.active es verdadero]
```

### 3.3 Clave de orden (RF-01, RF-04)

```
función clave_orden(p):
    devolver (normalizar(p.title), p.year, p.id)
```

El año y el id solo sirven para desempatar títulos iguales. El desempate por año es la propuesta de la spec (sección 10), aún sin confirmar.

### 3.4 Búsqueda por título (RF-02)

```
función buscar_por_titulo(películas, texto):
    consulta ← normalizar(texto)
    si consulta está vacía:
        devolver películas
    devolver [p para p en películas si consulta está contenida en normalizar(p.title)]
```

### 3.5 Filtro por género (RF-03)

```
función filtrar_por_género(películas, género):
    si género es nulo:
        devolver películas
    devolver [p para p en películas si p.genre es igual a género]
```

### 3.6 Géneros disponibles (RF-03)

```
función géneros_disponibles(películas):
    devolver los valores distintos de p.genre, ordenados alfabéticamente,
             usando solo películas activas
```

### 3.7 Vista del catálogo (RF-01, RF-02, RF-03, RF-04)

Esta función decide qué mensaje corresponde. Es la única que combina los filtros.

```
función vista_catálogo(películas, texto, género):
    activas ← películas_activas(películas)
    si activas está vacía:
        devolver (ESTADO_VACÍO, [])

    resultado ← buscar_por_titulo(activas, texto)
    resultado ← filtrar_por_género(resultado, género)
    resultado ← ordenar por clave_orden

    si resultado está vacío:
        devolver (ESTADO_SIN_COINCIDENCIAS, [])
    devolver (ESTADO_OK, resultado)
```

Los tres estados se convierten en mensajes en `messages.py`:

- `ESTADO_VACÍO` → "No hay películas disponibles por ahora"
- `ESTADO_SIN_COINCIDENCIAS` → "No se encontraron películas para tu búsqueda"

### 3.8 Detalle de película (RF-05)

```
función detalle(películas, id):
    para cada p en películas:
        si p.id es igual a id y p.active es verdadero:
            devolver p
    devolver NO_DISPONIBLE
```

`NO_DISPONIBLE` se convierte en el mensaje "La película no está disponible" y en un enlace al catálogo.

### 3.9 Validación del precio (RN-01)

```
función validar_película(datos):
    si datos.price no es número o datos.price ≤ 0:
        lanzar error de datos inválidos
    devolver película con esos campos
```

## 4. Decisiones técnicas

### D1. Framework web: Flask

- **Decisión:** usar Flask como única dependencia de interfaz. Plantillas Jinja2 incluidas.
- **Justificación:** las rutas, las plantillas y el escape de HTML ya están resueltos y son conocidos por un desarrollador junior. Reduce el código propio de HTTP y el riesgo de errores de seguridad.
- **Alternativa descartada:** `http.server` de la biblioteca estándar. No añade dependencias, pero obliga a escribir enrutamiento, parsing de parámetros y escape manual de HTML. Mayor riesgo y más código para mantener.

### D2. Persistencia: archivo JSON

- **Decisión:** guardar el catálogo en `data/movies.json` y leerlo con la biblioteca estándar.
- **Justificación:** el catálogo es pequeño, solo se lee y se puede inspeccionar a simple vista. No requiere servidor ni SQL.
- **Alternativa descartada:** SQLite. Es estándar y robusto, pero el MVP no escribe datos; añade consultas SQL que el principio 5 exige aislar, sin beneficio hoy.

### D3. Estado de búsqueda y filtro en la URL

- **Decisión:** el texto de búsqueda y el género van como parámetros de la URL (`?q=...&genero=...`). No se guardan en sesión ni en cookies.
- **Justificación:** sin estado en el servidor, el botón "atrás" y los enlaces compartidos funcionan igual. Cumple RNF-01 (sin inicio de sesión) y el caso límite 3 de la spec, porque el detalle no depende de la búsqueda.
- **Alternativa descartada:** guardar la búsqueda en la sesión. Requiere cookies y gestión de sesión sin ningún requisito que lo pida.

### D4. Búsqueda al enviar el formulario

- **Decisión:** la búsqueda y el filtro se aplican al pulsar el botón "Buscar". Sin JavaScript.
- **Justificación:** es lo más simple y verificable con pruebas automatizadas. La spec no fija el momento de aplicación (pendiente en sección 9); este plan asume el envío explícito.
- **Alternativa descartada:** buscar mientras se escribe. Requiere JavaScript, que añade una segunda capa de lógica en el navegador y complica las pruebas.

### D5. Pruebas: pytest

- **Decisión:** `pytest` para todas las pruebas. Es una dependencia de desarrollo declarada en `requirements-dev.txt`.
- **Justificación:** la constitución exige `pytest`, y su sintaxis con funciones simples es la más fácil para un desarrollador junior.
- **Alternativa descartada:** `unittest` de la biblioteca estándar, sin dependencias extra. Es válido, pero la constitución nombra `pytest` como criterio de verificación, así que usarlo evita una discrepancia.

## 5. Contrato de uso del sistema

El visitante usa el sistema en el navegador. No hay API de otros sistemas en este MVP.

| Ruta | Método | Parámetros | Respuesta | Cubre |
|---|---|---|---|---|
| `/` | GET | `q` (texto, opcional), `genero` (texto, opcional) | 200, página con el catálogo, el formulario de búsqueda, el selector de género y el mensaje correspondiente | RF-01, RF-02, RF-03, RF-04 |
| `/peliculas/<id>` | GET | `id` (texto) | 200, página con título, año, género, precio y sinopsis | RF-05 |
| `/peliculas/<id>` (no activa o inexistente) | GET | `id` | 404, página con "La película no está disponible" y enlace a `/` | RF-05 |

Reglas del contrato:

- `q` con solo espacios equivale a `q` vacío (RF-02).
- `genero` vacío o ausente equivale a "todos los géneros" (RF-03).
- El enlace "volver al catálogo" en el detalle apunta a `/` sin parámetros. Esto no decide si la búsqueda previa se conserva (sección 9).
- No hay autenticación en ninguna ruta (RNF-01).
- Las plantillas incluyen la etiqueta de viewport para que la página se adapte a móvil (RNF-02). La verificación es manual.

## 6. Mapa de cobertura de requisitos

| Requisito | Módulo y función | Prueba principal |
|---|---|---|
| RF-01 Listado | `catalog.películas_activas`, `catalog.vista_catálogo`, orden por `clave_orden` | `test_catalog`: solo activas, orden A-Z, estado vacío |
| RF-02 Búsqueda | `text.normalizar`, `catalog.buscar_por_titulo` | `test_text`, `test_catalog`: sin tildes, sin mayúsculas, texto vacío, sin coincidencias |
| RF-03 Filtro | `catalog.filtrar_por_género`, `catalog.géneros_disponibles` | `test_catalog`: género, quitar filtro, género sin películas |
| RF-04 Combinación | `catalog.vista_catálogo` | `test_catalog`: texto y género juntos, sin coincidencias combinadas |
| RF-05 Detalle | `catalog.detalle` | `test_catalog`: activa, inactiva, inexistente; `test_web`: código 404 y mensaje |
| RF-01 (datos incompletos y baja) | `storage` y `models` | `test_storage`: RN-01 y película inactiva |
| RN-01 Precio | `models.validar_película` | `test_storage`: precio cero y negativo se rechazan |
| RN-02 Baja sin borrado | `models`, `catalog.películas_activas` | `test_catalog`: inactiva no aparece y sigue en los datos |
| RNF-01 Acceso público | `web` (ninguna ruta con autenticación) | `test_web`: todas las rutas responden sin sesión |
| RNF-02 Usabilidad móvil | Plantillas con viewport | Revisión manual (sección 8) |

## 7. Estrategia de pruebas

Pirámide: muchas pruebas unitarias sobre funciones puras, pocas pruebas de integración.

**Pruebas unitarias** (`test_text.py`, `test_catalog.py`):

- Cada función de `catalog` y `text` se prueba con datos en memoria, sin archivos ni Flask.
- Cada caso de la spec aparece como mínimo una vez. El nombre de la prueba cita el ID (por ejemplo, `test_rf02_busqueda_ignora_tildes`), según el principio 2.
- Casos obligatorios: búsqueda vacía, solo espacios, tildes y mayúsculas, catálogo sin activas, género sin películas, combinación sin coincidencias, detalle de película inactiva e inexistente, dos películas con el mismo título.

**Pruebas de almacenamiento** (`test_storage.py`):

- Carga el archivo de ejemplo y obtiene las películas esperadas.
- Un precio cero o negativo lanza error (RN-01).
- Un archivo inexistente o mal formado produce un error claro, y no un resultado vacío silencioso.

**Pruebas de integración web** (`test_web.py`), con el cliente de pruebas de Flask:

- `/` devuelve 200 y solo muestra películas activas.
- `/?q=amelie` y `/?genero=Comedia` devuelven las películas esperadas.
- `/peliculas/<id>` devuelve 200 para una activa y 404 con el mensaje para una inactiva o inexistente.
- Ninguna ruta pide inicio de sesión (RNF-01).

**Pruebas de arquitectura** (`test_architecture.py`):

- Verifica con el análisis del código fuente que `catalog.py` y `text.py` no importan `flask`, `storage` ni `web`.
- Verifica que ningún módulo fuera de `messages.py` contiene los textos del visitante. Así se cumple el principio 6.
- Verifica que solo `storage.py` abre archivos.

**Verificación manual:**

- RNF-02: revisar el catálogo y el detalle en una pantalla de escritorio y en una de móvil. La lista, la búsqueda y el filtro deben ser usables en ambas.

**Criterio de aprobación:** `pytest` en verde, cada RF y RN con al menos una prueba (sección 6), y la revisión manual de RNF-02 hecha.

## 8. Orden de implementación sugerido

1. `text.py` y sus pruebas (base de RF-02).
2. `models.py` y `storage.py` con `data/movies.json` (RN-01, RN-02).
3. `catalog.py` completo con pruebas (RF-01 a RF-05).
4. `messages.py` y `test_architecture.py`.
5. `web.py`, plantillas y pruebas de integración (RNF-01).
6. Revisión manual de RNF-02.

## 9. Pendientes que este plan no resuelve

Estas decisiones dependen de las dudas abiertas de la spec. El plan asume un supuesto para poder avanzar, y el supuesto debe confirmarse antes de implementar:

1. **Géneros:** supuesto de que son los géneros de las películas activas (sección 3.6). Si la lista debe ser fija, cambia `géneros_disponibles`.
2. **Búsqueda en sinopsis:** supuesto de que solo se busca en el título.
3. **Desempate de títulos iguales:** supuesto de orden por año (sección 3.3).
4. **Moneda y formato de precio:** supuesto de número con dos decimales, sin símbolo. Pendiente de confirmar.
5. **Letra "ñ":** supuesto de que se conserva como letra distinta (sección 3.1).
6. **Paginación:** supuesto de una sola lista sin paginación.
7. **Momento de búsqueda:** supuesto de envío explícito (D4).
8. **Conservar búsqueda al volver del detalle:** no definido; el enlace va a `/` sin parámetros.
9. **Tiempo de respuesta:** no definido; no hay prueba de rendimiento en este plan.
10. **Registro de IDs:** la constitución pide que los requisitos estén en `README.md`. Los IDs de la spec 001 (RF-01 a RF-05, RNF-01, RNF-02) viven en la spec. Hay que decidir si se copian al README, o si la constitución se ajusta para permitir requisitos por funcionalidad.
11. **Nombre del paquete:** se usa `pelis_cat` por la mención en la solicitud. El repositorio se llama `peliculasSpec`; confirmar el nombre.
