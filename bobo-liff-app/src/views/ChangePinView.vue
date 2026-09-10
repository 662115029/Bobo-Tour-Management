<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100">
      <button class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center" @click="$router.back()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
      </button>
      <div>
        <p class="text-xs font-semibold text-red-600 uppercase tracking-wider">Security</p>
        <h2 class="text-lg font-bold text-gray-900 leading-tight">
          {{ step === 'current' ? 'Current PIN' : step === 'new' ? 'New PIN' : 'Confirm PIN' }}
        </h2>
      </div>
    </div>

    <!-- Step indicators -->
    <div class="flex items-center justify-center gap-2 px-4 py-3 bg-white border-b border-gray-100">
      <div v-for="(s, i) in steps" :key="i" class="flex items-center gap-2">
        <div class="flex items-center gap-1.5">
          <div class="w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold transition-colors"
            :class="stepIndex > i ? 'bg-green-500 text-white' : stepIndex === i ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-400'">
            <svg v-if="stepIndex > i" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3">
              <path d="M20 6L9 17l-5-5"/>
            </svg>
            <span v-else>{{ i + 1 }}</span>
          </div>
          <span class="text-xs font-medium" :class="stepIndex === i ? 'text-gray-800' : 'text-gray-400'">{{ s }}</span>
        </div>
        <div v-if="i < steps.length - 1" class="w-6 h-px bg-gray-200"/>
      </div>
    </div>

    <!-- Content -->
    <div class="flex-1 flex flex-col items-center justify-center p-6 gap-6">

      <!-- Success -->
      <template v-if="step === 'done'">
        <div class="w-20 h-20 rounded-full bg-green-100 flex items-center justify-center">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
        </div>
        <div class="text-center">
          <h3 class="text-xl font-bold text-gray-900 mb-1">PIN Updated!</h3>
          <p class="text-sm text-gray-400">Your PIN has been changed successfully.</p>
        </div>
        <button class="w-full bg-red-600 text-white text-sm font-bold py-3.5 rounded-xl" @click="$router.back()">
          Back to Profile
        </button>
      </template>

      <!-- PIN steps -->
      <template v-else>
        <div class="text-center">
          <div class="w-14 h-14 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-3">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="1.8">
              <rect x="5" y="11" width="14" height="10" rx="2"/>
              <path d="M8 11V7a4 4 0 0 1 8 0v4"/>
            </svg>
          </div>
          <p class="text-sm text-gray-500">{{ stepDesc }}</p>
        </div>

        <div v-if="pinError" class="w-full px-4 py-2.5 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 text-center">
          {{ pinError }}
        </div>

        <PinPad
          ref="pinPadRef"
          title=""
          :error="''"
          @complete="handlePinComplete"
        />

        <button v-if="step !== 'current'" class="text-xs text-gray-400 underline" @click="goBack">
          Back
        </button>
      </template>

    </div>

    <!-- Loading overlay -->
    <LoadingView v-if="loading" message="Updating PIN..." />

  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import PinPad from './PinPad.vue'
import LoadingView from './LoadingView.vue'

const props = defineProps({ user: Object })
const step = ref('current') // current | new | confirm | done
const steps = ['Current', 'New PIN', 'Confirm']
const stepIndex = computed(() => ({ current: 0, new: 1, confirm: 2, done: 3 }[step.value] ?? 0))
const stepDesc = computed(() => ({
  current: 'Enter your current PIN to verify',
  new: 'Enter your new 6-digit PIN',
  confirm: 'Re-enter your new PIN to confirm',
}[step.value] || ''))

const currentPin = ref('')
const newPin = ref('')
const pinError = ref('')
const loading = ref(false)
const pinPadRef = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

async function handlePinComplete(pin) {
  pinError.value = ''

  if (step.value === 'current') {
    currentPin.value = pin
    step.value = 'new'
    await nextTick(); pinPadRef.value?.reset()

  } else if (step.value === 'new') {
    newPin.value = pin
    step.value = 'confirm'
    await nextTick(); pinPadRef.value?.reset()

  } else if (step.value === 'confirm') {
    if (pin !== newPin.value) {
      pinError.value = 'PINs do not match. Please try again.'
      await nextTick(); pinPadRef.value?.reset()
      return
    }
    await submitChangePin()
  }
}

async function submitChangePin() {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/freelancers/${props.user.fl_id}/pin`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ current_pin: currentPin.value, new_pin: newPin.value }),
    })
    const data = await res.json()
    if (!res.ok) {
      pinError.value = data.detail || 'Failed to change PIN.'
      step.value = 'current'
      currentPin.value = ''
      newPin.value = ''
      await nextTick(); pinPadRef.value?.reset()
      return
    }
    step.value = 'done'
  } catch {
    pinError.value = 'Cannot connect to server.'
    step.value = 'current'
    await nextTick(); pinPadRef.value?.reset()
  } finally {
    loading.value = false
  }
}

async function goBack() {
  pinError.value = ''
  if (step.value === 'confirm') { step.value = 'new'; newPin.value = '' }
  else if (step.value === 'new') { step.value = 'current'; currentPin.value = '' }
  await nextTick(); pinPadRef.value?.reset()
}
</script>