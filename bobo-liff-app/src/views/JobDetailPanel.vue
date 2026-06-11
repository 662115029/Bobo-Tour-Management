<template>
  <div class="flex flex-col h-full bg-[#f5f5f5]" ref="panelRoot">
    <div class="flex-1 overflow-y-auto px-4 pb-24 pt-4 space-y-3" ref="scrollEl">

      <!-- Loading skeleton -->
      <div v-if="loadingDetail" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5">
        <div class="flex flex-col gap-2.5">
          <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
          <div class="animate-pulse bg-[#ebebeb] h-7 w-64 rounded"></div>
          <div class="animate-pulse bg-[#ebebeb] h-3.5 w-32 rounded"></div>
        </div>
        <div class="grid grid-cols-2 gap-3 mt-5 pt-4 border-t border-[#f0f0f0]">
          <div v-for="i in 4" :key="i" class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 flex flex-col gap-1.5">
            <div class="animate-pulse bg-[#ebebeb] h-2 w-14 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-4 w-20 rounded"></div>
          </div>
        </div>
      </div>

      <template v-else>

        <!-- Hero Card -->
        <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div class="flex-1 min-w-0">
              <div class="mb-2">
                <span :class="[BADGE_BASE, statusBadge.class]">{{ statusBadge.label }}</span>
              </div>
              <h1 class="text-[17px] font-bold text-[#111] leading-tight mb-1">{{ job.job_title }}</h1>
              <p v-if="job.job_description" class="text-[13px] text-[#888] leading-relaxed mt-1.5 max-w-sm">{{ job.job_description }}</p>
              <p class="text-[12px] text-[#bbb] mt-1">{{ job.company || job.em_name || '-' }}</p>
            </div>
            <div v-if="job.job_price" class="text-right shrink-0">
              <div class="text-[11px] text-[#bbb] tracking-wide font-medium mb-1">Rate (THB)</div>
              <div class="text-[22px] font-bold text-[#111]">฿{{ Number(job.job_price).toLocaleString() }}</div>
            </div>
          </div>

          <!-- Stat chips: date + vehicle + seats -->
          <div class="grid grid-cols-2 gap-2.5 pt-4 border-t border-[#f0f0f0]">
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Start Date</div>
              <div class="text-[13px] font-semibold text-[#222]">{{ formatDate(job.job_start_date) }}</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">End Date</div>
              <div class="text-[13px] font-semibold text-[#222]">{{ formatDate(job.job_end_date) || '-' }}</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Vehicle</div>
              <div class="text-[13px] font-semibold text-[#222]">{{ job.job_required_vehicle_type || 'VAN' }}</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Seats Required</div>
              <div class="text-[13px] font-semibold text-[#222]">{{ job.job_required_seat || '-' }}</div>
            </div>
          </div>

          <!-- Tab-specific timestamp -->
          <div v-if="tab === 'my-request' && job.applied_at" class="mt-3 pt-3 border-t border-[#f0f0f0] text-[12px] text-[#aaa]">
            Applied on {{ formatDate(job.applied_at) }}
          </div>
          <div v-if="tab === 'job-offer' && job.updated_at" class="mt-3 pt-3 border-t border-[#f0f0f0] text-[12px] text-[#aaa]">
            Offered on {{ formatDate(job.updated_at) }}
          </div>
          <div v-if="tab === 'my-job' && job.job_updated_at" class="mt-3 pt-3 border-t border-[#f0f0f0] text-[12px] text-[#aaa]">
            Matched on {{ formatDate(job.job_updated_at) }}
          </div>
        </div>

        <!-- Languages Required -->
        <div v-if="languages.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Languages Required</span>
          </div>
          <div class="px-4 py-4 flex flex-wrap gap-1.5">
            <span v-for="lang in languages" :key="lang.language_id || lang.language_name" class="info-tag language">
              {{ lang.language_name }}
            </span>
          </div>
        </div>

        <!-- Pickup Areas (my-job only) -->
        <div v-if="tab === 'my-job' && pickupAreas.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Pickup Areas</span>
          </div>
          <div class="px-4 py-4 flex flex-wrap gap-1.5">
            <span v-for="area in pickupAreas" :key="area.area_id" class="info-tag area">
              {{ area.area_name }}
            </span>
          </div>
        </div>

        <!-- Tour Schedule -->
        <div v-if="itineraries.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Tour Schedule</span>
          </div>
          <div class="px-4 py-3 flex flex-col gap-2">
            <div v-for="(it, i) in itineraries" :key="it.job_itinerary_id"
              class="flex items-center px-3 py-2.5 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8]">
              <div class="w-6 h-6 rounded-full bg-[#f3e5f5] text-[#7b1fa2] text-[11px] font-bold flex items-center justify-center shrink-0 mr-3">{{ i + 1 }}</div>
              <div class="flex-1 min-w-0">
                <div class="text-[13px] font-medium text-[#222]">{{ it.place_name }}</div>
                <div v-if="it.note" class="text-[11px] text-[#999] mt-0.5">{{ it.note }}</div>
              </div>
              <div class="flex flex-col items-end gap-0.5 ml-2 shrink-0">
                <span v-if="it.start_time" class="text-[12px] font-bold text-[#7b1fa2] bg-[#f3e5f5] px-2 py-0.5 rounded-md whitespace-nowrap">
                  {{ formatTime(it.start_time) }}{{ it.end_time ? ' – ' + formatTime(it.end_time) : '' }}
                </span>
                <span v-if="it.itinerary_date" class="text-[11px] text-[#aaa] whitespace-nowrap">{{ formatDate(it.itinerary_date) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Pick Up Points -->
        <div v-if="pickups.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Pick Up Points</span>
          </div>
          <div class="px-4 py-3 flex flex-col gap-2">
            <div v-for="(p, i) in pickups" :key="p.job_pickup_id"
              class="flex items-center gap-3 px-3 py-2.5 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8]">
              <div class="w-6 h-6 rounded-full bg-[#e8f5e9] text-[#2e7d32] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
              <div class="flex-1 min-w-0">
                <div class="text-[13px] font-medium text-[#222]">{{ p.hotel_name || p.pickup_location }}</div>
                <div v-if="p.note" class="text-[11px] text-[#999] mt-0.5">{{ p.note }}</div>
              </div>
              <span v-if="p.pickup_time" class="text-[12px] font-bold text-[#1976d2] bg-[#e3f2fd] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ formatTime(p.pickup_time) }}</span>
            </div>
          </div>
        </div>

        <!-- Pick Up Points (passengers): only visible after matched -->
        <div v-if="passengers.length && tab === 'my-job'" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Pick Up Points</span>
            <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ passengers.length }}</span>
          </div>
          <div class="px-4 py-3 flex flex-col gap-2">
            <div v-for="(p, i) in passengers" :key="p.job_passenger_id"
              class="flex items-center gap-3 px-3 py-2.5 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8]">
              <div class="w-6 h-6 rounded-full bg-[#e8f5e9] text-[#2e7d32] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
              <div class="flex-1 min-w-0">
                <div class="text-[13px] font-medium text-[#222]">{{ p.first_name }} {{ p.last_name }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">
                  <span v-if="p.hotel_name">{{ p.hotel_name }}</span>
                  <span v-if="p.hotel_name && p.note" class="mx-1 text-[#ddd]">·</span>
                  <span v-if="p.note">{{ p.note }}</span>
                </div>
              </div>
              <span v-if="p.pickup_time" class="text-[12px] font-bold text-[#1976d2] bg-[#e3f2fd] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ formatTime(p.pickup_time) }}</span>
            </div>
          </div>
        </div>

        <!-- Expenses -->
        <div v-if="expenses.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
            <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path stroke-linecap="round" stroke-linejoin="round" d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
            <span class="text-[13px] font-bold text-[#444] tracking-wide">Expenses</span>
          </div>
          <div class="px-4 py-3">
            <!-- Full breakdown: my-job only -->
            <template v-if="tab === 'my-job'">
              <div class="flex flex-col divide-y divide-[#f0f0f0]">
                <div v-for="exp in expenses" :key="exp.job_expense_id"
                  class="flex items-center justify-between py-2 px-1">
                  <span class="text-[13px] text-[#444]">{{ exp.item_name }}</span>
                  <span class="text-[13px] font-semibold text-[#222]">฿{{ Number(exp.amount).toLocaleString() }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between pt-3 mt-1 border-t-2 border-[#eee]">
                <span class="text-[13px] font-bold text-[#111]">Total</span>
                <span class="text-[15px] font-bold text-[#111]">฿{{ expenseTotal.toLocaleString() }}</span>
              </div>
            </template>
            <!-- Total only: other tabs -->
            <template v-else>
              <div class="flex items-center justify-between px-1">
                <span class="text-[13px] text-[#888]">Included in rate</span>
                <span class="text-[14px] font-bold text-[#111]">฿{{ expenseTotal.toLocaleString() }}</span>
              </div>
            </template>
          </div>
        </div>

        <!-- Status note -->
        <div v-if="tab === 'my-request'" class="bg-white rounded-xl border border-amber-200 p-4 flex items-start gap-3">
          <svg class="w-4 h-4 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
          <div>
            <p class="text-[13px] font-semibold text-amber-700">Waiting for review</p>
            <p class="text-[12px] text-amber-600 mt-0.5">Employer will review your application soon.</p>
          </div>
        </div>
        <div v-if="tab === 'job-offer'" class="bg-white rounded-xl border border-purple-200 p-4 flex items-start gap-3">
          <svg class="w-4 h-4 text-purple-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          <div>
            <p class="text-[13px] font-semibold text-purple-700">You've been invited</p>
            <p class="text-[12px] text-purple-600 mt-0.5">Employer has selected you. Please respond below.</p>
          </div>
        </div>

      </template>
    </div>

    <!-- Action buttons -->
    <div v-if="!loadingDetail" class="px-4 pb-5 pt-3 space-y-2 flex-shrink-0">

      <template v-if="tab === 'job-offer'">
        <p v-if="actionError" class="text-xs text-red-500 text-center">{{ actionError }}</p>
        <div v-if="!isVerified" class="bg-amber-50 border border-amber-200 rounded-xl px-3 py-2.5 flex items-start gap-2 mb-1">
          <svg class="w-4 h-4 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v4M12 17h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
          <p class="text-[12px] text-amber-700 leading-snug">Your account must be verified before accepting a job. Please complete your documents in Profile.</p>
        </div>
        <button class="w-full bg-red-600 text-white text-[14px] font-semibold py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:bg-red-700 transition"
          :disabled="acting || !isVerified" @click="handleAccept">
          <svg class="w-4 h-4" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg>
          {{ acting ? 'Processing...' : 'Accept' }}
        </button>
        <button class="w-full border border-[#e0e0e0] text-[#666] text-[14px] font-medium py-2.5 rounded-xl disabled:opacity-60 hover:bg-[#f5f5f5] transition"
          :disabled="acting" @click="handleReject">
          Decline
        </button>
      </template>

      <template v-if="tab === 'my-request'">
        <p v-if="actionError" class="text-xs text-red-500 text-center">{{ actionError }}</p>
        <button class="w-full border border-red-500 text-red-600 text-[14px] font-medium py-2.5 rounded-xl disabled:opacity-60 hover:bg-red-50 transition"
          :disabled="acting" @click="handleCancel">
          {{ acting ? 'Cancelling...' : 'Cancel Application' }}
        </button>
      </template>

      <template v-if="tab === 'job-opening'">
        <p v-if="actionError" class="text-xs text-red-500 text-center">{{ actionError }}</p>
        <div v-if="alreadyApplied" class="text-center text-[12px] text-[#bbb] py-2 flex items-center justify-center gap-1.5">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20 6L9 17l-5-5"/></svg>
          Already applied for this job
        </div>
        <template v-else>
          <div v-if="!isVerified" class="bg-amber-50 border border-amber-200 rounded-xl px-3 py-2.5 flex items-start gap-2 mb-1">
            <svg class="w-4 h-4 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v4M12 17h.01M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>
            <p class="text-[12px] text-amber-700 leading-snug">Your account must be verified before applying for jobs. Please complete your documents in Profile.</p>
          </div>
          <button class="w-full bg-red-600 text-white text-[14px] font-semibold py-3 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 hover:bg-red-700 transition"
            :disabled="acting || !isVerified" @click="handleApply">
            <svg class="w-4 h-4" fill="none" stroke="white" stroke-width="2.5" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>
            {{ acting ? 'Applying...' : 'Apply' }}
          </button>
        </template>
      </template>

    </div>

    <!-- Scroll to top button -->
    <button v-if="showScrollTop"
      class="fixed bottom-24 right-5 w-10 h-10 bg-white border border-[#e0e0e0] shadow-md rounded-full flex items-center justify-center text-[#666] hover:bg-[#f5f5f5] transition z-10"
      @click="scrollToTop">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 19V5M5 12l7-7 7 7"/></svg>
    </button>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { getJobStatusClass, formatJobStatus, BADGE_BASE } from '@/utils/statusClasses.js'

const props = defineProps({
  job: { type: Object, required: true },
  tab: { type: String, required: true },
  user: { type: Object, default: null },
})
const emit = defineEmits(['action-done', 'show-toast'])
const scrollEl = ref(null)
const showScrollTop = ref(false)

function onScroll() {
  showScrollTop.value = scrollEl.value?.scrollTop > 120
}

function scrollToTop() {
  scrollEl.value?.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  scrollEl.value?.addEventListener('scroll', onScroll)
})

onUnmounted(() => {
  scrollEl.value?.removeEventListener('scroll', onScroll)
})

const pickups = ref([])
const itineraries = ref([])
const passengers = ref([])
const expenses = ref([])
const languages = ref([])
const pickupAreas = ref([])
const loadingDetail = ref(false)
const acting = ref(false)
const actionError = ref('')
const alreadyApplied = ref(false)
const isVerified = ref(true)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

const jobId = computed(() => props.job.job_id)

const expenseTotal = computed(() =>
  expenses.value.reduce((sum, e) => sum + Number(e.amount || 0), 0)
)

onMounted(async () => {
  loadingDetail.value = true
  try {
    const [pickupRes, itinRes, passengerRes, expenseRes, langRes] = await Promise.all([
      fetch(`${API_BASE}/job-pickups?job_id=${jobId.value}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-itineraries?job_id=${jobId.value}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-passengers?job_id=${jobId.value}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-expenses?job_id=${jobId.value}`, { headers: HEADERS }),
      fetch(`${API_BASE}/job-required-languages?job_id=${jobId.value}`, { headers: HEADERS }),
    ])
    const [pickupData, itinData, passengerData, expenseData, langData] = await Promise.all([
      pickupRes.json(), itinRes.json(), passengerRes.json(), expenseRes.json(), langRes.json()
    ])
    pickups.value = pickupData.items || []
    itineraries.value = (itinData.items || []).sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
    passengers.value = passengerData.items || []
    expenses.value = (expenseData.items || []).sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
    languages.value = langData.items || []

    if (props.tab === 'job-opening' && props.user?.fl_id) {
      const appRes = await fetch(`${API_BASE}/job-applications?job_id=${jobId.value}&fl_id=${props.user.fl_id}`, { headers: HEADERS })
      if (appRes.ok) {
        const appData = await appRes.json()
        alreadyApplied.value = (appData.items || []).length > 0
      }
    }

    if (props.tab === 'my-job' && props.user?.fl_id) {
      const areaRes = await fetch(`${API_BASE}/fl-pickup-areas?fl_id=${props.user.fl_id}`, { headers: HEADERS })
      if (areaRes.ok) {
        const areaData = await areaRes.json()
        pickupAreas.value = areaData.items || []
      }
    }

    // Fresh verify status for apply/accept gating
    if ((props.tab === 'job-opening' || props.tab === 'job-offer') && props.user?.fl_id) {
      const flRes = await fetch(`${API_BASE}/freelancers/${props.user.fl_id}`, { headers: HEADERS })
      if (flRes.ok) {
        const flData = await flRes.json()
        isVerified.value = flData.fl_verify_status === 'VERIFIED'
      }
    }
  } catch (e) { console.error(e) }
  finally { loadingDetail.value = false }
})

const statusBadge = computed(() => {
  const s = props.job.job_status || props.job.application_status || ''
  return { label: formatJobStatus(s) || s, class: getJobStatusClass(s) }
})

async function handleAccept() {
  acting.value = true; actionError.value = ''
  try {
    const res = await fetch(`${API_BASE}/job-applications/${props.job.job_application_id}/accept`, {
      method: 'PATCH', headers: HEADERS
    })
    if (!res.ok) { const d = await res.json(); actionError.value = d.detail || 'Failed.'; return }
    emit('show-toast', { message: 'You have accepted this job', type: 'success' })
    emit('action-done')
  } catch { actionError.value = 'Cannot connect.' }
  finally { acting.value = false }
}

async function handleReject() {
  acting.value = true; actionError.value = ''
  try {
    const res = await fetch(`${API_BASE}/job-applications/${props.job.job_application_id}/reject`, {
      method: 'PATCH', headers: HEADERS
    })
    if (!res.ok) { const d = await res.json(); actionError.value = d.detail || 'Failed.'; return }
    emit('show-toast', { message: 'Offer declined', type: 'info' })
    emit('action-done')
  } catch { actionError.value = 'Cannot connect.' }
  finally { acting.value = false }
}

async function handleCancel() {
  acting.value = true; actionError.value = ''
  try {
    const res = await fetch(`${API_BASE}/job-applications/${props.job.job_application_id}?fl_id=${props.user.fl_id}`, {
      method: 'DELETE', headers: HEADERS
    })
    if (!res.ok) { const d = await res.json(); actionError.value = d.detail || 'Failed.'; return }
    emit('show-toast', { message: 'Application cancelled', type: 'info' })
    emit('action-done')
  } catch { actionError.value = 'Cannot connect.' }
  finally { acting.value = false }
}

async function handleApply() {
  acting.value = true; actionError.value = ''
  try {
    const res = await fetch(`${API_BASE}/job-applications`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ job_id: jobId.value, fl_id: props.user.fl_id }),
    })
    const data = await res.json()
    if (!res.ok) { actionError.value = data.detail || 'Failed to apply.'; return }
    alreadyApplied.value = true
    emit('show-toast', { message: 'Application submitted successfully', type: 'success' })
    emit('action-done')
  } catch { actionError.value = 'Cannot connect.' }
  finally { acting.value = false }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(String(dateStr).replace(' ', 'T'))
    .toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

function formatTime(val) {
  if (!val && val !== 0) return null
  // If it's a number (seconds from midnight)
  if (typeof val === 'number' || /^\d+$/.test(String(val))) {
    const secs = Number(val)
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`
  }
  // Already HH:MM:SS string - trim to HH:MM
  return String(val).slice(0, 5)
}
</script>