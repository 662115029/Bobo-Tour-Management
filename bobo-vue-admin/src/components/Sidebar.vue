<template>
  <div class="sidebar" :class="{ collapsed: !isOpen }">

    <!-- Brand -->
    <div class="brand">
      <transition name="fade">
        <div class="brand-text" v-if="isOpen">
          <span class="brand-name">Admin Panel</span>
          <span class="brand-sub">FreelanceJob v1.0</span>
        </div>
      </transition>
    </div>

    <!-- Main Nav -->
    <nav class="nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/>
          <rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Dashboard</span>
      </router-link>

      <router-link to="/jobs" class="nav-item" :class="{ active: $route.path.startsWith('/jobs') }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Jobs</span>
      </router-link>

      <router-link to="/verification" class="nav-item" :class="{ active: $route.path === '/verification' }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20z"/><path d="M9 12l2 2 4-4"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Verification</span>
      </router-link>

      <router-link to="/users" class="nav-item" :class="{ active: $route.path === '/users' }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Users</span>
      </router-link>

      <router-link to="/logs" class="nav-item" :class="{ active: $route.path === '/logs' }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="12" y2="17"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Admin Logs</span>
      </router-link>
    </nav>

    <!-- Bottom -->
    <div class="bottom-nav">
      <router-link to="/profile" class="nav-item" :class="{ active: $route.path === '/profile' }">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Profile</span>
      </router-link>

      <div class="admin-profile" @click="router.push('/profile')">
        <div class="admin-avatar" :style="{ background: avatarColor }">{{ adminInitials }}</div>
        <div class="admin-info" v-if="isOpen">
          <span class="admin-name">{{ adminName || 'Admin' }}</span>
          <span class="admin-role">Administrator</span>
        </div>
      </div>

      <button class="nav-item toggle-btn" @click="toggle">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline v-if="isOpen" points="15 18 9 12 15 6"/>
          <polyline v-else points="9 18 15 12 9 6"/>
        </svg>
        <span class="nav-label" v-if="isOpen">Collapse</span>
      </button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const emit = defineEmits(['toggle'])
const isOpen = ref(true)
const router = useRouter()

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const adminName = ref('')
const adminInitials = ref('?')
const avatarColor = ref(localStorage.getItem('avatar_color') || '#1a1a2e')

onMounted(async () => {
  isOpen.value = localStorage.getItem('sidebarOpen') !== 'false'
  const adminId = localStorage.getItem('admin_id')
  if (adminId) {
    try {
      const res = await fetch(`${API_BASE}/admin/me?admin_id=${adminId}`)
      const data = await res.json()
      if (data.name) {
        adminName.value = data.name
        adminInitials.value = data.name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2) || '?'
      }
    } catch (e) {}
  }
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
  left: 0; top: 0;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease;
  z-index: 100;
  overflow: hidden;
}
.sidebar.collapsed { width: 64px; }

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 14px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  min-height: 64px;
  flex-shrink: 0;
}
.brand-logo {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: #06c755;
  color: white;
  font-weight: 800;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.brand-text { display: flex; flex-direction: column; overflow: hidden; }
.brand-name { font-size: 15px; font-weight: 700; white-space: nowrap; }
.brand-sub { font-size: 11px; color: rgba(255,255,255,0.4); white-space: nowrap; }

.nav {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 10px 8px;
  gap: 2px;
  overflow: hidden;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 10px;
  color: rgba(255,255,255,0.5);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  border: none;
  background: none;
  border-radius: 8px;
  border-left: 3px solid transparent;
  transition: all 0.15s;
  white-space: nowrap;
  overflow: hidden;
  cursor: pointer;
  width: 100%;
  text-align: left;
}
.nav-item:hover { color: white; background: rgba(255,255,255,0.07); }
.nav-item.active { color: white; background: rgba(6,199,85,0.15); border-left-color: #06c755; }

.icon { width: 20px; height: 20px; flex-shrink: 0; }
.nav-label { overflow: hidden; text-overflow: ellipsis; }

.sidebar.collapsed .nav { padding: 10px 4px; }
.sidebar.collapsed .nav-item {
  justify-content: center;
  padding: 12px;
  border-left: none;
  border-radius: 8px;
}
.sidebar.collapsed .nav-item.active { background: rgba(6,199,85,0.15); }

.bottom-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 10px 8px;
  border-top: 1px solid rgba(255,255,255,0.08);
}
.sidebar.collapsed .bottom-nav { padding: 10px 4px; }

.admin-profile {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  margin-bottom: 4px;
}
.admin-profile:hover { background: rgba(255,255,255,0.07); }

.admin-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.admin-info {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}
.admin-name {
  font-size: 13px;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.admin-role {
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  white-space: nowrap;
}

.toggle-btn { color: rgba(255,255,255,0.35); }
.toggle-btn:hover { color: white; background: rgba(255,255,255,0.07); }

.fade-enter-active, .fade-leave-active { transition: opacity 0.15s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>