<template>
  <div class="app">
    <Sidebar @toggle="handleSidebarToggle" />
    <main class="main" :class="{ expanded: isExpanded, collapsed: !isExpanded }">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from './components/Sidebar.vue'

const isExpanded = ref(true)

onMounted(() => {
  isExpanded.value = localStorage.getItem('sidebarOpen') !== 'false'
})

const handleSidebarToggle = (val) => {
  isExpanded.value = val
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
}

.app {
  display: flex;
  min-height: 100vh;
}

.main {
  flex: 1;
  margin-left: 240px;
  transition: margin-left 0.3s ease;
}

.main.collapsed {
  margin-left: 72px;
}
</style>