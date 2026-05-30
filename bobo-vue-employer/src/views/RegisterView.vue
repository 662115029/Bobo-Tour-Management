<template>
  <div class="min-h-screen bg-white flex items-center justify-center p-4 font-['DM_Sans',sans-serif]">

    <!-- Centered container: mascot left + form right -->
    <div class="w-full max-w-3xl flex items-center gap-10">

      <!-- Left: Mascot + branding -->
      <div class="hidden md:flex flex-col items-center justify-center flex-1">
        <img src="@/assets/logo.png" alt="Bobo Tour" class="h-14 w-auto object-contain mb-6" />
        <img src="@/assets/mascot_default.png" alt="Bobo Mascot" class="w-full h-auto object-contain" />
      </div>

      <!-- Right: Form -->
      <div class="w-full md:max-w-sm flex-shrink-0">

        <!-- Card -->
        <div class="bg-white rounded-2xl border border-gray-200 shadow-md p-8">
          <h2 class="text-xl font-bold text-gray-800 mb-6">Create your account</h2>

          <div v-if="error" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {{ error }}
          </div>
          <div v-if="success" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
            Account created! Redirecting to login...
          </div>

          <form @submit.prevent="handleRegister" class="space-y-4">

            <!-- Username -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Username <span class="text-red-500">*Cannot be changed</span></label>
              <input
                v-model="form.em_username"
                type="text"
                required
                placeholder="e.g. chiang_mai_tours"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <!-- Full Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Full Name <span class="text-red-500">*</span></label>
              <input
                v-model="form.em_name"
                type="text"
                required
                placeholder="Your company or full name"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <!-- Email -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email <span class="text-red-500">*</span></label>
              <input
                v-model="form.em_email"
                type="email"
                required
                placeholder="your@email.com"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <!-- Phone -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number <span class="text-red-500">*</span></label>
              <input
                v-model="form.em_phone"
                type="tel"
                required
                placeholder="08x xxx xxxx"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <!-- Address -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Address <span class="text-red-500">*</span></label>
              <input
                v-model="form.em_address"
                type="text"
                required
                placeholder="e.g. Chiang Mai, Thailand"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <!-- Bio -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">
                Bio <span class="text-gray-400 font-normal text-xs">(optional)</span>
              </label>
              <textarea
                v-model="form.em_bio"
                rows="2"
                placeholder="Brief description of your tour company..."
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition resize-none"
              ></textarea>
            </div>

            <!-- Password -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Password <span class="text-red-500">*</span></label>
              <div class="relative">
                <input
                  v-model="form.password"
                  :type="showPassword ? 'text' : 'password'"
                  required
                  placeholder="At least 6 characters"
                  minlength="6"
                  class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition pr-10"
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

            <!-- Confirm Password -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Confirm Password <span class="text-red-500">*</span></label>
              <input
                v-model="form.confirmPassword"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="Re-enter password"
                class="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400 transition"
              />
            </div>

            <button
              type="submit"
              :disabled="loading"
              class="w-full py-3 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            >
              {{ loading ? 'Creating account...' : 'Create Account' }}
            </button>
          </form>

          <p class="text-center text-sm text-gray-500 mt-6">
            Already have an account?
            <router-link to="/login" class="text-red-600 font-medium hover:underline">Sign in</router-link>
          </p>
        </div>
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
  em_email: '',
  em_phone: '',
  em_address: '',
  em_bio: '',
  password: '',
  confirmPassword: '',
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
      body: JSON.stringify(payload),
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
