<template>
  <div class="pillar-tabs">
    <ul>
      <li
        v-for="pillar in pillars"
        :key="pillar as string"
        :class="{ active: pillar === selectedPillar }"
        @click="onTabClick(pillar)"
      >
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
  },
  selectedPillar: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:selectedPillar']);

function onTabClick(pillar: unknown) {
  emit('update:selectedPillar', String(pillar));
}
</script>

<style scoped>
.pillar-tabs {
  /* Add styles here */
}
.active a {
  font-weight: bold;
  color: #fff;
  background: #3b82f6;
  border-radius: 4px;
}
</style>

<style scoped>
.pillar-tabs {
  /* Add styles here */
}
</style>
