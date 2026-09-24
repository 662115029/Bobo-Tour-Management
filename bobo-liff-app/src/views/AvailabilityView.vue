<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-[#F8FAFC] font-sans overflow-hidden">

    <!-- Header -->
    <div class="bg-white border-b border-[#E2E8F0] flex-shrink-0 px-4 py-3">
      <div class="flex flex-col items-center justify-center">
        <p class="text-meta font-semibold text-[#DC2626] uppercase tracking-[0.16em] leading-none">Freelancer</p>
        <h2 class="text-[20px] font-bold text-[#0F172A] leading-none mt-1.5">Availability</h2>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto px-4 py-4 space-y-3">

      <!-- Loading -->
      <div v-if="loading" class="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm p-5">
        <div class="animate-pulse space-y-3">
          <div class="bg-[#F1F5F9] h-6 w-40 rounded mx-auto"></div>
          <div class="grid grid-cols-7 gap-1">
            <div v-for="i in 35" :key="i" class="bg-[#F1F5F9] h-8 rounded"></div>
          </div>
        </div>
      </div>

      <template v-else>

        <!-- Selected range summary -->
        <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm p-4">
          <div class="flex items-center gap-2.5 mb-3">
            <span class="w-8 h-8 rounded-full bg-[#FEF2F2] flex items-center justify-center shrink-0">
              <svg class="w-4 h-4 text-[#DC2626]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
            </span>
            <span class="text-[14px] font-bold text-[#0F172A] flex-1">Available Dates</span>
            <span v-if="selectedDays > 0" class="text-meta font-semibold text-[#DC2626] bg-[#FEF2F2] px-2 py-0.5 rounded-full">
              {{ selectedDays }} day{{ selectedDays > 1 ? 's' : '' }} selected
            </span>
          </div>
          <div class="flex items-center gap-2">
            <div class="flex-1 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2">
              <p class="text-meta font-medium text-[#94A3B8] uppercase tracking-wide">Start</p>
              <p class="text-body font-semibold text-[#0F172A]">{{ displayStart || '-' }}</p>
            </div>
            <svg class="w-4 h-4 text-[#CBD5E1] shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
            <div class="flex-1 bg-[#F8FAFC] border border-[#E2E8F0] rounded-xl px-3 py-2">
              <p class="text-meta font-medium text-[#94A3B8] uppercase tracking-wide">End</p>
              <p class="text-body font-semibold text-[#0F172A]">{{ displayEnd || '-' }}</p>
            </div>
          </div>
          <p v-if="!(selectedDays > 0) && !displayStart && !displayEnd" class="text-caption text-[#94A3B8] mt-2">No availability set yet.</p>
          <p v-if="selectedDays > 30" class="text-caption text-[#B91C1C] mt-2">Maximum 30 days allowed.</p>
        </div>

        <!-- Calendar card -->
        <div class="bg-white rounded-2xl border shadow-sm p-4 transition-colors"
          :class="editing ? 'border-[#DC2626] ring-2 ring-[#FEF2F2]' : 'border-[#E2E8F0]'">

          <!-- Month nav -->
          <div class="flex items-center justify-between mb-4">
            <button class="w-9 h-9 flex items-center justify-center rounded-full bg-[#F8FAFC] active:bg-[#F1F5F9] transition"
              @click="prevMonth">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
            </button>
            <p class="text-body font-bold text-[#0F172A]">{{ monthLabel }}</p>
            <button class="w-9 h-9 flex items-center justify-center rounded-full bg-[#F8FAFC] active:bg-[#F1F5F9] transition"
              @click="nextMonth">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5"><path d="M9 5l7 7-7 7"/></svg>
            </button>
          </div>

          <!-- Day headers -->
          <div class="grid grid-cols-7 mb-1">
            <div v-for="d in ['Su','Mo','Tu','We','Th','Fr','Sa']" :key="d"
              class="text-center text-meta font-semibold text-[#94A3B8] py-1">{{ d }}</div>
          </div>

          <!-- Days grid -->
          <div class="grid grid-cols-7 gap-y-1">
            <div v-for="_ in firstDayOfMonth" :key="'e' + _"></div>
            <div v-for="day in daysInMonth" :key="day"
              class="flex items-center justify-center h-10 text-caption relative select-none"
              :class="[
                editing ? 'cursor-pointer' : 'cursor-default',
                dayBg(day),
              ]"
              @click="editing && onDayClick(day)">
              <span class="relative z-10 w-9 h-9 flex items-center justify-center rounded-full transition-colors"
                :class="dayCircle(day)">
                {{ day }}
              </span>
            </div>
          </div>

          <!-- Hint -->
          <p v-if="editing" class="text-caption text-[#64748B] text-center mt-3 pt-3 border-t border-[#E2E8F0]">
            Tap a start date, then tap an end date. Maximum 30 days.
          </p>
        </div>

        <p v-if="saveError" class="text-caption text-[#B91C1C] bg-[#FEF2F2] rounded-lg px-3 py-2">{{ saveError }}</p>

      </template>
    </div>

    <!-- Footer actions -->
    <div v-if="!loading" class="flex-shrink-0 bg-white border-t border-[#E2E8F0] px-4 pt-3"
      style="padding-bottom: max(env(safe-area-inset-bottom), 12px);">
      <button v-if="!editing"
        class="w-full bg-[#DC2626] hover:bg-[#B91C1C] text-white text-body font-bold py-3 rounded-xl transition flex items-center justify-center gap-2"
        @click="editing = true">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
        Edit
      </button>
      <div v-else class="flex gap-2">
        <button class="flex-1 bg-[#F1F5F9] text-[#475569] text-body font-semibold py-3 rounded-xl active:bg-[#E2E8F0] transition"
          @click="cancelEdit">
          Cancel
        </button>
        <button class="flex-[2] bg-[#DC2626] hover:bg-[#B91C1C] text-white text-body font-bold py-3 rounded-xl transition disabled:bg-[#F1F5F9] disabled:text-[#94A3B8] disabled:cursor-not-allowed"
          :disabled="!canSave || saving"
          @click="handleSave">
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
      </div>
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
  if (ds > start && ds < end) return 'bg-[#FEF2F2]'
  if (start !== end && ds === start) return 'bg-[linear-gradient(to_right,transparent_50%,#FEF2F2_50%)]'
  if (start !== end && ds === end) return 'bg-[linear-gradient(to_left,transparent_50%,#FEF2F2_50%)]'
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

  if (isStart || isEnd) return 'bg-[#DC2626] text-white font-bold shadow-sm'
  if (inRange) return 'text-[#B91C1C] font-semibold'
  if (ds === today) return 'border-2 border-[#DC2626] text-[#DC2626] font-semibold'
  if (isPast(day)) return 'text-[#CBD5E1] cursor-not-allowed'
  return 'text-[#0F172A] hover:bg-[#F1F5F9]'
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