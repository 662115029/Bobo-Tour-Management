<template>
  <AppLayout>
    <div class="max-w-6xl mx-auto px-8 pb-10">
      <!-- Header -->
      <div class="flex items-center justify-center mt-8 mb-6">
        <h1 class="text-5xl font-bold text-center tracking-tight text-[#dc2626]" style="font-family: 'Georgia', serif;">My Tours</h1>
      </div>

      <!-- Filters + Create Tour -->
      <div class="bg-white rounded-xl border border-gray-200 p-4 mb-6 flex flex-wrap gap-3 items-center">
        <input
          v-model="search"
          type="text"
          placeholder="Search tour title..."
          class="flex-1 min-w-0 p-3 border border-gray-300 rounded-lg text-sm focus:outline-none"        />
        <select v-model="statusFilter" class="p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
          <option value="ALL">All</option>
          <option value="OPEN">Open</option>
          <option value="MATCHING">Matched</option>
          <option value="SELECTED">Pending</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
          <option value="CANCELLED">Cancelled</option>
        </select>
        <select v-model="yearFilter" class="p-3 border border-gray-300 rounded-lg text-sm focus:outline-none">
          <option value="">All Years</option>
          <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
        </select>
        <select v-model="monthFilter" class="p-3 border border-gray-300 rounded-lg text-sm focus:outline-none">
          <option value="">All Months</option>
          <option value="1">January</option>
          <option value="2">February</option>
          <option value="3">March</option>
          <option value="4">April</option>
          <option value="5">May</option>
          <option value="6">June</option>
          <option value="7">July</option>
          <option value="8">August</option>
          <option value="9">September</option>
          <option value="10">October</option>
          <option value="11">November</option>
          <option value="12">December</option>
        </select>
        <router-link
          to="/create-tour"
            class="px-5 py-3 bg-white text-black border border-black text-sm font-semibold rounded-lg hover:bg-black hover:text-white transition whitespace-nowrap"        >
          Create Tour
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-16 text-gray-400">
        <div class="text-4xl mb-3">⏳</div>
        <p>Loading tours...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="filteredJobs.length === 0" class="text-center py-16 bg-white rounded-xl border border-gray-200">
        <div class="text-5xl mb-4">🗺️</div>
        <h3 class="text-lg font-semibold text-gray-700 mb-1">No tours found</h3>
        <p class="text-gray-400 text-sm mb-6">Get started by creating your first tour.</p>
        <router-link to="/create-tour" class="px-6 py-2 bg-black text-white rounded-lg text-sm font-semibold hover:bg-black transition">
          Create Tour
        </router-link>
      </div>

      <!-- Tour Cards Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="job in filteredJobs"
          :key="job.job_id"
          class="bg-white rounded-xl border border-gray-200 hover:shadow-lg hover:border-gray-300 transition cursor-pointer flex flex-col shadow-sm overflow-hidden"
          @click="viewJob(job.job_id, job.job_title)"
        >
          <!-- Card Body -->
          <div class="p-5 flex flex-col gap-4">

            <!-- Title + Edit -->
            <div class="flex items-start justify-between gap-2">
              <h3 class="font-semibold text-gray-800 text-base leading-snug flex-1">{{ job.job_title }}</h3>
              <button
                @click.stop="viewJob(job.job_id, job.job_title)"
                class="flex items-center gap-1 text-xs text-gray-400 hover:text-[#dc2626] hover:bg-[#fef2f2] px-2 py-1 rounded-md transition shrink-0"
              >
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" />
                </svg>
                Edit
              </button>
            </div>

            <div class="border-t border-gray-100"></div>

            <!-- START → END -->
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
              </div>
              <div class="flex items-center gap-3 flex-1">
                <div>
                  <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Start</p>
                  <p class="text-md font-sm text-gray-700">{{ formatDate(job.job_start_date) }}</p>
                </div>
                <svg class="w-4 h-4 text-gray-300 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3"/>
                </svg>
                <div>
                  <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">End</p>
                  <p class="text-md font-sm text-gray-700">{{ formatDate(job.job_end_date) || '—' }}</p>
                </div>
              </div>
            </div>

            <!-- Rate -->
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center shrink-0">
                <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <div>
                <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Rate (THB)</p>
                <p class="text-sm text-gray-700">฿{{ job.job_price?.toLocaleString() }}</p>
              </div>
            </div>

          </div>

          <!-- Footer: status + created -->
          <div class="mt-auto border-t border-gray-100 grid grid-cols-2 divide-x divide-gray-100">
            <div class="px-4 py-3 flex items-center justify-center">
              <span
                class="px-2.5 py-1 rounded-md text-xs font-medium"
                :class="{
                  'bg-green-100 text-green-700': job.job_status === 'OPEN',
                  'bg-blue-100 text-blue-600': job.job_status === 'MATCHING',
                  'bg-yellow-100 text-yellow-700': job.job_status === 'SELECTED',
                  'bg-purple-100 text-purple-700': job.job_status === 'IN_PROGRESS',
                  'bg-gray-100 text-gray-500': job.job_status === 'COMPLETED' || job.job_status === 'CLOSED',
                  'bg-red-100 text-red-600': job.job_status === 'CANCELLED',
                }"
              >{{ job.job_status }}</span>
            </div>
            <div class="px-4 py-3 text-center">
              <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">Created</p>
              <p class="text-xs text-gray-600">{{ formatDate(job.job_created_at) }}</p>
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
import AppLayout from '@/components/AppLayout.vue'

const API_BASE = '/api'
const router = useRouter()

const jobs = ref([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('ALL')
const yearFilter = ref('')
const monthFilter = ref('')

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

const availableYears = computed(() => {
  const years = new Set()
  jobs.value.forEach(job => {
    if (job.job_start_date) years.add(new Date(job.job_start_date).getFullYear())
  })
  return [...years].sort((a, b) => b - a)
})

const filteredJobs = computed(() => {
  return jobs.value.filter(job => {
    const matchSearch = job.job_title?.toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === 'ALL' || job.job_status === statusFilter.value
    const date = job.job_start_date ? new Date(job.job_start_date) : null
    const matchYear = !yearFilter.value || (date && date.getFullYear() === Number(yearFilter.value))
    const matchMonth = !monthFilter.value || (date && date.getMonth() + 1 === Number(monthFilter.value))
    return matchSearch && matchStatus && matchYear && matchMonth
  })
})

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const viewJob = (id, title) => {
  router.push({ name: 'tour-detail', params: { id }, state: { jobTitle: title } })
}
</script>
