<template>
  <AppLayout>

    <div class="max-w-6xl mx-auto p-6 pb-10">
      <div class="bg-gray-100 rounded-2xl shadow-xl p-6">

        <!-- Header -->
        <div class="flex items-center justify-between mb-6">
          <h1 class="text-xl font-bold text-gray-800">Applications</h1>
          <select v-model="selectedJob" class="p-2 border border-gray-300 bg-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400">
            <option value="">Select a Tour</option>
            <option v-for="job in jobs" :key="job.job_id" :value="job.job_id">{{ job.job_title }}</option>
          </select>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-12 text-gray-400 text-sm">Loading applications...</div>

        <!-- Empty states -->
        <div v-else-if="!selectedJob" class="text-center py-12 text-gray-400 text-sm">Select a tour above to view applications.</div>
        <div v-else-if="applications.length === 0" class="text-center py-12 text-gray-400 text-sm">No applications received for this tour yet.</div>

        <!-- Application List -->
        <div v-else class="space-y-3">
          <div
            v-for="(app, idx) in applications"
            :key="app.application_id || idx"
            class="flex items-stretch bg-gray-300 rounded-xl overflow-hidden"
          >
            <!-- Avatar -->
            <div class="w-24 bg-gray-400 flex flex-col items-center justify-center py-3 px-2 shrink-0">
              <div class="w-12 h-12 rounded-full bg-gray-500 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
              </div>
            </div>

            <!-- Detail -->
            <div class="flex-1 bg-gray-200 mx-2 my-2 rounded-lg p-4 flex flex-col justify-center">
              <p class="font-semibold text-gray-800">{{ app.guide_name || 'Guide Name' }}</p>
              <div class="flex flex-wrap gap-3 mt-1 text-sm text-gray-600">
                <span>{{ app.guide_phone || '—' }}</span>
                <span v-if="app.languages?.length">{{ app.languages.join(', ') }}</span>
                <span v-if="app.vehicle_type">{{ app.vehicle_type }}</span>
                <span
                  class="px-2 py-0.5 rounded-full text-xs font-semibold"
                  :class="{
                    'bg-yellow-100 text-yellow-700': app.status === 'PENDING',
                    'bg-green-100 text-green-700': app.status === 'ACCEPTED',
                    'bg-red-100 text-red-600': app.status === 'REJECTED',
                  }"
                >{{ app.status }}</span>
              </div>
            </div>

            <!-- Accept / Reject -->
            <div class="flex flex-col justify-center gap-2 pr-3 py-2 shrink-0">
              <button
                @click="handleAccept(app)"
                :disabled="app.status !== 'PENDING'"
                class="w-9 h-9 flex items-center justify-center rounded-lg bg-gray-200 hover:bg-green-100 hover:text-green-700 text-gray-600 transition disabled:opacity-40 disabled:cursor-not-allowed"
                title="Accept"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
              <button
                @click="handleReject(app)"
                :disabled="app.status !== 'PENDING'"
                class="w-9 h-9 flex items-center justify-center rounded-lg bg-gray-300 hover:bg-red-100 hover:text-red-600 text-gray-600 transition disabled:opacity-40 disabled:cursor-not-allowed"
                title="Reject"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'

const jobs = ref([])
const selectedJob = ref('')
const applications = ref([])
const loading = ref(false)

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  try {
    const res = await fetch(`${API_BASE}/jobs?em_id=${em_id}`)
    const data = await res.json()
    jobs.value = Array.isArray(data) ? data : (data.jobs || [])
  } catch (e) {
    jobs.value = []
  }
})

watch(selectedJob, async (jobId) => {
  if (!jobId) { applications.value = []; return }
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/jobs/${jobId}/applications`)
    const data = await res.json()
    applications.value = Array.isArray(data) ? data : (data.applications || [])
  } catch (e) {
    applications.value = []
  } finally {
    loading.value = false
  }
})

const handleAccept = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/applications/${app.application_id}/accept`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.status = 'ACCEPTED'
    else alert('Failed to accept application.')
  } catch (e) {
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
  } catch (e) {
    alert('Failed to reject application.')
  }
}
</script>
