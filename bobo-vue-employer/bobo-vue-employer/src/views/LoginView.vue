<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="text-5xl mb-3">🧭</div>
        <h1 class="text-3xl font-bold text-blue-600">Bobo Tour</h1>
        <p class="text-gray-500 text-sm mt-1">Tour Management Platform</p>
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">Sign in to your account</h2>

        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {{ error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              v-model="form.em_username"
              type="text"
              required
              placeholder="your_username"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="••••••••"
                class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-10"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {{ showPassword ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Don't have an account?
          <router-link to="/register" class="text-blue-600 font-medium hover:underline">Register here</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = '/api'
const router = useRouter()

const form = reactive({ em_username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  // --- DEV MODE: bypass auth for demo ---
  localStorage.setItem('em_id', '00000000-0000-0000-0002-000000000001')
  localStorage.setItem('em_name', 'Travel Everywhere Co., Ltd.')
  localStorage.setItem('em_username', 'travel_everywhere')
  router.push('/my-tours')
  loading.value = false
  // --- END DEV MODE ---

  // TODO: re-enable real login below when done with demo
  // try {
  //   const res = await fetch(`${API_BASE}/auth/login`, {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify(form)
  //   })
  //   const data = await res.json()
  //   if (res.ok) {
  //     localStorage.setItem('em_id', data.em_id)
  //     localStorage.setItem('em_name', data.em_name)
  //     localStorage.setItem('em_username', data.em_username)
  //     router.push('/my-tours')
  //   } else {
  //     error.value = data.message || 'Invalid username or password.'
  //   }
  // } catch (e) {
  //   error.value = 'Unable to connect. Please try again.'
  // } finally {
  //   loading.value = false
  // }
}
</script>
