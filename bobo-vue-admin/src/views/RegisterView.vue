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
    <div class="relative z-10 flex w-full max-w-[900px] overflow-hidden rounded-2xl border border-[#e5e7eb] shadow-xl shadow-[#1a1a2e]/10 transition-shadow duration-300 hover:shadow-2xl hover:shadow-[#1a1a2e]/15">

      <!-- ── Left dark panel ── -->
      <div class="hidden md:flex md:w-[38%] relative flex-col justify-between bg-[#1a1a2e] p-10 overflow-hidden shrink-0">
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
            Create your<br/>account.
          </h1>
          <p class="text-white/40 text-[13px] leading-relaxed">
            Register to manage freelancers, employers, and job verifications.
          </p>
        </div>

        <!-- bottom: rules -->
        <div class="flex flex-col gap-2.5">
          <p class="text-white/25 text-[10px] uppercase tracking-widest mb-0.5">Requirements</p>
          <div v-for="rule in sideRules" :key="rule" class="flex items-start gap-2">
            <div class="w-1.5 h-1.5 rounded-full bg-[#06c755] shrink-0 mt-[5px]" />
            <span class="text-white/40 text-[11px] leading-relaxed">{{ rule }}</span>
          </div>
        </div>
      </div>

      <!-- ── Right form panel ── -->
      <div class="flex-1 bg-white px-10 py-10 flex flex-col justify-center overflow-y-auto">

        <!-- mobile logo -->
        <div class="md:hidden flex items-center gap-2 mb-6">
          <div class="w-7 h-7 rounded-lg bg-[#1a1a2e] flex items-center justify-center">
            <svg class="w-3.5 h-3.5 text-[#06c755]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
          </div>
          <span class="text-[#1a1a2e] font-bold text-[14px]">Admin Portal</span>
        </div>

        <h2 class="text-[#1a1a2e] text-xl font-bold mb-1 tracking-tight">Create account</h2>
        <p class="text-[#666] text-[12px] mb-6">Fill in your details to register a new admin account.</p>

        <form @submit.prevent="handleRegister" class="flex flex-col gap-4">

          <!-- Row 1: Name + Username -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Name</label>
              <input
                type="text"
                v-model="name"
                placeholder="Jane Smith"
                required
                autocomplete="name"
                class="w-full px-4 py-3 bg-[#fafafa] border border-[#e5e7eb] rounded-xl text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] focus:outline-none focus:bg-white focus:border-[#1a1a2e] focus:ring-2 focus:ring-[#1a1a2e]/8 hover:border-[#c5c7cb] transition-all"
              />
            </div>
            <div>
              <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Username</label>
              <input
                type="text"
                v-model="username"
                @input="onUsernameInput"
                placeholder="admin_jane"
                required
                autocomplete="username"
                class="w-full px-4 py-3 bg-[#fafafa] border border-[#e5e7eb] rounded-xl text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] focus:outline-none focus:bg-white focus:border-[#1a1a2e] focus:ring-2 focus:ring-[#1a1a2e]/8 hover:border-[#c5c7cb] transition-all"
              />
              <p class="mt-1 text-[10px] text-[#888]">Lowercase, numbers, <code class="bg-[#f0f0f0] px-0.5 rounded">_</code> and <code class="bg-[#f0f0f0] px-0.5 rounded">.</code> only</p>
            </div>
          </div>

          <!-- Email -->
          <div>
            <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Email</label>
            <input
              type="text"
              v-model="email"
              placeholder="jane@admin.com"
              required
              autocomplete="email"
              class="w-full px-4 py-3 bg-[#fafafa] border border-[#e5e7eb] rounded-xl text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] focus:outline-none focus:bg-white focus:border-[#1a1a2e] focus:ring-2 focus:ring-[#1a1a2e]/8 hover:border-[#c5c7cb] transition-all"
            />
            <p class="mt-1 text-[10px] text-[#888]">Must end with <code class="bg-[#f0f0f0] px-0.5 rounded">@admin.com</code></p>
          </div>

          <!-- Row 2: Password + Confirm -->
          <div class="grid grid-cols-2 gap-3">
            <!-- Password -->
            <div>
              <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Password</label>
              <div class="flex bg-[#fafafa] rounded-xl border border-[#e5e7eb] overflow-hidden hover:border-[#c5c7cb] focus-within:bg-white focus-within:border-[#1a1a2e] focus-within:ring-2 focus-within:ring-[#1a1a2e]/8 transition-all">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  placeholder="Min. 8 chars"
                  required
                  autocomplete="new-password"
                  @focus="passwordTouched = true"
                  class="flex-1 min-w-0 border-0 py-3 px-3 text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] outline-none bg-transparent"
                />
                <button type="button" class="shrink-0 px-2.5 text-[#aaa] hover:text-[#555] transition-colors flex items-center" @click="showPassword = !showPassword">
                  <svg v-if="!showPassword" class="w-[16px] h-[16px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else class="w-[16px] h-[16px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>

            <!-- Confirm -->
            <div>
              <label class="block mb-1.5 text-[11px] font-semibold text-[#444] uppercase tracking-wide">Confirm</label>
              <div class="flex bg-[#fafafa] rounded-xl border border-[#e5e7eb] overflow-hidden hover:border-[#c5c7cb] focus-within:bg-white focus-within:border-[#1a1a2e] focus-within:ring-2 focus-within:ring-[#1a1a2e]/8 transition-all">
                <input
                  :type="showConfirm ? 'text' : 'password'"
                  v-model="confirmPassword"
                  placeholder="Re-enter"
                  required
                  autocomplete="new-password"
                  class="flex-1 min-w-0 border-0 py-3 px-3 text-[13px] text-[#1a1a2e] placeholder:text-[#aaa] outline-none bg-transparent"
                />
                <button type="button" class="shrink-0 px-2.5 text-[#aaa] hover:text-[#555] transition-colors flex items-center" @click="showConfirm = !showConfirm">
                  <svg v-if="!showConfirm" class="w-[16px] h-[16px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                  </svg>
                  <svg v-else class="w-[16px] h-[16px]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Password checklist — compact 2×2 -->
          <div v-if="passwordTouched" class="grid grid-cols-2 gap-x-4 gap-y-1.5 bg-[#fafafa] border border-[#e5e7eb] rounded-xl px-4 py-3">
            <div v-for="rule in passwordRules" :key="rule.label" class="flex items-center gap-2">
              <svg v-if="rule.passed" class="w-3 h-3 shrink-0 text-[#06c755]" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 6L9 17l-5-5"/>
              </svg>
              <svg v-else class="w-3 h-3 shrink-0" :class="submitted && !rule.passed ? 'text-[#dc3545]' : 'text-[#ddd]'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <circle cx="12" cy="12" r="9"/>
              </svg>
              <span class="text-[11px]" :class="rule.passed ? 'text-[#2e7d32]' : submitted && !rule.passed ? 'text-[#dc3545]' : 'text-[#999]'">{{ rule.label }}</span>
            </div>
          </div>

          <!-- Error -->
          <div v-if="error" class="flex items-center gap-2 bg-[#fff5f5] border border-[#fecaca] rounded-xl px-3.5 py-2.5">
            <svg class="w-3.5 h-3.5 shrink-0 text-[#dc3545]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
              <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
            </svg>
            <span class="text-[#dc3545] text-[12px]">{{ error }}</span>
          </div>

          <!-- Success -->
          <div v-if="success" class="flex items-center gap-2 bg-[#f0fdf4] border border-[#bbf7d0] rounded-xl px-3.5 py-2.5">
            <svg class="w-3.5 h-3.5 shrink-0 text-[#2e7d32]" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M20 6L9 17l-5-5"/>
            </svg>
            <span class="text-[#2e7d32] text-[12px] font-medium">{{ success }}</span>
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
            {{ loading ? 'Creating account...' : 'Create account' }}
          </button>
        </form>

        <p class="mt-5 text-center text-[12px] text-[#888]">
          Already have an account?
          <button type="button"
            class="text-[#1a1a2e] font-semibold hover:underline border-none bg-transparent cursor-pointer p-0 ml-0.5 transition-colors hover:text-[#06c755]"
            @click="router.push({ name: 'Login' })"
          >
            Sign in
          </button>
        </p>
      </div>

    </div>
  </div>
  </Transition>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const router = useRouter()

const name = ref('')
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirm = ref(false)
const error = ref('')
const success = ref('')
const loading = ref(false)
const passwordTouched = ref(false)
const submitted = ref(false)

const sideRules = [
  'Email must use @admin.com domain',
  'Username: lowercase, numbers, _ and . only',
  'Password minimum 8 characters',
  'Must include uppercase, number & special character',
  'Access: manage users, jobs, verifications & logs',
]

const onUsernameInput = () => {
  username.value = username.value.toLowerCase().replace(/[^a-z0-9_.]/g, '')
}

const SPECIAL_RE = /[!@#$%^&*()\-_=+[\]{};':",.<>?/\\|`~]/

const passwordRules = computed(() => [
  { label: '8+ characters',  passed: password.value.length >= 8 },
  { label: '1 uppercase',    passed: /[A-Z]/.test(password.value) },
  { label: '1 number',       passed: /[0-9]/.test(password.value) },
  { label: '1 special char', passed: SPECIAL_RE.test(password.value) },
])

const passwordValid = computed(() => passwordRules.value.every(r => r.passed))

function validate() {
  const n = name.value.trim()
  const u = username.value.trim()
  const e = email.value.trim()
  const p = password.value
  const c = confirmPassword.value
  if (!n) return 'Name is required.'
  if (!u) return 'Username is required.'
  if (!/^[a-z0-9_.]+$/.test(u)) return 'Username may only contain lowercase letters, numbers, _ and .'
  if (!e) return 'Email is required.'
  if (!e.toLowerCase().endsWith('@admin.com')) return 'Email must use the @admin.com domain.'
  if (!p) return 'Password is required.'
  if (!passwordValid.value) return 'Password does not meet all requirements above.'
  if (p !== c) return 'Passwords do not match.'
  return null
}

const handleRegister = async () => {
  error.value = ''
  success.value = ''
  submitted.value = true
  passwordTouched.value = true

  const validationError = validate()
  if (validationError) { error.value = validationError; return }

  loading.value = true
  try {
    const res = await fetch(`${API_BASE}/admin/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: name.value.trim(),
        username: username.value.trim(),
        email: email.value.trim(),
        password: password.value,
      }),
    })
    let data = {}
    try { data = await res.json() } catch { error.value = 'The server returned an invalid response.'; return }
    if (res.ok && !data.error) {
      success.value = 'Account created! Redirecting to login…'
      setTimeout(() => router.push({ name: 'Login' }), 1500)
    } else {
      error.value = data.error || `Registration failed (${res.status}).`
    }
  } catch {
    error.value = 'Could not reach the server. Check that the API is running and try again.'
  } finally {
    loading.value = false
  }
}
</script>