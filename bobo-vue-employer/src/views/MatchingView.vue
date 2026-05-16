<template>
  <AppLayout>

    <div class="max-w-6xl mx-auto p-6 pb-10">
      <div class="bg-gray-100 rounded-2xl shadow-xl p-6">

        <!-- Header -->
        <div class="flex items-center justify-between mb-2">
          <h1 class="text-xl font-bold text-gray-800">Matching</h1>
          <select v-model="selectedJob" class="p-2 border border-gray-300 bg-white rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400">
            <option value="">Select a Tour</option>
            <option v-for="job in jobs" :key="job.job_id" :value="job.job_id">{{ job.job_title }}</option>
          </select>
        </div>

        <!-- Sort label -->
        <div class="flex items-center gap-2 mb-5 text-xs text-gray-500">
          <div class="flex flex-col items-center">
            <span class="font-semibold text-gray-600">Sort by Score Ranking</span>
            <div class="flex flex-col items-start mt-1 ml-1 gap-0.5">
              <span>High</span>
              <div class="w-px h-8 bg-gray-400 ml-3"></div>
              <div class="w-2 h-2 rounded-full bg-gray-400 ml-2.5"></div>
              <span>Low</span>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-12 text-gray-400 text-sm">Loading candidates...</div>

        <!-- Empty -->
        <div v-else-if="!selectedJob" class="text-center py-12 text-gray-400 text-sm">Select a tour above to view matched candidates.</div>
        <div v-else-if="candidates.length === 0" class="text-center py-12 text-gray-400 text-sm">No candidates found for this tour.</div>

        <!-- Candidate List -->
        <div v-else class="space-y-3">
          <div
            v-for="(c, idx) in candidates"
            :key="c.guide_id || idx"
            class="flex items-stretch bg-gray-300 rounded-xl overflow-hidden"
          >
            <!-- Avatar + Score -->
            <div class="w-24 bg-gray-400 flex flex-col items-center justify-center py-3 px-2 shrink-0">
              <div class="w-12 h-12 rounded-full bg-gray-500 flex items-center justify-center mb-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
                </svg>
              </div>
              <span class="text-xs font-bold bg-white text-gray-700 rounded px-2 py-0.5">{{ c.score ?? '—' }}</span>
            </div>

            <!-- Detail -->
            <div class="flex-1 bg-gray-200 mx-2 my-2 rounded-lg p-4 flex flex-col justify-center">
              <p class="font-semibold text-gray-800">{{ c.guide_name || 'Guide Name' }}</p>
              <div class="flex flex-wrap gap-3 mt-1 text-sm text-gray-600">
                <span>{{ c.guide_phone || '—' }}</span>
                <span v-if="c.languages?.length">{{ c.languages.join(', ') }}</span>
                <span v-if="c.vehicle_type">{{ c.vehicle_type }}</span>
              </div>
            </div>

            <!-- Accept / Reject -->
            <div class="flex flex-col justify-center gap-2 pr-3 py-2 shrink-0">
              <button
                @click="handleAccept(c)"
                class="w-9 h-9 flex items-center justify-center rounded-lg bg-gray-200 hover:bg-green-100 hover:text-green-700 text-gray-600 transition"
                title="Accept"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
              </button>
              <button
                @click="handleReject(c)"
                class="w-9 h-9 flex items-center justify-center rounded-lg bg-gray-300 hover:bg-red-100 hover:text-red-600 text-gray-600 transition"
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
const candidates = ref([])
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
  if (!jobId) { candidates.value = []; return }
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/jobs/${jobId}/matching`)
    const data = await res.json()
    candidates.value = Array.isArray(data) ? data : (data.candidates || [])
    candidates.value.sort((a, b) => (b.score ?? 0) - (a.score ?? 0))
  } catch (e) {
    candidates.value = []
  } finally {
    loading.value = false
  }
})

const handleAccept = async (c) => {
  try {
    await fetch(`${API_BASE}/jobs/${selectedJob.value}/select`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guide_id: c.guide_id })
    })
    candidates.value = candidates.value.filter(x => x.guide_id !== c.guide_id)
  } catch (e) {
    alert('Failed to accept candidate.')
  }
}

const handleReject = async (c) => {
  try {
    await fetch(`${API_BASE}/jobs/${selectedJob.value}/reject`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ guide_id: c.guide_id })
    })
    candidates.value = candidates.value.filter(x => x.guide_id !== c.guide_id)
  } catch (e) {
    alert('Failed to reject candidate.')
  }
}
</script>
