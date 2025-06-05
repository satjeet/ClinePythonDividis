<template>
  <!-- Últimas declaraciones y misiones activas -->
  <div class="user-log-root">
    <div class="flex flex-col md:flex-row gap-6">
      <!-- Declaraciones recientes -->
      <div class="flex-1">
        <h4 class="text-cosmic-300 font-semibold mb-2">Últimas declaraciones</h4>
        <ul class="space-y-1 text-cosmic-100 text-sm">
          <li>
            <span class="font-bold">Salud:</span> “Me comprometo a caminar 30 minutos diarios.”
            <span class="ml-2 text-xs text-cosmic-400">hace 2 días</span>
          </li>
          <li>
            <span class="font-bold">Intelecto:</span> “Dedicaré 20 minutos a la lectura cada noche.”
            <span class="ml-2 text-xs text-cosmic-400">ayer</span>
          </li>
        </ul>
      </div>
      <!-- Misiones activas -->
      <div class="flex-1">
        <h4 class="text-cosmic-300 font-semibold mb-2">Misiones activas</h4>
        <ul class="space-y-1 text-cosmic-100 text-sm">
          <li>
            <span class="font-bold">Misión diaria:</span> Completa una declaración en cualquier área.
            <span class="ml-2 text-xs text-cosmic-400">Progreso: 1/1</span>
          </li>
          <li>
            <span class="font-bold">Misión semanal:</span> Mantén tu racha de hábitos 5 días seguidos.
            <span class="ml-2 text-xs text-cosmic-400">Progreso: 3/5</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts" src="./UserLog.ts"></script>
<style scoped src="./UserLog.css"></style>
