<template>

  <!-- ── Loading skeleton ── -->
  <div v-if="loading" class="modal-overlay">
    <div class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col overflow-hidden">
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="skeleton w-20 h-5 rounded-full block"></span>
        <span class="skeleton w-7 h-7 rounded-full block"></span>
      </div>
      <div class="relative px-5 pt-5 pb-4">
        <div class="flex items-start gap-3.5">
          <span class="skeleton w-12 h-12 rounded-2xl block shrink-0"></span>
          <div class="flex-1 flex flex-col gap-2 pt-0.5">
            <span class="skeleton skeleton-text w-2/5 block"></span>
            <span class="skeleton skeleton-text w-3/5 block"></span>
            <span class="skeleton w-20 h-5 rounded-full block mt-1"></span>
          </div>
        </div>
        <div class="flex items-center justify-between mt-3.5">
          <span class="skeleton w-16 h-5 rounded-full block"></span>
        </div>
      </div>
      <div class="h-px bg-[#f0f0f0] mx-5"></div>
      <div class="px-5 py-4 flex flex-col gap-4">
        <div v-for="i in 4" :key="i" class="flex items-center gap-3">
          <span class="skeleton w-8 h-8 rounded-xl block shrink-0"></span>
          <div class="flex flex-col gap-1.5 flex-1">
            <span class="skeleton h-2 w-1/4 rounded block"></span>
            <span class="skeleton h-3.5 w-2/5 rounded block"></span>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-2 border-t border-[#f0f0f0] bg-[#fafafa]">
        <div v-for="i in 2" :key="i" class="flex flex-col items-center px-4 py-3">
          <span class="skeleton h-2 w-2/5 rounded block"></span>
          <span class="skeleton h-3.5 w-4/5 rounded block mt-1.5"></span>
        </div>
      </div>
      <div class="px-5 py-4"><span class="skeleton w-full h-11 rounded-xl block"></span></div>
    </div>
  </div>

  <!-- ── Freelancer Modal ── -->
  <div v-else-if="data && type === 'FREELANCER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- Topbar -->
      <div class="relative flex items-center justify-center px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="text-[11px] font-bold uppercase tracking-widest text-[#1565c0]">Freelancer</span>
        <button class="absolute right-4 w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer hover:bg-[#ebebeb] hover:text-[#111] transition-colors" @click="$emit('close')">✕</button>
      </div>

      <!-- Hero: avatar tinted bg -->
      <div class="relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.07]" :style="{ background: avatarStyle(data.fl_id, data.fl_name).backgroundColor }"></div>
        <div class="relative px-5 pt-5 pb-4">
          <div class="flex items-start gap-3.5">
            <div class="shrink-0 relative">
              <img v-if="data.fl_profile_image_url" :src="data.fl_profile_image_url" class="w-12 h-12 rounded-2xl object-cover ring-2 ring-white shadow-sm" />
              <div v-else class="w-12 h-12 rounded-2xl flex items-center justify-center text-lg font-bold ring-2 ring-white shadow-sm" :style="avatarStyle(data.fl_id, data.fl_name)">{{ initials2(data.fl_name) }}</div>
              <span class="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-white" :class="data.fl_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
            </div>
            <div class="flex-1 min-w-0 pt-0.5">
              <div class="text-[15px] font-bold text-[#111] leading-snug truncate">{{ data.fl_name || data.fl_username }}</div>
              <div class="text-[12px] mt-1 line-clamp-2 leading-relaxed" :class="data.fl_bio ? 'text-[#777]' : 'text-[#bbb] italic'">
                {{ data.fl_bio || 'No bio' }}
              </div>
            </div>
          </div>
          <!-- status + active pill -->
          <div class="flex items-center gap-2 mt-3.5 flex-wrap">
            <span class="badge" :class="data.fl_verify_status?.toLowerCase()">{{ data.fl_verify_status }}</span>
            <span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-full"
              :class="data.fl_is_active ? 'bg-[#e8f5e9] text-[#2e7d32]' : 'bg-[#f5f5f5] text-[#999]'">
              <span class="w-1.5 h-1.5 rounded-full" :class="data.fl_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
              {{ data.fl_is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="h-px bg-[#f0f0f0] mx-5"></div>

      <!-- Info block -->
      <div class="px-5 py-4 flex flex-col gap-4">

        <!-- Stats: Rating | Completed | Total Jobs -->
        <div class="grid grid-cols-3 -mx-5 border-y border-[#f0f0f0] divide-x divide-[#f0f0f0]">
          <div class="flex flex-col items-center py-3.5 px-1">
            <div class="flex items-center gap-1">
              <span class="text-[17px] font-bold text-[#111]">{{ Number(data.fl_rating_avg || 0).toFixed(1) }}</span>
              <svg width="13" height="13" fill="#f9a825" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Rating</div>
          </div>
          <div class="flex flex-col items-center py-3.5 px-1">
            <div class="text-[17px] font-bold text-[#111]">{{ data.fl_completed_jobs ?? 0 }}</div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Completed</div>
          </div>
          <div class="flex flex-col items-center py-3">
            <div class="text-[17px] font-bold text-[#111]">{{ data.fl_total_jobs ?? 0 }}</div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Total Jobs</div>
          </div>
        </div>

        <!-- Username -->
        <div v-if="data.fl_username" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          </div>
          <div class="min-w-0">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Username</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 truncate">{{ data.fl_username }}</div>
          </div>
        </div>

        <!-- Email -->
        <div v-if="data.fl_email" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div class="min-w-0 flex-1">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Email</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 break-all">{{ data.fl_email }}</div>
          </div>
        </div>

        <!-- Phone -->
        <div v-if="data.fl_phone" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Phone</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5">{{ data.fl_phone }}</div>
          </div>
        </div>

        <!-- Address -->
        <div v-if="data.fl_address" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0 mt-0.5">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Address</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 leading-snug">{{ data.fl_address }}</div>
          </div>
        </div>

      </div>

      <!-- Timestamps -->
      <div class="grid grid-cols-2 border-t border-[#f0f0f0] bg-[#fafafa]">
        <div class="flex flex-col items-center text-center px-4 py-3 border-r border-[#f0f0f0]">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.fl_created_at) }}</div>
        </div>
        <div class="flex flex-col items-center text-center px-4 py-3">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.fl_updated_at) }}</div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-5 py-4">
        <button class="w-full py-3 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:scale-[0.98] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', { id: data.fl_id, type: 'FREELANCER' })">
          View Full Detail
          <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </div>

    </div>
  </div>

  <!-- ── Employer Modal ── -->
  <div v-else-if="data && type === 'EMPLOYER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- Topbar -->
      <div class="relative flex items-center justify-center px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="text-[11px] font-bold uppercase tracking-widest text-[#6a1b9a]">Employer</span>
        <button class="absolute right-4 w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer hover:bg-[#ebebeb] hover:text-[#111] transition-colors" @click="$emit('close')">✕</button>
      </div>

      <!-- Hero -->
      <div class="relative overflow-hidden">
        <div class="absolute inset-0 opacity-[0.07]" :style="{ background: avatarStyle(data.em_id, data.em_name).backgroundColor }"></div>
        <div class="relative px-5 pt-5 pb-4">
          <div class="flex items-start gap-3.5">
            <div class="shrink-0 relative">
              <img v-if="data.em_profile_image_url" :src="data.em_profile_image_url" class="w-12 h-12 rounded-2xl object-cover ring-2 ring-white shadow-sm" />
              <div v-else class="w-12 h-12 rounded-2xl flex items-center justify-center text-lg font-bold ring-2 ring-white shadow-sm" :style="avatarStyle(data.em_id, data.em_name)">{{ initials2(data.em_name) }}</div>
              <span class="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-white" :class="data.em_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
            </div>
            <div class="flex-1 min-w-0 pt-0.5">
              <div class="text-[15px] font-bold text-[#111] leading-snug truncate">{{ data.em_name || data.em_username }}</div>
              <div class="text-[12px] mt-1 line-clamp-2 leading-relaxed" :class="data.em_bio ? 'text-[#777]' : 'text-[#bbb] italic'">
                {{ data.em_bio || 'No bio' }}
              </div>
            </div>
          </div>
          <div class="flex items-center gap-2 mt-3.5 flex-wrap">
            <span class="badge" :class="data.em_verify_status?.toLowerCase()">{{ data.em_verify_status }}</span>
            <span class="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-1 rounded-full"
              :class="data.em_is_active ? 'bg-[#e8f5e9] text-[#2e7d32]' : 'bg-[#f5f5f5] text-[#999]'">
              <span class="w-1.5 h-1.5 rounded-full" :class="data.em_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
              {{ data.em_is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>

      <!-- Divider -->
      <div class="h-px bg-[#f0f0f0] mx-5"></div>

      <!-- Info block -->
      <div class="px-5 py-4 flex flex-col gap-4">

        <!-- Stats: Rating | Completed | Total Jobs -->
        <div class="grid grid-cols-3 -mx-5 border-y border-[#f0f0f0] divide-x divide-[#f0f0f0]">
          <div class="flex flex-col items-center py-3.5 px-1">
            <div class="flex items-center gap-1">
              <span class="text-[17px] font-bold text-[#111]">{{ Number(data.em_rating_avg || 0).toFixed(1) }}</span>
              <svg width="13" height="13" fill="#f9a825" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
            </div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Rating</div>
          </div>
          <div class="flex flex-col items-center py-3.5 px-1">
            <div class="text-[17px] font-bold text-[#111]">{{ data.em_completed_jobs ?? 0 }}</div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Completed</div>
          </div>
          <div class="flex flex-col items-center py-3">
            <div class="text-[17px] font-bold text-[#111]">{{ data.em_total_jobs ?? 0 }}</div>
            <div class="text-[10px] font-semibold uppercase tracking-wide text-[#999] mt-0.5">Total Jobs</div>
          </div>
        </div>

        <!-- Username -->
        <div v-if="data.em_username" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          </div>
          <div class="min-w-0">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Username</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 truncate">{{ data.em_username }}</div>
          </div>
        </div>

        <!-- Email -->
        <div v-if="data.em_email" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div class="min-w-0 flex-1">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Email</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 break-all">{{ data.em_email }}</div>
          </div>
        </div>

        <!-- Phone -->
        <div v-if="data.em_phone" class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Phone</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5">{{ data.em_phone }}</div>
          </div>
        </div>

        <!-- Address -->
        <div v-if="data.em_address" class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0 mt-0.5">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Address</div>
            <div class="text-[13px] font-semibold text-[#222] mt-0.5 leading-snug">{{ data.em_address }}</div>
          </div>
        </div>

      </div>

      <!-- Timestamps -->
      <div class="grid grid-cols-2 border-t border-[#f0f0f0] bg-[#fafafa]">
        <div class="flex flex-col items-center text-center px-4 py-3 border-r border-[#f0f0f0]">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.em_created_at) }}</div>
        </div>
        <div class="flex flex-col items-center text-center px-4 py-3">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.em_updated_at) }}</div>
        </div>
      </div>

      <!-- Footer -->
      <div class="px-5 py-4">
        <button class="w-full py-3 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:scale-[0.98] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', { id: data.em_id, type: 'EMPLOYER' })">
          View Full Detail
          <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/></svg>
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