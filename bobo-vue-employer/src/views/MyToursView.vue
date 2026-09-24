<template>
  <AppLayout>
    <div class="px-5 pb-10">

      <div class="py-4">
        <h1 class="text-[24px] font-bold text-[#dc2626] text-center mb-4">My Tours</h1>

        <!-- Filter bar -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
          <div class="flex flex-wrap items-center gap-2">
            <input v-model="search" type="text" placeholder="Search tours…"
              class="px-3 py-2 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-[#bbb] w-full sm:w-44" />
            <select v-model="statusFilter" class="px-3 py-2 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-[#bbb] flex-1 sm:flex-none">
              <option value="ALL">All Status</option>
              <option value="OPEN">Open</option>
              <option value="PENDING">Pending</option>
              <option value="MATCHED">Matched</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="COMPLETED">Completed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>
            <select v-model="yearFilter" class="px-3 py-2 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-[#bbb] flex-1 sm:flex-none">
              <option value="">All Years</option>
              <option v-for="y in availableYears" :key="y" :value="y">{{ y }}</option>
            </select>
            <select v-model="monthFilter" class="px-3 py-2 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-[#bbb] flex-1 sm:flex-none">
              <option value="">All Months</option>
              <option v-for="(m, i) in months" :key="i" :value="i + 1">{{ m }}</option>
            </select>
            <button v-if="hasActiveFilter" type="button" @click="resetFilters"
              class="flex items-center gap-1 px-3 py-1.5 text-[12px] text-[#888] hover:text-[#dc2626] transition">
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              Reset
            </button>
          </div>
          <button type="button" @click="sortField = sortField === 'start' ? 'created' : 'start'"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#e0e0e0] text-[12px] text-[#888] hover:bg-[#f5f5f5] hover:text-[#444] transition select-none self-start sm:self-auto shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 4h13M3 8h9M3 12h5m10 4l-4-4 4-4"/></svg>
            Sort by {{ sortField === 'start' ? 'Start Date' : 'Created Date' }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="i in 6" :key="i" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="p-5 flex flex-col gap-3">
            <div class="animate-pulse bg-[#ebebeb] h-4 w-3/4 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-1/2 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-1/3 rounded"></div>
          </div>
          <div class="border-t border-[#f0f0f0] grid grid-cols-2 divide-x divide-[#f0f0f0]">
            <div class="p-3 flex justify-center"><div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div></div>
            <div class="p-3 flex justify-center"><div class="animate-pulse bg-[#ebebeb] h-3 w-20 rounded"></div></div>
          </div>
        </div>
      </div>

      <div v-else-if="filteredJobs.length === 0" class="text-center py-16">
        <p class="text-[15px] font-medium text-[#999]">No tours found</p>
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="job in filteredJobs" :key="job.job_id"
          class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm hover:shadow-md hover:border-[#ccc] transition-all cursor-pointer overflow-hidden flex flex-col"
          :class="['COMPLETED','CANCELLED'].includes(job.job_status) ? 'opacity-70 hover:opacity-100' : ''"
          @click="viewJob(job.job_id, job.job_title)">
          <div class="p-5 flex flex-col gap-2.5 flex-1">

            <!-- Title + status -->
            <div class="flex items-start justify-between gap-3">
              <h3 class="text-[15px] font-semibold text-[#111] leading-snug line-clamp-2">{{ job.job_title }}</h3>
              <span class="badge shrink-0" :class="job.job_status?.toLowerCase()">{{ statusLabel(job.job_status) }}</span>
            </div>

            <!-- Area -->
            <div v-if="job.area_name"><span class="info-tag area">{{ job.area_name }}</span></div>

            <!-- Dates -->
            <div class="flex items-center gap-2 text-[13px] text-[#666]">
              <svg class="w-3.5 h-3.5 text-[#bbb] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <span>{{ formatDate(job.job_start_date) }}</span>
              <span class="text-[#ddd]">→</span>
              <span>{{ formatDate(job.job_end_date) || '—' }}</span>
            </div>

            <!-- Driver -->
            <div v-if="job.selected_driver" class="flex items-center gap-2 text-[13px] text-[#666]">
              <svg class="w-3.5 h-3.5 text-[#bbb] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              <span class="truncate">{{ job.selected_driver }}</span>
            </div>

            <!-- Created -->
            <div class="flex items-center gap-2 text-[12px] text-[#999]">
              <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path stroke-linecap="round" d="M12 7v5l3 2"/></svg>
              <span>Created {{ formatDate(job.job_created_at) }}</span>
            </div>

            <!-- Rate -->
            <div class="mt-auto pt-3 border-t border-[#f0f0f0] flex items-end justify-between">
              <span class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Rate (THB)</span>
              <span class="text-[22px] font-bold text-[#111] leading-none">฿{{ Number(job.job_price || 0).toLocaleString() }}</span>
            </div>
          </div>

          <!-- Footer -->
          <div class="border-t border-[#f0f0f0] px-5 py-2.5 flex items-center justify-between">
            <span v-if="appliedCount(job.job_id) > 0" class="flex items-center gap-1.5 text-[12px] font-semibold text-[#DC2626]">
              <span class="w-1.5 h-1.5 rounded-full bg-[#DC2626]"></span>
              {{ appliedCount(job.job_id) }} applicant{{ appliedCount(job.job_id) > 1 ? 's' : '' }}
            </span>
            <span v-else></span>
            <span class="flex items-center gap-1 text-[13px] font-semibold text-[#DC2626]">
              View Detail
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path d="M9 18l6-6-6-6"/></svg>
            </span>
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

const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const router = useRouter()
const now = new Date()

const jobs = ref([])
const loading = ref(true)
const search = ref('')
const statusFilter = ref('ALL')
const sortField = ref('start')
const yearFilter = ref('')
const monthFilter = ref('')
const appliedCountMap = ref({})

const months = ['January','February','March','April','May','June','July','August','September','October','November','December']

const availableYears = computed(() => {
  const y = now.getFullYear()
  return Array.from({ length: 5 }, (_, i) => y - i)
})

const hasActiveFilter = computed(() =>
  search.value || statusFilter.value !== 'ALL' || yearFilter.value || monthFilter.value
)

const resetFilters = () => {
  search.value = ''
  statusFilter.value = 'ALL'
  yearFilter.value = ''
  monthFilter.value = ''
}

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  try {
    const res = await fetch(`${API_BASE}/tours?em_id=${em_id}`)
    const data = await res.json()
    jobs.value = Array.isArray(data) ? data : (data.jobs || [])
  } catch { jobs.value = [] }
  finally { loading.value = false }

  if (jobs.value.length) {
    const results = await Promise.allSettled(
      jobs.value.map(job =>
        fetch(`${API_BASE}/job-applications?job_id=${job.job_id}&limit=100`)
          .then(r => r.json())
          .then(d => ({ job_id: job.job_id, count: (d.items || []).filter(a => a.application_status === 'APPLIED').length }))
          .catch(() => ({ job_id: job.job_id, count: 0 }))
      )
    )
    const map = {}
    results.forEach(r => { if (r.status === 'fulfilled') map[r.value.job_id] = r.value.count })
    appliedCountMap.value = map
  }
})

