<template>
  <div class="min-h-screen bg-gray-100">
    <NavBar />

    <div class="max-w-4xl mx-auto p-4 pb-10">
      <!-- Header -->
      <div class="flex items-center justify-between mt-4 mb-6">
        <h1 class="text-2xl font-bold text-gray-800">My Tours</h1>
        <router-link
          to="/create-job"
          class="px-4 py-2 bg-blue-600 text-white text-sm font-semibold rounded-lg hover:bg-blue-700 transition"
        >
          + Create Tour
        </router-link>
      </div>

      <!-- Filters -->
      <div class="bg-white rounded-xl shadow p-3 mb-4 flex flex-wrap gap-2 items-center">
        <input
          v-model="search"
          type="text"
          placeholder="Search tour title..."
          class="flex-1 min-w-0 p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <select v-model="statusFilter" class="p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="ALL">All Status</option>
          <option value="OPEN">Open</option>
          <option value="CLOSED">Closed</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-16 text-gray-400">
        <div class="text-4xl mb-3">⏳</div>
        <p>Loading tours...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredJobs.length === 0" class="text-center py-16 bg-white rounded-xl shadow">
        <div class="text-5xl mb-4">🗺️</div>
        <h3 class="text-lg font-semibold text-gray-700 mb-1">No tours found</h3>
        <p class="text-gray-400 text-sm mb-6">Get started by creating your first tour.</p>
        <router-link to="/create-job" class="px-6 py-2 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 transition">
          + Create Tour
        </router-link>
      </div>

      <!-- Tour Cards -->
      <div v-else class="space-y-3">
        <div
          v-for="job in filteredJobs"
          :key="job.job_id"
          class="bg-white rounded-xl shadow hover:shadow-md transition cursor-pointer p-4"
          @click="viewJob(job.job_id, job.job_title)"
        >
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-800 truncate">{{ job.job_title }}</h3>
              <div class="flex flex-wrap gap-3 mt-1 text-sm text-gray-500">
                <span>📅 {{ formatDate(job.job_start_date) }}</span>
                <span>💰 ฿{{ job.job_price?.toLocaleString() }}</span>
                <span>🪑 {{ job.job_required_seat }} seats</span>
              </div>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <span
                class="px-2 py-1 rounded-full text-xs font-semibold"
                :class="{
                  'bg-green-100 text-green-700': job.job_status === 'OPEN',
                  'bg-gray-100 text-gray-600': job.job_status === 'CLOSED',
                  'bg-red-100 text-red-600': job.job_status === 'CANCELLED',
                }"
              >
                {{ job.job_status }}
              </span>
              <span class="text-gray-300">›</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'

const API_BASE = '/api'
const router = useRouter()

const jobs = ref([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('ALL')

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  try {
    const res = await fetch(`${API_BASE}/jobs?em_id=${em_id}`)
    const data = await res.json()
    jobs.value = Array.isArray(data) ? data : (data.jobs || [])
  } catch (e) {
    jobs.value = []
  } finally {
    loading.value = false
  }
})

const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    const matchSearch = job.job_title?.toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === 'ALL' || job.job_status === statusFilter.value
    return matchSearch && matchStatus
  })
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const viewJob = (id, title) => {
  router.push({ name: 'job-detail', params: { id }, state: { jobTitle: title } })
}
</script>
