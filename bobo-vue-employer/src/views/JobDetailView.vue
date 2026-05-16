<template>
  <AppLayout>
    <div class="max-w-3xl mx-auto p-6 pb-16">

      <!-- ── Loading ── -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-32 text-gray-400">
        <svg class="animate-spin w-8 h-8 mb-3 text-red-500" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        <span class="text-sm">Loading tour details…</span>
      </div>

      <!-- ── Error ── -->
      <div v-else-if="error" class="mt-20 text-center">
        <p class="text-red-500 font-medium mb-4">{{ error }}</p>
        <button @click="fetchJob" class="px-5 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition">Retry</button>
      </div>

      <!-- ── Content ── -->
      <template v-else-if="job">

        <!-- Back + Header -->
        <div class="flex items-start gap-3 mb-6 mt-4">
          <button @click="$router.back()" class="mt-1 p-1.5 rounded-lg hover:bg-gray-100 transition text-gray-400 hover:text-gray-700 flex-shrink-0">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
            </svg>
          </button>
          <div class="flex-1 min-w-0">
            <div class="flex flex-wrap items-center gap-2 mb-1">
              <span :class="statusClass(job.job_status)" class="text-xs font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wide flex-shrink-0">
                {{ statusLabel(job.job_status) }}
              </span>
              <span class="text-xs text-gray-400 flex-shrink-0">{{ job.job_id }}</span>
            </div>
            <h1 class="text-xl font-bold text-gray-800 leading-snug">
              {{ editing ? form.job_title || 'Edit Tour' : job.job_title }}
            </h1>
          </div>
          <!-- Edit mode indicator -->
          <span v-if="editing" class="mt-1 text-xs font-semibold text-amber-600 bg-amber-50 border border-amber-200 px-2.5 py-1 rounded-lg flex-shrink-0">Editing</span>
        </div>

        <!-- ── 1. General Info ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">General Information</h2>

          <!-- VIEW MODE -->
          <template v-if="!editing">
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div class="info-block"><span class="info-label">Start Date</span><span class="info-value">{{ formatDate(job.job_start_date) }}</span></div>
              <div class="info-block"><span class="info-label">End Date</span><span class="info-value">{{ formatDate(job.job_end_date) }}</span></div>
              <div class="info-block"><span class="info-label">Vehicle</span><span class="info-value">{{ job.job_required_vehicle_type || '—' }}</span></div>
              <div class="info-block"><span class="info-label">Seats</span><span class="info-value">{{ job.job_required_seat ?? '—' }}</span></div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div class="info-block">
                <span class="info-label">Rate (THB)</span>
                <span class="info-value text-red-600 font-bold text-base">฿{{ Number(job.job_price).toLocaleString() || '—' }}</span>
              </div>
              <div class="info-block" v-if="job.job_required_languages?.length">
                <span class="info-label">Languages Required</span>
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span v-for="lang in job.job_required_languages" :key="lang" class="px-2.5 py-0.5 bg-red-50 text-red-700 text-xs font-medium rounded-full border border-red-100">{{ lang }}</span>
                </div>
              </div>
            </div>
            <div v-if="job.job_description" class="info-block">
              <span class="info-label">Description</span>
              <p class="text-sm text-gray-700 mt-1 leading-relaxed">{{ job.job_description }}</p>
            </div>
          </template>

          <!-- EDIT MODE -->
          <template v-else>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="md:col-span-2">
                <label class="field-label">Tour Title *</label>
                <input v-model="form.job_title" type="text" class="field-input" />
              </div>
              <div>
                <label class="field-label">Start Date *</label>
                <input v-model="form.job_start_date" type="date" class="field-input" />
              </div>
              <div>
                <label class="field-label">End Date *</label>
                <input v-model="form.job_end_date" type="date" class="field-input" />
              </div>
              <div>
                <label class="field-label">Number of Seats *</label>
                <input v-model.number="form.job_required_seat" type="number" min="1" max="13" class="field-input" />
              </div>
              <div>
                <label class="field-label">Rate (THB) *</label>
                <input v-model.number="form.job_price" type="number" class="field-input" />
              </div>
              <div>
                <label class="field-label">Vehicle Type *</label>
                <select v-model="form.job_required_vehicle_type" class="field-input">
                  <option value="VAN">Van</option>
                  <option value="CAR">Car</option>
                </select>
              </div>
              <div>
                <label class="field-label">Languages Required</label>
                <div class="flex flex-wrap gap-2 mt-1">
                  <button
                    v-for="lang in allLanguages" :key="lang"
                    type="button"
                    @click="toggleLanguage(lang)"
                    :class="[
                      'px-3 py-1 rounded-full text-xs font-medium border transition-colors',
                      form.job_required_languages.includes(lang)
                        ? 'bg-red-600 text-white border-red-600'
                        : 'bg-white text-gray-600 border-gray-300 hover:border-red-400',
                    ]"
                  >{{ lang }}</button>
                </div>
              </div>
              <div class="md:col-span-2">
                <label class="field-label">Description</label>
                <textarea v-model="form.job_description" rows="3" class="field-input"></textarea>
              </div>
            </div>
          </template>
        </div>

        <!-- ── 2. Driver & Vehicle ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Driver & Vehicle</h2>
          <template v-if="!editing">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="info-block"><span class="info-label">Driver Name</span><span class="info-value">{{ job.driver_name || '—' }}</span></div>
              <div class="info-block"><span class="info-label">Phone Number</span><span class="info-value">{{ job.driver_phone || '—' }}</span></div>
            </div>
          </template>
          <template v-else>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="field-label">Driver Name</label>
                <input v-model="form.driver_name" type="text" class="field-input" placeholder="Driver Name" />
              </div>
              <div>
                <label class="field-label">Phone Number</label>
                <input v-model="form.driver_phone" type="tel" class="field-input" placeholder="08x xxx xxxx" />
              </div>
            </div>
          </template>
        </div>

        <!-- ── 3. Pickup Points ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Pickup Points <span class="count-badge">{{ editing ? form.job_pickups.length : job.job_pickups?.length }}</span></h2>
          <template v-if="!editing">
            <div class="space-y-2">
              <div v-for="(pickup, idx) in sortedPickups" :key="idx" class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl">
                <div class="w-7 h-7 rounded-full bg-red-100 text-red-600 text-xs font-bold flex items-center justify-center flex-shrink-0">{{ idx + 1 }}</div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-800">{{ pickup.hotel_name || '—' }}</p>
                  <p v-if="pickup.pickup_location" class="text-xs text-gray-500">{{ pickup.pickup_location }}</p>
                </div>
                <span v-if="pickup.pickup_time" class="text-xs font-semibold text-gray-600 bg-white border border-gray-200 px-2 py-0.5 rounded-lg flex-shrink-0">{{ pickup.pickup_time }}</span>
              </div>
              <p v-if="!job.job_pickups?.length" class="text-sm text-gray-400">No pickup points</p>
            </div>
          </template>
          <template v-else>
            <div v-for="(pickup, idx) in form.job_pickups" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div><label class="field-label">Hotel Name</label><input v-model="pickup.hotel_name" type="text" class="field-input" placeholder="Hotel" /></div>
              <div><label class="field-label">Group / Customer</label><input v-model="pickup.pickup_location" type="text" class="field-input" placeholder="Name" /></div>
              <div><label class="field-label">Pickup Time</label><input v-model="pickup.pickup_time" type="time" class="field-input" /></div>
              <button type="button" @click="form.job_pickups.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="form.job_pickups.push({ hotel_name: '', pickup_location: '', pickup_time: '', sequence: form.job_pickups.length + 1 })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Pickup Point</button>
          </template>
        </div>

        <!-- ── 4. Tour Schedule ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Tour Schedule <span class="count-badge">{{ editing ? form.job_itineraries.length : job.job_itineraries?.length }} stops</span></h2>
          <template v-if="!editing">
            <div class="relative">
              <div class="absolute left-3.5 top-4 bottom-4 w-px bg-gray-200"></div>
              <div class="space-y-3">
                <div v-for="(item, idx) in job.job_itineraries" :key="idx" class="flex gap-4 relative">
                  <div class="w-7 h-7 rounded-full bg-red-600 text-white text-xs font-bold flex items-center justify-center flex-shrink-0 z-10">{{ idx + 1 }}</div>
                  <div class="flex-1 pb-3">
                    <p class="text-sm font-semibold text-gray-800">{{ item.place_name || 'Unnamed Stop' }}</p>
                    <div class="flex gap-3 mt-0.5">
                      <span v-if="item.start_time" class="text-xs text-gray-500">▶ {{ item.start_time }}</span>
                      <span v-if="item.end_time" class="text-xs text-gray-500">⏹ {{ item.end_time }}</span>
                    </div>
                    <p v-if="item.note" class="text-xs text-gray-400 mt-0.5 italic">{{ item.note }}</p>
                  </div>
                </div>
              </div>
              <p v-if="!job.job_itineraries?.length" class="text-sm text-gray-400">No stops added</p>
            </div>
          </template>
          <template v-else>
            <div v-for="(item, idx) in form.job_itineraries" :key="idx" class="grid grid-cols-1 md:grid-cols-5 gap-2 mb-3 items-end">
              <div><label class="field-label">Start Time</label><input v-model="item.start_time" type="time" class="field-input" /></div>
              <div><label class="field-label">End Time</label><input v-model="item.end_time" type="time" class="field-input" /></div>
              <div class="md:col-span-2"><label class="field-label">Stop / Activity</label><input v-model="item.place_name" type="text" class="field-input" placeholder="e.g. Doi Suthep Temple" /></div>
              <button type="button" @click="form.job_itineraries.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="form.job_itineraries.push({ place_name: '', start_time: '', end_time: '', note: '' })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Stop</button>
          </template>
        </div>

        <!-- ── 5. Passengers ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Passengers <span class="count-badge">{{ editing ? form.job_customers.length : job.job_customers?.length }}</span></h2>
          <template v-if="!editing">
            <div class="divide-y divide-gray-100">
              <div v-for="(c, idx) in job.job_customers" :key="idx" class="flex items-center justify-between py-2.5">
                <div class="flex items-center gap-2.5">
                  <div class="w-7 h-7 rounded-full bg-gray-100 text-gray-500 text-xs font-bold flex items-center justify-center">{{ idx + 1 }}</div>
                  <span class="text-sm font-medium text-gray-700">{{ c.customer_name || 'Unnamed' }}</span>
                </div>
                <span v-if="c.note" class="text-xs text-gray-400 italic">{{ c.note }}</span>
              </div>
            </div>
            <p v-if="!job.job_customers?.length" class="text-sm text-gray-400">No passengers added</p>
          </template>
          <template v-else>
            <div v-for="(c, idx) in form.job_customers" :key="idx" class="flex gap-2 mb-3 items-end">
              <div class="flex-1"><label class="field-label">Passenger Name</label><input v-model="c.customer_name" type="text" class="field-input" placeholder="Full Name" /></div>
              <div class="flex-1"><label class="field-label">Note</label><input v-model="c.note" type="text" class="field-input" placeholder="e.g. Wheelchair" /></div>
              <button type="button" @click="form.job_customers.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="form.job_customers.push({ customer_name: '', note: '' })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Passenger</button>
          </template>
        </div>

        <!-- ── 6. Inclusions & Exclusions ── -->
        <div class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Inclusions & Exclusions</h2>
          <template v-if="!editing">
            <div class="space-y-2">
              <div v-for="(inc, idx) in job.job_inclusions" :key="idx" class="flex items-center gap-3">
                <span v-if="inc.inclusion_type === 'INCLUSION'" class="w-5 h-5 rounded-full bg-green-100 text-green-600 flex items-center justify-center flex-shrink-0">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                </span>
                <span v-else class="w-5 h-5 rounded-full bg-red-100 text-red-500 flex items-center justify-center flex-shrink-0">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
                </span>
                <span class="text-sm text-gray-700">{{ inc.description }}</span>
              </div>
            </div>
            <p v-if="!job.job_inclusions?.length" class="text-sm text-gray-400">None added</p>
          </template>
          <template v-else>
            <div v-for="(inc, idx) in form.job_inclusions" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div>
                <label class="field-label">Type</label>
                <select v-model="inc.inclusion_type" class="field-input">
                  <option value="INCLUSION">Included</option>
                  <option value="EXCLUSION">Not Included</option>
                </select>
              </div>
              <div class="md:col-span-2"><label class="field-label">Details</label><input v-model="inc.description" type="text" class="field-input" placeholder="Details" /></div>
              <button type="button" @click="form.job_inclusions.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="form.job_inclusions.push({ inclusion_type: 'INCLUSION', description: '', sequence: form.job_inclusions.length + 1 })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Item</button>
          </template>
        </div>

        <!-- ── 7. Entrance Fees ── -->
        <div v-if="editing || job.job_entrance_fees?.length" class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Entrance Fees</h2>
          <template v-if="!editing">
            <div class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead><tr class="text-left text-xs text-gray-400 border-b border-gray-100"><th class="pb-2 font-medium">Attraction</th><th class="pb-2 font-medium">Thai</th><th class="pb-2 font-medium">Foreigner</th></tr></thead>
                <tbody>
                  <tr v-for="(fee, idx) in sortedFees" :key="idx" class="border-b border-gray-50 last:border-0">
                    <td class="py-2.5 text-gray-700 font-medium">{{ fee.place_name }}</td>
                    <td class="py-2.5 text-gray-600">฿{{ Number(fee.thai_price).toLocaleString() }}</td>
                    <td class="py-2.5 text-gray-600">฿{{ Number(fee.foreigner_price).toLocaleString() }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </template>
          <template v-else>
            <div v-for="(fee, idx) in form.job_entrance_fees" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div><label class="field-label">Attraction</label><input v-model="fee.place_name" type="text" class="field-input" placeholder="Attraction" /></div>
              <div><label class="field-label">Thai (THB)</label><input v-model.number="fee.thai_price" type="number" class="field-input" /></div>
              <div><label class="field-label">Foreigner (THB)</label><input v-model.number="fee.foreigner_price" type="number" class="field-input" /></div>
              <button type="button" @click="form.job_entrance_fees.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="form.job_entrance_fees.push({ place_name: '', thai_price: 0, foreigner_price: 0, sequence: form.job_entrance_fees.length + 1 })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Entrance Fee</button>
          </template>
        </div>

        <!-- ── 8. Remarks ── -->
        <div v-if="editing || job.note" class="bg-white rounded-2xl shadow border border-gray-100 p-6 mb-4">
          <h2 class="section-title">Remarks</h2>
          <template v-if="!editing">
            <p class="text-sm text-gray-600 leading-relaxed">{{ job.note }}</p>
          </template>
          <template v-else>
            <textarea v-model="form.note" rows="3" class="field-input" placeholder="Additional remarks or special instructions..."></textarea>
          </template>
        </div>

        <!-- ── Timestamps ── -->
        <div class="flex gap-6 text-xs text-gray-400 px-1 mb-6">
          <span>Created: <span class="text-gray-500 font-medium">{{ formatDateTime(job.job_created_at) }}</span></span>
          <span>Updated: <span class="text-gray-500 font-medium">{{ formatDateTime(job.job_updated_at) }}</span></span>
        </div>

        <!-- ── Actions ── -->
        <div class="flex gap-3">

          <!-- View mode actions -->
          <template v-if="!editing">
            <button
              v-if="canEdit"
              @click="startEditing"
              class="flex-1 py-2.5 border-2 border-red-500 text-red-600 font-semibold rounded-xl hover:bg-red-50 transition text-sm"
            >
              Edit Tour
            </button>
            <button
              v-if="canCancel"
              @click="confirmCancel"
              :disabled="cancelling"
              class="px-6 py-2.5 border border-gray-300 text-gray-500 font-medium rounded-xl hover:bg-gray-50 transition text-sm disabled:opacity-50"
            >
              {{ cancelling ? 'Cancelling…' : 'Cancel Tour' }}
            </button>
          </template>

          <!-- Edit mode actions -->
          <template v-else>
            <button
              @click="cancelEditing"
              class="px-6 py-2.5 border border-gray-300 text-gray-500 font-medium rounded-xl hover:bg-gray-50 transition text-sm"
            >
              Discard
            </button>
            <button
              @click="saveJob"
              :disabled="submitting"
              class="flex-1 py-2.5 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition text-sm disabled:opacity-50"
            >
              {{ submitting ? 'Saving…' : 'Save Changes' }}
            </button>
          </template>

        </div>

      </template>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'
const router = useRouter()
const route = useRoute()

const job = ref(null)
const loading = ref(true)
const error = ref('')
const cancelling = ref(false)
const submitting = ref(false)
const editing = ref(false)

const allLanguages = ['English', 'Thai', 'Mandarin', 'Korean', 'Japanese', 'French', 'German']

const form = reactive({
  job_title: '',
  job_description: '',
  job_start_date: '',
  job_end_date: '',
  job_required_vehicle_type: 'VAN',
  job_required_seat: 9,
  job_price: null,
  job_required_languages: [],
  driver_name: '',
  driver_phone: '',
  note: '',
  job_itineraries: [],
  job_pickups: [],
  job_customers: [],
  job_inclusions: [],
  job_entrance_fees: [],
})

// ── Fetch ──────────────────────────────────────────────────────────────────
const fetchJob = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`${API_BASE}/jobs/${route.params.job_id}`)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.detail || data.message || 'Failed to load tour.')
    }
    job.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchJob)

