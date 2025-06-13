# Dividis

Plataforma de desarrollo personal con tema cósmico. Gestiona tu crecimiento personal a través de nueve dimensiones vitales, con un sistema de misiones y progresión gamificada.

## 🚀 Características

- Sistema de módulos desbloqueables
- Seguimiento de progreso y rachas
- Misiones personalizadas
- Tema visual cósmico inmersivo
- API RESTful con Django
- Frontend moderno con Vue 3

## ⚙️ Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python:** [Python 3.11+](https://www.python.org/downloads/)
- **Node.js y npm:** [Node.js 18+](https://nodejs.org/en/download/) (npm se instala con Node.js)
- **PostgreSQL:** [PostgreSQL 15+](https://www.postgresql.org/download/)
- **Git:** [Git](https://git-scm.com/downloads)

(Opcional: Docker y Docker Compose)

## 🐳 Instalación y uso con Docker (recomendado para principiantes)

### 1. Instalar Docker Desktop

- Descarga e instala Docker Desktop desde: https://www.docker.com/products/docker-desktop/
- Sigue las instrucciones del instalador y asegúrate de reiniciar tu PC si es necesario.
- Verifica la instalación abriendo una terminal y ejecutando:
  ```bash
  docker --version
  docker-compose --version
  ```

### 2. Clonar el repositorio

```bash
git clone https://github.com/tuusuario/dividis.git
cd dividis
```

### 3. Copiar archivos de entorno

- Copia los archivos de ejemplo:
  ```bash
  cp backend/.env.example backend/.env
  cp frontend/.env.example frontend/.env
  ```
- Edita los archivos `.env` si necesitas personalizar variables (por defecto funcionan para desarrollo local).

### 4. Levantar el proyecto

- En la raíz del proyecto, ejecuta:
  ```bash
  docker-compose up --build
  ```
- Esto descargará las dependencias y levantará tanto el backend (Django) como el frontend (Vue) automáticamente.

### 5. Acceder a la aplicación

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### 6. Comandos útiles

- Detener los servicios:
  ```bash
  docker-compose down
  ```
- Reconstruir si cambias dependencias:
  ```bash
  docker-compose build
  docker-compose up --build
  ```

> **Nota:** No necesitas instalar Python, Node.js ni PostgreSQL localmente si usas Docker.

---

## 🏗️ Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tuusuario/dividis.git
cd dividis
```

2. **Instalación del Backend:**

```bash
cd backend
```

   a. **Crear y activar el entorno virtual:**

   *   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   *   **Linux/Mac:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   b. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

   c. **Configurar variables de entorno:**
   Copia el archivo `.env.example` a `.env` y edita las variables según sea necesario:
   ```bash
   cp .env.example .env
   nano .env  # o tu editor de texto preferido
   ```

   d. **Configurar la base de datos:**

   *   Crea una base de datos llamada `dividis` en PostgreSQL. Puedes usar la línea de comandos o una herramienta GUI como pgAdmin.

   e. **Ejecutar migraciones y cargar datos iniciales:**
   ```bash
   python manage.py migrate
   python manage.py loaddata api/fixtures/initial_modules.json
   python manage.py loaddata api/fixtures/initial_missions.json
   ```

   f. **Crear superusuario:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Instalación del Frontend:**

```bash
cd ../frontend
```

   a. **Instalar dependencias:**
   ```bash
   npm install
   ```

   b. **Configurar variables de entorno:**
   Copia el archivo `.env.example` a `.env` y edita las variables según sea necesario:
   ```bash
   cp .env.example .env
   nano .env  # o tu editor de texto preferido
   ```

## 🚀 Desarrollo

Consulta la sección "Instalación" para configurar el entorno de desarrollo.

## 🐛 Solución de Problemas Comunes

*   **"python" o "pip" no se reconocen:** Asegúrate de que Python esté instalado y añadido al PATH de tu sistema.
*   **Error de conexión a la base de datos:** Verifica que PostgreSQL esté corriendo y que las credenciales en el archivo `.env` sean correctas.
*   **Error al activar el entorno virtual:** Revisa que el comando de activación sea el correcto para tu sistema operativo (ver sección "Instalación").

## 📚 Recursos Adicionales

*   **Documentación de Python:** [https://www.python.org/doc/](https://www.python.org/doc/)
*   **Documentación de Node.js:** [https://nodejs.org/en/docs/](https://nodejs.org/en/docs/)
*   **Documentación de PostgreSQL:** [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
*   **Memory Bank del proyecto:** (Enlace al Memory Bank)

## 🛠️ Tecnologías

### Backend
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- Django FSM

### Frontend
- Vue 3
- TypeScript
- Tailwind CSS
- Pinia
- Vue Router
- GSAP (animaciones)

## 📚 Documentación

### Estructura de directorios

```
dividis/
├── backend/               # Proyecto Django
│   ├── api/              # App principal
│   ├── dividis/          # Configuración del proyecto
│   └── requirements.txt  # Dependencias Python
│
├── frontend/             # Aplicación Vue
│   ├── src/
│   │   ├── assets/      # Recursos estáticos
│   │   ├── components/  # Componentes Vue
│   │   ├── stores/     # Stores Pinia
│   │   ├── views/      # Vistas principales
│   │   └── router/     # Configuración de rutas
│   │
│   └── package.json
│
└── package.json         # Scripts de desarrollo
```

### Módulos del Sistema

1. **Salud (Serpiente de Hábitos)**
   - Módulo inicial desbloqueado
   - Sistema de seguimiento de hábitos
   - Visualización de progreso tipo "snake"

2. **Personalidad (Diálogos Socráticos)**
   - Requiere 500 XP para desbloquear
   - Ejercicios de autoconocimiento
   - Sistema de diálogo guiado

(... otros módulos descritos en la documentación del proyecto)

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

[MIT](LICENSE)

## 👥 Equipo

- [Tu Nombre](https://github.com/tuusuario) - Desarrollador Principal
