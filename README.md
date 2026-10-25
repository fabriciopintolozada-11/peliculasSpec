# peliculasSpec

Especificación funcional de un sistema sencillo de venta de películas.

> Estado: borrador inicial. Este documento describe **qué** debe hacer el sistema. La implementación se definirá más adelante.

## 1. Objetivo

Permitir que un cliente consulte un catálogo de películas, las compre y acceda a su historial de compras, mientras el administrador gestiona el catálogo y las ventas.

## 2. Alcance

**Incluido**
- Catálogo de películas consultable por el público.
- Registro e inicio de sesión de clientes.
- Carrito de compra y proceso de compra.
- Historial de compras del cliente.
- Gestión del catálogo (alta, edición, baja) por parte del administrador.

**No incluido (por ahora)**
- Pasarela de pago real (el pago se simula).
- Streaming o descarga de las películas.
- Recomendaciones personalizadas, reseñas y valoraciones.
- Múltiples monedas o idiomas.

## 3. Actores

| Actor | Descripción |
|---|---|
| Visitante | Usuario no registrado. Puede explorar el catálogo. |
| Cliente | Usuario registrado. Puede comprar películas y ver su historial. |
| Administrador | Gestiona el catálogo de películas y consulta las ventas. |

## 4. Requisitos funcionales

### 4.1 Catálogo
- **RF-01** El sistema muestra la lista de películas con título, año, género, precio y sinopsis.
- **RF-02** El visitante puede buscar películas por título o filtrar por género.
- **RF-03** El visitante puede ver el detalle de una película.

### 4.2 Cuentas de usuario
- **RF-04** El visitante puede registrarse con nombre, correo electrónico y contraseña.
- **RF-05** El cliente puede iniciar y cerrar sesión.
- **RF-06** El correo electrónico es único en el sistema.

### 4.3 Compra
- **RF-07** El cliente puede agregar y quitar películas de su carrito.
- **RF-08** El carrito muestra las películas seleccionadas y el total a pagar.
- **RF-09** El cliente confirma la compra. El sistema registra la venta con fecha, películas, precios y total.
- **RF-10** El pago se simula: la compra se marca como pagada al confirmarla.
- **RF-11** Una película ya comprada por un cliente no se puede volver a comprar.

### 4.4 Historial
- **RF-12** El cliente puede ver la lista de sus compras con fecha y total.
- **RF-13** El cliente puede ver el detalle de cada compra.

### 4.5 Administración
- **RF-14** El administrador puede crear, editar y dar de baja películas del catálogo.
- **RF-15** El administrador puede ver el listado de todas las ventas y el total vendido.

## 5. Requisitos no funcionales

- **RNF-01 Seguridad:** las contraseñas se almacenan cifradas, nunca en texto plano.
- **RNF-02 Acceso:** las funciones de administración solo están disponibles para el rol administrador.
- **RNF-03 Usabilidad:** la interfaz debe ser clara y usable desde un navegador de escritorio y móvil.
- **RNF-04 Integridad:** una venta registrada no puede modificarse; los precios de una compra se guardan como estaban al momento de la compra.

## 6. Entidades principales

- **Usuario:** id, nombre, correo, contraseña (cifrada), rol (cliente / administrador).
- **Película:** id, título, año, género, precio, sinopsis, activa (sí / no).
- **Venta:** id, usuario, fecha, total.
- **Detalle de venta:** id, venta, película, precio unitario.

Relaciones: un usuario tiene muchas ventas; una venta tiene uno o más detalles; cada detalle referencia una película.

## 7. Reglas de negocio

- **RN-01** El precio de una película debe ser mayor que cero.
- **RN-02** Dar de baja una película la oculta del catálogo, pero no borra las compras anteriores.
- **RN-03** El total de una venta es la suma de los precios de sus detalles.
- **RN-04** No se puede confirmar una compra con el carrito vacío.

## 8. Preguntas abiertas

- ¿Se requiere recuperación de contraseña?
- ¿El administrador se crea manualmente o mediante registro?
- ¿Hay límite de películas por compra?
- ¿Qué plataforma o tecnología se usará? (pendiente de definir)
