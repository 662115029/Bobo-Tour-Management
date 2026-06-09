<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-[#b5cfe8] font-sans select-none">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-[#00b900] shadow-sm flex-shrink-0">
      <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#00b900" stroke-width="1.8">
          <rect x="3" y="8" width="18" height="13" rx="2"/>
          <path d="M12 8V5"/>
          <circle cx="12" cy="4" r="1"/>
          <circle cx="8.5" cy="14.5" r="1.5" fill="#00b900" stroke="none"/>
          <circle cx="15.5" cy="14.5" r="1.5" fill="#00b900" stroke="none"/>
          <path d="M9 18h6" stroke-linecap="round"/>
          <path d="M3 13h-1M22 13h-1"/>
        </svg>
      </div>
      <div class="flex-1">
        <p class="text-white font-bold text-base leading-tight">BOBO BOT</p>
        <p class="text-green-100 text-xs">Tour Management Assistant</p>
      </div>
      <div v-if="user" class="w-9 h-9 rounded-full overflow-hidden bg-white/30 flex items-center justify-center flex-shrink-0">
        <img v-if="user.fl_profile_image_url" :src="user.fl_profile_image_url" class="w-full h-full object-cover" />
        <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8">
          <circle cx="12" cy="8" r="4"/>
          <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
        </svg>
      </div>
    </div>

    <!-- Chat area -->
    <div class="flex-1 overflow-y-auto px-3 py-4 space-y-3">
      <div class="flex items-end gap-2">
        <div class="w-9 h-9 rounded-full bg-white flex items-center justify-center flex-shrink-0 shadow-sm">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#00b900" stroke-width="1.8">
            <rect x="3" y="8" width="18" height="13" rx="2"/>
            <path d="M12 8V5"/><circle cx="12" cy="4" r="1"/>
            <circle cx="8.5" cy="14.5" r="1.5" fill="#00b900" stroke="none"/>
            <circle cx="15.5" cy="14.5" r="1.5" fill="#00b900" stroke="none"/>
            <path d="M9 18h6" stroke-linecap="round"/>
          </svg>
        </div>
        <div class="flex flex-col gap-1 max-w-[75%]">
          <p class="text-xs text-gray-500 font-semibold ml-1">BOBO BOT</p>
          <div class="bg-white rounded-tr-2xl rounded-br-2xl rounded-bl-2xl px-4 py-3 shadow-sm">
            <p class="text-sm text-gray-800 leading-relaxed">
              Hello! Welcome to <span class="font-bold text-[#00b900]">Bobo Tour Management</span>
            </p>
          </div>
          <div class="bg-white rounded-tr-2xl rounded-br-2xl rounded-bl-2xl px-4 py-3 shadow-sm">
            <p class="text-sm text-gray-800 leading-relaxed">
              <span v-if="!user">Please Login or Register to get started.</span>
              <span v-else>Welcome back, <span class="font-bold text-gray-900">{{ user.fl_name }}</span>!</span>
            </p>
          </div>

          <!-- Jobs banner -->
          <div v-if="user && openJobCount !== null"
            class="bg-white rounded-tr-2xl rounded-br-2xl rounded-bl-2xl overflow-hidden shadow-sm cursor-pointer active:opacity-80"
            @click="$router.push('/jobs')">
            <div class="bg-gradient-to-r from-[#003087] to-[#0057b8] px-4 py-3 flex items-center justify-between">
              <div>
                <p class="text-blue-200 text-xs font-semibold uppercase tracking-wider">Available Now</p>
                <p class="text-white font-black text-2xl leading-tight">Jobs</p>
                <p class="text-yellow-300 font-bold text-lg leading-tight">{{ openJobCount }} Open</p>
              </div>
              <svg width="52" height="52" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.5" opacity="0.85">
                <rect x="1" y="8" width="15" height="10" rx="1.5"/>
                <path d="M16 10l4 2v6h-4V10z"/>
                <circle cx="5.5" cy="19.5" r="1.5" fill="white" stroke="none"/>
                <circle cx="13.5" cy="19.5" r="1.5" fill="white" stroke="none"/>
                <circle cx="19.5" cy="19.5" r="1.5" fill="white" stroke="none"/>
              </svg>
            </div>
            <div class="px-4 py-2 flex items-center gap-1">
              <span class="text-xs text-blue-600 font-semibold">Tap to browse jobs</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2.5">
                <path d="M9 18l6-6-6-6"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast -->
    <div v-if="toast"
      class="absolute bottom-28 left-1/2 -translate-x-1/2 bg-gray-800 text-white text-xs font-semibold px-4 py-2 rounded-full shadow-lg z-50 whitespace-nowrap">
      {{ toast }}
    </div>

    <!-- Bottom area -->
    <div class="flex-shrink-0 bg-white border-t border-gray-200">

      <!-- Rich menu (shown when menuOpen) -->
      <transition name="slide-up">
        <div v-if="menuOpen" class="grid grid-rows-2 border-b border-gray-200" style="grid-template-columns: 1fr 1fr 1fr;">

          <!-- Row 1: Login/Register, Profile, Job (spans 2 rows) -->
          <!-- Login/Register -->
          <button
            class="border-r border-b border-gray-200 py-5 flex flex-col items-center gap-2 active:bg-gray-50 transition-colors bg-white"
            @click="user ? handleLogout() : $router.push('/login')"
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
              <path v-if="!user" d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/>
              <polyline v-if="!user" points="10 17 15 12 10 7"/>
              <path v-if="!user" d="M15 12 L3 12" stroke-linecap="round"/>
              <path v-if="user" d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
              <polyline v-if="user" points="16 17 21 12 16 7"/>
              <path v-if="user" d="M21 12 L9 12" stroke-linecap="round"/>
            </svg>
            <span class="text-[11px] font-bold text-gray-700 text-center leading-tight">
              {{ user ? 'Logout' : 'Login /\nRegister' }}
            </span>
          </button>

          <!-- Profile -->
          <button
            class="border-r border-b border-gray-200 py-5 flex flex-col items-center gap-2 transition-colors bg-white"
            :class="user ? 'active:bg-gray-50' : 'opacity-40'"
            @click="guardedNav('/profile')"
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
              <circle cx="12" cy="8" r="4"/>
              <path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
            </svg>
            <span class="text-[11px] font-bold text-gray-700">Profile</span>
          </button>

          <!-- Job — spans 2 rows -->
          <button
            class="row-span-2 border-gray-200 py-5 flex flex-col items-center justify-center gap-2 transition-colors bg-white"
            :class="user ? 'active:bg-gray-50' : 'opacity-40'"
            @click="guardedNav('/jobs')"
          >
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
              <rect x="2" y="7" width="20" height="14" rx="2"/>
              <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
            </svg>
            <span class="text-[11px] font-bold text-gray-700">Job</span>
          </button>

          <!-- Row 2: Update Availability (spans 2 cols) -->
          <button
            class="col-span-2 border-r border-gray-200 py-5 flex flex-col items-center gap-2 transition-colors bg-white"
            :class="user ? 'active:bg-gray-50' : 'opacity-40'"
            @click="guardedNav('/availability')"
          >
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="1.8">
              <rect x="3" y="4" width="18" height="18" rx="2"/>
              <path d="M16 2v4M8 2v4M3 10h18"/>
              <path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>
            </svg>
            <span class="text-[11px] font-bold text-gray-700">Update Availability</span>
          </button>

        </div>
      </transition>

      <!-- Bottom bar: toggle button + input -->
      <div class="flex items-center gap-2 px-3 py-2">

        <!-- 3-bar toggle -->
        <button
          class="w-10 h-10 flex items-center justify-center rounded-full flex-shrink-0 transition-colors"
          :class="menuOpen ? 'bg-gray-200' : 'bg-white'"
          @click="menuOpen = !menuOpen"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#374151" stroke-width="2">
            <path v-if="!menuOpen" d="M3 6h18M3 12h18M3 18h18" stroke-linecap="round"/>
            <path v-else d="M18 6L6 18M6 6l12 12" stroke-linecap="round"/>
          </svg>
        </button>

        <!-- Input (shown when menu hidden) -->
        <transition name="fade">
          <div v-if="!menuOpen" class="flex-1 flex items-center gap-2">
            <input
              v-model="chatInput"
              type="text"
              placeholder="Message..."
              class="flex-1 bg-gray-100 rounded-full px-4 py-2 text-sm focus:outline-none focus:bg-white focus:ring-1 focus:ring-gray-300 transition-all"
            />
            <button class="w-9 h-9 bg-[#00b900] rounded-full flex items-center justify-center flex-shrink-0 active:opacity-80">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
                <path d="M22 2L11 13M22 2L15 22l-4-9-9-4 20-7z"/>
              </svg>
            </button>
          </div>
        </transition>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({ user: Object })
const emit = defineEmits(['logout'])

const menuOpen = ref(true)
const chatInput = ref('')
const openJobCount = ref(null)
const toast = ref('')

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

onMounted(() => {
  if (props.user?.fl_id) fetchOpenJobCount()
})

async function fetchOpenJobCount() {
  try {
    const res = await fetch(`${API_BASE}/jobs?job_status=OPEN&limit=1`, { headers: HEADERS })
    if (res.ok) {
      const data = await res.json()
      openJobCount.value = data.total ?? data.items?.length ?? 0
    }
  } catch {
    openJobCount.value = 0
  }
}

function guardedNav(path) {
  if (!props.user) {
    showToast('Please login first')
    return
  }
  window.location.hash = path
}

function handleLogout() {
  emit('logout')
}

function showToast(msg) {
  toast.value = msg
  setTimeout(() => { toast.value = '' }, 2000)
}
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>