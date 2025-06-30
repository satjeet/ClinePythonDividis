<template>
  <Card variant="interactive" class="dashboard-root">
    <div class="mb-6">
      <UserProgress
        :username="userProgress.username.value"
        :level="userProgress.level.value"
        :xp="userProgress.xp.value"
        :stats="userProgress.stats.value"
        :longest-streak="userProgress.longestStreak.value"
        :title="userProgress.title.value"
      />
    </div>
    <div class="mb-6">
      <MotivationalMessage />
    </div>
    <div class="mb-6">
      <VitalRadarChart :values="vitalRadar.values" />
    </div>
    <div class="mb-6">
      <ConstellationsMap />
    </div>
    <UserLog />
  </Card>
</template>

<script setup lang="ts">
import Card from '@/components/ui/Card.vue'
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useUserProgressStore } from '../../stores/userProgress'
import { useVitalRadarStore } from '../../stores/vitalRadar'
import UserProgress from './UserProgress/UserProgress.vue'
import MotivationalMessage from './MotivationalMessage/MotivationalMessage.vue'
import VitalRadarChart from './VitalRadarChart/VitalRadarChart.vue'
import ConstellationsMap from './ConstellationsMap/ConstellationsMap.vue'
import UserLog from './UserLog/UserLog.vue'

const userProgressStore = useUserProgressStore()
const userProgress = storeToRefs(userProgressStore)
const vitalRadar = useVitalRadarStore()

onMounted(() => {
  userProgressStore.fetchProgress()
  vitalRadar.fetchRadarValues()
})
</script>
<style scoped src="./Dashboard.css"></style>
