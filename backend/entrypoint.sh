#!/bin/bash
set -e

echo "==> Esperando a que Postgres esté listo..."
./wait-for-postgres.sh "$DB_HOST"

echo "==> Ejecutando migraciones de Django..."
python manage.py migrate --noinput

echo "==> Estado de migraciones Django:"
python manage.py showmigrations

# Cargar títulos de nivel desde el JSON usando management command (igual que misiones)
echo " - Cargando títulos de nivel..."
python manage.py load_level_titles || echo " [ERROR] Falló cargar títulos"

# Cargar los fixtures en orden específico (solo si los necesitas)
echo "==> Cargando fixtures iniciales en orden..."
echo " - Cargando módulos..."
python manage.py loaddata api/fixtures/initial_modules.json || echo " [ERROR] Falló cargar módulos"
echo " - Cargando misiones (solo si no existen)..."
python manage.py load_initial_missions || echo " [ERROR] Falló cargar misiones"

echo "==> Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
