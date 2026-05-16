<template>
  <header
    class="fixed top-0 right-0 h-14 bg-red-600 flex items-center px-4 gap-3 z-30 shadow-sm font-['DM_Sans',sans-serif] transition-all duration-300"
    :class="isOpen ? 'left-56' : 'left-16'"
  >
    <!-- Page title -->
    <slot>
      <span class="text-white font-semibold text-sm tracking-wide">Bobo Tour Management</span>
    </slot>

    <!-- Right side actions -->
    <div class="ml-auto flex items-center gap-1">

      <!-- Notifications -->
      <button
        class="relative text-white hover:bg-red-700 p-1.5 rounded-lg transition-colors"
        title="Notifications"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 10-12 0v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <!-- Badge -->
        <span class="absolute top-1 right-1 w-2 h-2 bg-yellow-400 rounded-full ring-2 ring-red-600"></span>
      </button>

      <!-- Profile -->
      <router-link
        to="/profile"
        class="flex items-center gap-2 text-white hover:bg-red-700 pl-2 pr-3 py-1.5 rounded-lg transition-colors text-sm font-medium"
        title="Profile"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
        <span class="hidden sm:inline whitespace-nowrap">Profile</span>
      </router-link>

    </div>
  </header>
</template>

<script setup>
import { useSidebar } from './useSidebar.js'
const { isOpen } = useSidebar()
</script>
