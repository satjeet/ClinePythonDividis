import { defineComponent, ref, onMounted } from 'vue'
import api from '@/services/api'

export default defineComponent({
  name: 'UserLog',
  setup() {
    const globalMissions = ref<{ id: string, title: string, description: string, xp_reward: number, state: string }[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    onMounted(async () => {
      loading.value = true
      try {
        const res = await api.get('/missions/global/')
        globalMissions.value = res.data
      } catch (e: any) {
        error.value = e.message || 'Error al cargar misiones globales'
      } finally {
        loading.value = false
      }
    })

    return {
      globalMissions,
      loading,
      error
    }
  }
})
