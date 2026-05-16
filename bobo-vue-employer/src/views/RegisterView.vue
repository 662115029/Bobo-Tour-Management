<template>
  <div class="min-h-screen flex items-center justify-center p-4" style="background-color: #FEFCFB;">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="flex justify-center mb-8">
        <img src="@/assets/logo_motto.png" alt="Bobo Tour Management" class="h-48 w-auto object-contain" />
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">Create your account</h2>

        <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {{ error }}
        </div>
        <div v-if="success" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
          Account created! Redirecting to login...
        </div>

        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Username *</label>
            <input
              v-model="form.em_username"
              type="text"
              required
              placeholder="your_username"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
            <input
              v-model="form.em_name"
              type="text"
              required
              placeholder="Your full name"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
            <input
              v-model="form.em_phone"
              type="tel"
              placeholder="08x xxx xxxx"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Address</label>
            <input
              v-model="form.em_address"
              type="text"
              placeholder="Your business address"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Bio</label>
            <textarea
              v-model="form.em_bio"
              rows="2"
              placeholder="Brief description of your tour company..."
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition resize-none"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password *</label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="At least 6 characters"
                minlength="6"
                class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition pr-10"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.187-3.592M6.53 6.533A9.97 9.97 0 0112 5c4.477 0 8.268 2.943 9.542 7a10.05 10.05 0 01-4.423 5.294M3 3l18 18" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password *</label>
            <input
              v-model="form.confirmPassword"
              :type="showPassword ? 'text' : 'password'"
              required
              placeholder="Re-enter password"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
          >
            {{ loading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Already have an account?
          <router-link to="/login" class="text-gray-800 font-medium hover:underline">Sign in</router-link>
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

const form = reactive({
  em_username: '',
  em_name: '',
  em_phone: '',
  em_address: '',
  em_bio: '',
  password: '',
  confirmPassword: ''
})
const loading = ref(false)
const error = ref('')
const success = ref(false)
const showPassword = ref(false)

const handleRegister = async () => {
  error.value = ''
  if (form.password !== form.confirmPassword) {
    error.value = 'Passwords do not match.'
    return
  }
  loading.value = true
  try {
    const { confirmPassword, ...payload } = form
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    if (res.ok) {
      success.value = true
      setTimeout(() => router.push('/login'), 1500)
    } else {
      error.value = data.message || 'Registration failed. Please try again.'
    }
  } catch (e) {
    error.value = 'Unable to connect. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
