<template>
  <!-- Radar chart de progreso vital -->
  <div class="vital-radar-chart-root">
    <div class="flex flex-col items-center w-full">
      <h3 class="text-cosmic-300 font-bold mb-2">Mapa de Progreso Vital</h3>
      <!-- Radar chart SVG mock -->
      <svg :width="size" :height="size" :viewBox="viewBox" class="select-none">
        <g>
          <!-- Círculos concéntricos -->
          <circle v-for="r in rings" :key="r" :r="r" fill="none" stroke="#475569" stroke-width="0.5" />

          <!-- Líneas radiales -->
          <line v-for="(angle, i) in angles" :key="'radial-' + i"
            x1="0" y1="0"
            :x2="polarToX(100, angle)" :y2="polarToY(100, angle)"
            stroke="#475569" stroke-width="0.5" />

          <!-- Área de progreso -->
          <path :d="progressPath" fill="#38bdf850" stroke="#38bdf8" stroke-width="1" />

          <!-- Etiquetas de las áreas -->
          <text v-for="(label, i) in labels" :key="'label-' + i"
            :x="polarToX(labelRadius, angles[i])"
            :y="polarToY(labelRadius, angles[i]) + 8"
            text-anchor="middle"
            class="text-white text-[10px] font-orbitron">
            {{ label }}
          </text>
        </g>
      </svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

// Áreas vitales en orden horario desde arriba
const labels = [
  'Salud',
  'Personalidad',
  'Intelecto',
  'Carrera',
  'Finanzas',
  'Calidad de Vida',
  'Emocionalidad',
  'Relaciones'
]

// Valores de ejemplo (0-100), en el mismo orden que labels
const props = defineProps<{ values?: number[]; size?: number }>();
const values = computed(() => props.values && props.values.length === 8 ? props.values : [80, 60, 70, 30, 40, 50, 20, 60]);
const size = props.size || 300; // Increased size to accommodate larger viewBox
const center = size / 2;
const viewBox = `-${center + 20} -${center + 20} ${size + 40} ${size + 40}`; // Expanded viewBox to prevent clipping
const rings = [20, 40, 60, 80, 100];
const labelRadius = 135; // Increased from 125 to 135 to move labels farther out

// Ángulos para 8 ejes (en radianes, 0 es arriba)
const angles = Array.from({ length: 8 }, (_, i) => (Math.PI / 2) - (i * (2 * Math.PI / 8)));

// Calcular el path dinámico para el área de progreso
const progressPath = computed(() => {
  return values.value
    .map((value, i) => {
      const x = polarToX(value, angles[i]);
      const y = polarToY(value, angles[i]);
      return `${i === 0 ? 'M' : 'L'}${x},${y}`;
    })
    .join(' ') + ' Z';
});

function polarToX(r: number, angle: number) {
  return +(r * Math.cos(angle)).toFixed(2);
}
function polarToY(r: number, angle: number) {
  return +(r * Math.sin(angle)).toFixed(2);
}
</script>

<style scoped>
.vital-radar-chart-root {
  @apply w-full max-w-md mx-auto bg-slate-900/50 backdrop-blur-sm border border-cosmic-700/30 rounded-lg p-6 flex items-center justify-center;
}
svg {
  @apply block mx-auto bg-transparent;
}
</style>