<template>
  <div class="app">
    <Sidebar />
    <main class="main">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
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
  padding: 24px 32px;
}
</style>