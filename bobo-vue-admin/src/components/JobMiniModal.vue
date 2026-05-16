<template>
  <div v-if="data" class="modal-overlay" @click.self="$emit('close')">
    <div class="mini-modal">
      <div class="mini-modal-header">
        <button class="close-btn" @click="$emit('close')" style="margin-left:auto">✕</button>
      </div>
      <div class="profile-hero">
        <div class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0 ring-2 ring-[#eee]"
          :style="jobIconStyle(data.job_id)">
          <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" />
            <path d="M12 2a9.5 9.5 0 0 1 0 19A9.5 9.5 0 0 1 12 2z" />
            <path d="M2 12h20" />
            <path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10" />
            <path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10" />
          </svg>
        </div>
        <div class="profile-info">
          <h3 class="profile-name">{{ data.job_title }}</h3>
          <p class="profile-bio" :class="{ muted: !data.job_description }">
            {{ data.job_description || 'No description' }}
          </p>
        </div>
      </div>
      <div class="mini-grid">
        <div class="mini-item">
          <label>Status</label>
          <span class="badge" :class="data.job_status?.toLowerCase()">{{ data.job_status }}</span>
        </div>
        <div class="mini-item">
          <label>Price</label>
          <span>{{ data.job_price ? '฿' + Number(data.job_price).toLocaleString() : '-' }}</span>
        </div>
        <div class="mini-item"><label>Vehicle</label><span>{{ data.job_required_vehicle_type || '-' }}</span></div>
        <div class="mini-item"><label>Seats</label><span>{{ data.job_required_seat || '-' }}</span></div>
        <div class="mini-item"><label>Start</label><span>{{ formatDate(data.job_start_date) }}</span></div>
        <div class="mini-item"><label>End</label><span>{{ formatDate(data.job_end_date) }}</span></div>
        <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(data.job_created_at) }}</span></div>
        <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(data.job_updated_at) }}</span></div>
      </div>
      <div class="mini-modal-footer">
        <button class="btn-full-view" @click="$emit('view-detail', data.job_id)">
          View Full Detail →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAvatar } from '../composables/useAvatar'
import { formatDate, formatDateTime } from '../utils/formatDate'

defineProps({
  data: { type: Object, default: null },
})

defineEmits(['close', 'view-detail'])

const { jobIconStyle } = useAvatar()
</script>