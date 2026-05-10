<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/my-tours" class="flex items-center gap-2">
        <span class="text-2xl">🧭</span>
        <span class="text-lg font-bold text-blue-600">Bobo Tour</span>
      </router-link>

      <!-- Nav Links -->
      <div class="flex items-center gap-1">
        <router-link
          to="/my-tours"
          class="px-3 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/my-tours' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-100'"
        >
          📋 My Tours
        </router-link>
        <router-link
          to="/profile"
          class="px-3 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="$route.path === '/profile' ? 'bg-blue-50 text-blue-600' : 'text-gray-600 hover:bg-gray-100'"
        >
          👤 Profile
        </router-link>
        <button
          @click="logout"
          class="ml-2 px-3 py-2 rounded-lg text-sm font-medium text-red-500 hover:bg-red-50 transition-colors"
        >
          🚪 Logout
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

const logout = () => {
  localStorage.removeItem('em_id')
  localStorage.removeItem('em_name')
  localStorage.removeItem('em_email')
  router.push('/login')
}
</script>
