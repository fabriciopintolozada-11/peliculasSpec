# Constitución del proyecto peliculas

Principios innegociables. Cualquier cambio que los viole se rechaza.

1. **Stack simple.** Solo Python estándar y las dependencias de `requirements.txt`. Cada nueva dependencia requiere justificación escrita en el PR. Verificable: el número de dependencias no crece sin justificación.
2. **La spec manda.** Ningún comportamiento se implementa sin un requisito (RF-xx o RN-xx) en `README.md`. Cada función pública y cada test citan su ID. Verificable: búsqueda de IDs en el código.
3. **Lógica separada de la interfaz.** El módulo de reglas de negocio no importa `input`, `print`, ni ningún framework de interfaz. Verificable: revisión de imports en el módulo de lógica.
4. **Tests obligatorios.** Cada regla de negocio (RN-xx) tiene al menos un test automatizado. No se fusiona código con tests fallando. Verificable: `pytest` pasa en verde y cada RN está cubierta.
5. **Persistencia aislada.** Solo el módulo de persistencia lee y escribe datos. El resto del código usa repositorios. Verificable: ningún módulo fuera de persistencia abre archivos ni ejecuta SQL.
6. **Idioma.** Código, nombres y comentarios en inglés. Mensajes al usuario en español, centralizados en un único módulo. Verificable: no hay textos de cara al usuario fuera de ese módulo.
