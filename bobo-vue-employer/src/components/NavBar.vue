<template>
  <!-- Fixed top bar that shifts right with the sidebar -->
  <header
    class="fixed top-0 right-0 z-30 flex items-center px-4 py-2 justify-between transition-all duration-300 font-['DM_Sans',sans-serif] bg-white border-b border-gray-200"
    style="left: 0;"
  >
    <!-- Left side: hamburger + logo + page title -->
    <div class="flex items-center gap-3">
      <!-- Hamburger toggle -->
      <button
        @click="toggle"
        class="p-1.5 rounded-lg text-gray-500 hover:bg-[#fef2f2] hover:text-[#dc2626] transition-colors focus:outline-none"
        :title="isOpen ? 'Collapse sidebar' : 'Expand sidebar'"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      <!-- Logo -->
      <img src="@/assets/logo.png" alt="Bobo Tour" class="h-14 w-auto object-contain" />

      <!-- Breadcrumbs -->
      <div class="pl-3 border-l border-gray-200 flex items-center gap-1.5 text-sm">
        <template v-for="(crumb, i) in breadcrumbs" :key="crumb.path">
          <span v-if="i > 0" class="text-gray-300">/</span>
          <router-link
            v-if="i < breadcrumbs.length - 1"
            :to="crumb.path"
            class="text-gray-400 hover:text-[#dc2626] transition-colors"
          >{{ crumb.label }}</router-link>
          <span v-else class="text-gray-700 font-medium">{{ crumb.label }}</span>
        </template>
      </div>
    </div>

    <!-- Right-side actions -->
    <div class="flex items-center gap-1">
      <!-- Profile button -->
      <router-link
        to="/profile"
        class="flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
        :class="route.path === '/profile'
          ? 'bg-[#fef2f2] text-[#dc2626] font-semibold'
          : 'text-gray-600 hover:bg-[#fef2f2] hover:text-[#dc2626]'"
      >
        <!-- Avatar: profile image if available, else initial -->
        <span
          class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 overflow-hidden"
          :style="!profileImageUrl ? avatarStyle(emId, userName) : {}"
        >
          <img
            v-if="profileImageUrl"
            :src="profileImageUrl"
            :alt="userName"
            class="w-full h-full object-cover rounded-full"
            @error="profileImageUrl = ''"
          />
          <template v-else>{{ initials2(userName) }}</template>
        </span>
        <span class="hidden sm:block">{{ userName }}</span>
      </router-link>
    </div>
  </header>

  <!-- Not-verified banner -->
  <div v-if="verifyStatus && verifyStatus !== 'VERIFIED'"
    class="fixed top-[72px] right-0 z-20 bg-amber-50 border-b border-amber-200 text-amber-800 text-[13px] px-4 py-2 text-center transition-all duration-300"
    :class="isOpen ? 'left-56' : 'left-16'">
    Your account is not yet verified. Please complete the verification to access all features.
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAvatar } from '@/composables/useAvatar'
import { useVerifyBanner } from '@/components/useVerifyBanner.js'
import { useSidebar } from '@/components/useSidebar.js'

const { avatarStyle, initials2 } = useAvatar()
const { verifyStatus } = useVerifyBanner()
const API_BASE = '/api'
const router = useRouter()
const route = useRoute()
const { isOpen, toggle } = useSidebar()

const emId = computed(() => localStorage.getItem('em_id') || '')
const userName = computed(() => localStorage.getItem('em_name') || '')
const profileImageUrl = ref('')

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  if (!em_id) return
  try {
    const res = await fetch(`${API_BASE}/employers/${em_id}`)
    if (res.ok) {
      const data = await res.json()
      profileImageUrl.value = data.em_profile_image_url || data.em_profile_url || ''
      verifyStatus.value = data.em_verify_status || ''
    } else {
      verifyStatus.value = 'PENDING'
    }
  } catch {
    // fail-safe: assume not verified rather than silently pass
    verifyStatus.value = 'PENDING'
  }
})

const staticLabels = {
  '/my-tours': 'My Tours',
  '/matching': 'Matching',
  '/applications': 'Applications',
  '/profile': 'Profile',
  '/create-tour': 'Create Tour',
}

const breadcrumbs = computed(() => {
  const path = route.path

  // Tour detail: My Tours > [Tour Title]
  if (path.startsWith('/tours/')) {
    const tourTitle = history.state?.jobTitle || route.params.id
    const shortTitle = tourTitle?.length > 20 ? tourTitle.slice(0, 20) + '…' : tourTitle
    return [
      { label: 'My Tours', path: '/my-tours' },
      { label: shortTitle, path },
    ]
  }

  // Create tour: My Tours > Create Tour
  if (path === '/create-tour') {
    return [
      { label: 'My Tours', path: '/my-tours' },
      { label: 'Create Tour', path: '/create-tour' },
    ]
  }

  // All other pages: single crumb
  const label = staticLabels[path] || 'Bobo Tour'
  return [{ label, path }]
})
</script>