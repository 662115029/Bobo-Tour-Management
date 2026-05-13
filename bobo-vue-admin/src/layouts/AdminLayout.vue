<template>
  <div class="min-h-screen">
    <Sidebar @toggle="sidebarOpen = $event" />
    <main
      class="min-h-screen bg-[#f5f6fa] transition-[margin-left] duration-200 ease-in-out"
      :class="sidebarOpen ? 'ml-[240px]' : 'ml-16'"
    >
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const sidebarOpen = ref(true)

onMounted(() => {
  sidebarOpen.value = localStorage.getItem('sidebarOpen') !== 'false'
})
</script>
