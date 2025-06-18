FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x entrypoint.sh wait-for-postgres.sh
RUN python manage.py collectstatic --noinput

# Asegurar que los scripts sean ejecutables y usar /bin/sh explícitamente
RUN chmod 755 entrypoint.sh wait-for-postgres.sh
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
