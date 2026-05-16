<template>
  <div class="min-h-screen bg-white font-['DM_Sans',sans-serif]">
    <!-- Sidebar -->
    <SideBar />

    <!-- Top bar -->
    <NavBar>
      <span class="text-white font-semibold text-sm tracking-wide">{{ pageTitle }}</span>
    </NavBar>

    <!-- Main content: shifts right when sidebar is open -->
    <main
      class="pt-14 min-h-screen transition-all duration-300"
      :class="isOpen ? 'ml-56' : 'ml-16'"
    >
      <slot />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import SideBar from './SideBar.vue'
import NavBar from './NavBar.vue'
import { useSidebar } from './useSidebar.js'

const route = useRoute()
const { isOpen } = useSidebar()

const titles = {
  '/my-tours': 'My Tours',
  '/matching': 'Matching',
  '/applications': 'Applications',
  '/profile': 'Profile',
  '/create-job': 'Create Tour',
}

const pageTitle = computed(() => titles[route.path] || 'Bobo Tour Management')
</script>
