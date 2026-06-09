<template>
  <!-- Loading / Splash -->
  <LoadingView v-if="loading" message="Tour Management" />

  <!-- Error -->
  <div v-else-if="error" class="flex flex-col items-center justify-center h-dvh max-w-md mx-auto gap-4 px-6 text-center">
    <img :src="boboLogo" alt="Bobo Bot" class="w-24 h-24 object-contain opacity-50" />
    <p class="text-sm text-red-500">{{ errorMessage }}</p>
    <button class="text-xs text-gray-400 underline" @click="retry">Try again</button>
  </div>

  <!-- App -->
  <div v-else>
    <RouterView :user="user" @login="handleLogin" @logout="handleLogout" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import boboLogo from '@/assets/logo.png'
import LoadingView from '@/views/LoadingView.vue'
import { RouterView } from 'vue-router'
import { initLiff } from './liff.js'

const user = ref(null)
const loading = ref(true)
const error = ref(false)
const errorMessage = ref('')

onMounted(() => init())

async function init() {
  loading.value = true
  error.value = false
  try {
    const stored = sessionStorage.getItem('dev_user')
    if (stored) {
      user.value = JSON.parse(stored)
    } else {
      user.value = await initLiff()
    }
  } catch (e) {
    error.value = true
    errorMessage.value = `Error: ${e.message || JSON.stringify(e)}`
  } finally {
    loading.value = false
  }
}

function retry() { init() }

function handleLogin(userData) {
  sessionStorage.setItem('dev_user', JSON.stringify(userData))
  user.value = userData
}

function handleLogout() {
  sessionStorage.removeItem('dev_user')
  user.value = null
}
</script>