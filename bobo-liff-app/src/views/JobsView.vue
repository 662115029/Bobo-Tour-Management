<template>
  <div class="relative flex flex-col h-dvh max-w-md mx-auto bg-[#F8FAFC] font-sans overflow-hidden">

    <!-- Header -->
    <div class="relative bg-white border-b border-[#E2E8F0] flex-shrink-0 px-4 py-3">
      <button v-if="selectedJob" class="absolute left-4 top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-[#F1F5F9] flex items-center justify-center z-10"
        @click="selectedJob = null">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#475569" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
      </button>
      <div class="flex flex-col items-center justify-center">
        <p class="text-meta font-semibold text-[#DC2626] uppercase tracking-[0.16em] leading-none">Freelancer</p>
        <h2 class="text-[20px] font-bold text-[#0F172A] leading-none mt-1.5">{{ currentTab.label }}</h2>
      </div>
    </div>

    <!-- Job Detail overlay -->
    <div v-if="selectedJob" class="flex-1 overflow-hidden bg-[#F8FAFC] relative flex flex-col">
      <div class="flex-1 overflow-hidden relative">
        <JobDetailPanel :job="selectedJob" :tab="activeTab" :user="user" @action-done="handleActionDone" @show-toast="$emit('show-toast', $event)" />
      </div>
    </div>

    <!-- List -->
    <div v-else class="flex-1 overflow-y-auto">
      <div v-if="loading" class="flex flex-col items-center justify-center h-40 gap-3">
        <img src="@/assets/logo.png" alt="Loading" class="w-16 h-16 object-contain animate-pulse" />
        <p class="text-caption text-[#94A3B8]">Loading...</p>
      </div>

      <div v-else-if="!items.length" class="flex flex-col items-center justify-center h-40 gap-2 text-center px-6">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#CBD5E1" stroke-width="1.5"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/></svg>
        <p class="text-caption text-[#94A3B8]">{{ emptyMessage }}</p>
      </div>

      <div v-else class="p-4 pb-[calc(104px+env(safe-area-inset-bottom))] space-y-3">
        <div v-for="item in items" :key="item.job_id || item.job_application_id"
          class="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm overflow-hidden">
          <div class="px-4 pt-4 pb-3">

            <!-- Employer row -->
            <div class="flex items-center gap-2.5 mb-3">
              <img v-if="item.em_profile_image_url" :src="item.em_profile_image_url" alt=""
                class="w-10 h-10 rounded-full object-cover border border-[#E2E8F0] flex-shrink-0" />
              <div v-else class="w-10 h-10 rounded-full bg-[#FEF2F2] text-[#DC2626] font-bold text-body flex items-center justify-center flex-shrink-0">
                {{ (item.company || item.em_name || '?').charAt(0).toUpperCase() }}
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-caption font-semibold text-[#0F172A] truncate">{{ item.company || item.em_name || '-' }}</p>
                <span v-if="item.em_verify_status" :class="[BADGE_BASE, getVerifyStatusClass(item.em_verify_status), 'mt-0.5 !text-meta !px-2']">
                  {{ formatVerifyStatus(item.em_verify_status) }}
                </span>
              </div>
              <span :class="[BADGE_BASE, statusBadge(item).class, 'flex-shrink-0']">{{ statusBadge(item).label }}</span>
            </div>

            <!-- Job -->
            <h3 class="text-body font-bold text-[#0F172A] leading-snug mb-2">{{ item.job_title }}</h3>
            <div class="space-y-1.5">
              <span v-if="item.area_name" class="info-tag area">{{ item.area_name }}</span>
              <p class="text-caption text-[#64748B] flex items-center gap-1.5">
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#94A3B8" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>
                {{ formatDate(item.job_start_date) }}<span v-if="item.job_end_date"> – {{ formatDate(item.job_end_date) }}</span>
              </p>
              <div class="flex items-center gap-3 pt-1">
                <p v-if="item.job_price" class="text-header font-bold text-[#0F172A]">฿{{ Number(item.job_price).toLocaleString() }}</p>
                <p v-if="activeTab === 'my-job'" class="text-caption text-[#94A3B8]">{{ item.job_required_seat }} pax</p>
                <p v-if="activeTab === 'job-offer' && item.updated_at" class="text-caption text-[#94A3B8]">Offered {{ daysAgo(item.updated_at) }}</p>
                <p v-if="activeTab === 'my-request' && item.applied_at" class="text-caption text-[#94A3B8]">Applied {{ daysAgo(item.applied_at) }}</p>
                <p v-if="activeTab === 'job-opening'" class="text-caption text-[#94A3B8]">{{ item.job_required_vehicle_type }} · {{ item.job_required_seat }} pax</p>
              </div>
            </div>
          </div>
          <div class="border-t border-[#E2E8F0] px-4 py-2.5 flex justify-end">
            <button class="flex items-center gap-1 text-caption font-semibold text-[#DC2626] hover:text-[#B91C1C] transition" @click="selectedJob = item">
              View Detail
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M9 18l6-6-6-6"/></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom Nav (floating) -->
    <div class="absolute inset-x-0 bottom-0 z-20 px-3 pointer-events-none" style="padding-bottom: max(env(safe-area-inset-bottom), 10px);">
      <nav class="pointer-events-auto flex bg-white/90 backdrop-blur-md rounded-3xl border border-[#E2E8F0] shadow-[0_8px_24px_rgba(15,23,42,0.10)] px-1 py-2.5">
        <button v-for="tab in tabs" :key="tab.key"
          class="flex-1 flex flex-col items-center gap-1 active:scale-95 transition"
          @click="switchTab(tab.key)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none"
            :stroke="activeTab === tab.key ? '#DC2626' : '#94A3B8'"
            :stroke-width="activeTab === tab.key ? 2.1 : 1.7"
            stroke-linecap="round" stroke-linejoin="round" class="transition-colors">
            <path :d="tab.icon"/>
          </svg>
          <span class="text-meta leading-tight text-center whitespace-nowrap transition-colors"
            :class="activeTab === tab.key ? 'text-[#0F172A] font-bold' : 'text-[#94A3B8] font-medium'">{{ tab.label }}</span>
        </button>
      </nav>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import JobDetailPanel from './JobDetailPanel.vue'
import { getJobStatusClass, formatJobStatus, getVerifyStatusClass, formatVerifyStatus, BADGE_BASE } from '@/utils/statusClasses.js'

const props = defineProps({ user: Object })
defineEmits(['show-toast'])
const route = useRoute()
const validTabKeys = ['my-job', 'job-offer', 'my-request', 'job-opening']
const activeTab = ref(validTabKeys.includes(route.query.tab) ? route.query.tab : 'my-job')
const items = ref([])
const loading = ref(false)
const selectedJob = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

const tabs = [
  { key: 'my-job',      label: 'My Job',       icon: 'M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2' },
  { key: 'job-offer',   label: 'Job Offer',    icon: 'M4 5h16a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1zM3 6l9 7 9-7' },
  { key: 'my-request',  label: 'Job Applied',  icon: 'M9 12l2 2 4-4M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z' },
  { key: 'job-opening', label: 'Job Openings', icon: 'M11 19a8 8 0 1 0 0-16 8 8 0 0 0 0 16zM21 21l-4.35-4.35' },
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