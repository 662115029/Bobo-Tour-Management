<template>
  <div class="user-avatar-wrap" :style="[sizeStyle, !imgSrc ? colorStyle : {}]">
    <img
      v-if="imgSrc && !imgError"
      :src="imgSrc"
      :alt="name"
      class="w-full h-full object-cover"
      @error="imgError = true"
    />
    <span v-else class="user-avatar-initials" :style="!imgSrc || imgError ? colorStyle : {}">
      {{ initials }}
    </span>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAvatar } from '../composables/useAvatar'

const props = defineProps({
  id:       { type: [String, Number], default: '' },
  name:     { type: String, default: '' },
  imageUrl: { type: String, default: null },
  size:     { type: Number, default: 32 },
  radius:   { type: String, default: '50%' },
})

const { avatarStyle, initials2 } = useAvatar()
const imgError = ref(false)
const imgSrc = computed(() => props.imageUrl || null)

const initials = computed(() => initials2(props.name))
const colorStyle = computed(() => avatarStyle(props.id, props.name))
const sizeStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  borderRadius: props.radius,
  flexShrink: 0,
  overflow: 'hidden',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: `${Math.max(10, props.size * 0.35)}px`,
  fontWeight: '700',
}))
</script>