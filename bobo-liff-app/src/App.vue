<template>
  <!-- Loading / Splash -->
  <LoadingView v-if="loading" message="Tour Management" />

  <!-- Error -->
  <div v-else-if="error" class="flex flex-col items-center justify-center h-dvh max-w-md mx-auto gap-4 px-6 text-center">
    <img :src="boboLogo" alt="Bobo Bot" class="w-24 h-24 object-contain opacity-50" />
    <p class="text-sm text-red-500">{{ errorMessage }}</p>
    <button class="text-xs text-gray-400 underline" @click="retry">Try again</button>
  </div>

  <!-- App -->
  <div v-else>
    <RouterView :user="appUser" :lineProfile="lineProfile" @login="handleLogin" @logout="handleLogout" @show-toast="showToast" />

    <!-- Toast notification (legacy, kept for existing callers using @show-toast) -->
    <Transition name="toast">
      <div v-if="toast.visible"
        class="fixed top-5 left-1/2 -translate-x-1/2 z-50 flex items-center gap-3 px-4 py-3 rounded-2xl shadow-lg max-w-[320px] w-[calc(100%-2rem)]"
        :class="toastBg">
        <div class="w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0" :class="toastIconBg">
          <svg v-if="toast.type === 'success'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><path d="M20 6L9 17l-5-5"/></svg>
          <svg v-else-if="toast.type === 'error'" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><path d="M18 6L6 18M6 6l12 12"/></svg>
          <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="3"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
        </div>
        <p class="text-[13px] font-semibold text-white leading-snug flex-1">{{ toast.message }}</p>
      </div>
    </Transition>

    <!-- New Toast/ConfirmDialog components -->
    <Toast />
    <ConfirmDialog />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import boboLogo from '@/assets/logo.png'
import LoadingView from '@/views/LoadingView.vue'
import { RouterView } from 'vue-router'
import { initLiff } from './liff.js'
import Toast from '@/components/Toast.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const router = useRouter()

// lineProfile: identity from LINE (lineUserId, displayName, pictureUrl) — available
// as soon as the LIFF app opens, regardless of whether the person is registered.
const lineProfile = ref(null)

// appUser: the authenticated app session (has fl_id) — only set after PIN is verified.
// Every view (Home/Jobs/Profile/Availability/ChangePin) gates access on this, not lineProfile.
const appUser = ref(null)

const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')

const toast = ref({ visible: false, message: '', type: 'success' })
let toastTimer = null

const toastBg = computed(() => ({
  'bg-green-600': toast.value.type === 'success',
  'bg-red-600': toast.value.type === 'error',
  'bg-gray-700': toast.value.type === 'info',
}))

const toastIconBg = computed(() => ({
  'bg-green-700': toast.value.type === 'success',
  'bg-red-700': toast.value.type === 'error',
  'bg-gray-600': toast.value.type === 'info',
}))

function showToast({ message, type = 'success' }) {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { visible: true, message, type }
  toastTimer = setTimeout(() => { toast.value.visible = false }, 3000)
}

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

onMounted(() => init())

async function init() {
  loading.value = true
  error.value = false
  try {
    // Always get LINE identity first — this is free, no user interaction needed.
    lineProfile.value = await initLiff()

    const stored = sessionStorage.getItem('fl_session')
    if (stored) {
      // Already logged in this session (PIN was verified earlier) — restore it.
      appUser.value = JSON.parse(stored)
    } else if (lineProfile.value?.lineUserId) {
      // Not logged in yet this session — figure out whether this LINE user
      // is already registered, and route to PIN-unlock or Register accordingly.
      await routeByLineStatus(lineProfile.value.lineUserId)
    } else {
      router.push('/login')
    }
  } catch (e) {
    error.value = true
    errorMessage.value = `Error: ${e.message || JSON.stringify(e)}`
  } finally {
    loading.value = false
  }
}

async function routeByLineStatus(lineUserId) {
  try {
    const res = await fetch(`${API_BASE}/freelancers/by-line/${lineUserId}`, { headers: HEADERS })
    const data = await res.json()
    router.push(data.exists ? '/login' : '/register')
  } catch {
    // Backend unreachable — fall back to the login screen either way.
    router.push('/login')
  }
}

function retry() { init() }

function handleLogin(userData) {
  sessionStorage.setItem('fl_session', JSON.stringify(userData))
  appUser.value = userData
}

function handleLogout() {
  sessionStorage.removeItem('fl_session')
  appUser.value = null
  router.push('/login')
}
</script>

<style scoped>
.toast-enter-active { animation: slideDown 0.3s ease; }
.toast-leave-active { animation: slideDown 0.3s ease reverse; }
@keyframes slideDown {
  from { opacity: 0; transform: translateX(-50%) translateY(-16px); }
  to   { opacity: 1; transform: translateX(-50%) translateY(0); }
}
</style>