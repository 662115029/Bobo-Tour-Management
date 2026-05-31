<template>
  <div
    class="fixed left-0 top-0 z-[100] flex h-screen flex-col overflow-hidden bg-[#1a1a2e] text-white transition-[width] duration-300 ease-in-out"
    :class="isOpen ? 'w-[240px]' : 'w-16'"
  >
    <!-- Logo -->
    <div class="flex min-h-16 shrink-0 items-center gap-3 border-b border-white/[0.08] px-3.5 py-4">
      <transition
        enter-active-class="transition-opacity duration-150"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div v-if="isOpen" class="flex min-w-0 flex-col overflow-hidden">
          <span class="whitespace-nowrap text-[15px] font-bold">Admin Panel</span>
          <span class="whitespace-nowrap text-[11px] text-white/40">BoboTourManagement</span>
        </div>
      </transition>
    </div>

    <!-- Nav -->
    <nav class="flex flex-1 flex-col gap-0.5 overflow-hidden py-2.5" :class="isOpen ? 'px-2' : 'px-1'">
      <router-link to="/" class="nav-item" :class="navClasses($route.path === '/')">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="7" height="7" rx="1" /><rect x="14" y="3" width="7" height="7" rx="1" />
          <rect x="3" y="14" width="7" height="7" rx="1" /><rect x="14" y="14" width="7" height="7" rx="1" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Dashboard</span>
      </router-link>

      <router-link to="/jobs" class="nav-item" :class="navClasses($route.path.startsWith('/jobs'))">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="8" y1="13" x2="16" y2="13" /><line x1="8" y1="17" x2="16" y2="17" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Jobs</span>
      </router-link>

      <router-link to="/verification" class="nav-item" :class="navClasses($route.path === '/verification')">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z" /><path d="M9 12l2 2 4-4" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Verification</span>
      </router-link>

      <router-link to="/users" class="nav-item" :class="navClasses($route.path === '/users')">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
          <circle cx="9" cy="7" r="4" />
          <path d="M23 21v-2a4 4 0 0 0-3-3.87" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Users</span>
      </router-link>

      <router-link to="/logs" class="nav-item" :class="navClasses($route.path === '/logs')">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
          <polyline points="14 2 14 8 20 8" />
          <line x1="8" y1="13" x2="16" y2="13" /><line x1="8" y1="17" x2="12" y2="17" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Admin Logs</span>
      </router-link>
    </nav>

    <!-- Bottom section -->
    <div class="flex flex-col gap-0.5 border-t border-white/[0.08] py-2.5" :class="isOpen ? 'px-2' : 'px-1'">

      <!-- Profile nav link (icon row) -->
      <router-link to="/profile" class="nav-item" :class="navClasses($route.path === '/profile')">
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="8" r="4" /><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Profile</span>
      </router-link>

      <!-- Admin profile card -->
      <div
        class="mx-0.5 mt-1 mb-1 cursor-pointer rounded-xl bg-white/[0.05] p-2.5 transition-colors hover:bg-white/[0.09]"
        :class="isOpen ? 'block' : 'flex justify-center'"
        @click="router.push('/profile')"
      >
        <!-- collapsed: just avatar -->
        <template v-if="!isOpen">
          <div
            class="flex h-8 w-8 items-center justify-center rounded-full text-[12px] font-bold text-white"
            :style="{ background: avatarColor }"
          >
            {{ adminInitials }}
          </div>
        </template>

        <!-- expanded: avatar + name/username -->
        <template v-else>
          <div class="flex items-center gap-2.5 min-w-0">
            <!-- Avatar -->
            <div
              class="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-[13px] font-bold text-white"
              :style="{ background: avatarColor }"
            >
              {{ adminInitials }}
            </div>
            <!-- Text -->
            <div class="flex min-w-0 flex-1 flex-col">
              <span class="truncate text-[13px] font-semibold leading-tight text-white">
                {{ adminName || 'Admin' }}
              </span>
              <span class="truncate text-[11px] leading-tight text-white/40">
                @{{ adminUsername || 'administrator' }}
              </span>
            </div>
            <!-- Arrow icon -->
            <svg class="h-3.5 w-3.5 shrink-0 text-white/25" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </template>
      </div>

      <!-- Collapse toggle -->
      <button
        type="button"
        class="nav-item text-white/35 hover:text-white"
        :class="isOpen ? 'px-2.5 py-[11px]' : 'justify-center border-l-0 py-3 px-3'"
        @click="toggle"
      >
        <svg class="h-5 w-5 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline v-if="isOpen" points="15 18 9 12 15 6" />
          <polyline v-else points="9 18 15 12 9 6" />
        </svg>
        <span v-if="isOpen" class="min-w-0 overflow-hidden text-ellipsis whitespace-nowrap">Collapse</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE } from '../data/api'
