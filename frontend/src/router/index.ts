import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: () => import('@/views/Landing.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/auth/Login.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/auth/Register.vue'),
      meta: { guestOnly: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('@/views/Dashboard.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Dashboard'
      }
    },
   {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/Profile.vue'),
      meta: {
        requiresAuth: true,
        title: 'Perfil'
      }
    },
    {
      path: '/modules/:id',
      name: 'module',
      component: () => import('@/views/modules/ModuleView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Módulo'
      },
      props: true
    },
    {
      path: '/constellation/:area',
      name: 'constellation',
      component: () => import('@/views/ConstellationView.vue'),
      meta: { 
        requiresAuth: true,
        title: 'Constelación'
      },
      props: true
    },
    {
      path: '/wellness-survey',
      name: 'WellnessSurvey',
      component: () => import('@/components/WellnessSurvey/WellnessSurvey.vue'),
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
      meta: { title: 'Página no encontrada' }
    }
  ]
})

// Navigation guards
router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // Set page title
  document.title = `${to.meta.title ? `${to.meta.title} | ` : ''}Dividis`

  // Esperar a que termine la validación de sesión tras refresh
  if (authStore.isAuthLoading) {
    await new Promise(resolve => {
      const stop = authStore.$subscribe(() => {
        if (!authStore.isAuthLoading) {
          stop()
          resolve(true)
        }
      })
    })
  }

  // Check if route requires auth
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }

  // Check if user is authenticated for auth pages
  if (to.meta.guestOnly && authStore.isAuthenticated) {
    return { name: 'dashboard' }
  }

  return true
})

export default router
