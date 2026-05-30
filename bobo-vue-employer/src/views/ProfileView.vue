<template>
  <AppLayout>
    <div class="flex gap-8 px-8 pt-6 pb-10 min-h-screen items-start">

      <!-- Left panel: back button -->
      <aside class="hidden lg:flex flex-col w-52 shrink-0 sticky top-20">
        <button
          type="button"
          @click="$router.back()"
          class="flex items-center gap-1.5 text-sm font-medium text-gray-600 bg-white hover:bg-[#ffd8d8] hover:text-[#dc2626] px-4 py-2 rounded-full transition w-fit"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
      </aside>

      <!-- Main content -->
      <div class="flex-1 min-w-0 max-w-2xl pb-10">
        <h1 class="text-2xl font-bold text-gray-800 mb-6 mt-4">My Profile</h1>

        <!-- Profile Card -->
        <div class="bg-white rounded-2xl shadow-md p-6 mb-4">
          <div class="flex items-center gap-4 mb-6">
            <!-- Profile picture -->
            <div class="w-16 h-16 rounded-full bg-gray-200 overflow-hidden flex items-center justify-center shrink-0">
              <img
                v-if="form.em_profile_url"
                :src="form.em_profile_url"
                alt="Profile picture"
                class="w-full h-full object-cover"
                @error="form.em_profile_url = ''"
              />
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                class="w-8 h-8 text-gray-500"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-semibold text-gray-800">
                {{ form.em_name || "Your Name" }}
              </h2>
              <p class="text-sm text-gray-400">@{{ form.em_username }}</p>
              <div class="flex items-center gap-2 mt-1">
                <span
                  class="text-xs font-semibold px-2 py-0.5 rounded-full"
                  :class="form.em_verify_status === 'VERIFIED' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'"
                >{{ form.em_verify_status || "PENDING" }}</span>
                <span class="text-xs text-gray-500" v-if="form.em_rating_avg > 0">★ {{ form.em_rating_avg }}</span>
              </div>
            </div>
          </div>

          <div v-if="saveSuccess" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
            Profile updated successfully!
          </div>
          <div v-if="saveError" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {{ saveError }}
          </div>

          <h3 class="text-sm font-semibold text-gray-500 border-b pb-2 mb-4 uppercase tracking-wide">
            Account Information
          </h3>

          <!-- Timestamps -->
          <div class="flex gap-6 mb-4 text-xs text-gray-400">
            <span>Created: <span class="text-gray-500 font-medium">{{ formatDate(form.em_created_at) }}</span></span>
            <span>Last Updated: <span class="text-gray-500 font-medium">{{ formatDate(form.em_updated_at) }}</span></span>
          </div>

          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

              <!-- Username -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Username</label>
                  <span v-if="isEditing" class="text-xs text-red-500 font-medium">Username cannot be changed</span>
                </div>
                <input
                  v-model="form.em_username"
                  type="text"
                  disabled
                  class="w-full p-2 border border-gray-200 rounded-lg bg-gray-50 text-gray-400 cursor-not-allowed"
                />
              </div>

              <!-- Full Name -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Full Name</label>
                  <span v-if="isEditing && touched.em_name && !form.em_name" class="text-xs text-red-500 font-medium">* Required</span>
                </div>
                <input
                  v-model="form.em_name"
                  type="text"
                  :disabled="!isEditing"
                  @input="touched.em_name = true"
                  :class="isEditing ? 'border-gray-300 focus:ring-2 focus:ring-red-400 bg-white' : 'border-gray-200 bg-gray-50 text-gray-600 cursor-default'"
                  class="w-full p-2 border rounded-lg focus:outline-none transition"
                />
              </div>

              <!-- Phone -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Phone Number</label>
                  <span v-if="isEditing && touched.em_phone && !form.em_phone" class="text-xs text-red-500 font-medium">* Required</span>
                </div>
                <input
                  v-model="form.em_phone"
                  type="tel"
                  :disabled="!isEditing"
                  placeholder="08x xxx xxxx"
                  @input="touched.em_phone = true"
                  :class="isEditing ? 'border-gray-300 focus:ring-2 focus:ring-red-400 bg-white' : 'border-gray-200 bg-gray-50 text-gray-600 cursor-default'"
                  class="w-full p-2 border rounded-lg focus:outline-none transition"
                />
              </div>

              <!-- Email -->
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Email</label>
                  <span v-if="isEditing && touched.em_email && !form.em_email" class="text-xs text-red-500 font-medium">* Required</span>
                </div>
                <input
                  v-model="form.em_email"
                  type="email"
                  :disabled="!isEditing"
                  @input="touched.em_email = true"
                  :class="isEditing ? 'border-gray-300 focus:ring-2 focus:ring-red-400 bg-white' : 'border-gray-200 bg-gray-50 text-gray-600 cursor-default'"
                  class="w-full p-2 border rounded-lg focus:outline-none transition"
                />
              </div>

              <!-- Address -->
              <div class="md:col-span-2">
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Address</label>
                  <span v-if="isEditing && touched.em_address && !form.em_address" class="text-xs text-red-500 font-medium">* Required</span>
                </div>
                <input
                  v-model="form.em_address"
                  type="text"
                  :disabled="!isEditing"
                  placeholder="e.g. Chiang Mai, Thailand"
                  @input="touched.em_address = true"
                  :class="isEditing ? 'border-gray-300 focus:ring-2 focus:ring-red-400 bg-white' : 'border-gray-200 bg-gray-50 text-gray-600 cursor-default'"
                  class="w-full p-2 border rounded-lg focus:outline-none transition"
                />
              </div>

              <!-- Bio -->
              <div class="md:col-span-2">
                <div class="flex items-center gap-2 mb-1">
                  <label class="block text-sm font-medium text-gray-700">Bio</label>
                  <span v-if="isEditing" class="text-gray-400 font-normal text-xs">(optional)</span>
                </div>
                <textarea
                  v-model="form.em_bio"
                  rows="3"
                  :disabled="!isEditing"
                  placeholder="Brief description of your tour company..."
                  :class="isEditing ? 'border-gray-300 focus:ring-2 focus:ring-red-400 bg-white' : 'border-gray-200 bg-gray-50 text-gray-600 cursor-default'"
                  class="w-full p-2 border rounded-lg focus:outline-none transition resize-none"
                ></textarea>
              </div>
            </div>

            <div class="flex justify-end gap-2 pt-2">
              <!-- View mode: Edit button -->
              <button
                v-if="!isEditing"
                type="button"
                @click="startEditing"
                class="px-6 py-2 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 transition"
              >
                Edit
              </button>
              <!-- Edit mode: Cancel + Save -->
              <template v-else>
                <button
                  type="button"
                  @click="cancelEditing"
                  class="px-6 py-2 border border-gray-300 text-gray-600 font-medium rounded-lg hover:bg-gray-50 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="saving"
                  class="px-6 py-2 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50"
                >
                  {{ saving ? "Saving..." : "Save Changes" }}
                </button>
              </template>
            </div>
          </form>
        </div>

        <!-- Verification Documents -->
        <div class="bg-white rounded-2xl shadow-md p-6 mb-4">
          <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide border-b border-gray-100 pb-2 mb-4 flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>
            </svg>
            Verification Documents
          </h2>

          <div v-if="docsLoading" class="text-sm text-gray-400 py-4 text-center">Loading documents...</div>
          <div v-else-if="documents.length === 0" class="text-sm text-gray-400 py-4 text-center italic">No documents uploaded.</div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div
              v-for="doc in documents"
              :key="doc.em_doc_id"
              class="border border-gray-200 rounded-xl overflow-hidden"
            >
              <div class="flex items-center justify-between px-3 py-2 bg-gray-50 border-b border-gray-100">
                <p class="text-xs font-semibold text-gray-600">{{ formatDocType(doc.em_doc_type) }}</p>
                <span
                  class="text-[10px] font-bold px-2 py-0.5 rounded-full"
                  :class="{
                    'bg-green-100 text-green-700': doc.em_doc_status === 'APPROVED',
                    'bg-yellow-100 text-yellow-700': doc.em_doc_status === 'PENDING',
                    'bg-red-100 text-red-600': doc.em_doc_status === 'REJECTED',
                  }"
                >{{ doc.em_doc_status }}</span>
              </div>
              <a :href="doc.file_url" target="_blank" class="block group">
                <div class="h-40 bg-gray-100 flex items-center justify-center overflow-hidden">
                  <img
                    v-if="isImage(doc.file_url)"
                    :src="doc.file_url"
                    :alt="doc.em_doc_type"
                    class="w-full h-full object-cover group-hover:opacity-90 transition"
                    @error="e => e.target.style.display='none'"
                  />
                  <div v-else class="flex flex-col items-center gap-2 text-gray-400 group-hover:text-[#dc2626] transition">
                    <svg class="w-10 h-10" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"/>
                    </svg>
                    <span class="text-xs font-medium">Tap to view</span>
                  </div>
                </div>
              </a>
              <div class="px-3 py-2 text-[10px] text-gray-400">
                Uploaded {{ formatDate(doc.em_uploaded_at) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Change Password Card -->
        <div class="bg-white rounded-2xl shadow-md p-6 mb-4">
          <h3 class="text-sm font-semibold text-gray-500 border-b pb-2 mb-4 uppercase tracking-wide">
            Security
          </h3>

          <!-- Step 0: just a button -->
          <div v-if="pwStep === 0">
            <button
              @click="pwStep = 1"
              class="px-5 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition"
            >
              Change Password
            </button>
          </div>

          <!-- Step 1: verify current password -->
          <div v-else-if="pwStep === 1" class="space-y-3">
            <div v-if="pwError" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
              {{ pwError }}
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Current Password</label>
              <input
                v-model="pwForm.current"
                type="password"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400 transition"
                placeholder="Enter your current password"
                @keyup.enter="verifyCurrentPassword"
              />
            </div>
            <div class="flex items-center justify-between pt-1">
              <button type="button" @click="resetPw" class="text-xs text-gray-400 hover:text-gray-600">Cancel</button>
              <div class="flex items-center gap-3">
                <button type="button" @click="forgotPassword" class="text-xs text-red-500 hover:underline">Forgot password?</button>
                <button
                  type="button"
                  @click="verifyCurrentPassword"
                  :disabled="!pwForm.current || verifying"
                  class="px-4 py-2 bg-gray-700 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition disabled:opacity-50"
                >
                  {{ verifying ? "Verifying..." : "Continue" }}
                </button>
              </div>
            </div>
          </div>

          <!-- Step 2: set new password -->
          <div v-else-if="pwStep === 2" class="space-y-3">
            <div v-if="pwSuccess" class="p-3 bg-green-50 border border-green-200 rounded-lg text-green-600 text-sm">
              Password changed successfully!
            </div>
            <div v-if="pwError" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
              {{ pwError }}
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">New Password</label>
              <input
                v-model="pwForm.newPw"
                type="password"
                minlength="6"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400 transition"
                placeholder="At least 6 characters"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Confirm New Password</label>
              <input
                v-model="pwForm.confirm"
                type="password"
                class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400 transition"
                placeholder="Re-enter new password"
              />
            </div>
            <div class="flex items-center justify-between pt-1">
              <button type="button" @click="resetPw" class="text-xs text-gray-400 hover:text-gray-600">Cancel</button>
              <button
                type="button"
                @click="changePassword"
                :disabled="changingPw || !pwForm.newPw || !pwForm.confirm"
                class="px-4 py-2 bg-red-600 text-white text-sm font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50"
              >
                {{ changingPw ? "Updating..." : "Update Password" }}
              </button>
            </div>
          </div>
        </div>

        <!-- Logout -->
        <div class="bg-white rounded-2xl shadow-md p-6">
          <h3 class="text-sm font-semibold text-gray-500 border-b pb-2 mb-4 uppercase tracking-wide">
            Session
          </h3>
          <p class="text-sm text-gray-500 mb-4">
            You are currently signed in. Logging out will end your session.
          </p>
          <button
            @click="logout"
            class="w-full py-2.5 border-2 border-red-500 text-red-600 font-semibold rounded-lg hover:bg-red-50 transition"
          >
            Log Out
          </button>
        </div>
      </div>

      <!-- Right spacer to balance aside -->
      <div class="hidden lg:block w-52 shrink-0"></div>

    </div>
  </AppLayout>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'

const documents = ref([])
const docsLoading = ref(false)
const router = useRouter()

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  })
}

