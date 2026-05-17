<template>
  <Transition
    appear
    enter-active-class="transition-all duration-[220ms] ease-out"
    enter-from-class="opacity-0 scale-[0.97]"
    enter-to-class="opacity-100 scale-100"
  >
  <div class="relative min-h-screen flex items-center justify-center bg-[#f8f9fb] px-4 py-10 overflow-hidden">
  <!-- dot grid background -->
      <div class="pointer-events-none absolute inset-0 z-0" style="background-image: radial-gradient(circle, #c8cad0 1px, transparent 1px); background-size: 28px 28px; opacity: 0.55;" />

    <!-- Card -->
    <div class="relative z-10 flex w-full max-w-[820px] overflow-hidden rounded-2xl border border-[#e5e7eb] shadow-xl shadow-[#1a1a2e]/10 transition-shadow duration-300 hover:shadow-2xl hover:shadow-[#1a1a2e]/15">

      <!-- ── Left dark panel ── -->
      <div class="hidden md:flex md:w-[42%] relative flex-col justify-between bg-[#1a1a2e] p-10 overflow-hidden shrink-0">
        <!-- decorative circles -->
        <div class="pointer-events-none absolute -top-20 -left-20 w-72 h-72 rounded-full opacity-[0.08]" style="background: radial-gradient(circle, #06c755, transparent 70%);" />
        <div class="pointer-events-none absolute -bottom-16 -right-16 w-64 h-64 rounded-full opacity-[0.06]" style="background: radial-gradient(circle, #06c755, transparent 70%);" />
        <div class="pointer-events-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[340px] h-[340px] rounded-full opacity-[0.04] border border-white" />

        <!-- top -->
        <div>
          <div class="flex items-center gap-2.5 mb-12">
            <div class="w-8 h-8 rounded-xl bg-[#06c755] flex items-center justify-center shadow-lg shadow-[#06c755]/40">
              <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
              </svg>
            </div>
            <span class="text-white font-bold text-[15px] tracking-tight">Admin Portal</span>
          </div>

          <h1 class="text-white text-3xl font-bold leading-tight mb-3 tracking-tight">
            Welcome<br/>back.
          </h1>
          <p class="text-white/40 text-[13px] leading-relaxed">
            Manage freelancers, employers, jobs and verifications — all in one place.
          </p>
        </div>

        <!-- bottom: project feature pills -->
        <div class="flex flex-col gap-2">
          <p class="text-white/25 text-[10px] uppercase tracking-widest mb-1">What you can manage</p>
          <div v-for="feat in features" :key="feat.label" class="flex items-center gap-2.5">
            <div class="w-6 h-6 rounded-lg bg-white/[0.07] flex items-center justify-center shrink-0">
              <svg class="w-3 h-3 text-[#06c755]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" :d="feat.icon"/>
              </svg>
            </div>
            <span class="text-white/40 text-[11px]">{{ feat.label }}</span>
          </div>
        </div>
      </div>

      <!-- ── Right form panel ── -->
      <div class="flex-1 bg-white px-10 py-10 flex flex-col justify-center">

        <!-- mobile logo -->
        <div class="md:hidden flex items-center gap-2 mb-7">
          <div class="w-7 h-7 rounded-lg bg-[#1a1a2e] flex items-center justify-center">
            <svg class="w-3.5 h-3.5 text-[#06c755]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <span class="text-[#1a1a2e] font-bold text-[14px]">Admin Portal</span>
        </div>

        <h2 class="text-[#1a1a2e] text-xl font-bold mb-1 tracking-tight">Sign in</h2>
        <p class="text-[#666] text-[12px] mb-7">Enter your credentials to continue.</p>

        <form @submit.prevent="handleLogin" class="flex flex-col gap-4">

          <!-- Username -->
          <div>
            <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Username or Email</label>
            <input
              type="text"
              v-model="username"
              placeholder="admin_jane or jane@admin.com"
              required
              autocomplete="username"
              class="w-full px-4 py-3 bg-[#fafafa] border border-[#e5e7eb] rounded-xl text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] focus:outline-none focus:bg-white focus:border-[#1a1a2e] focus:ring-2 focus:ring-[#1a1a2e]/8 hover:border-[#c5c7cb] transition-all"
            />
          </div>

          <!-- Password -->
          <div>
            <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Password</label>
            <div class="flex bg-[#fafafa] rounded-xl border border-[#e5e7eb] overflow-hidden hover:border-[#c5c7cb] focus-within:bg-white focus-within:border-[#1a1a2e] focus-within:ring-2 focus-within:ring-[#1a1a2e]/8 transition-all">
              <input
                :type="showPassword ? 'text' : 'password'"
                v-model="password"
                placeholder="Your password"
                required
                autocomplete="current-password"
                class="flex-1 min-w-0 border-0 py-3 px-4 text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] outline-none bg-transparent"
              />
              <button type="button"
                class="shrink-0 px-3.5 text-[#aaa] hover:text-[#555] transition-colors flex items-center"
                @click="showPassword = !showPassword"
              >
                <svg v-if="!showPassword" class="w-[17px] h-[17px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                </svg>
                <svg v-else class="w-[17px] h-[17px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                  <line x1="1" y1="1" x2="23" y2="23"/>
                </svg>
              </button>
            </div>
          </div>

          <!-- Error -->
          <div v-if="error" class="flex items-center gap-2 bg-[#fff5f5] border border-[#fecaca] rounded-xl px-3.5 py-2.5">
            <svg class="w-3.5 h-3.5 shrink-0 text-[#dc3545]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span class="text-[#dc3545] text-[12px]">{{ error }}</span>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3.5 bg-[#1a1a2e] text-white rounded-xl text-[13px] font-semibold border border-[#1a1a2e] cursor-pointer hover:bg-[#2a2a4e] hover:border-[#2a2a4e] active:scale-[0.99] disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 mt-1"
          >
            <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
            </svg>
            {{ loading ? 'Signing in...' : 'Sign in' }}
          </button>
        </form>

        <p class="mt-6 text-center text-[12px] text-[#888]">
          Don't have an account?
          <button type="button"
            class="text-[#1a1a2e] font-semibold hover:underline border-none bg-transparent cursor-pointer p-0 ml-0.5 transition-colors hover:text-[#06c755]"
            @click="router.push({ name: 'Register' })"
          >
            Register
          </button>
        </p>
      </div>

    </div>
  </div>
  </Transition>
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

const features = [
  { label: 'Freelancer & employer management', icon: 'M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75' },
  { label: 'Job posting oversight',            icon: 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' },
  { label: 'Document verification queue',      icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' },
  { label: 'Admin activity logs',              icon: 'M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z' },
]

function validateLoginForm(usernameRaw, passwordRaw) {
  const u = (usernameRaw || '').trim()
  const p = (passwordRaw || '').trim()
  if (!u) return 'Username or email is required.'
  if (!p) return 'Password is required.'
  if (u.includes('@')) {
    const i = u.lastIndexOf('@')
    const domain = u.slice(i + 1).trim()
    if (i <= 0 || !domain) return 'Email address is not valid.'
    if (domain.toLowerCase() !== 'admin.com') return `Admin email must use @admin.com (entered: ${domain}).`
  }
  return null
}

function formatApiError(res, data) {
  if (data && typeof data.error === 'string') return data.error
  if (data && Array.isArray(data.detail)) {
    const msg = data.detail.map((d) => (d.msg ? `${d.loc?.join?.('.') || ''}: ${d.msg}` : JSON.stringify(d))).join(' ')
    if (msg) return msg
  }
  if (data && typeof data.detail === 'string') return data.detail
  return `Request failed (${res.status}).`
}

const handleLogin = async () => {
  error.value = ''
  const raw = username.value.trim()
  const normalizedUsername = raw.includes('@') ? raw : raw.toLowerCase()
  const formErr = validateLoginForm(normalizedUsername, password.value)
  if (formErr) { error.value = formErr; return }

  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: normalizedUsername, password: password.value })
    })
    let data = {}
    try { data = await res.json() } catch { error.value = 'The server returned an invalid response.'; return }
    if (data.success) {
      localStorage.setItem('admin_id', data.admin.admin_id)
      localStorage.setItem('admin_name', data.admin.name)
      router.push({ name: 'Dashboard' })
    } else if (!res.ok || data.success === false) {
      error.value = formatApiError(res, data)
    } else {
      error.value = 'Login could not be completed.'
    }
  } catch {
    error.value = 'Could not reach the server. Check that the API is running and try again.'
  } finally {
    loading.value = false
  }
}
</script>