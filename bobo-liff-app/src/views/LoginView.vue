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
        <h2 class="text-lg font-bold text-gray-900 leading-tight">Enter PIN</h2>
      </div>
    </div>

    <!-- PIN pad -->
    <div class="flex-1 flex flex-col items-center justify-center p-6 gap-4">

      <div class="text-center">
        <div class="w-14 h-14 rounded-full bg-gray-100 flex items-center justify-center mx-auto mb-3 overflow-hidden">
          <img v-if="lineProfile?.pictureUrl" :src="lineProfile.pictureUrl" class="w-full h-full object-cover" />
          <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
            <circle cx="12" cy="8" r="4"/>
            <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
          </svg>
        </div>
        <p class="text-sm font-bold text-gray-800">{{ lineProfile?.displayName || 'Welcome back' }}</p>
        <p class="text-xs text-gray-400 mt-1">Enter your 6-digit PIN</p>
      </div>

      <PinPad
        ref="pinPadRef"
        title=""
        :error="pinError"
        @complete="handlePinComplete"
      />

    </div>

    <!-- Loading overlay -->
    <LoadingView v-if="loading" message="Logging in..." />

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import PinPad from './PinPad.vue'
import LoadingView from './LoadingView.vue'

const props = defineProps({ user: Object, lineProfile: Object })
const emit = defineEmits(['login'])
const router = useRouter()
const route = useRoute()

const pinError = ref('')
const loading = ref(false)
const pinPadRef = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

async function handlePinComplete(pin) {
  loading.value = true
  pinError.value = ''
  try {
    const res = await fetch(`${API_BASE}/freelancers/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ line_user_id: props.lineProfile?.lineUserId, pin }),
    })
    const data = await res.json()
    if (!res.ok) {
      pinError.value = data.detail || 'Login failed. Please try again.'
      pinPadRef.value?.reset()
      return
    }
    emit('login', data)
    router.push(route.query.redirect || '/')
  } catch {
    pinError.value = 'Cannot connect to server.'
    pinPadRef.value?.reset()
  } finally {
    loading.value = false
  }
}
</script>