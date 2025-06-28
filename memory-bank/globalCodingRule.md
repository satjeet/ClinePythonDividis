# Reglas Globales de Codificación

## 1. DRY y SOLID

- Evita duplicación de lógica y código.
- Aplica principios SOLID en arquitectura y componentes.

## 2. Refactorización y Revisión

- Refactoriza frecuentemente.
- Realiza revisiones de código y usa herramientas automáticas.

## 3. Documentación

- Documenta decisiones de diseño y excepciones a las reglas.
- Mantén la documentación actualizada.

## 4. Pruebas y Automatización

- Implementa pruebas automatizadas y mantén cobertura adecuada.

## 5. Buenas prácticas para filtrado y paginación

- Prefiere limitar y ordenar datos desde el backend cuando sea posible.
- Si el backend no lo soporta, filtra y limita en frontend, pero documenta la decisión.
- Usa parámetros claros en endpoints para paginación y orden.

## 6. UX en dashboards y listas dinámicas

- Muestra siempre estados de carga y mensajes de error claros.
- Limita la cantidad de elementos mostrados para evitar sobrecargar al usuario.
- Usa títulos descriptivos y consistentes según el contexto de los datos.

## 7. Nota de Flexibilidad

Estas reglas deben guiar el desarrollo, pero pueden existir excepciones justificadas. Documenta y comunica cualquier excepción.
