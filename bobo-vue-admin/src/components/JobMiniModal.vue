<template>
  <div v-if="data" class="modal-overlay" @click.self="$emit('close')">
    <div class="w-[380px] rounded-2xl bg-white shadow-[0_12px_48px_rgba(0,0,0,0.16)] flex flex-col max-h-[90vh] overflow-y-auto">

      <!-- ── Top bar ── -->
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-lg flex items-center justify-center" :style="jobIconStyle(data.job_id)">
            <svg width="13" height="13" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/>
              <path d="M2 12h20"/><path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/>
              <path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/>
            </svg>
          </div>
          <span class="text-[11px] font-semibold uppercase tracking-wide text-[#1a73e8]">Job</span>
        </div>
        <button
          class="w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer transition-colors hover:bg-[#ebebeb] hover:text-[#111]"
          @click="$emit('close')">✕</button>
      </div>

      <!-- ── Hero: title + status ── -->
      <div class="px-5 pt-4 pb-3.5 border-b border-[#f0f0f0]">
        <div class="flex items-start gap-3">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center shrink-0" :style="jobIconStyle(data.job_id)">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 2a9.5 9.5 0 0 1 0 19A9.5 9.5 0 0 1 12 2z"/>
              <path d="M2 12h20"/>
              <path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/>
              <path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/>
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-[16px] font-bold text-[#111] leading-tight m-0 mb-1">{{ data.job_title }}</h3>
            <p class="text-[12px] text-[#777] leading-snug m-0 line-clamp-2" :class="{ 'italic text-[#bbb]': !data.job_description }">
              {{ data.job_description || 'No description' }}
            </p>
          </div>
        </div>
        <!-- status + price row -->
        <div class="flex items-center gap-2 mt-3">
          <span class="badge" :class="data.job_status?.toLowerCase()">{{ data.job_status }}</span>
          <span v-if="data.job_price" class="text-[13px] font-semibold text-[#1a73e8]">
            ฿{{ Number(data.job_price).toLocaleString() }}
          </span>
        </div>
      </div>

      <!-- ── Date range bar ── -->
      <div class="px-5 py-3.5 border-b border-[#f0f0f0] bg-[#f8fffe]">
        <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-2">Job Period</div>
        <div class="flex items-center gap-2">
          <!-- Start -->
          <div class="flex-1 bg-white rounded-xl border border-[#e8f5e9] px-3 py-2">
            <div class="text-[10px] font-semibold text-[#2e7d32] uppercase tracking-wide mb-0.5">Start</div>
            <div class="text-[13px] font-semibold text-[#111]">{{ formatDate(data.job_start_date) || '—' }}</div>
          </div>
          <!-- Arrow -->
          <div class="flex flex-col items-center shrink-0 gap-0.5">
            <svg width="20" height="20" fill="none" stroke="#bbb" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/>
            </svg>
          </div>
          <!-- End -->
          <div class="flex-1 bg-white rounded-xl border border-[#fce4ec] px-3 py-2">
            <div class="text-[10px] font-semibold text-[#c62828] uppercase tracking-wide mb-0.5">End</div>
            <div class="text-[13px] font-semibold text-[#111]">{{ formatDate(data.job_end_date) || '—' }}</div>
          </div>
        </div>
      </div>

      <!-- ── Details grid ── -->
      <div class="px-5 py-3.5 border-b border-[#f0f0f0]">
        <div class="text-[10px] font-semibold uppercase tracking-[0.08em] text-[#bbb] mb-2.5">Details</div>
        <div class="grid grid-cols-2 gap-x-5 gap-y-3">
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Vehicle</div>
            <div class="text-[13px] font-medium text-[#222] mt-0.5">{{ data.job_required_vehicle_type || '—' }}</div>
          </div>
          <div>
            <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Seats</div>
            <div class="text-[13px] font-medium text-[#222] mt-0.5">{{ data.job_required_seat || '—' }}</div>
          </div>
        </div>
      </div>

      <!-- ── Timestamps ── -->
      <div class="grid grid-cols-2 gap-3 px-5 py-3 bg-[#fafafa]">
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Created</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.job_created_at) }}</div>
        </div>
        <div>
          <div class="text-[10px] font-semibold uppercase tracking-[0.07em] text-[#bbb]">Last Updated</div>
          <div class="text-[12px] text-[#999] mt-0.5">{{ formatDateTime(data.job_updated_at) }}</div>
        </div>
      </div>

      <!-- ── Footer ── -->
      <div class="px-5 py-3.5">
        <button
          class="w-full py-2.5 bg-[#111] text-white text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#2a2a2a] active:bg-[#000] flex items-center justify-center gap-1.5"
          @click="$emit('view-detail', data.job_id)">
          View Full Detail
          <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 12h14M13 6l6 6-6 6"/>
          </svg>
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useAvatar } from '../composables/useAvatar'
import { formatDate, formatDateTime } from '../utils/formatDate'

defineProps({ data: { type: Object, default: null } })
defineEmits(['close', 'view-detail'])
const { jobIconStyle } = useAvatar()
</script>