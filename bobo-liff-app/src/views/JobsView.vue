<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-[#f5f5f5] font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-[#e0e0e0] flex-shrink-0">
      <button class="w-9 h-9 rounded-full bg-[#f5f5f5] flex items-center justify-center"
        @click="selectedJob = null">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#444" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
      </button>
      <div class="flex-1">
        <p class="text-[11px] font-bold text-red-600 uppercase tracking-widest">Freelancer</p>
        <h2 class="text-[17px] font-bold text-[#111] leading-tight">{{ currentTab.label }}</h2>
      </div>
    </div>

    <!-- Job Detail overlay -->
    <div v-if="selectedJob" class="flex-1 overflow-hidden bg-[#f5f5f5] relative flex flex-col">
      <div class="flex-1 overflow-hidden relative">
        <JobDetailPanel :job="selectedJob" :tab="activeTab" :user="user" @action-done="handleActionDone" @show-toast="$emit('show-toast', $event)" />
      </div>
    </div>

    <!-- List -->
    <div v-else class="flex-1 overflow-y-auto">
      <div v-if="loading" class="flex flex-col items-center justify-center h-40 gap-3">
        <img src="@/assets/logo.png" alt="Loading" class="w-16 h-16 object-contain animate-pulse" />
        <p class="text-[13px] text-[#aaa]">Loading...</p>
      </div>

      <div v-else-if="!items.length" class="flex flex-col items-center justify-center h-40 gap-2 text-center px-6">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ddd" stroke-width="1.5"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
        <p class="text-[13px] text-[#bbb]">{{ emptyMessage }}</p>
      </div>

      <div v-else class="p-4 space-y-3">
        <div v-for="item in items" :key="item.job_id || item.job_application_id"
          class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
          <div class="px-4 pt-4 pb-3">
            <div class="flex items-start justify-between gap-2 mb-2.5">
              <h3 class="text-[15px] font-bold text-[#111] flex-1 leading-snug">{{ item.job_title }}</h3>
              <span :class="[BADGE_BASE, statusBadge(item).class, 'flex-shrink-0']">{{ statusBadge(item).label }}</span>
            </div>
            <div class="space-y-1.5">
              <p class="text-[13px] text-[#888] flex items-center gap-1.5">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                {{ formatDate(item.job_start_date) }}<span v-if="item.job_end_date"> – {{ formatDate(item.job_end_date) }}</span>
              </p>
              <p class="text-[13px] text-[#888] flex items-center gap-1.5">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                {{ item.company || item.em_name || '-' }}
              </p>
              <div class="flex items-center gap-3 pt-0.5">
                <p v-if="item.job_price" class="text-[14px] font-bold text-[#111]">฿{{ Number(item.job_price).toLocaleString() }}</p>
                <p v-if="activeTab === 'my-job'" class="text-[12px] text-[#bbb]">{{ item.job_required_seat }} pax</p>
                <p v-if="activeTab === 'job-offer' && item.updated_at" class="text-[12px] text-[#bbb]">Offered {{ daysAgo(item.updated_at) }}</p>
                <p v-if="activeTab === 'my-request' && item.applied_at" class="text-[12px] text-[#bbb]">Applied {{ daysAgo(item.applied_at) }}</p>
                <p v-if="activeTab === 'job-opening'" class="text-[12px] text-[#bbb]">{{ item.job_required_vehicle_type }} · {{ item.job_required_seat }} pax</p>
              </div>
            </div>
          </div>
          <div class="border-t border-[#f0f0f0] px-4 py-2.5 flex justify-end">
            <button class="flex items-center gap-1 text-[12px] font-semibold text-red-600 hover:text-red-700 transition" @click="selectedJob = item">
              View Detail
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Nav -->
    <div class="flex bg-white border-t border-[#e0e0e0] flex-shrink-0">
      <button v-for="tab in tabs" :key="tab.key"
        class="flex-1 flex flex-col items-center gap-1 py-2.5 transition-colors"
        :class="activeTab === tab.key ? 'text-red-600' : 'text-[#aaa]'"
        @click="switchTab(tab.key)">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" :stroke="activeTab === tab.key ? '#dc2626' : '#ccc'" stroke-width="1.8">
          <path :d="tab.icon"/>
        </svg>
        <span class="text-[10px] font-semibold leading-tight text-center whitespace-pre-line">{{ tab.label }}</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import JobDetailPanel from './JobDetailPanel.vue'
import { getJobStatusClass, formatJobStatus, BADGE_BASE } from '@/utils/statusClasses.js'

const props = defineProps({ user: Object })
defineEmits(['show-toast'])
const activeTab = ref('my-job')
const items = ref([])
const loading = ref(false)
const selectedJob = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

const tabs = [
  { key: 'my-job',      label: 'My Job',       icon: 'M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2' },
  { key: 'job-offer',   label: 'Job Offer',    icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z' },
  { key: 'my-request',  label: 'Job Applied',  icon: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 0 0 1.946-.806 3.42 3.42 0 0 1 4.438 0 3.42 3.42 0 0 0 1.946.806 3.42 3.42 0 0 1 3.138 3.138 3.42 3.42 0 0 0 .806 1.946 3.42 3.42 0 0 1 0 4.438 3.42 3.42 0 0 0-.806 1.946 3.42 3.42 0 0 1-3.138 3.138 3.42 3.42 0 0 0-1.946.806 3.42 3.42 0 0 1-4.438 0 3.42 3.42 0 0 0-1.946-.806 3.42 3.42 0 0 1-3.138-3.138 3.42 3.42 0 0 0-.806-1.946 3.42 3.42 0 0 1 0-4.438 3.42 3.42 0 0 0 .806-1.946 3.42 3.42 0 0 1 3.138-3.138z' },
  { key: 'job-opening', label: 'Job Openings', icon: 'M21 13.255A23.931 23.931 0 0 1 12 15c-3.183 0-6.22-.62-9-1.745M16 6l2 2-2 2M8 6l-2 2 2 2' },
]

const currentTab = computed(() => tabs.find(t => t.key === activeTab.value) || tabs[0])
const emptyMessage = computed(() => ({
  'my-job': 'No active jobs.', 'job-offer': 'No pending offers.',
  'my-request': 'No pending requests.', 'job-opening': 'No open jobs available.',
}[activeTab.value]))

onMounted(() => fetchTab(activeTab.value))
watch(activeTab, (val) => { selectedJob.value = null; fetchTab(val) })

async function fetchTab(tab) {
  loading.value = true; items.value = []
  const flId = props.user?.fl_id
  if (!flId) { loading.value = false; return }
  try {
    let url = ''
    if (tab === 'my-job')       url = `${API_BASE}/jobs?fl_id=${flId}&status=MATCHED&limit=100`
    else if (tab === 'job-offer')    url = `${API_BASE}/job-applications?fl_id=${flId}&application_status=PENDING&limit=100`
    else if (tab === 'my-request')   url = `${API_BASE}/job-applications?fl_id=${flId}&application_status=APPLIED&limit=100`
    else if (tab === 'job-opening')  url = `${API_BASE}/jobs?status=OPEN&limit=100`
    const res = await fetch(url, { headers: HEADERS })
    if (res.ok) { const data = await res.json(); items.value = data.items || [] }
  } catch (e) { console.error(e) }
  finally { loading.value = false }
}

function switchTab(key) { activeTab.value = key }
function handleActionDone() { selectedJob.value = null; fetchTab(activeTab.value) }
function statusBadge(item) {
  const s = item.job_status || item.application_status || ''
  return { label: formatJobStatus(s) || s, class: getJobStatusClass(s) }
}
function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
function daysAgo(dateStr) {
  if (!dateStr) return ''
  const diff = Math.floor((Date.now() - new Date(dateStr)) / 86400000)
  if (diff === 0) return 'today'
  if (diff === 1) return '1 day ago'
  return `${diff} days ago`
}
</script>