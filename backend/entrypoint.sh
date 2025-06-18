#!/bin/sh
set -e

echo "==> Esperando a que Postgres esté listo..."
./wait-for-postgres.sh "$DB_HOST"

echo "==> Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# Cargar los fixtures en orden específico
echo "==> Cargando fixtures iniciales en orden..."
echo "   - Cargando módulos..."
python manage.py loaddata api/fixtures/initial_modules.json || echo "   [ERROR] Falló cargar módulos"
echo "   - Cargando misiones..."
python manage.py loaddata api/fixtures/initial_missions.json || echo "   [ERROR] Falló cargar misiones"

echo "==> Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
