<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100">
      <button class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center" @click="$router.push('/jobs')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
      </button>
      <div>
        <p class="text-xs font-semibold text-red-600 uppercase tracking-wider">Job</p>
        <h2 class="text-lg font-bold text-gray-900 leading-tight">Details</h2>
      </div>
    </div>

    <!-- Loading -->
    <LoadingView v-if="loading" message="Loading job details..." />

    <!-- Not found -->
    <div v-else-if="!job" class="flex-1 flex flex-col items-center justify-center gap-3 text-center px-6">
      <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="1.5">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>
        </svg>
      </div>
      <p class="text-sm font-semibold text-gray-500">Job not found</p>
    </div>

    <div v-else class="flex-1 overflow-y-auto p-4 space-y-3">

      <!-- Job card -->
      <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5">
        <div class="flex items-start justify-between gap-2 mb-2">
          <h3 class="text-base font-bold text-gray-900 flex-1">{{ job.job_title }}</h3>
          <span class="text-xs font-bold px-2.5 py-1 rounded-full flex-shrink-0" :class="statusStyle(job.job_status).badge">
            {{ job.job_status }}
          </span>
        </div>
        <p class="text-xs text-gray-400 flex items-center gap-1 mb-4">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
          {{ job.company }}
        </p>

        <!-- Description -->
        <p v-if="job.job_description" class="text-sm text-gray-600 leading-relaxed mb-4 pb-4 border-b border-gray-50">
          {{ job.job_description }}
        </p>

        <!-- Schedule -->
        <div class="mb-4">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Schedule</p>
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                Start Date
              </span>
              <span class="font-medium text-gray-700">{{ formatDate(job.job_start_date) }}</span>
            </div>
            <div v-if="job.job_end_date" class="flex justify-between text-sm">
              <span class="text-gray-400 flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                End Date
              </span>
              <span class="font-medium text-gray-700">{{ formatDate(job.job_end_date) }}</span>
            </div>
          </div>
        </div>

        <!-- Requirements -->
        <div class="mb-4">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Requirements</p>
          <div class="space-y-2">
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><rect x="1" y="8" width="15" height="10" rx="1.5"/><path d="M16 10l4 2v6h-4V10z"/><circle cx="5.5" cy="19.5" r="1.5"/><circle cx="13.5" cy="19.5" r="1.5"/><circle cx="19.5" cy="19.5" r="1.5"/></svg>
                Vehicle
              </span>
              <span class="font-medium text-gray-700">{{ job.job_required_vehicle_type }}</span>
            </div>
            <div class="flex justify-between text-sm">
              <span class="text-gray-400 flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>
                Passengers
              </span>
              <span class="font-medium text-gray-700">{{ job.job_required_seat }} people</span>
            </div>
            <div v-if="job.job_price" class="flex justify-between text-sm">
              <span class="text-gray-400 flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 1 0 0 7h5a3.5 3.5 0 1 1 0 7H6"/></svg>
                Pay
              </span>
              <span class="font-bold text-green-600">฿{{ Number(job.job_price).toLocaleString() }}</span>
            </div>
          </div>
        </div>

        <!-- Pickups -->
        <div v-if="pickups.length" class="mb-4">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Pickup Points</p>
          <div class="space-y-2">
            <div v-for="(p, i) in pickups" :key="p.job_pickup_id"
              class="flex items-start gap-2 text-sm">
              <div class="w-5 h-5 rounded-full bg-red-100 text-red-600 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                {{ i + 1 }}
              </div>
              <div>
                <p class="font-medium text-gray-700">{{ p.hotel_name || p.pickup_location }}</p>
                <p v-if="p.pickup_time" class="text-xs text-gray-400">{{ p.pickup_time }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Itineraries -->
        <div v-if="itineraries.length">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Itinerary</p>
          <div class="space-y-2">
            <div v-for="(it, i) in itineraries" :key="it.job_itinerary_id"
              class="flex items-start gap-2 text-sm">
              <div class="w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                {{ i + 1 }}
              </div>
              <div>
                <p class="font-medium text-gray-700">{{ it.place_name }}</p>
                <p v-if="it.start_time" class="text-xs text-gray-400">{{ it.start_time }}{{ it.end_time ? ' – ' + it.end_time : '' }}</p>
                <p v-if="it.note" class="text-xs text-gray-400 italic">{{ it.note }}</p>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Applied already -->
      <div v-if="alreadyApplied" class="bg-blue-50 border border-blue-200 rounded-2xl p-4 text-center">
        <svg class="mx-auto mb-2" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2">
          <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
        </svg>
        <p class="text-sm font-semibold text-blue-700">Application Submitted</p>
        <p class="text-xs text-blue-500 mt-1">Waiting for employer to review your application.</p>
      </div>

      <!-- Success -->
      <div v-else-if="applied" class="bg-green-50 border border-green-200 rounded-2xl p-4 text-center">
        <svg class="mx-auto mb-2" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5">
          <path d="M20 6L9 17l-5-5"/>
        </svg>
        <p class="text-sm font-semibold text-green-700">Applied Successfully!</p>
        <p class="text-xs text-green-500 mt-1">The employer will review your application.</p>
        <button class="mt-3 text-xs text-green-700 font-semibold underline" @click="$router.push('/jobs')">
          Back to Jobs
        </button>
      </div>

      <!-- Apply button (only for OPEN jobs) -->
      <div v-else-if="job.job_status === 'OPEN'" class="pb-2">
        <p v-if="applyError" class="text-xs text-red-500 text-center mb-2">{{ applyError }}</p>
        <button
          class="w-full bg-red-600 text-white text-sm font-bold py-4 rounded-2xl disabled:opacity-60 flex items-center justify-center gap-2 active:scale-[0.98] transition-transform"
          :disabled="applying"
          @click="handleApply">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          {{ applying ? 'Applying...' : 'Apply for this Job' }}
        </button>
      </div>

    </div>

  </div>
</template>

<script setup>
import LoadingView from './LoadingView.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({ user: Object })
const route = useRoute()

const job = ref(null)
const pickups = ref([])
const itineraries = ref([])
const loading = ref(true)
const applying = ref(false)
const applied = ref(false)
const alreadyApplied = ref(false)
const applyError = ref('')

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

onMounted(async () => {
  const jobId = route.params.id
  try {
    const [jobRes, pickupRes, itineraryRes] = await Promise.all([
      fetch(`${API_BASE}/jobs/${jobId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-pickups?job_id=${jobId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-itineraries?job_id=${jobId}`, { headers: HEADERS }),
    ])
    const [jobData, pickupData, itineraryData] = await Promise.all([
      jobRes.json(), pickupRes.json(), itineraryRes.json()
    ])
    job.value = jobRes.ok ? jobData : null
    pickups.value = pickupData.items || []
    itineraries.value = itineraryData.items || []

    // Check if already applied
    if (props.user?.fl_id) {
      const appRes = await fetch(`${API_BASE}/job-applications?job_id=${jobId}&fl_id=${props.user.fl_id}`, { headers: HEADERS })
      if (appRes.ok) {
        const appData = await appRes.json()
        alreadyApplied.value = (appData.items || []).length > 0
      }
    }
  } catch (e) {
    console.error('Failed to load job:', e)
  } finally {
    loading.value = false
  }
})

async function handleApply() {
  if (!props.user?.fl_id) { applyError.value = 'Please login first.'; return }
  applying.value = true; applyError.value = ''
  try {
    const res = await fetch(`${API_BASE}/job-applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ job_id: job.value.job_id, fl_id: props.user.fl_id }),
    })
    const data = await res.json()
    if (!res.ok) { applyError.value = data.detail || 'Failed to apply.'; return }
    applied.value = true
  } catch { applyError.value = 'Cannot connect to server.' }
  finally { applying.value = false }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

function statusStyle(status) {
  if (status === 'OPEN')    return { badge: 'bg-green-100 text-green-700' }
  if (status === 'MATCHED') return { badge: 'bg-blue-100 text-blue-700' }
  if (status === 'CLOSED')  return { badge: 'bg-gray-100 text-gray-500' }
  return                           { badge: 'bg-amber-100 text-amber-700' }
}
</script>