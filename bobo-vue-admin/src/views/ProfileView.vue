<template>
  <div>
    <BreadcrumbBar />
    <div class="mx-5 rounded-lg bg-white p-6">
      <div class="rounded-xl bg-white p-6">
        <div class="mb-6 flex items-center gap-5 border-b border-[#eee] pb-6">
          <div class="relative h-[72px] w-[72px] shrink-0">
            <div
              class="flex h-[72px] w-[72px] items-center justify-center rounded-full text-[28px] font-semibold text-white"
              :style="{ background: avatarColor }"
            >
              {{ initials }}
            </div>
            <button
              type="button"
              class="absolute bottom-0 right-0 flex h-[22px] w-[22px] cursor-pointer items-center justify-center rounded-full bg-white text-[11px] shadow-md"
              title="Change color"
              @click="showPalette = !showPalette"
            >
              ✏️
            </button>
            <div
              v-if="showPalette"
              class="absolute left-0 top-[80px] z-10 grid grid-cols-5 gap-2 rounded-xl bg-white p-3 shadow-lg"
            >
              <div
                v-for="color in colors"
                :key="color"
                class="h-7 w-7 cursor-pointer rounded-full border-[3px] border-transparent transition-transform hover:scale-110"
                :class="{ '!border-[#333] !scale-110': avatarColor === color }"
                :style="{ background: color }"
                @click="pickColor(color)"
              />
            </div>
          </div>
          <div class="min-w-0">
            <h2 class="m-0 mb-1 text-xl text-[#1a1a2e]">{{ admin.name }}</h2>
          </div>
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-[#666]">Status</label>
            <span class="badge" :class="admin.status?.toLowerCase()">{{ admin.status }}</span>
          </div>
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-[#666]">Created</label>
            <span class="text-sm text-[#333]">{{ formatDate(admin.created_at) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <label class="text-sm font-medium text-[#666]">Last Updated</label>
            <span class="text-sm text-[#333]">{{ formatDate(admin.updated_at) }}</span>
          </div>
        </div>
      </div>
      <button
        type="button"
        class="mt-6 cursor-pointer rounded-md border-none bg-[#ffebee] px-6 py-3 text-sm font-medium text-[#c62828] hover:bg-[#ffcdd2]"
        @click="handleLogout"
      >
        Logout
      </button>
    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const admin = ref({})
const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const avatarColor = ref(localStorage.getItem('avatar_color') || '#1a1a2e')
const showPalette = ref(false)

const initials = ref('')

const colors = [
  '#1a1a2e', '#5c6bc0', '#1565c0', '#0277bd', '#00838f',
  '#2e7d32', '#558b2f', '#827717', '#e65100', '#bf360c',
  '#6a1b9a', '#ad1457', '#c62828', '#4e342e', '#37474f'
]

onMounted(async () => {
  const adminId = localStorage.getItem('admin_id')
  if (!adminId) {
    router.push('/login')
    return
  }

  try {
    const res = await fetch(`${API_BASE}/admin/me?admin_id=${adminId}`)
    const data = await res.json()

    if (data.admin_id) {
      admin.value = data
      initials.value = data.name?.split(' ').map(w => w[0]).join('').toUpperCase() || '?'
    }
  } catch (e) {
    console.error('Failed to load admin:', e)
  }
})

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const handleLogout = () => {
  localStorage.removeItem('admin_id')
  localStorage.removeItem('admin_name')
  localStorage.removeItem('admin_username')
  router.push('/login')
}

const pickColor = (color) => {
  avatarColor.value = color
  localStorage.setItem('avatar_color', color)
  showPalette.value = false
}
</script>
