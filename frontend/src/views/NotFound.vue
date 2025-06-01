<template>
  <div class="min-h-screen bg-slate-950 flex flex-col justify-center items-center py-12 px-4 sm:px-6 lg:px-8">
    <!-- Animated stars background -->
    <div class="absolute inset-0 z-0">
      <div v-for="i in 50" :key="i" 
           class="star absolute bg-white rounded-full"
           :style="{
             width: `${Math.random() * 2 + 1}px`,
             height: `${Math.random() * 2 + 1}px`,
             left: `${Math.random() * 100}%`,
             top: `${Math.random() * 100}%`,
             animation: `cosmic-pulse ${Math.random() * 3 + 2}s infinite`
           }">
      </div>
    </div>

    <div class="relative z-10 text-center">
      <!-- Error code -->
      <h1 class="text-9xl font-bold text-cosmic-400 mb-4 cosmic-glow">
        404
      </h1>

      <!-- Error message -->
      <h2 class="text-2xl md:text-3xl font-bold text-cosmic-100 mb-8">
        Te has desviado de tu ruta cósmica
      </h2>

      <!-- Description -->
      <p class="text-slate-400 max-w-md mx-auto mb-8">
        La constelación que buscas parece estar en otra dimensión. 
        ¿Quizás deberíamos volver a un territorio conocido?
      </p>

      <!-- Navigation buttons -->
      <div class="flex flex-col sm:flex-row justify-center gap-4">
        <button 
          @click="router.go(-1)"
          class="btn-cosmic bg-transparent border border-cosmic-500 hover:bg-cosmic-500/20">
          Regresar
        </button>
        <RouterLink 
          to="/" 
          class="btn-cosmic">
          Volver al Inicio
        </RouterLink>
      </div>
    </div>

    <!-- Decorative elements -->
    <div class="absolute bottom-10 left-1/2 transform -translate-x-1/2 text-slate-600 text-sm">
      Coordenadas no encontradas
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.floating {
  animation: float 6s ease-in-out infinite;
}

.star {
  animation: twinkle 1s infinite;
}

@keyframes twinkle {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}
</style>
