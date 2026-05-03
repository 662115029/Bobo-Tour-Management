<template>
  <div class="sidebar" :class="{ collapsed: !isOpen }">
    <button class="toggle-btn" @click="toggle">
      <span class="hamburger">{{ isOpen ? '✕' : '☰' }}</span>
    </button>
    <div class="brand">
      <h1 :class="{ hidden: !isOpen }">Admin Panel</h1>
      <p v-if="isOpen">FreelanceJob v1.0</p>
    </div>
    <nav class="nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <span class="icon">▦</span>
        <span v-if="isOpen">Dashboard</span>
      </router-link>
      <router-link to="/jobs" class="nav-item" :class="{ active: $route.path === '/jobs' }">
        <span class="icon">📄</span>
        <span v-if="isOpen">Jobs</span>
      </router-link>
      <router-link to="/verification" class="nav-item" :class="{ active: $route.path === '/verification' }">
        <span class="icon">★</span>
        <span v-if="isOpen">Verification</span>
      </router-link>
      <router-link to="/users" class="nav-item" :class="{ active: $route.path === '/users' }">
        <span class="icon">👤</span>
        <span v-if="isOpen">Users</span>
      </router-link>
      <router-link to="/logs" class="nav-item" :class="{ active: $route.path === '/logs' }">
        <span class="icon">☰</span>
        <span v-if="isOpen">Admin Logs</span>
      </router-link>
    </nav>
    <div class="bottom-nav">
      <router-link to="/profile" class="nav-item" :class="{ active: $route.path === '/profile' }">
        <span class="icon">⚙</span>
        <span v-if="isOpen">Profile</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineEmits } from 'vue'

const emit = defineEmits(['toggle'])

const isOpen = ref(true)

onMounted(() => {
  isOpen.value = localStorage.getItem('sidebarOpen') !== 'false'
})

const toggle = () => {
  isOpen.value = !isOpen.value
  localStorage.setItem('sidebarOpen', isOpen.value)
  emit('toggle', isOpen.value)
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: #1a1a2e;
  color: white;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  padding: 10px 0px;
  transition: width 0.3s;
  z-index: 100;
}

.sidebar.collapsed {
  width: 72px;
}

.toggle-btn {
  position: absolute;
  top: 24px;
  right: 16px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: none;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
  z-index: 101;
}

.sidebar.collapsed .toggle-btn {
  right: 20px;
}

.hamburger {
  line-height: 1;
}

.brand {
  padding: 0 0 10px 10px;
  border-bottom: 2px solid #29293d;
  overflow: hidden;
  min-height: 60px;
}

.sidebar.collapsed .brand {
  padding-right: 40px;
}

.brand h1 {
  margin: 0;
  font-size: 17.5px;
  font-weight: 700;
  white-space: nowrap;
  letter-spacing: 0.2px;
  visibility: visible;
}

.sidebar.collapsed .brand h1 {
  visibility: hidden;
}

.brand p {
  font-size: 12px;
  opacity: 0.5;
  white-space: nowrap;
  visibility: visible;
}

.sidebar.collapsed .brand p {
  visibility: hidden;
}

.nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding:5px 10px;
  color: white;
  text-decoration: none;
  opacity: 0.4;
  transition: all 0.2s;
  border-left: 3px solid transparent;
  white-space: nowrap;
  overflow: hidden;
}

.sidebar.collapsed .nav-item {
  padding: 5px;
  justify-content: center;
}

.nav-item:hover {
  opacity: 2;
  background: rgba(255,255,255,0.05);
}

.nav-item.active {
  opacity: 1;
  background: rgba(255, 255, 255, 0.05);
}

.icon {
  font-size: 18px;
  flex-shrink: 0;
}

.bottom-nav {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-top: 2px solid #29293d;
  padding-top: 0px;
}

.sidebar.collapsed .bottom-nav .nav-item {
  padding: 10px;
  justify-content: center;
}
</style>