import { ref, onMounted } from 'vue'
import { fetchStats } from '../data/api'

export const useStats = () => {
  const stats = ref({
    totalJobs: 0,
    pendingVerify: 0,
    freelancers: 0,
    employers: 0
  })
  const loading = ref(true)
  const error = ref(null)

  const loadStats = async () => {
    try {
      loading.value = true
      const data = await fetchStats()
      stats.value = {
        totalJobs: 0,
        pendingVerify: data.pendingVerify || 0,
        freelancers: data.freelancers || 0,
        employers: data.employers || 0
      }
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  onMounted(loadStats)

  return { stats, loading, error }
}