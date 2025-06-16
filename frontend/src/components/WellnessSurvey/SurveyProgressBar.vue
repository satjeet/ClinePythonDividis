<template>
  <!-- Barra de progreso de la encuesta -->
  <div class="survey-progress-bar mb-6">
    <div class="flex items-center justify-between mb-1">
      <span class="text-cosmic-400 font-semibold">Paso {{ currentStep }} de {{ totalSteps }}</span>
    </div>
    <div class="w-full bg-slate-800 rounded-full h-2">
      <div
        class="bg-sky-400 h-2 rounded-full transition-all duration-500"
        :style="{ width: `${Math.round((currentStep / totalSteps) * 100)}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ currentStep: number; totalSteps: number }>();
</script>

<style scoped>
.survey-progress-bar {
  width: 100%;
}
</style>
