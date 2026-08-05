<template>
  <Transition
    appear
    enter-active-class="transition-all duration-[220ms] ease-out"
    enter-from-class="opacity-0 scale-[0.97]"
    enter-to-class="opacity-100 scale-100"
  >
    <div class="relative min-h-screen bg-[#f8f9fb] flex items-center justify-center p-4 font-['DM_Sans',sans-serif] overflow-hidden">

      <!-- dot grid -->
      <div class="pointer-events-none absolute inset-0 z-0" style="background-image: radial-gradient(circle, #c8cad0 1px, transparent 1px); background-size: 28px 28px; opacity: 0.55;" />

      <div class="relative z-10 w-full max-w-3xl flex items-center gap-10">

        <!-- Left: Mascot + branding -->
        <div class="hidden md:flex flex-col items-center justify-center flex-1">
          <img src="@/assets/logo.png" alt="Bobo Tour" class="h-14 w-auto object-contain mb-6" />
          <img src="@/assets/mascot_default.png" alt="Bobo Mascot" class="w-72 h-auto object-contain" />
        </div>

        <!-- Right: Form -->
        <div class="w-full md:max-w-sm flex-shrink-0">
          <div class="bg-white rounded-2xl border border-gray-200 shadow-md p-8 transition-shadow duration-300 hover:shadow-xl hover:shadow-gray-200/80">
            <h2 class="text-2xl font-bold text-gray-800 mb-6">Sign in to your account</h2>

            <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm flex items-center gap-2">
              <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>

            <form @submit.prevent="handleLogin" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Username or Email</label>
                <input
                  v-model="form.identifier"
                  type="text"
                  required
                  placeholder="Your username or email"
                  autocomplete="username"
                  class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Password</label>
                <div class="relative">
                  <input
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    placeholder="••••••••"
                    autocomplete="current-password"
                    class="w-full px-3 py-2.5 pr-9 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition pr-10"
                  />
                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition"
                  >
                    <svg v-if="showPassword" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-5 0-9-4-9-7s4-7 9-7a9.96 9.96 0 015.362 1.562M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" d="M3 3l18 18"/>
                    </svg>
                    <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>
                    </svg>
                  </button>
                </div>
              </div>

              <button
                type="submit"
                :disabled="loading"
                class="w-full py-2.5 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2 flex items-center justify-center gap-2"
              >
                <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
                {{ loading ? 'Signing in...' : 'Sign In' }}
              </button>
            </form>

            <p class="text-center text-sm text-gray-500 mt-6">
              Don't have an account?
              <router-link to="/register" class="text-red-600 font-medium hover:underline">Register here</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = import.meta.env.VITE_API_BASE || '/api'
const router = useRouter()

const form = reactive({ identifier: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPassword = ref(false)

function validateForm() {
  if (!form.identifier.trim()) return 'Username or email is required.'
  if (!form.password.trim()) return 'Password is required.'
  return null
}

function formatApiError(res, data) {
  if (data && typeof data.error === 'string') return data.error
  if (data && Array.isArray(data.detail)) {
    const msg = data.detail.map(d => d.msg ? `${d.loc?.join?.('.') || ''}: ${d.msg}` : JSON.stringify(d)).join(' ')
    if (msg) return msg
  }
  if (data && typeof data.detail === 'string') return data.detail
  return `Request failed (${res.status}).`
}

const handleLogin = async () => {
  error.value = ''
  const formErr = validateForm()
  if (formErr) { error.value = formErr; return }

  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier: form.identifier.trim(), password: form.password })
    })
    let data = {}
    try { data = await res.json() } catch { error.value = 'The server returned an invalid response.'; return }

    if (res.ok) {
      localStorage.setItem('em_id',                data.em_id)
      localStorage.setItem('em_username',          data.em_username || '')
      localStorage.setItem('em_name',              data.em_name || '')
      localStorage.setItem('em_email',             data.em_email || '')
      localStorage.setItem('em_profile_image_url', data.em_profile_image_url || '')
      router.push('/my-tours')
    } else {
      error.value = formatApiError(res, data)
    }
  } catch {
    error.value = 'Unable to connect. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
