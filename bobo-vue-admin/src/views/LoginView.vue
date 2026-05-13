<template>
  <div class="min-h-screen flex items-center justify-center bg-[#1a1a2e]">
    <div class="bg-white p-10 rounded-xl w-[440px]">
      <h1 class="mt-0 mb-6 text-2xl font-semibold text-[#1a1a2e] text-center">Admin Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="mb-5">
          <label class="block mb-2 text-sm font-medium text-[#333]">Username or email</label>
          <input
            type="text"
            v-model="username"
            placeholder="e.g. admin_khimmy or name@admin.com"
            required
            autocomplete="username"
            class="w-full px-[14px] py-3 border border-[#ddd] rounded-md text-sm focus:outline-none focus:border-[#1a1a2e]"
          />
        </div>
        <div class="mb-5">
          <label class="block mb-2 text-sm font-medium text-[#333]">Password</label>
          <div
            class="flex rounded-md border border-[#ddd] overflow-hidden focus-within:border-[#1a1a2e] focus-within:ring-1 focus-within:ring-[#1a1a2e]/20"
          >
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Password"
              required
              autocomplete="current-password"
              class="flex-1 min-w-0 border-0 py-3 px-[14px] text-sm outline-none bg-white"
            />
            <button
              type="button"
              class="shrink-0 px-3 border-l border-[#eee] bg-[#fafafa] text-[#444] hover:bg-[#f0f0f0] transition-colors flex items-center justify-center"
              :aria-pressed="showPassword"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
              :title="showPassword ? 'Hide password' : 'Show password'"
              @click="showPassword = !showPassword"
            >
              <svg
                v-if="!showPassword"
                class="w-5 h-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <svg
                v-else
                class="w-5 h-5"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path
                  d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"
                />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
            </button>
          </div>
        </div>
        <p v-if="error" class="text-[#dc3545] text-sm mb-4">{{ error }}</p>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-[14px] bg-[#1a1a2e] text-white border-none rounded-md text-base font-medium cursor-pointer hover:bg-[#2a2a4e] disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const RETRY_HINT = ' Please verify your details and try again.'

function validateLoginForm(usernameRaw, passwordRaw) {
  const u = (usernameRaw || '').trim()
  const p = (passwordRaw || '').trim()
  if (!u) {
    return 'Username or email is missing.' + RETRY_HINT
  }
  if (!p) {
    return 'Password is missing.' + RETRY_HINT
  }
  if (u.includes('@')) {
    const i = u.lastIndexOf('@')
    const domain = u.slice(i + 1).trim()
    const domainLower = domain.toLowerCase()
    if (i <= 0 || !domain) {
      return (
        'That email address is not valid (check the part before and after @).' +
        RETRY_HINT
      )
    }
    if (domainLower !== 'admin.com') {
      return (
        `Admin email must use the domain @admin.com only (you entered: ${domain}).` +
        RETRY_HINT
      )
    }
  }
  return null
}

function formatApiError(res, data) {
  if (data && typeof data.error === 'string') return data.error
  if (data && Array.isArray(data.detail)) {
    const msg = data.detail
      .map((d) => (d.msg ? `${d.loc?.join?.('.') || ''}: ${d.msg}` : JSON.stringify(d)))
      .join(' ')
    if (msg) return msg + RETRY_HINT
  }
  if (data && typeof data.detail === 'string') return data.detail + RETRY_HINT
  return `Request failed (${res.status}).` + RETRY_HINT
}

const handleLogin = async () => {
  error.value = ''
  const formErr = validateLoginForm(username.value, password.value)
  if (formErr) {
    error.value = formErr
    return
  }

  loading.value = true

  try {
    const res = await fetch(`${API_BASE}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    let data = {}
    try {
      data = await res.json()
    } catch {
      error.value =
        'The server returned an invalid response.' + RETRY_HINT
      return
    }

    if (data.success) {
      localStorage.setItem('admin_id', data.admin.admin_id)
      localStorage.setItem('admin_name', data.admin.name)
      router.push({ name: 'Dashboard' })
    } else if (!res.ok || data.success === false) {
      error.value = formatApiError(res, data)
    } else {
      error.value = 'Login could not be completed.' + RETRY_HINT
    }
  } catch (e) {
    error.value =
      'Could not reach the server. Check that the API is running and your network, then try again.'
  } finally {
    loading.value = false
  }
}
</script>