<template>
  <div class="pillar-tabs">
    <ul>
      <li v-for="pillar in pillars" :key="pillar as string" @click="emit('pillar-click', pillar)">
        <a href="#">{{ pillar }}</a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
defineProps({
  pillars: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['pillar-click']);
</script>

<style scoped>
.pillar-tabs {
  /* Add styles here */
}
</style>
