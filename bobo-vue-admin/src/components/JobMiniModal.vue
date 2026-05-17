<template>
  <div v-if="data" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[400px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- ── Topbar ── -->
      <div class="relative flex items-center justify-center px-5 py-3.5 border-b border-[#f0f0f0]">
        <span class="text-[11px] font-bold uppercase tracking-widest text-[#1a73e8]">Job</span>
        <button
          class="absolute right-4 w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer hover:bg-[#ebebeb] hover:text-[#111] transition-colors"
          @click="$emit('close')">✕</button>
      </div>

      <!-- ── Hero ── -->
      <div class="relative overflow-hidden">
        <div class="absolute inset-0" :style="{ background: jobBg, opacity: 0.08 }"></div>
        <div class="relative px-5 pt-5 pb-4">
          <div class="flex items-start gap-3.5">
            <div class="w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 shadow-sm" :style="jobIconStyle(data.job_id)">
              <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 2a9.5 9.5 0 0 1 0 19A9.5 9.5 0 0 1 12 2z"/>
                <path d="M2 12h20"/>
                <path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/>
                <path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/>
              </svg>
            </div>
            <div class="flex-1 min-w-0 pt-0.5">
              <div class="text-[15px] font-bold text-[#111] leading-snug">{{ data.job_title }}</div>
              <div class="text-[12px] mt-1 line-clamp-2 leading-relaxed" :class="data.job_description ? 'text-[#777]' : 'text-[#bbb] italic'">
                {{ data.job_description || 'No description' }}
              </div>
            </div>
          </div>

          <!-- status + price -->
          <div class="flex items-center justify-between mt-3.5">
            <span class="badge" :class="data.job_status?.toLowerCase()">{{ formatJobStatus(data.job_status) }}</span>
            <span v-if="data.job_price" class="text-[15px] font-bold text-[#1a73e8]">
              ฿{{ Number(data.job_price).toLocaleString() }}
            </span>
          </div>
        </div>
      </div>

      <!-- ── Divider ── -->
      <div class="h-px bg-[#f0f0f0] mx-5"></div>

      <!-- ── Info block ── -->
      <div class="px-5 py-4 flex flex-col gap-4">

        <!-- Employer -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full flex items-center justify-center text-[12px] font-bold shrink-0 ring-2 ring-[#eee]"
            :style="avatarStyle(data.em_id, data.company)">{{ initials2(data.company) }}</div>
          <div class="min-w-0">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Employer</div>
            <div class="text-[13px] font-semibold text-[#222] truncate mt-0.5">{{ data.company || '—' }}</div>
          </div>
        </div>

        <!-- Date range -->
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
            </svg>
          </div>
          <div class="flex items-center gap-3 flex-1">
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#2e7d32]">Start</div>
              <div class="text-[13px] font-semibold text-[#111] mt-0.5">{{ formatDate(data.job_start_date) || '—' }}</div>
            </div>
            <svg width="18" height="18" fill="none" stroke="#ccc" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/>
            </svg>
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#c62828]">End</div>
              <div class="text-[13px] font-semibold text-[#111] mt-0.5">{{ formatDate(data.job_end_date) || '—' }}</div>
            </div>
          </div>
        </div>

        <!-- Vehicle + Seats inline -->
        <div class="flex items-center gap-6">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
              <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 3v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
            </div>
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Vehicle</div>
              <div class="text-[13px] font-semibold text-[#222] mt-0.5">{{ data.job_required_vehicle_type || '—' }}</div>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0">
              <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>
            </div>
            <div>
              <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Seats</div>
              <div class="text-[13px] font-semibold text-[#222] mt-0.5">{{ data.job_required_seat || '—' }}</div>
            </div>
          </div>
        </div>

        <!-- Driver -->
        <div class="flex items-center gap-3">
          <div v-if="data.selected_driver"
            class="w-8 h-8 rounded-full flex items-center justify-center text-[12px] font-bold shrink-0 ring-2 ring-[#eee]"
            :style="avatarStyle(data.selected_fl_id, data.selected_driver)">
            {{ initials2(data.selected_driver) }}
          </div>
          <div v-else class="w-8 h-8 rounded-full bg-[#f5f5f5] flex items-center justify-center shrink-0 ring-2 ring-[#eee]">
            <svg width="14" height="14" fill="none" stroke="#ccc" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Driver</div>
            <div class="text-[13px] font-semibold mt-0.5 truncate"
              :class="data.selected_driver ? 'text-[#222]' : 'text-[#bbb] italic'">
              {{ data.selected_driver || 'Not assigned' }}
            </div>
          </div>
        </div>

        <!-- Languages -->
        <div class="flex items-start gap-3">
          <div class="w-8 h-8 rounded-xl bg-[#f5f5f5] flex items-center justify-center shrink-0 mt-0.5">
            <svg width="14" height="14" fill="none" stroke="#888" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Required Languages</div>
            <div v-if="data.languages?.length" class="flex flex-wrap gap-1.5 mt-1.5">
              <span v-for="lang in data.languages" :key="lang"
                class="text-[11px] font-semibold bg-[#e8f0fe] text-[#1a73e8] px-2.5 py-0.5 rounded-full">{{ lang }}</span>
            </div>
            <div v-else class="text-[13px] text-[#bbb] italic mt-0.5">No requirement</div>
          </div>
        </div>

      </div>

      <!-- ── Timestamps ── -->
      <div class="grid grid-cols-2 border-t border-[#f0f0f0] bg-[#fafafa]">
        <div class="flex flex-col items-center text-center px-4 py-3 border-r border-[#f0f0f0]">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.job_created_at) }}</div>
        </div>
        <div class="flex flex-col items-center text-center px-4 py-3">
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] font-medium text-[#999] mt-0.5">{{ formatDateTime(data.job_updated_at) }}</div>
        </div>
      </div>

      <!-- ── Footer ── -->
      <div class="px-5 py-4">
        <button
          class="w-full py-3 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:scale-[0.98] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', data.job_id)">
          View Full Detail
          <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/>
          </svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAvatar } from '../composables/useAvatar'
import { formatDate, formatDateTime } from '../utils/formatDate'

const props = defineProps({ data: { type: Object, default: null } })
defineEmits(['close', 'view-detail'])

const { jobIconStyle, avatarStyle, initials2 } = useAvatar()
const jobBg = computed(() => props.data ? jobIconStyle(props.data.job_id).backgroundColor : '#e8f0fe')

function formatJobStatus(status) {
  if (!status) return ''
  const map = { MATCHING: 'Pending', SELECTED: 'Matched' }
  return map[status.toUpperCase()] ?? status
}
</script>