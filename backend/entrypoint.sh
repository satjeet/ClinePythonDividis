#!/bin/sh
set -e

echo "==> Esperando a que Postgres esté listo..."
./wait-for-postgres.sh "$DB_HOST"

echo "==> Ejecutando migraciones de Django..."
python manage.py migrate --noinput

# Cargar todos los fixtures (debug: sin condicional)
echo "==> Intentando cargar todos los fixtures iniciales..."
for fixture in api/fixtures/*.json; do
  echo "   - Cargando $fixture"
  python manage.py loaddata "$fixture" || echo "   [ERROR] Falló cargar $fixture"
done

echo "==> Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
