<template>
  <div class="sidebar">
    <div class="brand">
      <h1>AdminPanel</h1>
      <p>FreelanceJob v1.0</p>
    </div>
    <nav class="nav">
      <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
        <span class="icon">▦</span>
        <span>Dashboard</span>
      </router-link>
      <router-link to="/jobs" class="nav-item" :class="{ active: $route.path === '/jobs' }">
        <span class="icon">📄</span>
        <span>Jobs</span>
      </router-link>
      <router-link to="/verification" class="nav-item" :class="{ active: $route.path === '/verification' }">
        <span class="icon">★</span>
        <span>Verification</span>
      </router-link>
      <router-link to="/users" class="nav-item" :class="{ active: $route.path === '/users' }">
        <span class="icon">👤</span>
        <span>Users</span>
      </router-link>
      <router-link to="/logs" class="nav-item" :class="{ active: $route.path === '/logs' }">
        <span class="icon">☰</span>
        <span>Admin Logs</span>
      </router-link>
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 240px;
  background: #1a1a2e;
  color: white;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  padding: 24px 0;
}

.brand {
  padding: 0 24px 32px;
  border-bottom: 1px solid #2a2a4a;
  margin-bottom: 24px;
}

.brand h1 {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
}

.brand p {
  margin: 4px 0 0;
  font-size: 12px;
  opacity: 0.6;
}

.nav {
  display: flex;
  flex-direction: column;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 24px;
  color: white;
  text-decoration: none;
  opacity: 0.7;
  transition: all 0.2s;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  opacity: 1;
  background: rgba(255,255,255,0.05);
}

.nav-item.active {
  opacity: 1;
  border-left-color: #06C755;
  background: rgba(6, 199, 85, 0.1);
}

.icon {
  font-size: 18px;
}
</style>