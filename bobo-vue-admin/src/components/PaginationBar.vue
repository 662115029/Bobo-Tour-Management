<template>
  <div
    class="flex items-center justify-between px-2 py-3 text-sm text-muted"
    v-if="hasItems || page > 1"
  >
    <button
      class="btn-action view"
      :disabled="page === 1"
      :class="{ 'opacity-40 cursor-not-allowed': page === 1 }"
      @click="$emit('prev')"
    >← Prev</button>
    <span>Page {{ page }}</span>
    <button
      class="btn-action view"
      :disabled="!hasMore"
      :class="{ 'opacity-40 cursor-not-allowed': !hasMore }"
      @click="$emit('next')"
    >Next →</button>
  </div>
</template>

<script setup>
defineProps({
  page:     { type: Number, default: 1 },
  hasMore:  { type: Boolean, default: false },
  hasItems: { type: Boolean, default: false },
})
defineEmits(['prev', 'next'])
</script>