<template>
  <AppLayout>

    <div class="max-w-6xl mx-auto p-6 pb-10">

      <!-- Outer container matching prototype's large rounded grey box -->
      <div class="bg-white-100 rounded-2xl shadow-xl p-6">

        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-xl font-bold text-gray-800 tracking-tight">My Tours</h1>
          <router-link
            to="/create-job"
            class="px-4 py-2 bg-gray-300 hover:bg-red-600 hover:text-white text-gray-700 text-sm font-semibold rounded-lg transition"
          >
            + Create Tour
          </router-link>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap gap-2 items-center mb-6">
          <input
            v-model="search"
            type="text"
            placeholder="Search tour title..."
            class="flex-1 min-w-0 p-2 border border-gray-300 bg-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400"
          />
          <select v-model="statusFilter" class="p-2 border border-gray-300 bg-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400">
            <option value="ALL">All Status</option>
            <option value="OPEN">Open</option>
            <option value="CLOSED">Closed</option>
            <option value="CANCELLED">Cancelled</option>
            <option value="MATCHING">Matching</option>
            <option value="SELECTED">Selected</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-16 text-gray-400">
          <p class="text-sm">Loading tours...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="filteredJobs.length === 0" class="text-center py-16 bg-white rounded-xl shadow-md border border-gray-200">
          <h3 class="text-lg font-semibold text-gray-700 mb-1">No tours found</h3>
          <p class="text-gray-400 text-sm mb-6">Get started by creating your first tour.</p>
          <router-link to="/create-job" class="px-6 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition">
            + Create Tour
          </router-link>
        </div>

        <!-- Tour Grid -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="job in filteredJobs"
            :key="job.job_id"
            class="relative bg-gray-100 hover:bg-gray-200 rounded-xl cursor-pointer transition group p-5 min-h-[140px] flex flex-col justify-between"
            @click="viewJob(job.job_id, job.job_title)"
          >
            <!-- Edit icon top-right -->
            <div class="absolute top-3 right-3 text-gray-600 group-hover:text-red-600 transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </div>

            <!-- Card body -->
            <div class="flex-1 flex items-center justify-center">
              <h3 class="font-semibold text-gray-800 text-center text-sm leading-snug px-4">{{ job.job_title }}</h3>
            </div>

            <!-- Footer: date, price, seats, status -->
            <div class="mt-3 flex items-end justify-between gap-2">
              <div class="text-xs text-gray-600 space-y-0.5">
                <div>{{ formatDate(job.job_start_date) }}</div>
                <div>฿{{ job.job_price?.toLocaleString() }} · {{ job.job_required_seat }} seats</div>
              </div>
              <span
                class="px-2 py-0.5 rounded-full text-xs font-semibold shrink-0"
                :class="{
                  'bg-green-100 text-green-700': job.job_status === 'OPEN',
                  'bg-gray-400 text-gray-800': job.job_status === 'CLOSED',
                  'bg-red-100 text-red-600': job.job_status === 'CANCELLED',
                  'bg-blue-100 text-blue-700': job.job_status === 'MATCHING',
                  'bg-yellow-100 text-yellow-700': job.job_status === 'SELECTED',
                  'bg-purple-100 text-purple-700': job.job_status === 'IN_PROGRESS',
                  'bg-teal-100 text-teal-700': job.job_status === 'COMPLETED',
                }"
              >
                {{ job.job_status }}
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

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

const viewJob = (id) => {
  router.push(`/my-tours/${id}`)
}
</script>
