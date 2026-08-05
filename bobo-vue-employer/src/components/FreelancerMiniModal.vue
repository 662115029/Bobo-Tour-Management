<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="$emit('close')">

    <div v-if="loading" class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col overflow-hidden">
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="animate-pulse bg-[#ebebeb] w-20 h-4 rounded-full block"></span>
        <span class="animate-pulse bg-[#ebebeb] w-7 h-7 rounded-full block"></span>
      </div>
      <div class="px-5 pt-5 pb-4 flex items-start gap-3.5">
        <span class="animate-pulse bg-[#ebebeb] w-12 h-12 rounded-2xl block shrink-0"></span>
        <div class="flex-1 flex flex-col gap-2 pt-0.5">
          <span class="animate-pulse bg-[#ebebeb] h-4 w-2/5 rounded block"></span>
          <span class="animate-pulse bg-[#ebebeb] h-3 w-3/5 rounded block"></span>
          <span class="animate-pulse bg-[#ebebeb] w-20 h-5 rounded-full block mt-1"></span>
        </div>
      </div>
      <div class="h-px bg-[#f0f0f0] mx-5"></div>
      <div class="px-5 py-4 flex flex-col gap-4">
        <div v-for="i in 3" :key="i" class="flex items-center gap-3">
          <span class="animate-pulse bg-[#ebebeb] w-8 h-8 rounded-xl block shrink-0"></span>
          <div class="flex flex-col gap-1.5 flex-1">
            <span class="animate-pulse bg-[#ebebeb] h-2 w-1/4 rounded block"></span>
            <span class="animate-pulse bg-[#ebebeb] h-3.5 w-2/5 rounded block"></span>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] p-8 text-center">
      <p class="text-[13px] text-red-500 mb-3">{{ error }}</p>
      <button @click="$emit('close')" class="px-4 py-2 bg-[#f5f5f5] rounded-lg text-[13px] text-[#555] hover:bg-[#ebebeb] transition">Close</button>
    </div>

    <div v-else-if="fl" class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col max-h-[90vh] overflow-y-auto">

      <div class="relative flex items-center justify-center px-5 py-3.5 border-b border-[#f0f0f0] shrink-0">
        <span class="text-[11px] font-bold uppercase tracking-widest text-[#1565c0]">Freelancer</span>
        <button class="absolute right-4 w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center hover:bg-[#ebebeb] hover:text-[#111] transition-colors" @click="$emit('close')">✕</button>
      </div>

      <div class="relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.06]" :style="{ background: avatarStyle(fl.fl_id, fl.fl_name).backgroundColor }"></div>
        <div class="relative px-5 pt-5 pb-4">
          <div class="flex items-start gap-3.5">
            <div class="shrink-0 relative">
              <img v-if="fl.fl_profile_image_url" :src="fl.fl_profile_image_url" class="w-12 h-12 rounded-2xl object-cover ring-2 ring-white shadow-sm" />
              <div v-else class="w-12 h-12 rounded-2xl flex items-center justify-center text-lg font-bold ring-2 ring-white shadow-sm text-white" :style="avatarStyle(fl.fl_id, fl.fl_name)">{{ initials2(fl.fl_name) }}</div>
              <span class="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-white" :class="fl.fl_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
            </div>
            <div class="flex-1 min-w-0 pt-0.5">
              <div class="text-[15px] font-bold text-[#111] leading-snug truncate">{{ fl.fl_name || fl.fl_username }}</div>
              <div class="text-[12px] mt-1 line-clamp-2 leading-relaxed" :class="fl.fl_bio ? 'text-[#777]' : 'text-[#bbb] italic'">{{ fl.fl_bio || 'No bio' }}</div>
            </div>
          </div>
          <div class="flex items-center gap-2 mt-3.5 flex-wrap">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wide" :class="verifyClass(fl.fl_verify_status)">{{ fl.fl_verify_status }}</span>
            <span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-full" :class="fl.fl_is_active ? 'bg-[#e8f5e9] text-[#2e7d32]' : 'bg-[#f5f5f5] text-[#999]'">
              <span class="w-1.5 h-1.5 rounded-full" :class="fl.fl_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
              {{ fl.fl_is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-3 border-y border-[#f0f0f0] divide-x divide-[#f0f0f0]">
        <div class="flex flex-col items-center py-3.5 px-1">
          <div class="flex items-center gap-1">
            <span class="text-[17px] font-bold text-[#111]">{{ Number(fl.fl_rating_avg || 0).toFixed(1) }}</span>
            <svg width="13" height="13" fill="#f9a825" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
          </div>
          <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Rating</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-1">
          <div class="text-[17px] font-bold text-[#111]">{{ fl.fl_completed_jobs ?? 0 }}</div>
          <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Completed</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-1">
          <div class="text-[17px] font-bold text-[#111]">{{ fl.fl_total_jobs ?? 0 }}</div>
          <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Total Jobs</div>
        </div>
      </div>

      <div class="px-5 py-4 flex flex-col gap-4">

        <div v-if="fl.fl_phone" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Phone</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5">{{ fl.fl_phone }}</div>
          </div>
        </div>

        <div v-if="fl.fl_email" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div class="min-w-0 flex-1">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Email</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 break-all">{{ fl.fl_email }}</div>
          </div>
        </div>

        <div v-if="fl.fl_address" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0 mt-0.5">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Address</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 leading-snug">{{ fl.fl_address }}</div>
          </div>
        </div>

        <div v-if="fl.languages?.length" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
          </div>
          <div class="flex-1">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-1.5">Languages</div>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="l in fl.languages" :key="l" class="info-tag language">{{ l }}</span>
            </div>
          </div>
        </div>

        <div v-if="fl.pickup_areas?.length" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div class="flex-1">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-1.5">Pickup Areas</div>
            <div class="flex flex-wrap gap-1.5">
              <span v-for="a in fl.pickup_areas" :key="a" class="info-tag area">{{ a }}</span>
            </div>
          </div>
        </div>

      </div>

      <div class="grid grid-cols-2 border-t border-[#f0f0f0] bg-[#fafafa]">
        <div class="flex flex-col items-center text-center px-4 py-3 border-r border-[#f0f0f0]">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Joined</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDate(fl.fl_created_at) }}</div>
        </div>
        <div class="flex flex-col items-center text-center px-4 py-3">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDate(fl.fl_updated_at) }}</div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAvatar } from '@/composables/useAvatar'

