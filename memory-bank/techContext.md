# Dividis Technical Context

## Development Environment

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 15+
- Flyctl CLI
- Tailwind CSS CLI
- GSAP (for animations)

### Local Setup Commands
```bash
# Backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata initial_missions  # Load initial mission data
python manage.py runserver

# Frontend
npm install
npm run dev  # Vite dev server with HMR
```

## Technology Stack

### Backend (Django + DRF)
```txt
Django==5.0
djangorestframework==3.14
djangorestframework-simplejwt==5.3
django-cors-headers==4.3
psycopg2-binary==2.9
python-dotenv==1.0
gunicorn==21.2
drf-spectacular==0.26
django-activity-stream==1.4.0  # For mission tracking
django-fsm==2.8.1  # For module unlock state machine
```

### Frontend (Vue.js + Pinia)
```json
{
  "dependencies": {
    "vue": "^3.3",
    "pinia": "^2.1",
    "vue-router": "^4.2",
    "axios": "^1.6",
    "@headlessui/vue": "^1.7",
    "gsap": "^3.12",
    "tailwindcss": "^3.3",
    "@heroicons/vue": "^2.0",
    "tippy.js": "^6.3",
    "echarts": "^5.6",
    "vue-echarts": "^6.6"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5",
    "vite": "^5.0",
    "typescript": "^5.2",
    "@vue/compiler-sfc": "^3.3",
    "autoprefixer": "^10.4",
    "postcss": "^8.4",
    "tailwindcss": "^3.3"
  }
}
```

## Environment Variables y Configuración de Autenticación

### Archivos de Configuración Críticos

#### Backend (.env)
```env
# Configuración básica
DJANGO_SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración CORS (crítica para autenticación)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Base de datos
DATABASE_URL=postgres://postgres:postgres@db:5432/dividis
DB_HOST=db
DB_USER=postgres
DB_PASSWORD=postgres

# Configuración del módulo
INITIAL_MODULE=salud
DEFAULT_MISSION_POINTS=100
```

#### Frontend (.env)
```env
# Configuración del servidor
VITE_PORT=3000
VITE_HOST=0.0.0.0

# URL de la API (crítica para autenticación)
VITE_API_URL=http://localhost:8000

# Configuración de desarrollo
NODE_ENV=development
VITE_ENABLE_DEVTOOLS=true
VITE_ENABLE_DEBUG=true

# Configuración de la API
VITE_API_TIMEOUT=30000
VITE_ENABLE_API_CACHE=true
```

### Consideraciones Importantes para Autenticación

1. **Configuración del Frontend**:
   - La URL de la API (`VITE_API_URL`) DEBE usar `localhost` cuando se accede desde el navegador
   - NO usar `http://backend:8000` ya que este nombre solo funciona dentro de la red Docker
   - Configurar los timeouts y caché según necesidades

2. **Configuración del Backend**:
   - CORS_ALLOWED_ORIGINS debe incluir TODAS las URLs desde donde se accederá al frontend
   - Incluir tanto `http://localhost:3000` como `http://127.0.0.1:3000`
   - DEBUG=True en desarrollo para ver errores detallados

3. **Solución de Problemas Comunes**:
   - Error "ERR_NAME_NOT_RESOLVED": Verificar que la URL de la API usa `localhost`
   - Error CORS: Verificar que la URL del frontend está en CORS_ALLOWED_ORIGINS
   - Error de conexión: Asegurar que los servicios están corriendo (`docker-compose ps`)
   - Error de autenticación: Verificar token JWT y su almacenamiento en localStorage

4. **Pasos de Verificación**:
   ```bash
   # 1. Verificar servicios activos
   docker-compose ps
   
   # 2. Reiniciar servicios si hay problemas
   docker-compose restart backend frontend
   
   # 3. Verificar logs
   docker-compose logs backend
   docker-compose logs frontend
   ```

## Docker Configuration

### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "dividis.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Frontend Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    env_file: ./backend/.env
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    env_file: ./frontend/.env

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: dividis
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Deployment Configuration

### Backend fly.toml
```toml
app = "dividis-backend"
primary_region = "scl"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[services]]
  protocol = "tcp"
  internal_port = 8000
```

### Frontend fly.toml
```toml
app = "dividis-frontend"
primary_region = "scl"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 80
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
```

## Development Tools

### VS Code Extensions
- Python
- Pylance
- Volar (Vue Language Features)
- Tailwind CSS IntelliSense
- Docker
- PostgreSQL
- GitLens
- ESLint
- Prettier

### Code Formatting & Styling
- Black for Python
- ESLint + Prettier for JavaScript/Vue
- Tailwind CSS for styling
- GSAP for animations
- Custom theme system for cosmic UI

## Testing Infrastructure

### Backend Tests
- pytest for Python tests
- pytest-django for Django integration
- coverage.py for test coverage
- pytest-factoryboy for test data
- django-fsm-test for state machine testing

### Frontend Tests
- Vitest for unit tests
- Cypress for E2E testing
- Vue Test Utils for component testing
- @testing-library/vue for component testing
- Mock Service Worker for API mocking

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      # Test steps here

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      # Deploy steps here
```

## Database Management

### Migration Commands
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

## API Documentation
- Swagger UI at `/api/schema/swagger-ui/`
- ReDoc at `/api/schema/redoc/`
- OpenAPI Schema at `/api/schema/`
- Custom mission and unlock endpoints documentation
- Module progression state machine documentation

## Security Measures
- HTTPS enforcement
- JWT token rotation
- Rate limiting
- SQL injection prevention
- XSS protection
- CSRF protection
