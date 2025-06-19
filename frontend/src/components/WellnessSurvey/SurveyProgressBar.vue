<template>
  <!-- Barra de progreso de la encuesta -->
  <div class="survey-progress-bar mb-8">
    <div class="flex items-center justify-between mb-3">
      <span class="text-cosmic-100 text-lg font-semibold">
        Paso {{ currentStep }} de {{ totalSteps }}
        <span class="text-cosmic-400 text-sm ml-2">
          {{ Math.round((currentStep / totalSteps) * 100) }}% completado
        </span>
      </span>
    </div>
    <div class="w-full bg-cosmic-700 rounded-full h-3 shadow-inner">
      <div
        class="bg-cosmic-400 h-3 rounded-full transition-all duration-500 shadow"
        :style="{ width: `${Math.round((currentStep / totalSteps) * 100)}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ currentStep: number; totalSteps: number }>();
</script>

<style scoped>
.survey-progress-bar {
  width: 100%;
}
</style>
