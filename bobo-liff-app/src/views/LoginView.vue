<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100">
      <button class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center" @click="$router.push('/')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
      </button>
      <div>
        <p class="text-xs font-semibold text-red-600 uppercase tracking-wider">Freelancer</p>
        <h2 class="text-lg font-bold text-gray-900 leading-tight">
          {{ step === 'pin' ? 'Enter PIN' : 'Login' }}
        </h2>
      </div>
    </div>

    <!-- Step: Username -->
    <div v-if="step === 'username'" class="flex-1 flex flex-col p-6 gap-6">

      <div class="bg-blue-50 border-l-4 border-blue-400 rounded-lg px-3 py-2.5 text-xs text-blue-700">
        Enter your username or email to continue.
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Username or Email</label>
        <div class="relative">
          <svg class="absolute left-3 top-1/2 -translate-y-1/2" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2">
            <circle cx="12" cy="8" r="4"/>
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
          <input
            v-model="identifier"
            type="text"
            placeholder="e.g. somchai99"
            class="w-full border border-gray-200 rounded-xl pl-10 pr-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
            :class="identifierError ? 'border-red-400' : ''"
            @keyup.enter="submitIdentifier"
          />
        </div>
        <p v-if="identifierError" class="text-xs text-red-500">{{ identifierError }}</p>
      </div>

      <button
        class="w-full bg-red-600 text-white text-sm font-bold py-3.5 rounded-xl flex items-center justify-center gap-2"
        @click="submitIdentifier"
      >
        Next
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
          <path d="M9 18l6-6-6-6"/>
        </svg>
      </button>

      <!-- Register link -->
      <div class="flex items-center gap-3">
        <div class="flex-1 h-px bg-gray-200"/>
        <span class="text-xs text-gray-400">or</span>
        <div class="flex-1 h-px bg-gray-200"/>
      </div>

      <button
        class="w-full border-2 border-red-600 text-red-600 text-sm font-bold py-3.5 rounded-xl"
        @click="$router.push('/register')"
      >
        Create an Account
      </button>

    </div>

    <!-- Step: PIN pad -->
    <div v-else-if="step === 'pin'" class="flex-1 flex flex-col items-center justify-center p-6 gap-4">

      <div class="text-center">
        <div class="w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
            <circle cx="12" cy="8" r="4"/>
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
        </div>
        <p class="text-sm font-bold text-gray-800">{{ identifier }}</p>
        <p class="text-xs text-gray-400 mt-1">Enter your 6-digit PIN</p>
      </div>

      <PinPad
        ref="pinPadRef"
        title=""
        :error="pinError"
        @complete="handlePinComplete"
      />

      <button class="text-xs text-gray-400 underline" @click="step = 'username'; pinError = ''">
        Back
      </button>

    </div>

    <!-- Loading overlay -->
    <div v-if="loading" class="absolute inset-0 bg-white/70 flex items-center justify-center z-50">
      <div class="flex flex-col items-center gap-3">
        <div class="w-10 h-10 border-3 border-red-600 border-t-transparent rounded-full animate-spin"/>
        <p class="text-sm text-gray-500">Logging in...</p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import PinPad from './PinPad.vue'

defineProps({ user: Object })
const emit = defineEmits(['login'])
const router = useRouter()

const step = ref('username')
const identifier = ref('')
const identifierError = ref('')
const pinError = ref('')
const loading = ref(false)
const pinPadRef = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

function submitIdentifier() {
  if (!identifier.value.trim()) {
    identifierError.value = 'Please enter your username or email.'
    return
  }
  identifierError.value = ''
  step.value = 'pin'
}

async function handlePinComplete(pin) {
  loading.value = true
  pinError.value = ''
  try {
    const res = await fetch(`${API_BASE}/auth/freelancer-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ identifier: identifier.value, pin }),
    })
    const data = await res.json()
    if (!res.ok) {
      pinError.value = data.detail || 'Login failed. Please try again.'
      pinPadRef.value?.reset()
      return
    }
    emit('login', data)
    router.push('/')
  } catch {
    pinError.value = 'Cannot connect to server.'
    pinPadRef.value?.reset()
  } finally {
    loading.value = false
  }
}
</script>