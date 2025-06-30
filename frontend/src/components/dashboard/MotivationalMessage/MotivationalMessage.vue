<template>
  <Card variant="interactive">
    <div class="">
      <blockquote>
        “Tu constelación de Salud brilla con intensidad. Has completado 3 declaraciones esta semana. ¡Continúa tu viaje y descubre nuevas estrategias para fortalecer tu bienestar!”
        <footer class="mt-2" :style="{ color: 'var(--theme-border)' }">— Guía Cósmico</footer>
      </blockquote>
    </div>
  </Card>
</template>

<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
</script>
<style scoped src="./MotivationalMessage.css"></style>