const form = reactive({
  em_username: '',
  em_name: '',
  em_phone: '',
  em_email: '',
  em_address: '',
  em_bio: '',
  em_verify_status: '',
  em_rating_avg: 0,
  em_created_at: '',
  em_updated_at: '',
  em_profile_url: '',
})

// Tracks whether the user has cleared a required field after entering edit mode
const touched = reactive({
  em_name: false,
  em_phone: false,
  em_email: false,
  em_address: false,
})

const resetTouched = () => {
  touched.em_name = false
  touched.em_phone = false
  touched.em_email = false
  touched.em_address = false
}

const pwForm = reactive({ current: '', newPw: '', confirm: '' })
const saving = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')
const isEditing = ref(false)
let snapshot = {}

const startEditing = () => {
  snapshot = { ...form }
  resetTouched()
  isEditing.value = true
}

const cancelEditing = () => {
  Object.assign(form, snapshot)
  isEditing.value = false
  saveError.value = ''
  resetTouched()
}

// On submit: mark all required fields as touched so * Required appears if empty
const handleSubmit = () => {
  touched.em_name = true
  touched.em_phone = true
  touched.em_email = true
  touched.em_address = true

  if (!form.em_name || !form.em_phone || !form.em_email || !form.em_address) return

  saveProfile()
}

