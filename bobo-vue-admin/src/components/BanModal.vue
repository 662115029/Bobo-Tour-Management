<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal">
      <div class="modal-icon">
        <svg v-if="isActive" class="w-10 h-10 mx-auto text-red-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/>
        </svg>
        <svg v-else class="w-10 h-10 mx-auto text-green-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
      </div>
      <h3>{{ isActive ? "Ban" : "Unban" }} {{ userType }}</h3>
      <p>Are you sure you want to {{ isActive ? "ban" : "unban" }}<br />
        <strong>"{{ name }}"</strong>?
      </p>
      <p v-if="isActive" class="modal-warning">
        They will not be able to accept any jobs or use the platform.
      </p>
      <div class="modal-actions">
        <button class="btn-cancel" @click="$emit('cancel')">Cancel</button>
        <button class="btn-confirm" :class="isActive ? 'ban' : 'unban'" @click="$emit('confirm')">
          {{ isActive ? "Ban" : "Unban" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show:     { type: Boolean, default: false },
  isActive: { type: Boolean, default: true },
  name:     { type: String, default: '' },
  userType: { type: String, default: 'User' }
})
defineEmits(['confirm', 'cancel'])
</script>