<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center px-4">
    <div class="text-center space-y-8">
      <!-- 404 number -->
      <div class="relative">
        <h1 class="text-9xl font-bold text-cosmic-500/20">404</h1>
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="space-y-4">
            <div class="w-24 h-24 mx-auto">
              <svg 
                class="text-cosmic-400 animate-cosmic-float" 
                fill="none" 
                viewBox="0 0 24 24" 
                stroke="currentColor">
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="1" 
                  d="M12 14l9-5-9-5-9 5 9 5z" />
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="1" 
                  d="M12 14l9-5-9-5-9 5 9 5z" />
                <path 
                  stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="1" 
                  d="M12 14l9-5-9-5-9 5 9 5z" />
              </svg>
            </div>
            <h2 class="text-2xl font-medium text-cosmic-100">Página no encontrada</h2>
          </div>
        </div>
      </div>

      <!-- Description -->
      <p class="text-slate-400 max-w-md mx-auto">
        Parece que te has aventurado en un área inexplorada del cosmos. 
        No te preocupes, siempre puedes volver al camino conocido.
      </p>

      <!-- Navigation buttons -->
      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <Button @click="goBack">
          <i class="fas fa-arrow-left mr-2"></i>
          Volver atrás
        </Button>
        <Button @click="goHome" variant="outline">
          <i class="fas fa-home mr-2"></i>
          Ir al inicio
        </Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import Button from '@/components/ui/Button.vue'

const router = useRouter()

function goBack() {
  router.back()
}

function goHome() {
  router.push('/')
}
</script>