// ── Edit helpers ───────────────────────────────────────────────────────────
const toDateInput = (d) => d ? new Date(d).toISOString().slice(0, 10) : ''

const startEditing = () => {
  const j = job.value
  Object.assign(form, {
    job_title: j.job_title || '',
    job_description: j.job_description || '',
    job_start_date: toDateInput(j.job_start_date),
    job_end_date: toDateInput(j.job_end_date),
    job_required_vehicle_type: j.job_required_vehicle_type || 'VAN',
    job_required_seat: j.job_required_seat ?? 9,
    job_price: j.job_price ?? null,
    job_required_languages: [...(j.job_required_languages || [])],
    driver_name: j.driver_name || '',
    driver_phone: j.driver_phone || '',
    note: j.note || '',
    job_itineraries: (j.job_itineraries || []).map(i => ({ ...i })),
    job_pickups: (j.job_pickups || []).map(p => ({ ...p })),
    job_customers: (j.job_customers || []).map(c => ({ ...c })),
    job_inclusions: (j.job_inclusions || []).map(i => ({ ...i })),
    job_entrance_fees: (j.job_entrance_fees || []).map(f => ({ ...f })),
  })
  editing.value = true
}

const cancelEditing = () => { editing.value = false }

const toggleLanguage = (lang) => {
  const idx = form.job_required_languages.indexOf(lang)
  if (idx > -1) form.job_required_languages.splice(idx, 1)
  else form.job_required_languages.push(lang)
}

