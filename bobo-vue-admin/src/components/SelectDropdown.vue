<template>
  <div class="select-dropdown" ref="wrapRef">
    <button
      type="button"
      class="select-trigger"
      :class="{ open: isOpen }"
      @click="toggle"
    >
      <span class="select-value">{{ selectedLabel }}</span>
      <svg class="select-chevron" :class="{ rotated: isOpen }" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"/>
      </svg>
    </button>

    <Teleport to="body">
      <div v-if="isOpen" ref="panelRef" class="select-panel" :style="panelStyle">
        <div
          v-for="opt in options"
          :key="opt.value"
          class="select-option"
          :class="{ selected: opt.value === modelValue }"
          @click="select(opt)"
        >
          <span class="select-option-label">{{ opt.label }}</span>
          <svg v-if="opt.value === modelValue" class="select-check" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  modelValue: { type: [String, Number], default: '' },
  options: { type: Array, default: () => [] }, // [{ label, value }]
})
const emit = defineEmits(['update:modelValue', 'change'])

const wrapRef = ref(null)
const isOpen = ref(false)
const panelStyle = ref({})

const selectedLabel = computed(() => {
  const found = props.options.find(o => String(o.value) === String(props.modelValue))
  return found ? found.label : props.modelValue
})

const updatePanelPosition = () => {
  if (!wrapRef.value) return
  const rect = wrapRef.value.getBoundingClientRect()
  const panelWidth = Math.max(rect.width, 160)
  const spaceRight = window.innerWidth - rect.left
  const alignRight = spaceRight < panelWidth + 16

  panelStyle.value = {
    top: rect.bottom + 6 + 'px',
    minWidth: panelWidth + 'px',
    ...(alignRight
      ? { right: window.innerWidth - rect.right + 'px', left: 'auto' }
      : { left: rect.left + 'px' }
    ),
  }
}

const toggle = async () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    await nextTick()
    updatePanelPosition()
  }
}

const select = (opt) => {
  emit('update:modelValue', opt.value)
  emit('change', opt.value)
  isOpen.value = false
}

const panelRef = ref(null)

const onOutside = (e) => {
  if (
    wrapRef.value && !wrapRef.value.contains(e.target) &&
    !(panelRef.value && panelRef.value.contains(e.target))
  ) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', onOutside))
onUnmounted(() => document.removeEventListener('mousedown', onOutside))
</script>

<style scoped>
.select-dropdown {
  position: relative;
  display: inline-block;
}

.select-trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 14px;
  background: #fff;
  border: 1.5px solid #ddd;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 500;
  color: #333;
  cursor: pointer;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  transition: border-color 0.15s, box-shadow 0.15s;
  white-space: nowrap;
  user-select: none;
}

.select-trigger:hover,
.select-trigger.open {
  border-color: #06c755;
  box-shadow: 0 0 0 3px rgba(6,199,85,0.10);
}

.select-chevron {
  color: #999;
  transition: transform 0.2s ease;
  flex-shrink: 0;
}
.select-chevron.rotated {
  transform: rotate(180deg);
  color: #06c755;
}

.select-panel {
  position: fixed;
  z-index: 9999;
  background: #fff;
  border: 1.5px solid #e8e8e8;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.13), 0 1.5px 6px rgba(0,0,0,0.07);
  padding: 5px;
  max-height: 260px;
  overflow-y: auto;
  animation: dropIn 0.15s ease;
}

@keyframes dropIn {
  from { opacity: 0; transform: translateY(-6px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

.select-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 450;
  color: #333;
  cursor: pointer;
  transition: background 0.1s;
}

.select-option:hover {
  background: #f4fef7;
  color: #06c755;
}

.select-option.selected {
  background: #edfff4;
  color: #06a045;
  font-weight: 600;
}

.select-check {
  color: #06c755;
  flex-shrink: 0;
}

.select-panel::-webkit-scrollbar {
  width: 4px;
}
.select-panel::-webkit-scrollbar-track {
  background: transparent;
}
.select-panel::-webkit-scrollbar-thumb {
  background: #e0e0e0;
  border-radius: 4px;
}
</style>