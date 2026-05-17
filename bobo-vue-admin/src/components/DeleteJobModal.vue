<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal">
      <div class="modal-icon">
        <svg class="w-10 h-10 mx-auto text-red-500" fill="none"
             stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <polyline points="3 6 5 6 21 6"/>
          <path stroke-linecap="round" stroke-linejoin="round"
                d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6m5 0V4a1 1 0 011-1h2a1 1 0 011 1v2"/>
        </svg>
      </div>
      <h3>Delete Job</h3>
      <p>Are you sure you want to delete<br /><strong>"{{ title }}"</strong>?</p>
      <p class="modal-warning">This action cannot be undone.</p>
      <div class="modal-actions">
        <button class="btn-cancel" @click="$emit('cancel')">Cancel</button>
        <button class="btn-confirm-delete" @click="$emit('confirm')">Delete</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: { type: Boolean, default: false },
  title: { type: String, default: '' }
})
defineEmits(['confirm', 'cancel'])
</script>