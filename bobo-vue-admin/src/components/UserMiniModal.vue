<template>
  <!-- ── Loading skeleton ── -->
  <div v-if="loading" class="modal-overlay">
    <div class="w-[380px] rounded-2xl bg-white shadow-[0_12px_48px_rgba(0,0,0,0.16)] flex flex-col overflow-hidden">
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="skeleton w-20 h-5 rounded-full block"></span>
        <span class="skeleton w-7 h-7 rounded-full block"></span>
      </div>
      <div class="px-5 pt-5 pb-4 border-b border-[#f0f0f0]">
        <div class="flex items-center gap-4">
          <span class="skeleton w-16 h-16 rounded-full block shrink-0"></span>
          <div class="flex-1 flex flex-col gap-2">
            <span class="skeleton skeleton-text w-2/5 block"></span>
            <span class="skeleton skeleton-text w-3/5 block"></span>
            <span class="skeleton w-16 h-5 rounded-full block mt-1"></span>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-3 divide-x divide-[#f0f0f0] border-b border-[#f0f0f0]">
        <div v-for="i in 3" :key="i" class="px-4 py-3.5 flex flex-col items-center gap-1.5">
          <span class="skeleton w-8 h-5 rounded block"></span>
          <span class="skeleton w-12 h-2.5 rounded block"></span>
        </div>
      </div>
      <div class="px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="skeleton skeleton-text w-1/4 block mb-3"></span>
        <div class="flex flex-col gap-2.5">
          <div v-for="i in 2" :key="i" class="flex flex-col gap-1">
            <span class="skeleton h-2 w-1/4 rounded block"></span>
            <span class="skeleton h-3.5 w-2/5 rounded block"></span>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-2 gap-3 px-5 py-3 bg-[#fafafa]">
        <div v-for="i in 2" :key="i" class="flex flex-col gap-1">
          <span class="skeleton h-2 w-2/5 rounded block"></span>
          <span class="skeleton h-3.5 w-4/5 rounded block"></span>
        </div>
      </div>
      <div class="px-5 py-3.5"><span class="skeleton w-full h-10 rounded-xl block"></span></div>
    </div>
  </div>

  <!-- ── Freelancer Modal ── -->
  <div v-else-if="data && type === 'FREELANCER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[380px] rounded-2xl bg-white shadow-[0_12px_48px_rgba(0,0,0,0.16)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- Top bar -->
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="text-[11px] font-semibold uppercase tracking-wide text-[#1565c0] bg-[#e3f2fd] px-2.5 py-1 rounded-full">Freelancer</span>
        <button class="w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer transition-colors hover:bg-[#ebebeb] hover:text-[#111]" @click="$emit('close')">✕</button>
      </div>

      <!-- Profile hero -->
      <div class="px-5 pt-5 pb-4 border-b border-[#f0f0f0]">
        <div class="flex items-center gap-4">
          <div class="shrink-0 relative">
            <img v-if="data.fl_profile_image_url" :src="data.fl_profile_image_url" class="w-16 h-16 rounded-full object-cover ring-2 ring-[#eee]" />
            <div v-else class="w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold ring-2 ring-[#eee]" :style="avatarStyle(data.fl_id, data.fl_name)">{{ initials2(data.fl_name) }}</div>
            <!-- active dot -->
            <span class="absolute bottom-0.5 right-0.5 w-3 h-3 rounded-full border-2 border-white" :style="{ background: data.fl_is_active ? '#06c755' : '#bbb' }"></span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-[16px] font-bold text-[#111] truncate">{{ data.fl_name || data.fl_username }}</div>
            <div class="text-[12px] mt-0.5 leading-snug line-clamp-2" :class="data.fl_bio ? 'text-[#666]' : 'text-[#bbb] italic'">{{ data.fl_bio || 'No bio' }}</div>
            <div class="flex items-center gap-2 mt-2">
              <span class="badge" :class="data.fl_verify_status?.toLowerCase()">{{ data.fl_verify_status }}</span>
              <span class="text-[11px] font-medium" :style="{ color: data.fl_is_active ? '#2e7d32' : '#999' }">{{ data.fl_is_active ? 'Active' : 'Inactive' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats strip -->
      <div class="grid grid-cols-3 divide-x divide-[#f0f0f0] border-b border-[#f0f0f0]">
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="flex items-center gap-1">
            <span class="text-[18px] font-bold text-[#111]">{{ Number(data.fl_rating_avg || 0).toFixed(1) }}</span>
            <svg width="14" height="14" fill="#f9a825" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
          </div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Rating</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="text-[18px] font-bold text-[#111]">{{ data.fl_phone || '—' }}</div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Phone</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="text-[15px] font-bold" :style="{ color: data.fl_is_active ? '#2e7d32' : '#999' }">
            {{ data.fl_is_active ? 'ON' : 'OFF' }}
          </div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Status</div>
        </div>
      </div>

      <!-- Contact info -->
      <div class="px-5 py-3.5 border-b border-[#f0f0f0]">
        <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-2.5">Contact</div>
        <div class="flex flex-col gap-2.5">
          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-[#f5f5f5] flex items-center justify-center shrink-0">
              <svg width="13" height="13" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            </div>
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Phone</div>
              <div class="text-[13px] font-medium text-[#222]">{{ data.fl_phone || '—' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Timestamps -->
      <div class="grid grid-cols-2 gap-3 px-5 py-3 bg-[#fafafa]">
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.fl_created_at) }}</div>
        </div>
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.fl_updated_at) }}</div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-5 py-3.5">
        <button
          class="w-full py-2.5 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:bg-[#000] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', { id: data.fl_id, type: 'FREELANCER' })">
          View Full Detail
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </div>

    </div>
  </div>

  <!-- ── Employer Modal ── -->
  <div v-else-if="data && type === 'EMPLOYER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[380px] rounded-2xl bg-white shadow-[0_12px_48px_rgba(0,0,0,0.16)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- Top bar -->
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="text-[11px] font-semibold uppercase tracking-wide text-[#6a1b9a] bg-[#f3e5f5] px-2.5 py-1 rounded-full">Employer</span>
        <button class="w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer transition-colors hover:bg-[#ebebeb] hover:text-[#111]" @click="$emit('close')">✕</button>
      </div>

      <!-- Profile hero -->
      <div class="px-5 pt-5 pb-4 border-b border-[#f0f0f0]">
        <div class="flex items-center gap-4">
          <div class="shrink-0 relative">
            <img v-if="data.em_profile_image_url" :src="data.em_profile_image_url" class="w-16 h-16 rounded-full object-cover ring-2 ring-[#eee]" />
            <div v-else class="w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold ring-2 ring-[#eee]" :style="avatarStyle(data.em_id, data.em_name)">{{ initials2(data.em_name) }}</div>
            <span class="absolute bottom-0.5 right-0.5 w-3 h-3 rounded-full border-2 border-white" :style="{ background: data.em_is_active ? '#06c755' : '#bbb' }"></span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-[16px] font-bold text-[#111] truncate">{{ data.em_name || data.em_username }}</div>
            <div class="text-[12px] mt-0.5 leading-snug line-clamp-2" :class="data.em_bio ? 'text-[#666]' : 'text-[#bbb] italic'">{{ data.em_bio || 'No bio' }}</div>
            <div class="flex items-center gap-2 mt-2">
              <span class="badge" :class="data.em_verify_status?.toLowerCase()">{{ data.em_verify_status }}</span>
              <span class="text-[11px] font-medium" :style="{ color: data.em_is_active ? '#2e7d32' : '#999' }">{{ data.em_is_active ? 'Active' : 'Inactive' }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats strip -->
      <div class="grid grid-cols-3 divide-x divide-[#f0f0f0] border-b border-[#f0f0f0]">
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="flex items-center gap-1">
            <span class="text-[18px] font-bold text-[#111]">{{ Number(data.em_rating_avg || 0).toFixed(1) }}</span>
            <svg width="14" height="14" fill="#f9a825" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
          </div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Rating</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="text-[15px] font-bold text-[#111] truncate max-w-full px-1">{{ data.em_phone || '—' }}</div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Phone</div>
        </div>
        <div class="flex flex-col items-center py-3.5 px-2">
          <div class="text-[15px] font-bold" :style="{ color: data.em_is_active ? '#2e7d32' : '#999' }">
            {{ data.em_is_active ? 'ON' : 'OFF' }}
          </div>
          <div class="text-[10px] text-[#999] mt-0.5 uppercase tracking-wide font-medium">Status</div>
        </div>
      </div>

      <!-- Contact info -->
      <div class="px-5 py-3.5 border-b border-[#f0f0f0]">
        <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-2.5">Contact</div>
        <div class="flex flex-col gap-2.5">
          <div class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-[#f5f5f5] flex items-center justify-center shrink-0">
              <svg width="13" height="13" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
            </div>
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Phone</div>
              <div class="text-[13px] font-medium text-[#222]">{{ data.em_phone || '—' }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Timestamps -->
      <div class="grid grid-cols-2 gap-3 px-5 py-3 bg-[#fafafa]">
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.em_created_at) }}</div>
        </div>
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.em_updated_at) }}</div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-5 py-3.5">
        <button
          class="w-full py-2.5 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:bg-[#000] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', { id: data.em_id, type: 'EMPLOYER' })">
          View Full Detail
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime } from '../utils/formatDate'

defineProps({
  data:    { type: Object,  default: null },
  type:    { type: String,  default: '' },
  loading: { type: Boolean, default: false },
})
defineEmits(['close', 'view-detail'])
const { avatarStyle, initials2 } = useAvatar()
</script>