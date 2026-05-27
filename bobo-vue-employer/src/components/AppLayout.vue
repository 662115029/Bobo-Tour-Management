<template>
  <div class="min-h-screen bg-gray font-['DM_Sans',sans-serif]">
    <!-- Sidebar -->
    <SideBar />

    <!-- Top bar -->
    <NavBar>
      <span class="text-sm font-semibold text-gray-700">{{ pageTitle }}</span>
    </NavBar>

    <!-- Main content: shifts right when sidebar is open, shifts down past the fixed top bar -->
    <main
      class="pt-[72px] min-h-screen transition-all duration-300"
      :class="isOpen ? 'ml-56' : 'ml-16'"
    >
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
// FIX: use @/ aliases so these resolve correctly regardless of which view imports AppLayout
import SideBar from '@/components/SideBar.vue'
import NavBar from '@/components/NavBar.vue'
import { useSidebar } from '@/components/useSidebar.js'

const route = useRoute()
const { isOpen } = useSidebar()

const titles = {
  '/my-tours': 'My Tours',
  '/matching': 'Matching',
  '/applications': 'Applications',
  '/profile': 'Profile',
  '/create-tour': 'Create Tour',
}

const pageTitle = computed(() => {
  // Handle dynamic routes like /tours/:id
  if (route.path.startsWith('/tours/')) return 'Tour Detail'
  return titles[route.path] || 'Bobo Tour Management'
})
</script>
