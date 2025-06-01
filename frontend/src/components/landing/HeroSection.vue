<template>
  <section class="relative min-h-screen bg-slate-950 overflow-hidden flex items-center">
    <!-- Background elements -->
    <div class="absolute inset-0 z-0">
      <!-- Gradient overlay -->
      <div class="absolute inset-0 bg-gradient-to-b from-slate-950 via-slate-950/95 to-slate-950"></div>
      
      <!-- Animated stars -->
      <div class="absolute inset-0">
        <div v-for="i in 50" :key="i" 
             class="star"
             :style="{
               left: `${Math.random() * 100}%`,
               top: `${Math.random() * 100}%`,
               animationDelay: `${Math.random() * 3}s`
             }">
        </div>
      </div>

      <!-- Cosmic rays -->
      <div class="absolute inset-0 opacity-30">
        <div v-for="i in 3" :key="`ray-${i}`" 
             class="cosmic-ray"
             :style="{
               left: `${Math.random() * 100}%`,
               transform: `rotate(${Math.random() * 360}deg)`,
               animationDelay: `${Math.random() * 5}s`
             }">
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 relative z-10">
      <div class="max-w-4xl mx-auto text-center">
        <!-- Hero title -->
        <h1 class="text-5xl md:text-6xl font-bold tracking-tight text-cosmic-100 mb-8 animate-fade-in">
          Tu viaje de 
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-cosmic-400 to-cosmic-600">
            desarrollo personal
          </span>
          comienza aquí
        </h1>

        <!-- Description -->
        <p class="text-xl text-slate-400 mb-12 animate-fade-in animation-delay-200">
          Descubre un camino único hacia tu mejor versión a través de módulos interactivos, 
          misiones personalizadas y un sistema de progresión que te mantiene motivado.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row justify-center gap-4 animate-fade-in animation-delay-400">
          <Button @click="$emit('register')" size="lg">
            Comenzar mi viaje
          </Button>
          <Button @click="$emit('login')" variant="outline" size="lg">
            Ya tengo una cuenta
          </Button>
        </div>

        <!-- Features -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-24 animate-fade-in animation-delay-600">
          <div v-for="(feature, index) in features" 
               :key="index"
               class="p-6 bg-slate-900/50 backdrop-blur-sm rounded-lg border border-cosmic-700/30">
            <div class="w-12 h-12 rounded-lg bg-cosmic-500/20 flex items-center justify-center mb-4 mx-auto">
              <i :class="[feature.icon, 'text-cosmic-400 text-2xl']"></i>
            </div>
            <h3 class="text-lg font-medium text-cosmic-300 mb-2">
              {{ feature.title }}
            </h3>
            <p class="text-slate-400">
              {{ feature.description }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import Button from '@/components/ui/Button.vue'

const features = [
  {
    icon: 'fas fa-rocket',
    title: 'Progresión Personal',
    description: 'Sistema de niveles y experiencia que refleja tu crecimiento real.'
  },
  {
    icon: 'fas fa-tasks',
    title: 'Misiones Diarias',
    description: 'Tareas personalizadas que te ayudan a mantener el impulso.'
  },
  {
    icon: 'fas fa-star',
    title: 'Logros',
    description: 'Reconocimiento de tus hitos y celebración de tus éxitos.'
  }
]

defineEmits<{
  (e: 'register'): void
  (e: 'login'): void
}>()
</script>

<style scoped>
.star {
  @apply absolute w-1 h-1 rounded-full bg-white;
  animation: twinkle 3s infinite;
}

.cosmic-ray {
  @apply absolute w-96 h-px bg-cosmic-400;
  animation: ray 5s infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

@keyframes ray {
  0% { transform: translateX(-100%) rotate(var(--rotation)); opacity: 0; }
  50% { opacity: 0.5; }
  100% { transform: translateX(200%) rotate(var(--rotation)); opacity: 0; }
}

.animate-fade-in {
  animation: fade-in 1s ease-out forwards;
  opacity: 0;
}

.animation-delay-200 {
  animation-delay: 200ms;
}

.animation-delay-400 {
  animation-delay: 400ms;
}

.animation-delay-600 {
  animation-delay: 600ms;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