// ── Save ───────────────────────────────────────────────────────────────────
const saveJob = async () => {
  submitting.value = true
  try {
    const res = await fetch(`${API_BASE}/jobs/${route.params.job_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    let data = {}
    const text = await res.text()
    if (text) { try { data = JSON.parse(text) } catch (_) {} }
    if (res.ok) {
      editing.value = false
      await fetchJob() // refresh displayed data
    } else {
      alert('Failed to save: ' + (data.error || data.message || data.detail || 'Unknown error'))
    }
  } catch (e) {
    alert('An error occurred: ' + e.message)
  } finally {
    submitting.value = false
  }
}

// ── Computed helpers ───────────────────────────────────────────────────────
const sortedPickups = computed(() =>
  [...(job.value?.job_pickups ?? [])].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
)
const sortedFees = computed(() =>
  [...(job.value?.job_entrance_fees ?? [])].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
)
const canEdit = computed(() => ['OPEN', 'MATCHING'].includes(job.value?.job_status))
const canCancel = computed(() => ['OPEN', 'MATCHING'].includes(job.value?.job_status))

// ── Status display ─────────────────────────────────────────────────────────
const STATUS_MAP = {
  OPEN:        { label: 'Open',        cls: 'bg-green-100 text-green-700' },
  MATCHING:    { label: 'Matching',    cls: 'bg-blue-100 text-blue-700' },
  SELECTED:    { label: 'Selected',    cls: 'bg-indigo-100 text-indigo-700' },
  IN_PROGRESS: { label: 'In Progress', cls: 'bg-amber-100 text-amber-700' },
  COMPLETED:   { label: 'Completed',   cls: 'bg-gray-100 text-gray-600' },
  CANCELLED:   { label: 'Cancelled',   cls: 'bg-red-100 text-red-600' },
}
const statusLabel = (s) => STATUS_MAP[s]?.label ?? s
const statusClass = (s) => STATUS_MAP[s]?.cls ?? 'bg-gray-100 text-gray-500'

// ── Formatters ─────────────────────────────────────────────────────────────
const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
const formatDateTime = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// ── Cancel tour ────────────────────────────────────────────────────────────
const confirmCancel = async () => {
  if (!confirm('Are you sure you want to cancel this tour? This cannot be undone.')) return
  cancelling.value = true
  try {
    const res = await fetch(`${API_BASE}/jobs/${route.params.job_id}/cancel`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
    })
    if (res.ok) {
      job.value.job_status = 'CANCELLED'
    } else {
      const data = await res.json().catch(() => ({}))
      alert(data.detail || data.message || 'Failed to cancel tour.')
    }
  } catch (e) {
    alert('Unable to connect.')
  } finally {
    cancelling.value = false
  }
}
</script>

<style scoped>
.section-title {
  @apply text-sm font-semibold text-gray-500 uppercase tracking-wide border-b border-gray-100 pb-2 mb-4 flex items-center gap-2;
}
.count-badge {
  @apply text-xs font-medium text-gray-400 normal-case tracking-normal;
}
.info-block { @apply flex flex-col gap-0.5; }
.info-label { @apply text-xs text-gray-400 font-medium uppercase tracking-wide; }
.info-value { @apply text-sm font-semibold text-gray-700; }
.field-label { @apply block text-xs text-gray-500 font-medium mb-1; }
.field-input { @apply w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400; }
</style>
