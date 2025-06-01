# Dividis

Plataforma de desarrollo personal con tema cósmico. Gestiona tu crecimiento personal a través de nueve dimensiones vitales, con un sistema de misiones y progresión gamificada.

## 🚀 Características

- Sistema de módulos desbloqueables
- Seguimiento de progreso y rachas
- Misiones personalizadas
- Tema visual cósmico inmersivo
- API RESTful con Django
- Frontend moderno con Vue 3

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

## 🏗️ Instalación

1. **Clonar el repositorio:**
```bash
git clone https://github.com/tuusuario/dividis.git
cd dividis
```

2. **Instalar dependencias:**
```bash
# Instalar todas las dependencias (frontend y backend)
npm run install:all
```

3. **Configurar variables de entorno:**
```bash
# Backend
cp backend/.env.example backend/.env
# Frontend
cp frontend/.env.example frontend/.env
```

4. **Configurar la base de datos:**
```bash
cd backend
python manage.py migrate
python manage.py loaddata api/fixtures/initial_modules.json
python manage.py loaddata api/fixtures/initial_missions.json
```

5. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

## 🚀 Desarrollo

Ejecutar los servidores de desarrollo:

```bash
# Ejecutar ambos servidores (frontend + backend)
npm run dev

# Ejecutar solo el frontend
npm run frontend

# Ejecutar solo el backend
npm run backend
```

### URLs de desarrollo:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/api/schema/swagger-ui/
- Admin: http://localhost:8000/admin/

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
