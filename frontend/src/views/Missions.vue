<template>
  <div class="min-h-screen bg-[var(--theme-bg)]">
    <AppNavbar sectionTitle="Misiones" />
    <main class="container mx-auto px-2 sm:px-4 lg:px-8 py-8">
      <div class="mb-6">
        <div class="flex gap-2 border-b border-slate-700">
          <button
            v-for="tab in tabs"
            :key="tab"
            @click="activeTab = tab"
            :class="[
              'px-4 py-2 font-semibold transition',
              activeTab === tab
                ? 'border-b-2 border-cosmic-400 text-cosmic-400'
                : 'text-slate-400 hover:text-cosmic-300'
            ]"
          >
            {{ tabLabels[tab] }}
          </button>
        </div>
      </div>

      <div v-if="missionsStore.loading">
        <div class="flex justify-center items-center py-8">
          <span class="text-cosmic-400 text-lg font-semibold animate-pulse">Cargando misiones...</span>
        </div>
      </div>

      <div v-else-if="activeTab === 'activas'">
<MissionCard
          v-for="mission in activeMissions"
          :key="mission.id"
          :mission="mission"
          :user-level="userLevel"
          :show-actions="true"
        />
        <p v-if="activeMissions.length === 0" class="text-slate-400 mt-4">No tienes misiones activas.</p>
      </div>

      <div v-else-if="activeTab === 'completadas'">
<MissionCard
          v-for="mission in completedMissions"
          :key="mission.id"
          :mission="mission"
          :user-level="userLevel"
          :show-actions="false"
        />
        <p v-if="completedMissions.length === 0" class="text-slate-400 mt-4">No hay misiones completadas.</p>
      </div>

      <div v-else-if="activeTab === 'activables'">
<MissionCard
          v-for="mission in activableMissions"
          :key="mission.id"
          :mission="mission"
          :user-level="userLevel"
          :show-actions="true"
          @show-requirements="showRequirements(mission)"
          @activate="activateMission(mission)"
        />
        <p v-if="activableMissions.length === 0" class="text-slate-400 mt-4">No hay misiones activables.</p>
        <MissionRequirementsModal
          v-if="selectedMission"
          :mission="selectedMission"
          :requirements="selectedMission.requirements"
          :open="requirementsModalOpen"
          @close="requirementsModalOpen = false"
        />
      </div>

      <div v-else-if="activeTab === 'diarias'">
<MissionCard
          v-for="mission in dailyMissions"
          :key="mission.id"
          :mission="mission"
          :user-level="userLevel"
          :show-actions="true"
        />
        <p v-if="dailyMissions.length === 0" class="text-slate-400 mt-4">No hay misiones diarias.</p>
      </div>

      <div v-else-if="activeTab === 'semanales'">
<MissionCard
          v-for="mission in weeklyMissions"
          :key="mission.id"
          :mission="mission"
          :user-level="userLevel"
          :show-actions="true"
        />
        <p v-if="weeklyMissions.length === 0" class="text-slate-400 mt-4">No hay misiones semanales.</p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppNavbar from '@/components/ui/AppNavbar.vue'
import MissionCard from '@/components/missions/MissionCard.vue'
import MissionRequirementsModal from '@/components/missions/MissionRequirementsModal.vue'
import { useMissionsStore } from '@/stores/missions'
import { useAuthStore } from '@/stores/auth'

const tabs = ['activas', 'completadas', 'activables', 'diarias', 'semanales']
const tabLabels: Record<string, string> = {
  activas: 'Activas',
  completadas: 'Completadas',
  activables: 'Activables',
  diarias: 'Diarias',
  semanales: 'Semanales'
}
const activeTab = ref('activas')

const missionsStore = useMissionsStore()
const authStore = useAuthStore()
const userLevel = computed(() => authStore.user?.profile?.current_level || 1)
const activeMissions = computed(() => missionsStore.activeMissions)
const completedMissions = computed(() => missionsStore.completedMissions)
const activableMissions = computed(() => missionsStore.activableMissions)
const dailyMissions = computed(() => missionsStore.dailyMissions)
const weeklyMissions = computed(() => missionsStore.weeklyMissions)

const requirementsModalOpen = ref(false)
const selectedMission = ref(null as any)

function showRequirements(mission: any) {
  selectedMission.value = mission
  requirementsModalOpen.value = true
}

function activateMission(mission: any) {
  missionsStore.activateMission(mission)
}

// Llamar fetchMissions al montar la vista
onMounted(() => {
  missionsStore.fetchMissions()
})
</script>
