<template>
  <div class="min-h-screen bg-slate-950 overflow-hidden relative">
    <!-- Background star effect -->
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

    <!-- Content -->
    <div class="relative z-10">
      <!-- Navigation -->
      <nav class="container mx-auto px-6 py-4 flex justify-between items-center">
        <div class="text-2xl font-bold text-cosmic-400">
          Dividis
        </div>
        <div class="space-x-4">
          <RouterLink 
            to="/login" 
            class="btn-cosmic">
            Iniciar Sesión
          </RouterLink>
          <RouterLink 
            to="/register" 
            class="btn-cosmic bg-transparent border border-cosmic-500 hover:bg-cosmic-500/20">
            Registrarse
          </RouterLink>
        </div>
      </nav>

      <!-- Hero section -->
      <main class="container mx-auto px-6 py-20 text-center">
        <h1 class="text-5xl md:text-7xl font-bold mb-8 text-cosmic-100 cosmic-glow">
          Diseña una Vida que
          <span class="text-cosmic-400 block mt-2">Disfrutes</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-slate-300 max-w-3xl mx-auto mb-12">
          Un sistema integral de desarrollo personal que te guía a través de 
          <span class="text-cosmic-400">nueve dimensiones vitales</span>, 
          ayudándote a crear una vida más plena y significativa.
        </p>

        <RouterLink 
          to="/register" 
          class="btn-cosmic text-lg px-8 py-4">
          Comienza tu Viaje
        </RouterLink>

        <!-- Features grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24">
          <div v-for="(feature, index) in features" 
               :key="index"
               class="card-cosmic transform hover:-translate-y-2 transition-transform duration-300">
            <div class="text-3xl text-cosmic-400 mb-4">
              <component :is="feature.icon" class="w-12 h-12 mx-auto" />
            </div>
            <h3 class="text-xl font-bold mb-2">{{ feature.title }}</h3>
            <p class="text-slate-400">{{ feature.description }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ChartBarIcon, SparklesIcon, UserGroupIcon } from '@heroicons/vue/24/outline'

const features = [
  {
    icon: ChartBarIcon,
    title: 'Progreso Medible',
    description: 'Visualiza tu crecimiento personal a través de métricas claras y objetivos alcanzables.'
  },
  {
    icon: SparklesIcon,
    title: 'Experiencia Única',
    description: 'Una narrativa cósmica inmersiva que hace del desarrollo personal una aventura emocionante.'
  },
  {
    icon: UserGroupIcon,
    title: 'Comunidad Activa',
    description: 'Comparte tu viaje con otros navegantes cósmicos y aprende de sus experiencias.'
  }
]
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
