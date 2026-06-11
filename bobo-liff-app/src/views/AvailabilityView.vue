<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-[#f5f5f5] font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-[#e0e0e0] flex-shrink-0">
      <button class="w-9 h-9 rounded-full bg-[#f5f5f5] flex items-center justify-center" @click="$router.push('/')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
      </button>
      <div class="flex-1">
        <p class="text-[11px] font-bold text-red-600 uppercase tracking-widest">Freelancer</p>
        <h2 class="text-[17px] font-bold text-[#111] leading-tight">Availability</h2>
      </div>
      <button v-if="!editing" class="px-4 py-1.5 text-[13px] font-semibold border border-[#e0e0e0] rounded-lg text-[#444] hover:bg-[#f5f5f5] transition"
        @click="editing = true">
        Edit
      </button>
      <template v-else>
        <button class="px-3 py-1.5 text-[13px] font-medium border border-[#e0e0e0] rounded-lg text-[#666] hover:bg-[#f5f5f5] transition mr-1"
          @click="cancelEdit">
          Cancel
        </button>
        <button class="px-4 py-1.5 text-[13px] font-semibold bg-red-600 text-white rounded-lg hover:bg-red-700 transition disabled:opacity-50"
          :disabled="!canSave || saving"
          @click="handleSave">
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
      </template>
    </div>

    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-3">

      <!-- Loading -->
      <div v-if="loading" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5">
        <div class="animate-pulse space-y-3">
          <div class="bg-[#ebebeb] h-6 w-40 rounded mx-auto"></div>
          <div class="grid grid-cols-7 gap-1">
            <div v-for="i in 35" :key="i" class="bg-[#ebebeb] h-8 rounded"></div>
          </div>
        </div>
      </div>

      <template v-else>

        <!-- Calendar card -->
        <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-4">

          <!-- Month nav -->
          <div class="flex items-center justify-between mb-4">
            <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-[#f5f5f5] transition"
              @click="prevMonth">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
            </button>
            <p class="text-[14px] font-bold text-[#111]">{{ monthLabel }}</p>
            <button class="w-8 h-8 flex items-center justify-center rounded-full hover:bg-[#f5f5f5] transition"
              @click="nextMonth">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="2.5"><path d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>

          <!-- Day headers -->
          <div class="grid grid-cols-7 mb-1">
            <div v-for="d in ['Su','Mo','Tu','We','Th','Fr','Sa']" :key="d"
              class="text-center text-[11px] font-bold text-[#bbb] py-1">{{ d }}</div>
          </div>

          <!-- Days grid -->
          <div class="grid grid-cols-7 gap-y-1">
            <!-- Empty cells before first day -->
            <div v-for="_ in firstDayOfMonth" :key="'e' + _"></div>
            <!-- Day cells -->
            <div v-for="day in daysInMonth" :key="day"
              class="flex items-center justify-center h-9 text-[13px] relative select-none"
              :class="[
                editing ? 'cursor-pointer' : 'cursor-default',
                dayBg(day),
              ]"
              @click="editing && onDayClick(day)">
              <span class="relative z-10 w-8 h-8 flex items-center justify-center rounded-full"
                :class="dayCircle(day)">
                {{ day }}
              </span>
            </div>
          </div>

        </div>

        <!-- Selected range summary (always visible) -->
        <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm px-4 py-3">
          <div class="grid grid-cols-2 gap-3">
            <div>
              <p class="text-[11px] font-bold text-[#bbb] uppercase tracking-widest mb-0.5">Start</p>
              <p class="text-[13px] font-semibold text-[#222]">{{ displayStart || '-' }}</p>
            </div>
            <div>
              <p class="text-[11px] font-bold text-[#bbb] uppercase tracking-widest mb-0.5">End</p>
              <p class="text-[13px] font-semibold text-[#222]">{{ displayEnd || '-' }}</p>
            </div>
          </div>
          <p v-if="selectedDays > 0" class="text-[12px] text-[#888] mt-2">{{ selectedDays }} day{{ selectedDays > 1 ? 's' : '' }} selected</p>
          <p v-else-if="!displayStart && !displayEnd" class="text-[12px] text-[#bbb] mt-2">No availability set yet.</p>
          <p v-if="selectedDays > 30" class="text-[12px] text-red-500 mt-1">Maximum 30 days allowed.</p>
        </div>

        <p v-if="saveError" class="text-[12px] text-red-500 px-1">{{ saveError }}</p>

        <!-- Hint -->
        <div v-if="editing" class="px-1">
          <p class="text-[12px] text-[#bbb]">Tap a start date, then tap an end date. Maximum 30 days.</p>
        </div>

      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({ user: Object })

const availability = ref(null)
const loading = ref(false)
const saving = ref(false)
const editing = ref(false)
const saveError = ref('')

// Calendar state
const viewYear = ref(new Date().getFullYear())
const viewMonth = ref(new Date().getMonth()) // 0-indexed

// Selection state (YYYY-MM-DD strings)
const selStart = ref(null)
const selEnd = ref(null)
const picking = ref('start') // 'start' | 'end'

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

const MONTH_NAMES = ['January','February','March','April','May','June','July','August','September','October','November','December']

const monthLabel = computed(() => `${MONTH_NAMES[viewMonth.value]} ${viewYear.value}`)

const daysInMonth = computed(() => {
  return new Date(viewYear.value, viewMonth.value + 1, 0).getDate()
})

const firstDayOfMonth = computed(() => {
  return new Date(viewYear.value, viewMonth.value, 1).getDay()
})

function dateStr(day) {
  const m = String(viewMonth.value + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  return `${viewYear.value}-${m}-${d}`
}

function isPast(day) {
  return dateStr(day) < new Date().toISOString().slice(0, 10)
}

function onDayClick(day) {
  if (isPast(day)) return
  const ds = dateStr(day)
  if (picking.value === 'start') {
    selStart.value = ds
    selEnd.value = null
    picking.value = 'end'
  } else {
    if (ds < selStart.value) {
      selEnd.value = selStart.value
      selStart.value = ds
    } else {
      selEnd.value = ds
    }
    picking.value = 'start'
  }
}

function dayBg(day) {
  if (!selStart.value || !selEnd.value) return ''
  const ds = dateStr(day)
  const start = selStart.value < selEnd.value ? selStart.value : selEnd.value
  const end = selStart.value < selEnd.value ? selEnd.value : selStart.value
  if (ds > start && ds < end) return 'bg-red-50'
  return ''
}

function dayCircle(day) {
  const ds = dateStr(day)
  const today = new Date().toISOString().slice(0, 10)
  const start = selStart.value && selEnd.value
    ? (selStart.value < selEnd.value ? selStart.value : selEnd.value)
    : selStart.value
  const end = selStart.value && selEnd.value
    ? (selStart.value < selEnd.value ? selEnd.value : selStart.value)
    : selEnd.value

  const isStart = ds === start
  const isEnd = ds === end && selEnd.value
  const inRange = start && end && ds > start && ds < end

  if (isStart || isEnd) return 'bg-red-600 text-white font-bold'
  if (inRange) return 'text-red-600 font-medium'
  if (ds === today) return 'border border-red-300 text-red-600'
  if (isPast(day)) return 'text-[#ccc] cursor-not-allowed'
  return 'text-[#222] hover:bg-[#f5f5f5]'
}

const selectedDays = computed(() => {
  if (!selStart.value || !selEnd.value) return 0
  return Math.floor((new Date(selEnd.value) - new Date(selStart.value)) / 86400000) + 1
})

const canSave = computed(() =>
  selStart.value && selEnd.value && selectedDays.value >= 1 && selectedDays.value <= 30
)

const displayStart = computed(() => selStart.value ? formatDate(selStart.value) : null)
const displayEnd = computed(() => selEnd.value ? formatDate(selEnd.value) : null)

function prevMonth() {
  if (viewMonth.value === 0) { viewMonth.value = 11; viewYear.value-- }
  else viewMonth.value--
}

function nextMonth() {
  if (viewMonth.value === 11) { viewMonth.value = 0; viewYear.value++ }
  else viewMonth.value++
}

function cancelEdit() {
  editing.value = false
  // restore saved values
  if (availability.value) {
    selStart.value = availability.value.fl_available_start_date?.slice(0, 10) || null
    selEnd.value = availability.value.fl_available_end_date?.slice(0, 10) || null
  } else {
    selStart.value = null
    selEnd.value = null
  }
  picking.value = 'start'
}

onMounted(async () => {
  if (!props.user?.fl_id) { loading.value = false; return }
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/fl-availability?fl_id=${props.user.fl_id}&limit=1`, { headers: HEADERS })
    if (res.ok) {
      const data = await res.json()
      const item = data.items?.[0] || null
      availability.value = item
      if (item) {
        selStart.value = item.fl_available_start_date?.slice(0, 10) || null
        selEnd.value = item.fl_available_end_date?.slice(0, 10) || null
        // Always stay on current month, not jump to saved date
      }
    }
  } catch (e) { console.error(e) }
  finally { loading.value = false }
})

async function handleSave() {
  saving.value = true; saveError.value = ''
  try {
    const res = await fetch(`${API_BASE}/fl-availability`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({
        fl_id: props.user.fl_id,
        fl_available_start_date: selStart.value,
        fl_available_end_date: selEnd.value,
      }),
    })
    const data = await res.json()
    if (!res.ok) { saveError.value = data.detail || 'Failed to save.'; return }
    availability.value = data
    editing.value = false
  } catch { saveError.value = 'Cannot connect.' }
  finally { saving.value = false }
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(String(dateStr).replace(' ', 'T'))
    .toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
</script>