const pwStep = ref(0)
const verifying = ref(false)
const changingPw = ref(false)
const pwSuccess = ref(false)
const pwError = ref('')

const resetPw = () => {
  pwStep.value = 0
  pwError.value = ''
  pwSuccess.value = false
  pwForm.current = ''
  pwForm.newPw = ''
  pwForm.confirm = ''
}

const forgotPassword = () => {}

const verifyCurrentPassword = async () => {
  if (!pwForm.current) return
  pwError.value = ''
  verifying.value = true
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}/verify-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ current_password: pwForm.current }),
    })
    if (res.ok) {
      pwStep.value = 2
    } else {
      const data = await res.json()
      pwError.value = data.message || 'Incorrect password. Please try again.'
    }
  } catch (e) {
    pwError.value = 'Unable to connect. Please try again.'
  } finally {
    verifying.value = false
  }
}

const changePassword = async () => {
  pwError.value = ''
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
      body: JSON.stringify({ current_password: pwForm.current, new_password: pwForm.newPw }),
    })
    if (res.ok) {
      pwSuccess.value = true
      setTimeout(() => resetPw(), 2000)
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

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')

  // Fetch documents
  docsLoading.value = true
  try {
    const docRes = await fetch(`${API_BASE}/em-documents?em_id=${em_id}`)
    if (docRes.ok) {
      const docData = await docRes.json()
      documents.value = Array.isArray(docData) ? docData : (docData.items || docData.documents || [])
    }
  } catch (e) {
    documents.value = []
  } finally {
    docsLoading.value = false
  }

  // Fetch profile
  try {
    const res = await fetch(`${API_BASE}/employers/${em_id}`)
    const data = await res.json()
    if (res.ok) {
      form.em_username      = data.em_username      || ''
      form.em_name          = data.em_name          || ''
      form.em_phone         = data.em_phone         || ''
      form.em_email         = data.em_email         || ''
      form.em_address       = data.em_address       || ''
      form.em_bio           = data.em_bio           || ''
      form.em_verify_status = data.em_verify_status || ''
      form.em_rating_avg    = data.em_rating_avg    || 0
      form.em_created_at    = data.em_created_at    || ''
      form.em_updated_at    = data.em_updated_at    || ''
      form.em_profile_url   = data.em_profile_image_url || data.em_profile_url || ''
    }
  } catch (e) {
    form.em_name     = localStorage.getItem('em_name')     || ''
    form.em_email    = localStorage.getItem('em_email')    || ''
    form.em_username = localStorage.getItem('em_username') || ''
  }
})

const logout = () => {
  localStorage.removeItem('em_id')
  localStorage.removeItem('em_name')
  localStorage.removeItem('em_email')
  router.push('/login')
}

const saveProfile = async () => {
  saving.value = true
  saveError.value = ''
  saveSuccess.value = false
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    if (res.ok) {
      localStorage.setItem('em_name', form.em_name)
      localStorage.setItem('em_email', form.em_email)
      form.em_updated_at = new Date().toISOString().replace('T', ' ').substring(0, 19)
      isEditing.value = false
      resetTouched()
      saveSuccess.value = true
      setTimeout(() => (saveSuccess.value = false), 3000)
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

const formatDocType = (type) => {
  const map = {
    COMPANY_REGISTRATION: 'Company Registration',
    BUSINESS_LICENSE: 'Business License',
    TOURISM_LICENSE: 'Tourism License',
    TAX_ID_DOCUMENT: 'Tax ID Document',
    AUTHORIZED_PERSON_ID: 'Authorized Person ID',
  }
  return map[type] || type
}

const isImage = (url) => /\.(jpg|jpeg|png|gif|webp)(\?|$)/i.test(url || '')
</script>
