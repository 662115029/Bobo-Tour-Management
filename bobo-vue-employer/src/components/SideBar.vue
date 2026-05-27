<template>
  <!-- Sidebar -->
  <aside
    class="fixed top-[72px] left-0 bg-white border-r border-gray-200 flex flex-col z-40 font-['DM_Sans',sans-serif] transition-all duration-300 overflow-hidden" style="height: calc(100vh - 72px)"
    :class="isOpen ? 'w-56' : 'w-16'"
  >
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
// FIX: use @/ alias so this resolves correctly from any location
import { useSidebar } from '@/components/useSidebar.js'

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