const props = defineProps({
  flId:  { type: [String, Number], required: true },
  jobId: { type: [String, Number], default: null },
})
defineEmits(['close'])

const { avatarStyle, initials2 } = useAvatar()
const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const fl = ref(null)
const loading = ref(true)
const error = ref('')

const verifyClass = (status) => ({
  verified:  'bg-green-100 text-green-800',
  pending:   'bg-amber-100 text-amber-800',
  rejected:  'bg-red-100 text-red-800',
  suspended: 'bg-gray-100 text-gray-600',
}[status?.toLowerCase()] || 'bg-gray-100 text-gray-500')

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(String(d).replace(' ', 'T')).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'Asia/Bangkok' })
}

onMounted(async () => {
  try {
    const [flRes, langRes, areaRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers/${props.flId}`),
      fetch(`${API_BASE}/fl-languages?fl_id=${props.flId}&limit=20`),
      fetch(`${API_BASE}/fl-pickup-areas?fl_id=${props.flId}&limit=20`),
    ])
    const [flData, langData, areaData] = await Promise.all([flRes.json(), langRes.json(), areaRes.json()])
    if (!flRes.ok) throw new Error(flData.detail || 'Failed to load freelancer')
    fl.value = {
      ...flData,
      languages:    (langData.items || []).map(l => l.language_name),
      pickup_areas: (areaData.items || []).map(a => a.area_name),
    }
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>
