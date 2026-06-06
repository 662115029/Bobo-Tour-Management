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

      <div class="relative z-10 w-full max-w-5xl flex items-center gap-10">

        <!-- Left: Mascot + branding -->
        <div class="hidden md:flex flex-col items-center justify-center flex-1">
          <img src="@/assets/logo.png" alt="Bobo Tour" class="h-14 w-auto object-contain mb-6" />
          <img src="@/assets/mascot_default.png" alt="Bobo Mascot" class="w-72 h-auto object-contain" />
        </div>

        <!-- Right: Form -->
        <div class="w-full md:max-w-lg flex-shrink-0">
          <div class="bg-white rounded-2xl border border-gray-200 shadow-md p-7 transition-shadow duration-300 hover:shadow-xl hover:shadow-gray-200/80">

            <h2 class="text-2xl font-bold text-gray-800 mb-1">Create your account</h2>
            <p class="text-sm text-gray-400 mb-5">Fields marked <span class="text-red-500">*</span> are required.</p>

            <!-- Error / Success -->
            <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm flex items-center gap-2">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
              {{ error }}
            </div>
            <div v-if="success" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm flex items-center gap-2">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
              </svg>
              Account created! Redirecting to login...
            </div>

            <form @submit.prevent="handleRegister" class="space-y-3">

              <!-- Row 1: Username -->
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">
                  Username <span class="text-red-500">*</span>
                  <span class="text-gray-400 font-normal ml-1">(cannot be changed)</span>
                </label>
                <div class="relative">
                  <input
                    v-model="form.em_username"
                    @input="onUsernameInput"
                    type="text"
                    required
                    placeholder="e.g. chiang_mai_tours"
                    autocomplete="username"
                    :class="[
                      'w-full px-3 py-2.5 pr-9 border rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:border-transparent transition',
                      usernameState === 'taken'
                        ? 'border-red-400 focus:ring-red-300'
                        : usernameState === 'available'
                        ? 'border-green-400 focus:ring-green-300'
                        : 'border-gray-300 focus:ring-red-400'
                    ]"
                  />
                  <!-- status icon -->
                  <span class="absolute right-2.5 top-1/2 -translate-y-1/2">
                    <svg v-if="usernameChecking" class="w-4 h-4 text-gray-400 animate-spin" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                    </svg>
                    <svg v-else-if="usernameState === 'available'" class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                    </svg>
                    <svg v-else-if="usernameState === 'taken'" class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                    </svg>
                  </span>
                </div>
                <p v-if="usernameState === 'taken'" class="mt-1 text-[11px] text-red-500">Username is already taken.</p>
                <p v-else-if="usernameState === 'available'" class="mt-1 text-[11px] text-green-600">Username is available.</p>
              </div>

              <!-- Row 2: Full Name + Email (2-col) -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Employer Name <span class="text-red-500">*</span></label>
                  <input
                    v-model="form.em_name"
                    type="text"
                    required
                    placeholder="Your name"
                    class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Email <span class="text-red-500">*</span></label>
                  <input
                    v-model="form.em_email"
                    type="email"
                    required
                    placeholder="you@email.com"
                    autocomplete="email"
                    class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                  />
                </div>
              </div>

              <!-- Row 3: Phone + Address (2-col) -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Phone <span class="text-red-500">*</span></label>
                  <input
                    v-model="form.em_phone"
                    type="tel"
                    placeholder="08x xxx xxxx"
                    autocomplete="tel"
                    class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Address <span class="text-red-500">*</span></label>
                  <input
                    v-model="form.em_address"
                    type="text"
                    placeholder="City, Country"
                    class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                  />
                </div>
              </div>

              <!-- Row 4: Bio -->
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-1">Bio <span class="text-gray-400 font-normal">(optional)</span></label>
                <textarea
                  v-model="form.em_bio"
                  rows="2"
                  placeholder="Brief description of your tour company..."
                  class="w-full px-3 py-2.5 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition resize-none"
                ></textarea>
              </div>

              <!-- Row 5: Password + Confirm (2-col) -->
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Password <span class="text-red-500">*</span></label>
                  <div class="relative">
                    <input
                      v-model="form.password"
                      :type="showPassword ? 'text' : 'password'"
                      required
                      placeholder="Min. 8 chars"
                      autocomplete="new-password"
                      class="w-full px-3 py-2.5 pr-9 border border-gray-300 rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:ring-red-400 focus:border-transparent transition"
                    />
                    <button type="button" @click="showPassword = !showPassword"
                      class="absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition">
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
                  <!-- Password strength bar -->
                  <div v-if="form.password" class="mt-1.5">
                    <div class="flex gap-1 mb-0.5">
                      <div v-for="i in 4" :key="i"
                        class="h-1 flex-1 rounded-full transition-all duration-300"
                        :class="i <= passwordStrength.score ? passwordStrength.color : 'bg-gray-200'"
                      />
                    </div>
                    <p class="text-[10px]" :class="passwordStrength.textColor">{{ passwordStrength.label }}</p>
                  </div>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-1">Confirm <span class="text-red-500">*</span></label>
                  <div class="relative">
                    <input
                      v-model="form.confirmPassword"
                      :type="showPassword ? 'text' : 'password'"
                      required
                      placeholder="Re-enter"
                      autocomplete="new-password"
                      :class="[
                        'w-full px-3 py-2.5 pr-9 border rounded-lg text-[13px] focus:outline-none focus:ring-2 focus:border-transparent transition',
                        form.confirmPassword && form.password !== form.confirmPassword
                          ? 'border-red-400 focus:ring-red-300'
                          : form.confirmPassword && form.password === form.confirmPassword
                          ? 'border-green-400 focus:ring-green-300'
                          : 'border-gray-300 focus:ring-red-400'
                      ]"
                    />
                    <!-- confirm match icon -->
                    <span class="absolute right-2.5 top-1/2 -translate-y-1/2">
                      <svg v-if="form.confirmPassword && form.password === form.confirmPassword" class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>
                      </svg>
                      <svg v-else-if="form.confirmPassword && form.password !== form.confirmPassword" class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                      </svg>
                    </span>
                  </div>
                  <p v-if="form.confirmPassword && form.password !== form.confirmPassword" class="mt-1 text-[10px] text-red-500">Passwords do not match.</p>
                  <p v-else-if="form.confirmPassword && form.password === form.confirmPassword" class="mt-1 text-[10px] text-green-600">Passwords match.</p>
                </div>
              </div>

              <button
                type="submit"
                :disabled="loading || usernameState === 'taken' || usernameChecking"
                class="w-full py-2.5 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed mt-1 flex items-center justify-center gap-2"
              >
                <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"/>
                </svg>
                {{ loading ? 'Creating account...' : 'Create Account' }}
              </button>
            </form>

            <p class="text-center text-sm text-gray-500 mt-4">
              Already have an account?
              <router-link to="/login" class="text-red-600 font-medium hover:underline">Sign in</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = '/api'
