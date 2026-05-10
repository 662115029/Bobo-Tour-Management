<template>
  <div class="min-h-screen bg-gray-100">
    <NavBar />

    <div class="max-w-2xl mx-auto p-4 pb-10">
      <h1 class="text-2xl font-bold text-gray-800 mb-6 mt-4">My Profile</h1>

      <!-- Profile Card -->
      <div class="bg-white rounded-2xl shadow p-6 mb-4">
        <div class="flex items-center gap-4 mb-6">
          <div class="w-16 h-16 rounded-full bg-blue-100 flex items-center justify-center text-3xl">
            👤
          </div>
          <div>
            <h2 class="text-xl font-semibold text-gray-800">{{ form.em_name || 'Your Name' }}</h2>
            <p class="text-sm text-gray-500">{{ form.em_email }}</p>
          </div>
        </div>

        <div v-if="saveSuccess" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
          ✅ Profile updated successfully!
        </div>
        <div v-if="saveError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {{ saveError }}
        </div>

        <h3 class="text-sm font-semibold text-blue-600 border-b pb-2 mb-4">Account Information</h3>
        <form @submit.prevent="saveProfile" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Full Name *</label>
              <input
                v-model="form.em_name"
                type="text"
                required
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
              <input
                v-model="form.em_company"
                type="text"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
              <input
                v-model="form.em_phone"
                type="tel"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="08x xxx xxxx"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
              <input
                v-model="form.em_email"
                type="email"
                required
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
          </div>

          <div class="flex justify-end pt-2">
            <button
              type="submit"
              :disabled="saving"
              class="px-6 py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-50"
            >
              {{ saving ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>

      <!-- Change Password Card -->
      <div class="bg-white rounded-2xl shadow p-6">
        <h3 class="text-sm font-semibold text-blue-600 border-b pb-2 mb-4">Change Password</h3>

        <div v-if="pwSuccess" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
          ✅ Password changed successfully!
        </div>
        <div v-if="pwError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
          {{ pwError }}
        </div>

        <form @submit.prevent="changePassword" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
            <input
              v-model="pwForm.current"
              type="password"
              required
              class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input
                v-model="pwForm.newPw"
                type="password"
                required
                minlength="6"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
              <input
                v-model="pwForm.confirm"
                type="password"
                required
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
              />
            </div>
          </div>
          <div class="flex justify-end pt-2">
            <button
              type="submit"
              :disabled="changingPw"
              class="px-6 py-2 bg-gray-700 text-white font-semibold rounded-lg hover:bg-gray-800 transition disabled:opacity-50"
            >
              {{ changingPw ? 'Updating...' : 'Update Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'

const API_BASE = '/api'

const form = reactive({ em_name: '', em_company: '', em_phone: '', em_email: '' })
const pwForm = reactive({ current: '', newPw: '', confirm: '' })
const saving = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')
const changingPw = ref(false)
const pwSuccess = ref(false)
const pwError = ref('')

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  try {
    const res = await fetch(`${API_BASE}/employers/${em_id}`)
    const data = await res.json()
    if (res.ok) {
      form.em_name = data.em_name || ''
      form.em_company = data.em_company || ''
      form.em_phone = data.em_phone || ''
      form.em_email = data.em_email || ''
    }
  } catch (e) {
    // fallback to localStorage
    form.em_name = localStorage.getItem('em_name') || ''
    form.em_email = localStorage.getItem('em_email') || ''
  }
})

const saveProfile = async () => {
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    if (res.ok) {
      localStorage.setItem('em_name', form.em_name)
      localStorage.setItem('em_email', form.em_email)
      saveSuccess.value = true
      setTimeout(() => saveSuccess.value = false, 3000)
    } else {
      const data = await res.json()
      saveError.value = data.message || 'Failed to save.'
    }
  } catch (e) {
    saveError.value = 'Unable to connect.'
  } finally {
    saving.value = false
  }
}

const changePassword = async () => {
  pwError.value = ''
  pwSuccess.value = false
  if (pwForm.newPw !== pwForm.confirm) {
    pwError.value = 'New passwords do not match.'
    return
  }
  changingPw.value = true
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}/password`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ current_password: pwForm.current, new_password: pwForm.newPw })
    })
    if (res.ok) {
      pwSuccess.value = true
      pwForm.current = ''
      pwForm.newPw = ''
      pwForm.confirm = ''
      setTimeout(() => pwSuccess.value = false, 3000)
    } else {
      const data = await res.json()
      pwError.value = data.message || 'Failed to change password.'
    }
  } catch (e) {
    pwError.value = 'Unable to connect.'
  } finally {
    changingPw.value = false
  }
}
</script>
