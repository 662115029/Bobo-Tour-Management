<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 font-sans overflow-hidden">

    <!-- Header -->
    <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100">
      <button class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center" @click="$router.push('/')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
      </button>
      <div>
        <p class="text-xs font-semibold text-red-600 uppercase tracking-wider">Freelancer</p>
        <h2 class="text-lg font-bold text-gray-900 leading-tight">
          {{ step === 'pin' ? 'Set PIN' : step === 'confirm' ? 'Confirm PIN' : 'Register' }}
        </h2>
      </div>
    </div>

    <!-- Step: Info form -->
    <div v-if="step === 'info'" class="flex-1 overflow-y-auto p-4 space-y-4">

      <div class="bg-blue-50 border-l-4 border-blue-400 rounded-lg px-3 py-2.5 text-xs text-blue-700">
        Fill in basic information - vehicle details and documents can be added later in Profile
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Firstname</label>
        <input v-model="form.firstName" type="text" placeholder="e.g. Somchai"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
          :class="errors.firstName ? 'border-red-400' : ''" />
        <p v-if="errors.firstName" class="text-xs text-red-500">{{ errors.firstName }}</p>
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Surname</label>
        <input v-model="form.lastName" type="text" placeholder="e.g. Jaidee"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
          :class="errors.lastName ? 'border-red-400' : ''" />
        <p v-if="errors.lastName" class="text-xs text-red-500">{{ errors.lastName }}</p>
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Username</label>
        <input v-model="form.username" type="text" placeholder="e.g. somchai99"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
          :class="errors.username ? 'border-red-400' : ''" />
        <p v-if="errors.username" class="text-xs text-red-500">{{ errors.username }}</p>
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Email</label>
        <input v-model="form.email" type="email" placeholder="e.g. somchai@email.com"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
          :class="errors.email ? 'border-red-400' : ''" />
        <p v-if="errors.email" class="text-xs text-red-500">{{ errors.email }}</p>
      </div>

      <div class="space-y-1">
        <label class="text-xs font-semibold text-gray-500 uppercase tracking-wide">Phone number</label>
        <input v-model="form.phone" type="tel" placeholder="e.g. 0812345678"
          class="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm bg-white focus:outline-none focus:border-red-400"
          :class="errors.phone ? 'border-red-400' : ''" />
        <p v-if="errors.phone" class="text-xs text-red-500">{{ errors.phone }}</p>
      </div>

    </div>

    <!-- Step: Set PIN -->
    <div v-else-if="step === 'pin'" class="flex-1 flex flex-col items-center justify-center p-4">
      <PinPad
        ref="pinPadRef"
        title="Set your 6-digit PIN"
        :error="errors.pin"
        @complete="handleSetPin"
      />
    </div>

    <!-- Step: Confirm PIN -->
    <div v-else-if="step === 'confirm'" class="flex-1 flex flex-col items-center justify-center p-4">
      <PinPad
        ref="confirmPadRef"
        title="Confirm your PIN"
        :error="errors.pinConfirm"
        @complete="handleConfirmPin"
      />
    </div>

    <!-- API error -->
    <p v-if="apiError" class="text-xs text-red-500 bg-red-50 px-4 py-2 mx-4 rounded-lg">{{ apiError }}</p>

    <!-- Footer -->
    <div class="px-4 py-3 bg-white border-t border-gray-100">
      <button
        v-if="step === 'info'"
        class="w-full bg-red-600 text-white text-sm font-bold py-3.5 rounded-xl disabled:opacity-60 transition-opacity"
        @click="handleNext"
      >
        Next
      </button>
      <button
        v-if="step === 'pin' || step === 'confirm'"
        class="text-sm text-gray-400 underline w-full text-center"
        @click="step = 'info'"
      >
        Back
      </button>
    </div>

    <!-- Success overlay -->
    <div v-if="submitted" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-6">
      <div class="bg-white rounded-2xl p-8 text-center max-w-xs w-full">
        <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#16a34a" stroke-width="2.5">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 mb-2">Registration Successful!</h3>
        <p class="text-sm text-gray-500 mb-2 leading-relaxed">Please add vehicle details and upload documents in Profile for Admin review.</p>
        <p class="text-xs text-gray-400 mb-6">We'll notify you via LINE once approved.</p>
        <button class="w-full bg-red-600 text-white font-bold py-3 rounded-xl" @click="$router.push('/')">
          Back to Home
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import PinPad from './PinPad.vue'

const props = defineProps({ user: Object })

const step = ref('info') // info | pin | confirm
const submitting = ref(false)
const submitted = ref(false)
const apiError = ref('')

const pinPadRef = ref(null)
const confirmPadRef = ref(null)

const form = reactive({
  firstName: '',
  lastName: '',
  username: '',
  email: '',
  phone: '',
  pin: '',
})

const errors = reactive({
  firstName: '', lastName: '', username: '',
  email: '', phone: '', pin: '', pinConfirm: '',
})

function validateInfo() {
  let valid = true
  Object.keys(errors).forEach(k => errors[k] = '')
  if (!form.firstName.trim()) { errors.firstName = 'Required'; valid = false }
  if (!form.lastName.trim())  { errors.lastName  = 'Required'; valid = false }
  if (!form.username.trim())  { errors.username  = 'Required'; valid = false }
  if (!form.email.trim())     { errors.email     = 'Required'; valid = false }
  else if (!/\S+@\S+\.\S+/.test(form.email)) { errors.email = 'Invalid email'; valid = false }
  if (!form.phone.trim())     { errors.phone     = 'Required'; valid = false }
  return valid
}

function handleNext() {
  if (validateInfo()) step.value = 'pin'
}

function handleSetPin(pin) {
  form.pin = pin
  step.value = 'confirm'
  nextTick(() => confirmPadRef.value?.reset())
}

function handleConfirmPin(confirmPin) {
  if (confirmPin !== form.pin) {
    errors.pinConfirm = 'PINs do not match. Try again.'
    nextTick(() => confirmPadRef.value?.reset())
    return
  }
  submitRegister()
}

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

async function submitRegister() {
  apiError.value = ''
  submitting.value = true
  try {
    const res = await fetch(`${API_BASE}/freelancers/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({
        fl_username: form.username,
        fl_email: form.email,
        fl_name: `${form.firstName} ${form.lastName}`.trim(),
        fl_phone: form.phone,
        fl_pin: form.pin,
        line_user_id: props.user?.lineUserId || null,
      })
    })
    const data = await res.json()
    if (data.success) {
      submitted.value = true
    } else {
      apiError.value = data.detail || data.error || 'Registration failed'
      step.value = 'info'
    }
  } catch {
    apiError.value = 'Network error. Please try again.'
    step.value = 'info'
  } finally {
    submitting.value = false
  }
}
</script>