import { useAvatar } from '../composables/useAvatar'

const emit = defineEmits(['toggle'])
const isOpen = ref(true)
const router = useRouter()
const adminName = ref('')
const adminUsername = ref('')
const avatarColor = ref('#1a1a2e')

const { initials2 } = useAvatar()
const adminInitials = computed(() => initials2(adminName.value))

function navClasses(active) {
  const pad = isOpen.value ? 'px-2.5 py-[11px]' : 'justify-center border-l-0 py-3 px-3'
  if (active) {
    return [
      pad,
      '!bg-[rgba(6,199,85,0.15)] !text-white',
      isOpen.value ? '!border-[#06c755]' : '!border-transparent',
    ]
  }
  return [pad, 'border-transparent text-white/50 hover:bg-white/[0.07] hover:text-white']
}

// sync from localStorage when ProfileView saves changes
const syncFromStorage = () => {
  const adminId = localStorage.getItem('admin_id')
  if (!adminId) return
  const storedName = localStorage.getItem('admin_name')
  if (storedName) {
    adminName.value = storedName
  }
  const colorKey = `avatar_color_${adminId}`
  const storedColor = localStorage.getItem(colorKey)
  if (storedColor) avatarColor.value = storedColor
}

const onStorageChange = (e) => {
  if (e.key === 'admin_name' || e.key?.startsWith('avatar_color_')) {
    syncFromStorage()
  }
}

onMounted(async () => {
  isOpen.value = localStorage.getItem('sidebarOpen') !== 'false'
  const adminId = localStorage.getItem('admin_id')
  if (adminId) {
    try {
      const res = await fetch(`${API_BASE}/admin/me`, {
        headers: { "X-Admin-ID": adminId },
      })
      const data = await res.json()
      if (data.name) {
        adminName.value = data.name
        adminUsername.value = data.username || ''
        localStorage.setItem('admin_name', data.name)
      }
      // avatar color: use existing or create
      const colorKey = `avatar_color_${adminId}`
      const stored = localStorage.getItem(colorKey)
      if (stored) {
        avatarColor.value = stored
      } else {
        const COLORS = [
          '#1565c0','#00838f','#2e7d32','#558b2f',
          '#6a1b9a','#ad1457','#e65100','#4e342e',
          '#37474f','#5c6bc0','#0277bd','#827717',
          '#bf360c','#c62828','#1a1a2e'
        ]
        const picked = COLORS[Math.floor(Math.random() * COLORS.length)]
        localStorage.setItem(colorKey, picked)
        avatarColor.value = picked
      }
    } catch (e) {}
  }

  // listen for profile updates from ProfileView
  window.addEventListener('storage', onStorageChange)
})

onUnmounted(() => {
  window.removeEventListener('storage', onStorageChange)
})

const toggle = () => {
  isOpen.value = !isOpen.value
  localStorage.setItem('sidebarOpen', isOpen.value)
  emit('toggle', isOpen.value)
}
</script>

<style scoped>
@import "tailwindcss" reference;
.nav-item {
  @apply flex w-full cursor-pointer items-center gap-3 rounded-lg border-l-[3px] border-transparent bg-transparent text-left text-sm font-medium no-underline transition-all duration-150;
}
</style>