const router = useRouter()

const form = reactive({
  em_username:     '',
  em_name:         '',
  em_email:        '',
  em_phone:        '',
  em_address:      '',
  em_bio:          '',
  password:        '',
  confirmPassword: '',
})

const loading      = ref(false)
const error        = ref('')
const success      = ref(false)
const showPassword = ref(false)

// --- Username availability check ---
const usernameState    = ref('') // '' | 'available' | 'taken'
const usernameChecking = ref(false)
let usernameTimer = null

function onUsernameInput() {
  usernameState.value = ''
  clearTimeout(usernameTimer)
  const val = form.em_username.trim()
  if (!val) return
  usernameChecking.value = true
  usernameTimer = setTimeout(async () => {
    try {
      const res = await fetch(`${API_BASE}/auth/check-username?username=${encodeURIComponent(val)}`)
      if (res.ok) {
        const data = await res.json()
        usernameState.value = data.taken ? 'taken' : 'available'
      }
    } catch {
      // silently ignore network errors during check
    } finally {
      usernameChecking.value = false
    }
  }, 500)
}

// --- Password strength ---
const passwordStrength = computed(() => {
  const pw = form.password
  if (!pw) return { score: 0, label: '', color: 'bg-gray-200', textColor: 'text-gray-400' }

  let score = 0
  if (pw.length >= 8)                          score++
  if (/[A-Z]/.test(pw))                        score++
  if (/[0-9]/.test(pw))                        score++
  if (/[^A-Za-z0-9]/.test(pw))                score++

  const levels = [
    { score: 1, label: 'Weak',   color: 'bg-red-400',    textColor: 'text-red-500' },
    { score: 2, label: 'Fair',   color: 'bg-orange-400', textColor: 'text-orange-500' },
    { score: 3, label: 'Good',   color: 'bg-yellow-400', textColor: 'text-yellow-600' },
    { score: 4, label: 'Strong', color: 'bg-green-500',  textColor: 'text-green-600' },
  ]
  const level = levels[score - 1] || levels[0]
  return { score, ...level }
})

function validateForm() {
  if (!form.em_username.trim())  return 'Username is required.'
  if (usernameState.value === 'taken') return 'Username is already taken.'
  if (!form.em_name.trim())      return 'Full name is required.'
  if (!form.em_email.trim())     return 'Email is required.'
  if (!form.password)            return 'Password is required.'
  if (form.password.length < 8)  return 'Password must be at least 8 characters.'
  if (passwordStrength.value.score < 2) return 'Password is too weak. Add uppercase letters or numbers.'
  if (form.password !== form.confirmPassword) return 'Passwords do not match.'
  return null
}

function formatApiError(res, data) {
  if (data && typeof data.detail === 'string') return data.detail
  if (data && Array.isArray(data.detail)) {
    const msg = data.detail.map(d => d.msg || JSON.stringify(d)).join(' ')
    if (msg) return msg
  }
  if (data && typeof data.message === 'string') return data.message
  return `Request failed (${res.status}).`
}

const handleRegister = async () => {
  error.value = ''
  const formErr = validateForm()
  if (formErr) { error.value = formErr; return }

  loading.value = true
  try {
    const { confirmPassword, ...payload } = form
    if (!payload.em_phone)   delete payload.em_phone
    if (!payload.em_address) delete payload.em_address
    if (!payload.em_bio)     delete payload.em_bio

    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    let data = {}
    try { data = await res.json() } catch { error.value = 'The server returned an invalid response.'; return }

    if (res.ok) {
      success.value = true
      setTimeout(() => router.push('/login'), 1500)
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