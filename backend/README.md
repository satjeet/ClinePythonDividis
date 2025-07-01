# Backend Dividis

## Inicialización automática de la base de datos

- Al levantar el backend con Docker, el contenedor ejecuta automáticamente:
  - Migraciones de Django (`python manage.py migrate`)
  - Carga de todos los fixtures `.json` en `api/fixtures` (solo si la base está vacía)

Esto asegura que siempre tendrás los módulos, misiones y datos iniciales necesarios, tanto en desarrollo como en producción/nube.

## Crear un superusuario

Para acceder al admin de Django, crea un superusuario ejecutando:

```bash
docker-compose exec backend python manage.py createsuperuser
```

Sigue las instrucciones en consola para definir usuario, email y contraseña.

## Archivos estáticos y Django Admin (WhiteNoise)

- El backend está configurado para servir archivos estáticos (CSS/JS) usando [WhiteNoise](https://whitenoise.evans.io/).
- Al construir la imagen Docker, se ejecuta automáticamente `python manage.py collectstatic --noinput` y los archivos se copian a `/app/staticfiles`.
- Esto asegura que el admin de Django y cualquier otro recurso estático se vea correctamente, incluso con `DEBUG=False` y en producción/nube.
- No necesitas configurar nginx para servir los estáticos: WhiteNoise lo hace por ti.

## Resumen de mejoras recientes

- **Persistencia real de datos:** Ahora el backend usa siempre Postgres (no SQLite), y los datos persisten entre reinicios.
- **Migraciones automáticas:** Las migraciones se ejecutan automáticamente al levantar el contenedor.
- **Carga automática de fixtures:** Todos los datos iniciales se cargan si la base está vacía.
- **Limpieza de código frontend:** El flujo de selección de pilares y navegación entre constelaciones es completamente reactivo y controlado por el estado del padre.
- **Solución de errores 400:** Los errores al guardar declaraciones se resolvieron asegurando que los módulos y misiones existan en la base de datos.
- **Admin Django con estilos:** El admin de Django ahora siempre se ve correctamente, sin importar el entorno.

## Notas

- Si necesitas reiniciar todo desde cero, ejecuta:
  ```
  docker-compose down -v
  docker-compose up --build
  ```
  Esto borrará la base de datos y recargará los datos iniciales.

- Si agregas nuevos fixtures `.json` en `api/fixtures`, se cargarán automáticamente la próxima vez que la base esté vacía.

## Lecciones de refactorización y buenas prácticas

- **Modularización:** Separar los serializers por dominio (usuario, perfil, módulos, etc.) facilita el mantenimiento y la escalabilidad.
- **Evitar relaciones inversas inexistentes:** Siempre verifica la relación real entre modelos antes de usar `obj.x_set.all()`. Prefiere filtrar explícitamente por usuario.
- **Compatibilidad legacy:** Mantener un `serializers.py` que reexporta desde el paquete permite migraciones progresivas y evita romper endpoints existentes.
- **Pruebas tras refactor:** Cada cambio estructural debe ir acompañado de pruebas manuales y automáticas de los endpoints críticos (login, perfil, módulos).
- **Documentación:** Toda decisión de arquitectura y lección aprendida debe quedar registrada en este README para futuros desarrolladores.
