<template>
  <!-- Loading skeleton -->
  <div v-if="loading" class="modal-overlay">
    <div class="mini-modal">
      <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px">
        <span class="skeleton skeleton-btn" style="width:24px;height:24px;border-radius:50%"></span>
      </div>
      <div class="profile-hero">
        <span class="skeleton" style="width:48px;height:48px;border-radius:50%;display:block;flex-shrink:0"></span>
        <div style="flex:1;display:flex;flex-direction:column;gap:6px;">
          <span class="skeleton skeleton-text" style="width:55%"></span>
          <span class="skeleton skeleton-text" style="width:80%"></span>
        </div>
      </div>
      <div class="mini-grid" style="margin-top:12px">
        <div v-for="i in 6" :key="i" class="mini-item">
          <span class="skeleton skeleton-text" style="width:40%;height:10px"></span>
          <span class="skeleton skeleton-text" style="width:70%;height:14px;margin-top:4px"></span>
        </div>
      </div>
    </div>
  </div>

  <!-- Freelancer Modal -->
  <div v-else-if="data && type === 'FREELANCER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="mini-modal">
      <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px">
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>
      <div class="profile-hero">
        <div class="profile-avatar-wrap">
          <img v-if="data.fl_profile_image_url" :src="data.fl_profile_image_url"
            class="w-12 h-12 rounded-full object-cover ring-2 ring-[#eee]" />
          <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ring-2 ring-[#eee]"
            :style="avatarStyle(data.fl_id, data.fl_name)">{{ initials2(data.fl_name) }}</div>
        </div>
        <div class="profile-info">
          <h3 class="profile-name">{{ data.fl_name || data.fl_username }}</h3>
          <p class="profile-bio" :class="{ muted: !data.fl_bio }">{{ data.fl_bio || 'No bio' }}</p>
        </div>
      </div>
      <div class="mini-grid">
        <div class="mini-item">
          <label>Status</label>
          <span class="badge" :class="data.fl_verify_status?.toLowerCase()">{{ data.fl_verify_status }}</span>
        </div>
        <div class="mini-item">
          <label>Active</label>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: data.fl_is_active ? '#06c755' : '#bbb' }"></div>
            <span :style="{ color: data.fl_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">
              {{ data.fl_is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
        <div class="mini-item">
          <label>Rating</label>
          <span class="flex items-center gap-1">
            <span class="font-semibold text-[#333]">{{ Number(data.fl_rating_avg || 0).toFixed(1) }}</span>
            <svg class="w-3.5 h-3.5 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
          </span>
        </div>
        <div class="mini-item"><label>Phone</label><span>{{ data.fl_phone || '-' }}</span></div>
        <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(data.fl_created_at) }}</span></div>
        <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(data.fl_updated_at) }}</span></div>
      </div>
      <div class="mini-modal-footer">
        <button class="btn-full-view" @click="$emit('view-detail', { id: data.fl_id, type: 'FREELANCER' })">
          View Full Detail →
        </button>
      </div>
    </div>
  </div>

  <!-- Employer Modal -->
  <div v-else-if="data && type === 'EMPLOYER'" class="modal-overlay" @click.self="$emit('close')">
    <div class="mini-modal">
      <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px">
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>
      <div class="profile-hero">
        <div class="profile-avatar-wrap">
          <img v-if="data.em_profile_image_url" :src="data.em_profile_image_url"
            class="w-12 h-12 rounded-full object-cover ring-2 ring-[#eee]" />
          <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ring-2 ring-[#eee]"
            :style="avatarStyle(data.em_id, data.em_name)">{{ initials2(data.em_name) }}</div>
        </div>
        <div class="profile-info">
          <h3 class="profile-name">{{ data.em_name || data.em_username }}</h3>
          <p class="profile-bio" :class="{ muted: !data.em_bio }">{{ data.em_bio || 'No bio' }}</p>
        </div>
      </div>
      <div class="mini-grid">
        <div class="mini-item">
          <label>Status</label>
          <span class="badge" :class="data.em_verify_status?.toLowerCase()">{{ data.em_verify_status }}</span>
        </div>
        <div class="mini-item">
          <label>Active</label>
          <div style="display:flex;align-items:center;gap:6px;">
            <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: data.em_is_active ? '#06c755' : '#bbb' }"></div>
            <span :style="{ color: data.em_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">
              {{ data.em_is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
        <div class="mini-item">
          <label>Rating</label>
          <span class="flex items-center gap-1">
            <span class="font-semibold text-[#333]">{{ Number(data.em_rating_avg || 0).toFixed(1) }}</span>
            <svg class="w-3.5 h-3.5 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
            </svg>
          </span>
        </div>
        <div class="mini-item"><label>Phone</label><span>{{ data.em_phone || '-' }}</span></div>
        <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(data.em_created_at) }}</span></div>
        <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(data.em_updated_at) }}</span></div>
      </div>
      <div class="mini-modal-footer">
        <button class="btn-full-view" @click="$emit('view-detail', { id: data.em_id, type: 'EMPLOYER' })">
          View Full Detail →
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
  type:    { type: String,  default: '' },   // 'FREELANCER' | 'EMPLOYER'
  loading: { type: Boolean, default: false },
})

defineEmits(['close', 'view-detail'])
// 'view-detail' payload → { id, type }

const { avatarStyle, initials2 } = useAvatar()
</script>