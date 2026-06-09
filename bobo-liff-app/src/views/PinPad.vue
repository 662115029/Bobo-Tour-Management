<template>
  <div class="flex flex-col items-center gap-6 w-full">

    <!-- Title -->
    <p v-if="title" class="text-sm font-semibold text-gray-500">{{ title }}</p>

    <!-- Dots -->
    <div class="flex items-center gap-4">
      <div
        v-for="i in 6"
        :key="i"
        class="w-3.5 h-3.5 rounded-full border-2 transition-all duration-150"
        :class="i <= pin.length
          ? 'bg-red-600 border-red-600 scale-110'
          : 'bg-white border-gray-400'"
      />
    </div>

    <!-- Error -->
    <p v-if="error" class="text-xs text-red-500 -mt-3">{{ error }}</p>

    <!-- Keypad -->
    <div class="grid grid-cols-3 gap-y-3 gap-x-6 w-full max-w-[280px]">
      <template v-for="key in keys" :key="key">
        <!-- Empty slot -->
        <div v-if="key === ''" />

        <!-- Backspace -->
        <button
          v-else-if="key === '⌫'"
          class="h-16 w-16 mx-auto rounded-full flex items-center justify-center bg-gray-100 active:bg-gray-300 transition-colors duration-100"
          @click="pressKey('⌫')"
        >
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="2">
            <path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"/>
            <path d="M18 9l-6 6M12 9l6 6" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- Number -->
        <button
          v-else
          class="h-16 w-16 mx-auto rounded-full flex items-center justify-center text-2xl font-light text-gray-800 bg-white shadow-sm active:bg-gray-100 transition-colors duration-100 select-none"
          style="box-shadow: 0 2px 8px rgba(0,0,0,0.10);"
          @click="pressKey(key)"
        >
          {{ key }}
        </button>
      </template>
    </div>

  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

defineProps({
  title: { type: String, default: '' },
  error: { type: String, default: '' },
})

const emit = defineEmits(['complete', 'update:modelValue'])

const keys = ['1','2','3','4','5','6','7','8','9','','0','⌫']
const pin = ref('')

watch(pin, (val) => {
  emit('update:modelValue', val)
  if (val.length === 6) {
    emit('complete', val)
  }
})

function pressKey(key) {
  if (key === '⌫') {
    pin.value = pin.value.slice(0, -1)
  } else if (pin.value.length < 6) {
    pin.value += key
  }
}

function reset() {
  pin.value = ''
}

defineExpose({ reset })
</script>