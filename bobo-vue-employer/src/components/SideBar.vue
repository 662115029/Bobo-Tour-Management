<template>
  <!-- Overlay (mobile / when open) -->
  <div
    v-if="isOpen"
    class="fixed inset-0 z-30 bg-black/20 lg:hidden"
    @click="toggle"
  />

  <!-- Sidebar -->
  <aside
    class="fixed top-0 left-0 h-screen bg-white border-r border-gray-200 flex flex-col z-40 font-['DM_Sans',sans-serif] shadow-sm transition-all duration-300 overflow-hidden"
    :class="isOpen ? 'w-56' : 'w-16'"
  >
    <!-- Logo (click to toggle sidebar) -->
    <div class="px-3 py-5 border-b border-gray-100 flex items-center justify-center shrink-0" :class="isOpen ? 'px-5' : 'px-3'">
      <button @click="toggle" class="flex items-center overflow-hidden cursor-pointer focus:outline-none" :title="isOpen ? 'Collapse sidebar' : 'Expand sidebar'">
        <img v-if="isOpen" src="@/assets/logo.png" alt="Bobo Tour" class="h-16 w-auto object-contain hover:opacity-80 transition-opacity" />
        <img v-else src="@/assets/logo_b.png" alt="Bobo Tour" class="h-10 w-auto object-contain hover:opacity-70 transition-opacity" />      </button>
    </div>

    <!-- Nav Items -->
    <nav class="flex-1 overflow-y-auto py-4 px-2 space-y-1">

      <router-link to="/my-tours" class="nav-item" :class="[isActive('/my-tours') ? 'active' : '', !isOpen ? 'justify-center px-0' : '']" :title="!isOpen ? 'My Tours' : ''">
        <svg xmlns="http://www.w3.org/2000/svg" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <span v-if="isOpen" class="whitespace-nowrap">My Tours</span>
      </router-link>

      <router-link to="/matching" class="nav-item" :class="[isActive('/matching') ? 'active' : '', !isOpen ? 'justify-center px-0' : '']" :title="!isOpen ? 'Matching' : ''">
        <svg xmlns="http://www.w3.org/2000/svg" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-5.916-3.51M9 20H4v-2a4 4 0 015.916-3.51M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
        <span v-if="isOpen" class="whitespace-nowrap">Matching</span>
      </router-link>

      <router-link to="/applications" class="nav-item" :class="[isActive('/applications') ? 'active' : '', !isOpen ? 'justify-center px-0' : '']" :title="!isOpen ? 'Applications' : ''">
        <svg xmlns="http://www.w3.org/2000/svg" class="nav-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
        </svg>
        <span v-if="isOpen" class="whitespace-nowrap">Applications</span>
      </router-link>

    </nav>


  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useSidebar } from './useSidebar.js'

const route = useRoute()
const { isOpen, toggle } = useSidebar()
const isActive = (path) => route.path === path
</script>

<style scoped>
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
  transition: background 0.15s, color 0.15s;
  text-decoration: none;
}
.nav-item:hover {
  background: #fef2f2;
  color: #dc2626;
}
.nav-item.active {
  background: #fef2f2;
  color: #dc2626;
  font-weight: 600;
}
.nav-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
</style>
