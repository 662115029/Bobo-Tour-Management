<template>
  <div>
    <BreadcrumbBar />

    <div class="mx-5 mb-6 flex flex-col gap-5">

      <!-- Profile Card -->
      <div class="overflow-hidden rounded-2xl bg-white shadow-sm">

        <!-- Top banner + avatar -->
        <div class="relative h-28 w-full" :style="{ background: isLoading ? 'linear-gradient(135deg,#f0f0f0,#e0e0e0)' : bannerGradient }">
          <div v-if="!isLoading" class="absolute -right-6 -top-6 h-32 w-32 rounded-full opacity-20" :style="{ background: avatarColor }" />
          <div v-if="!isLoading" class="absolute -bottom-4 left-16 h-16 w-16 rounded-full opacity-10" :style="{ background: avatarColor }" />
        </div>

        <div class="px-6 pb-6">
          <!-- Avatar + name -->
          <div class="relative -mt-10 mb-4 flex items-end gap-4">
            <!-- Avatar skeleton / real -->
            <div
              v-if="isLoading"
              class="skeleton h-20 w-20 shrink-0 rounded-2xl ring-4 ring-white"
            />
            <div
              v-else
              class="flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl text-3xl font-bold text-white shadow-lg ring-4 ring-white"
              :style="{ background: avatarColor }"
            >
              {{ initials }}
            </div>

            <div class="mb-1 flex-1 min-w-0">
              <template v-if="isLoading">
                <span class="skeleton skeleton-text mb-2 block" style="width:55%"></span>
                <span class="skeleton skeleton-text block" style="width:30%"></span>
              </template>
              <template v-else>
                <div class="flex items-center gap-2 flex-wrap">
                  <span class="text-lg font-bold text-[#1a1a2e] leading-tight">{{ admin.name || '—' }}</span>
                  <span class="badge active text-[10px]">{{ admin.status }}</span>
                </div>
                <p class="text-xs text-[#999] mt-0.5">@{{ admin.username }}</p>
              </template>
            </div>
          </div>

          <!-- Info grid skeleton -->
          <template v-if="isLoading">
            <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div v-for="i in 6" :key="i" class="rounded-xl bg-[#f8f9fb] px-4 py-3">
                <span class="skeleton skeleton-text mb-2 block" style="width:35%"></span>
                <span class="skeleton skeleton-text block" style="width:65%"></span>
              </div>
            </div>
          </template>

          <!-- Info grid -->
          <template v-else>
          <div class="grid grid-cols-1 gap-3 sm:grid-cols-2">

            <!-- Username (read-only) -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Username</span>
              <div class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 shrink-0 text-[#bbb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
                </svg>
                <span class="text-sm font-medium text-[#555]">{{ admin.username || '—' }}</span>
                <span class="ml-auto rounded-md bg-[#eee] px-1.5 py-0.5 text-[9px] font-semibold text-[#999] tracking-wide">FIXED</span>
              </div>
            </div>

            <!-- Status -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Account Status</span>
              <div class="flex items-center gap-2">
                <div class="h-2 w-2 rounded-full bg-[#06c755]" />
                <span class="text-sm font-medium text-[#2e7d32]">{{ admin.status || '—' }}</span>
              </div>
            </div>

            <!-- Name (editable) -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3 transition-all"
              :class="{ 'ring-2 ring-[#06c755]/40 bg-[#f0fdf4]': editingName }">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Display Name</span>
              <div class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 shrink-0 text-[#bbb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M5.121 17.804A4 4 0 018 17h8a4 4 0 012.879 1.196M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
                <template v-if="!editingName">
                  <span class="flex-1 text-sm font-medium text-[#333]">{{ admin.name || '—' }}</span>
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md text-[#aaa] transition-colors hover:bg-[#e8f5e9] hover:text-[#2e7d32]"
                    title="Edit name"
                    @click="startEditName"
                  >
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                </template>
                <template v-else>
                  <input
                    ref="nameInputRef"
                    v-model="nameInput"
                    class="flex-1 rounded-md border border-[#06c755] bg-white px-2 py-0.5 text-sm outline-none"
                    placeholder="Enter name"
                    @keydown.enter="saveName"
                    @keydown.esc="cancelEditName"
                  />
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md bg-[#06c755] text-white transition-opacity hover:opacity-80"
                    :class="{ 'opacity-50 pointer-events-none': savingName }"
                    title="Save"
                    @click="saveName"
                  >
                    <svg v-if="!savingName" class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    <svg v-else class="h-3.5 w-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                    </svg>
                  </button>
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md text-[#aaa] hover:bg-[#fee2e2] hover:text-[#c62828]"
                    title="Cancel"
                    @click="cancelEditName"
                  >
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </template>
              </div>
            </div>

            <!-- Email (editable) -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3 transition-all"
              :class="{ 'ring-2 ring-[#06c755]/40 bg-[#f0fdf4]': editingEmail }">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Email</span>
              <div class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 shrink-0 text-[#bbb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
                <template v-if="!editingEmail">
                  <span class="flex-1 truncate text-sm font-medium text-[#333]">{{ admin.email || '—' }}</span>
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md text-[#aaa] transition-colors hover:bg-[#e8f5e9] hover:text-[#2e7d32]"
                    title="Edit email"
                    @click="startEditEmail"
                  >
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                    </svg>
                  </button>
                </template>
                <template v-else>
                  <input
                    ref="emailInputRef"
                    v-model="emailInput"
                    type="email"
                    class="flex-1 rounded-md border border-[#06c755] bg-white px-2 py-0.5 text-sm outline-none"
                    placeholder="Enter email"
                    @keydown.enter="saveEmail"
                    @keydown.esc="cancelEditEmail"
                  />
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md bg-[#06c755] text-white transition-opacity hover:opacity-80"
                    :class="{ 'opacity-50 pointer-events-none': savingEmail }"
                    title="Save"
                    @click="saveEmail"
                  >
                    <svg v-if="!savingEmail" class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                    </svg>
                    <svg v-else class="h-3.5 w-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                    </svg>
                  </button>
                  <button
                    class="flex h-6 w-6 items-center justify-center rounded-md text-[#aaa] hover:bg-[#fee2e2] hover:text-[#c62828]"
                    title="Cancel"
                    @click="cancelEditEmail"
                  >
                    <svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </button>
                </template>
              </div>
            </div>

            <!-- Created -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Created</span>
              <div class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 shrink-0 text-[#bbb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
                </svg>
                <span class="text-sm text-[#555]">{{ formatDate(admin.created_at) }}</span>
              </div>
            </div>

            <!-- Last Updated -->
            <div class="flex flex-col gap-1 rounded-xl bg-[#f8f9fb] px-4 py-3">
              <span class="text-[10px] font-semibold uppercase tracking-wide text-[#aaa]">Last Updated</span>
              <div class="flex items-center gap-2">
                <svg class="h-3.5 w-3.5 shrink-0 text-[#bbb]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <span class="text-sm text-[#555]">{{ formatDate(admin.updated_at) }}</span>
              </div>
            </div>

          </div><!-- /grid -->
          </template><!-- /v-else -->
        </div>
      </div>

      <!-- Toast -->
      <transition
        enter-active-class="transition-all duration-300 ease-out"
        enter-from-class="opacity-0 translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition-all duration-300 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 translate-y-2"
      >
        <div
          v-if="toast.show"
          class="fixed bottom-6 right-6 z-50 flex items-center gap-3 rounded-xl px-5 py-3 text-sm font-medium text-white shadow-lg"
          :class="toast.type === 'success' ? 'bg-[#2e7d32]' : 'bg-[#c62828]'"
        >
          <svg v-if="toast.type === 'success'" class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
          <svg v-else class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
          {{ toast.message }}
        </div>
      </transition>

      <!-- Logout -->
      <div>
        <button
          type="button"
          class="flex cursor-pointer items-center gap-2 rounded-xl border-none bg-[#ffebee] px-5 py-3 text-sm font-semibold text-[#c62828] transition-colors hover:bg-[#ffcdd2]"
          @click="handleLogout"
        >
          <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
          </svg>
          Logout
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { formatDateTime as formatDate } from '../utils/formatDate'

const router = useRouter()
const admin = ref({})
const isLoading = ref(true)
const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

// ── Avatar color (random per user, persisted by admin_id) ──────────────────
const AVATAR_COLORS = [
  '#1565c0', '#00838f', '#2e7d32', '#558b2f',
  '#6a1b9a', '#ad1457', '#e65100', '#4e342e',
  '#37474f', '#5c6bc0', '#0277bd', '#827717',
  '#bf360c', '#c62828', '#1a1a2e'
]

const avatarColor = ref('#1a1a2e')

const getOrCreateColor = (adminId) => {
  const key = `avatar_color_${adminId}`
  const stored = localStorage.getItem(key)
  if (stored) return stored
  const picked = AVATAR_COLORS[Math.floor(Math.random() * AVATAR_COLORS.length)]
  localStorage.setItem(key, picked)
  return picked
}

const bannerGradient = computed(() => {
  // lighter version of avatarColor for banner
  return `linear-gradient(135deg, ${avatarColor.value}22 0%, ${avatarColor.value}55 100%)`
})

// ── Initials ───────────────────────────────────────────────────────────────
const initials = computed(() =>
  (admin.value.name || '?')
    .split(' ')
    .map(w => w[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
)

// ── Edit Name ──────────────────────────────────────────────────────────────
const editingName = ref(false)
const nameInput = ref('')
const savingName = ref(false)
const nameInputRef = ref(null)

const startEditName = () => {
  nameInput.value = admin.value.name || ''
  editingName.value = true
  nextTick(() => nameInputRef.value?.focus())
}
const cancelEditName = () => { editingName.value = false }

const saveName = async () => {
  const trimmed = nameInput.value.trim()
  if (!trimmed || trimmed === admin.value.name) { cancelEditName(); return }
  savingName.value = true
  try {
    const adminId = localStorage.getItem('admin_id')
    const res = await fetch(`${API_BASE}/admin/${adminId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: trimmed })
    })
    const data = await res.json()
    if (data.error) throw new Error(data.error)
    admin.value.name = trimmed
    admin.value.updated_at = data.updated_at || new Date().toISOString()
    localStorage.setItem('admin_name', trimmed)
    editingName.value = false
    showToast('Name updated', 'success')
  } catch (e) {
    showToast('Failed to update name', 'error')
  } finally {
    savingName.value = false
  }
}

// ── Edit Email ─────────────────────────────────────────────────────────────
const editingEmail = ref(false)
const emailInput = ref('')
const savingEmail = ref(false)
const emailInputRef = ref(null)

const startEditEmail = () => {
  emailInput.value = admin.value.email || ''
  editingEmail.value = true
  nextTick(() => emailInputRef.value?.focus())
}
const cancelEditEmail = () => { editingEmail.value = false }

const saveEmail = async () => {
  const trimmed = emailInput.value.trim()
  if (!trimmed || trimmed === admin.value.email) { cancelEditEmail(); return }
  if (!trimmed.toLowerCase().endsWith('@admin.com')) {
    showToast('Email must use @admin.com domain', 'error')
    return
  }
  savingEmail.value = true
  try {
    const adminId = localStorage.getItem('admin_id')
    const res = await fetch(`${API_BASE}/admin/${adminId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: trimmed })
    })
    const data = await res.json()
    if (data.error) throw new Error(data.error)
    admin.value.email = trimmed
    admin.value.updated_at = data.updated_at || new Date().toISOString()
    editingEmail.value = false
    showToast('Email updated', 'success')
  } catch (e) {
    showToast('Failed to update email', 'error')
  } finally {
    savingEmail.value = false
  }
}

// ── Toast ──────────────────────────────────────────────────────────────────
const toast = ref({ show: false, message: '', type: 'success' })
let toastTimer = null
const showToast = (message, type = 'success') => {
  if (toastTimer) clearTimeout(toastTimer)
  toast.value = { show: true, message, type }
  toastTimer = setTimeout(() => { toast.value.show = false }, 2500)
}

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(async () => {
  const adminId = localStorage.getItem('admin_id')
  if (!adminId) { router.push('/login'); return }

  try {
    const res = await fetch(`${API_BASE}/admin/me?admin_id=${adminId}`)
    const data = await res.json()
    if (data.admin_id) {
      admin.value = data
      avatarColor.value = getOrCreateColor(adminId)
    }
  } catch (e) {
    console.error('Failed to load admin:', e)
  } finally {
    isLoading.value = false
  }
})


const handleLogout = () => {
  localStorage.removeItem('admin_id')
  localStorage.removeItem('admin_name')
  localStorage.removeItem('admin_username')
  router.push('/login')
}
</script>