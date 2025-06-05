<template>
  <!-- Galactic Dashboard Layout -->
  <section class="dashboard-root">
    <UserProgress
      username="CosmoUser"
      :level="1"
      :xp="50"
      :stats="{
        modules_unlocked: 3,
        missions_completed: 12,
        achievements_earned: 2
      }"
      :longest-streak="5"
    />
    <MotivationalMessage />
    <VitalRadarChart />
    <ConstellationsMap />
    <UserLog />
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import UserProgress from './UserProgress/UserProgress.vue'
import MotivationalMessage from './MotivationalMessage/MotivationalMessage.vue'
import VitalRadarChart from './VitalRadarChart/VitalRadarChart.vue'
import ConstellationsMap from './ConstellationsMap/ConstellationsMap.vue'
import UserLog from './UserLog/UserLog.vue'

export default defineComponent({
  name: 'Dashboard',
  components: {
    UserProgress,
    MotivationalMessage,
    VitalRadarChart,
    ConstellationsMap,
    UserLog
  }
})
</script>
<style scoped src="./Dashboard.css"></style>