const appliedCount = (job_id) => appliedCountMap.value[job_id] || 0

const getSortDate = (job) => {
  const raw = sortField.value === 'created' ? job.job_created_at : job.job_start_date
  return raw ? new Date(String(raw).replace(' ', 'T') + 'Z') : new Date(0)
}

const getFilterDate = (job) => {
  const raw = sortField.value === 'created' ? job.job_created_at : job.job_start_date
  return raw ? new Date(String(raw).replace(' ', 'T') + 'Z') : null
}

const filteredJobs = computed(() =>
  jobs.value
    .filter(job => {
      const matchSearch = job.job_title?.toLowerCase().includes(search.value.toLowerCase())
      const matchStatus = statusFilter.value === 'ALL' || job.job_status === statusFilter.value
      const date = getFilterDate(job)
      const matchYear = !yearFilter.value || (date && date.getFullYear() === Number(yearFilter.value))
      const matchMonth = !monthFilter.value || (date && date.getMonth() + 1 === Number(monthFilter.value))
      return matchSearch && matchStatus && matchYear && matchMonth
    })
    .sort((a, b) => getSortDate(b) - getSortDate(a))
)

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(String(d).replace(' ', 'T') + 'Z').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'Asia/Bangkok' })
}

const STATUS_LABELS = { OPEN:'Open', PENDING:'Pending', MATCHED:'Matched', IN_PROGRESS:'In Progress', COMPLETED:'Completed', CANCELLED:'Cancelled' }
const statusLabel = (s) => STATUS_LABELS[s] || s

const viewJob = (id, title) => router.push({ name: 'tour-detail', params: { id }, state: { jobTitle: title } })
</script>