<template>
  <!-- Barra de experiencia cósmica -->
  <div class="experience-bar-root">
    <div class="flex flex-col w-full">
      <div class="flex items-center justify-between mb-1">
        <span class="text-cosmic-300 font-bold text-lg">Nivel 7</span>
        <span class="text-cosmic-400 font-semibold">Explorador Estelar</span>
      </div>
      <div class="w-full bg-cosmic-700/30 rounded-full h-3 relative">
        <div class="bg-cosmic-400 h-3 rounded-full" style="width: 68%"></div>
        <span class="absolute right-2 top-0 text-xs text-cosmic-100 font-mono">340 / 500 XP</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./ExperienceBar.ts"></script>
<style scoped src="./ExperienceBar.css"></style>
