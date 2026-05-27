<template>
  <AppLayout>
    <div class="max-w-6xl mx-auto px-8 pt-6 pb-10">

      <!-- Header + filter -->
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-3xl font-bold text-gray-800">Applications</h1>
        <select v-model="selectedJob" class="p-2.5 border border-gray-300 bg-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 min-w-[220px]">
          <option value="">All Tours</option>
          <option v-for="job in jobs" :key="job.job_id" :value="job.job_id">{{ job.job_title }}</option>
        </select>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-16 text-gray-400 text-sm">Loading applications...</div>

      <!-- Empty -->
      <div v-else-if="filteredApplications.length === 0" class="text-center py-16 text-gray-400 text-sm bg-white rounded-2xl border border-gray-200">
        No applications found.
      </div>

      <!-- Application List -->
      <div v-else class="space-y-3">
        <div
          v-for="(app, idx) in filteredApplications"
          :key="app.application_id || idx"
          class="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition p-4 flex items-center gap-4"
        >
          <!-- Avatar -->
          <div class="w-11 h-11 rounded-full bg-[#fef2f2] text-[#dc2626] text-base font-bold flex items-center justify-center shrink-0">
            {{ (app.guide_name || '?').charAt(0).toUpperCase() }}
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-gray-800 text-sm">{{ app.guide_name || '—' }}</p>
            <p class="text-xs text-[#dc2626] font-medium mt-0.5 truncate">{{ app.job_title || '—' }}</p>
            <div class="flex flex-wrap gap-3 mt-1 text-xs text-gray-400">
              <span v-if="app.guide_phone">{{ app.guide_phone }}</span>
              <span v-if="app.languages?.length">{{ app.languages.join(', ') }}</span>
              <span v-if="app.vehicle_type">{{ app.vehicle_type }}</span>
              <span v-if="app.applied_at">Applied {{ formatDate(app.applied_at) }}</span>
            </div>
          </div>

          <!-- Status badge -->
          <span
            class="px-2.5 py-1 rounded-full text-xs font-semibold shrink-0"
            :class="{
              'bg-yellow-100 text-yellow-700': app.status === 'APPLIED' || app.status === 'PENDING',
              'bg-green-100 text-green-700': app.status === 'ACCEPTED',
              'bg-red-100 text-red-600': app.status === 'REJECTED',
            }"
          >{{ app.status }}</span>

          <!-- Accept / Reject -->
          <div class="flex items-center gap-2 shrink-0">
            <button
              @click="handleAccept(app)"
              :disabled="app.status === 'ACCEPTED' || app.status === 'REJECTED'"
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-400 hover:bg-green-50 hover:text-green-600 hover:border-green-200 transition disabled:opacity-30 disabled:cursor-not-allowed"
              title="Accept"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
              </svg>
            </button>
            <button
              @click="handleReject(app)"
              :disabled="app.status === 'ACCEPTED' || app.status === 'REJECTED'"
              class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-400 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition disabled:opacity-30 disabled:cursor-not-allowed"
              title="Reject"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>

    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'

const jobs = ref([])
const selectedJob = ref('')
const allApplications = ref([])
const loading = ref(false)

// Load all employer's tours, then fetch all applications for each
onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/tours?em_id=${em_id}`)
    const data = await res.json()
    jobs.value = Array.isArray(data) ? data : (data.jobs || [])

    // Fetch applications for all tours in parallel
    const results = await Promise.all(
      jobs.value.map(async (job) => {
        try {
          const r = await fetch(`${API_BASE}/tours/${job.job_id}/applications`)
          const apps = await r.json()
          const list = Array.isArray(apps) ? apps : (apps.applications || [])
          // Attach job title to each application
          return list.map(a => ({ ...a, job_title: job.job_title, job_id: job.job_id }))
        } catch {
          return []
        }
      })
    )
    // Flatten and sort by applied_at descending
    allApplications.value = results
      .flat()
      .sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
  } catch (e) {
    jobs.value = []
    allApplications.value = []
  } finally {
    loading.value = false
  }
})

// Filter by selected tour
const filteredApplications = computed(() => {
  if (!selectedJob.value) return allApplications.value
  return allApplications.value.filter(a => a.job_id === selectedJob.value)
})

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const handleAccept = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/applications/${app.application_id}/accept`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.status = 'ACCEPTED'
    else alert('Failed to accept application.')
  } catch {
    alert('Failed to accept application.')
  }
}

const handleReject = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/applications/${app.application_id}/reject`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.status = 'REJECTED'
    else alert('Failed to reject application.')
  } catch {
    alert('Failed to reject application.')
  }
}
</script>
