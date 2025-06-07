# Dividis Active Context

## Current Development Focus

### Nota sobre migración FSM

La migración de django-fsm a viewflow.fsm no es posible actualmente porque viewflow.fsm no está disponible como paquete estable en PyPI. El proyecto sigue usando django-fsm==3.0.0. Se recomienda revisar periódicamente la documentación oficial para futuras migraciones.

### Phase: Constellations & Declarations Management
We are currently focusing on:
1. Implementación de la funcionalidad de constelaciones interactivas y gestión de declaraciones.
2. Refactorización de ConstellationsMap para áreas reactivas y navegación.
3. Integración de DeclarationInput, DeclarationList, ConstellationNavBar, UnlockedTools, PillarTabs y ConstellationView.
4. Nuevas rutas protegidas para vistas de constelaciones.
5. Sincronización de declaraciones y módulos entre frontend y backend vía nuevo API.

## Recent Changes
- Implemented constellations feature with declarations management and interactive navigation.
- Refactored ConstellationsMap to use reactive areas and router links.
- Added DeclarationInput, DeclarationList, ConstellationNavBar, UnlockedTools, PillarTabs, and ConstellationView components.
- Introduced declaration API and expanded modules store for backend synchronization.
- Added new protected routes for constellation views with authentication.
- Updated docker-compose version and documented technical decisions in README.md.

## Active Decisions

### Architecture Decisions
1. Cosmic UI theme with Tailwind CSS and GSAP animations
2. Progressive module unlocking system
3. Mission-based user motivation
4. Galactic Dashboard as central navigation
5. Mobile-first responsive design

### Implementation Preferences
1. User Experience:
   - Welcoming and intuitive onboarding
   - Space-themed visual elements
   - Smooth animations and transitions
   - Clear progression path

2. Development Workflow:
   - Component-driven development
   - Mobile-first approach
   - Progressive enhancement
   - Performance optimization

3. Testing Strategy:
   - End-to-end onboarding flow tests
   - Module unlocking system tests
   - Responsive design tests
   - Animation performance tests

## Next Steps

### Immediate Tasks
1. Landing Page Development:
   - Design welcoming cosmic interface
   - Implement login/register flow
   - Create engaging animations
   - Optimize for mobile devices

2. Galactic Dashboard:
   - Build constellation map interface
   - Implement Salud module stub
   - Create initial mission system
   - Design progress visualization

3. Implement user authentication flow
4. Implement initial mission system
5. Migrar VitalRadarChart a ECharts
   - Se corrigieron los colores y estilos para que coincidan con el resto del dashboard
   - Se refactorizó el componente para cumplir con los principios SOLID (script y estilo en archivos separados)

4. Setup Docker environment:
   - Dockerfiles for backend y frontend creados
   - docker-compose.yml configurado para desarrollo local
   - Probada la construcción y levantamiento de servicios con Docker

5. Configure deployment:
   - Create fly.toml files
   - Set up environment variables
   - Configure domains

### Pending Decisions
1. UI/UX framework selection
2. Testing framework specific configuration
3. CI/CD pipeline detailed steps
4. Monitoring and logging solutions

## Active Patterns and Preferences

### Code Style
1. Backend:
   - Black formatter for Python
   - Django REST framework viewsets
   - Service layer pattern
   - State machine for module unlocking

2. Frontend:
   - Tailwind CSS for styling
   - GSAP for animations
   - Composition API with TypeScript
   - Reusable cosmic UI components

### API Design
1. RESTful endpoints
2. JWT authentication
3. Mission management endpoints
4. Module state tracking
5. Progress monitoring

## Project Insights

### Key Learnings
1. Cosmic theme enhances user engagement
2. Progressive unlocking maintains interest
3. Initial motivation crucial for retention
4. Mobile-first ensures wider accessibility

### Challenges Identified
1. Animation performance on mobile
2. Complex state management for unlocks
3. Mission progression balance
4. Intuitive cosmic navigation

### Risk Mitigation
1. Performance monitoring
2. State machine testing
3. User feedback collection
4. Progressive enhancement

## Reference Information

### Important Commands
```bash
# Backend Development
python manage.py runserver
python manage.py loaddata initial_missions
python manage.py create_cosmic_superuser

# Frontend Development
npm run dev
npm run build
npm run test:e2e  # Test onboarding flow

# Docker Commands
docker-compose up
docker-compose build

# Deployment
flyctl deploy
```

### Key Endpoints
1. Backend API: https://dividis-backend.fly.dev
2. Frontend: https://dividis-frontend.fly.dev
3. API Documentation: /api/schema/swagger-ui/

### Local Development URLs
1. Backend: http://localhost:8000
2. Frontend: http://localhost:3000
3. API Docs: http://localhost:8000/api/schema/swagger-ui/

## Progress Tracking

### Completed
- Memory Bank structure
- Architecture documentation
- Technical requirements
- Development environment specs

### In Progress
- Project initialization
- Infrastructure setup
- Deployment configuration

### Completed (último commit)
- Docker configuration (backend y frontend)
- Vite + Vue 3 + TypeScript + Tailwind en frontend
- Vite config files y scripts de build
- docker-compose.yml funcional para desarrollo local

### Upcoming
- Backend implementation
- Frontend implementation
- Initial deployment
