<template>
  <div v-if="loading" class="loading">
    Loading...
  </div>
  <div v-else-if="error" class="error">
    {{ errorMessage }}
  </div>
  <div v-else-if="user">
    <p>Welcome, {{ user.displayName }}</p>
    <RouterView :user="user" />
  </div>
  <div v-else>
    <p>Initializing LINE login...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import { initLiff } from './liff.js'

const user = ref(null)
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')

onMounted(async () => {
  try {
    user.value = await initLiff()
  } catch (e) {
    error.value = true
    errorMessage.value = `Error: ${e.message || JSON.stringify(e)}`
  } finally {
    loading.value = false
  }
})
</script>
