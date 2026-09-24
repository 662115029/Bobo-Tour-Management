<template>
  <div class="flex flex-col h-dvh max-w-md mx-auto bg-white font-sans overflow-hidden"
    :style="step === 'info' ? 'background-image: radial-gradient(circle, #d6d9df 1px, transparent 1px); background-size: 24px 24px;' : ''">

    <!-- Header -->
    <div class="relative bg-white border-b border-[#E2E8F0] shrink-0 px-4 py-3">
      <button class="absolute left-4 top-1/2 -translate-y-1/2 w-9 h-9 rounded-full bg-[#F1F5F9] text-[#475569] flex items-center justify-center z-10" @click="closeLiff">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M19 12H5M5 12l7-7M5 12l7 7"/>
        </svg>
      </button>
      <div class="flex flex-col items-center justify-center">
        <p class="text-meta font-semibold text-[#DC2626] uppercase tracking-[0.16em] leading-none">Freelancer</p>
        <h2 class="text-[20px] font-bold text-[#0F172A] leading-none mt-1.5">
          {{ step === 'pin' ? 'Set PIN' : step === 'confirm' ? 'Confirm PIN' : 'Register' }}
        </h2>
      </div>
    </div>

    <!-- Step: Info form -->
    <div v-if="step === 'info'" class="flex-1 min-h-0 flex flex-col gap-3 overflow-hidden px-5 py-3">

      <!-- Mascot: fills leftover space, shrinks on small screens -->
      <div class="flex-1 min-h-0 flex flex-col items-center justify-center gap-2">
        <img src="@/assets/logo copy.png" alt="Bobo Tour" class="h-12 w-auto object-contain shrink-0" />
        <div class="flex-1 min-h-0 w-full flex justify-center">
          <img src="@/assets/mascot_default.png" alt="Bobo Mascot" class="h-full max-h-72 w-auto max-w-full object-contain" />
        </div>
      </div>


      <!-- Form card -->
      <div class="bg-white rounded-2xl border border-[#E2E8F0] shadow-sm p-4 space-y-2.5 shrink-0">

      <!-- Firstname + Surname -->
      <div class="grid grid-cols-2 gap-3">
        <div class="space-y-0.5">
          <label class="block text-caption font-medium text-[#475569]">Firstname</label>
          <input v-model="form.firstName" type="text" placeholder="e.g. Somchai"
            class="w-full border border-[#E2E8F0] rounded-lg px-3 py-2 text-body font-medium text-[#0F172A] bg-[#F8FAFC] placeholder:text-[#94A3B8] placeholder:font-normal focus:bg-white focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/15"
            :class="errors.firstName ? 'border-[#B91C1C]' : ''" />
          <p v-if="errors.firstName" class="text-meta text-[#B91C1C]">{{ errors.firstName }}</p>
        </div>

        <div class="space-y-0.5">
          <label class="block text-caption font-medium text-[#475569]">Surname</label>
          <input v-model="form.lastName" type="text" placeholder="e.g. Jaidee"
            class="w-full border border-[#E2E8F0] rounded-lg px-3 py-2 text-body font-medium text-[#0F172A] bg-[#F8FAFC] placeholder:text-[#94A3B8] placeholder:font-normal focus:bg-white focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/15"
            :class="errors.lastName ? 'border-[#B91C1C]' : ''" />
          <p v-if="errors.lastName" class="text-meta text-[#B91C1C]">{{ errors.lastName }}</p>
        </div>
      </div>

      <div class="space-y-0.5">
        <label class="block text-caption font-medium text-[#475569]">Username</label>
        <input v-model="form.username" type="text" placeholder="e.g. somchai99"
          class="w-full border border-[#E2E8F0] rounded-lg px-3 py-2 text-body font-medium text-[#0F172A] bg-[#F8FAFC] placeholder:text-[#94A3B8] placeholder:font-normal focus:bg-white focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/15"
          :class="errors.username ? 'border-[#B91C1C]' : ''" />
        <p class="text-meta text-[#64748B]">Username cannot be changed.</p>
        <p v-if="errors.username" class="text-meta text-[#B91C1C]">{{ errors.username }}</p>
      </div>

      <div class="space-y-0.5">
        <label class="block text-caption font-medium text-[#475569]">Email</label>
        <input v-model="form.email" type="email" placeholder="e.g. somchai@email.com"
          class="w-full border border-[#E2E8F0] rounded-lg px-3 py-2 text-body font-medium text-[#0F172A] bg-[#F8FAFC] placeholder:text-[#94A3B8] placeholder:font-normal focus:bg-white focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/15"
          :class="errors.email ? 'border-[#B91C1C]' : ''" />
        <p v-if="errors.email" class="text-meta text-[#B91C1C]">{{ errors.email }}</p>
      </div>

      <div class="space-y-0.5">
        <label class="block text-caption font-medium text-[#475569]">Phone number</label>
        <input v-model="form.phone" type="tel" placeholder="e.g. 0812345678"
          class="w-full border border-[#E2E8F0] rounded-lg px-3 py-2 text-body font-medium text-[#0F172A] bg-[#F8FAFC] placeholder:text-[#94A3B8] placeholder:font-normal focus:bg-white focus:outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]/15"
          :class="errors.phone ? 'border-[#B91C1C]' : ''" />
        <p v-if="errors.phone" class="text-meta text-[#B91C1C]">{{ errors.phone }}</p>
      </div>

      <div class="flex items-center gap-2 bg-[#EFF6FF] border border-[#BFDBFE] rounded-xl px-3 py-2 text-[12px] leading-4 text-[#1D4ED8] shrink-0">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="shrink-0"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>
        <span>Fill in basic information - vehicle details and documents can be added later in Profile</span>
      </div>
      </div><!-- end form card -->

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
    <p v-if="apiError" class="text-[12px] text-[#B91C1C] bg-[#FEF2F2] px-4 py-2 mx-5 rounded-lg shrink-0">{{ apiError }}</p>

    <!-- Footer -->
    <div class="px-5 py-4 shrink-0">
      <button
        v-if="step === 'info'"
        class="w-full bg-[#DC2626] hover:bg-[#B91C1C] active:bg-[#B91C1C] text-white text-body font-bold py-3 rounded-xl disabled:opacity-60 transition-colors"
        @click="handleNext"
      >
        Next
      </button>
      <button
        v-if="step === 'pin' || step === 'confirm'"
        class="text-[14px] text-[#64748B] underline w-full text-center"
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
        <h3 class="text-title font-bold text-[#0F172A] mb-2">Registration Successful!</h3>
        <p class="text-body text-[#64748B] mb-2 leading-relaxed">Please add vehicle details and upload documents in Profile for Admin review.</p>
        <p class="text-caption text-[#94A3B8] mb-6">We'll notify you via LINE once approved.</p>
        <button class="w-full bg-[#DC2626] hover:bg-[#B91C1C] text-white font-bold py-3 rounded-xl transition-all active:scale-[0.98]" @click="closeLiff">
          Done
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import PinPad from './PinPad.vue'
import { closeLiff } from '@/liff.js'

const props = defineProps({ user: Object, lineProfile: Object })
const emit = defineEmits(['login'])

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
        line_user_id: props.lineProfile?.lineUserId || null,
      })
    })
    const data = await res.json()
    if (data.success) {
      emit('login', {
        fl_id: data.fl_id,
        fl_username: form.username,
        fl_name: `${form.firstName} ${form.lastName}`.trim(),
        fl_email: form.email,
        fl_profile_image_url: null,
      })
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