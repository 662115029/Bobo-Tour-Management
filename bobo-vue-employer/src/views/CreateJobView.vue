<template>
  <div class="max-w-4xl mx-auto p-4 pb-20">
    <h1 class="text-2xl font-bold text-center mb-6 text-gray-800">Create New Job</h1>

    <form @submit.prevent="submitJob">
      <!-- Section 1: Job Core Info -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">1. General Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-sm font-medium mb-1">Tour Title *</label>
            <input v-model="form.job_title" type="text" required class="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500" placeholder="Tour Title">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Start Date *</label>
            <input v-model="form.job_start_date" type="date" required class="w-full p-2 border rounded">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">End Date *</label>
            <input v-model="form.job_end_date" type="date" required class="w-full p-2 border rounded">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Number of Seats Required *</label>
            <input v-model.number="form.job_required_seat" type="number" min="1" max="13" required class="w-full p-2 border rounded" placeholder="9-13">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Rate (THB) *</label>
            <input v-model.number="form.job_price" type="number" required class="w-full p-2 border rounded" placeholder="0.00">
          </div>
          <div class="col-span-2">
            <label class="block text-sm font-medium mb-2">Language Required </label>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="lang in languages" 
                :key="lang.value"
                type="button"
                @click="toggleLanguage(lang.value)"
                :class="[
                  'px-4 py-1.5 rounded-full text-sm font-medium transition-colors border',
                  form.job_required_languages.includes(lang.value)
                    ? 'bg-teal-500 text-white border-teal-500'
                    : 'bg-white text-gray-600 border-gray-300 hover:border-teal-300'
                ]"
              >
                {{ lang.label }}
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Section 2: Driver & Guide -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">2. Driver & Guide</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-1">Driver</label>
            <input v-model="form.driver_name" type="text" class="w-full p-2 border rounded" placeholder="ชื่อคนขับ">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">Phone Number</label>
            <input v-model="form.driver_phone" type="tel" class="w-full p-2 border rounded" placeholder="08x xxx xxxx">
          </div>
          <div>
            <label class="block text-sm font-medium mb-1">ประเภทรถ *</label>
            <select v-model="form.job_required_vehicle_type" required class="w-full p-2 border rounded">
              <option value="VAN">รถตู้</option>
              <option value="CAR">รถเก๋ง</option>
            </select>
          </div>
        </div>
      </section>

      <!-- Section 3: Tour Schedule -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">3. Tour Schedule</h2>
        <div v-for="(item, idx) in form.job_itineraries" :key="idx" class="grid grid-cols-1 md:grid-cols-5 gap-2 mb-2 items-end">
          <div>
            <label class="block text-xs text-gray-500">Start time</label>
            <input v-model="item.start_time" type="time" class="w-full p-2 border rounded text-sm">
          </div>
          <div>
            <label class="block text-xs text-gray-500">End time</label>
            <input v-model="item.end_time" type="time" class="w-full p-2 border rounded text-sm">
          </div>
          <div class="md:col-span-2">
            <label class="block text-xs text-gray-500">Stop / Activity</label>
            <input v-model="item.place_name" type="text" class="w-full p-2 border rounded text-sm" placeholder="Stop / Activity">
          </div>
          <button type="button" @click="removeItinerary(idx)" class="p-2 bg-red-100 text-red-600 rounded hover:bg-red-200">Delete</button>
        </div>
        <button type="button" @click="addItinerary" class="mt-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">+ Add stop</button>
      </section>

      <!-- Section 4: Pickup Points -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">4. Pickup Points</h2>
        <div v-for="(pickup, idx) in form.job_pickups" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-2 items-end">
          <div>
            <label class="block text-xs text-gray-500">Hotel Name</label>
            <input v-model="pickup.hotel_name" type="text" class="w-full p-2 border rounded text-sm" placeholder="Hotel Name">
          </div>
          <div>
            <label class="block text-xs text-gray-500">ชื่อกลุ่ม / ลูกค้า</label>
            <input v-model="pickup.pickup_location" type="text" class="w-full p-2 border rounded text-sm" placeholder="ชื่อกลุ่ม / ลูกค้า">
          </div>
          <div>
            <label class="block text-xs text-gray-500">Pickup Time</label>
            <input v-model="pickup.pickup_time" type="time" class="w-full p-2 border rounded text-sm">
          </div>
          <button type="button" @click="removePickup(idx)" class="p-2 bg-red-100 text-red-600 rounded hover:bg-red-200">Delete</button>
        </div>
        <button type="button" @click="addPickup" class="mt-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">+ Add Pickup Point</button>
      </section>

      <!-- Section 5: Passenger List -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">5. Passenger List</h2>
        <div v-for="(customer, idx) in form.job_customers" :key="idx" class="flex gap-2 mb-2 items-end">
          <div class="flex-1">
            <label class="block text-xs text-gray-500">Passenger Name</label>
            <input v-model="customer.customer_name" type="text" class="w-full p-2 border rounded text-sm" placeholder="Name - Surname">
          </div>
          <button type="button" @click="removeCustomer(idx)" class="p-2 bg-red-100 text-red-600 rounded hover:bg-red-200">Delete</button>
        </div>
        <div class="mt-3 flex justify-between items-center border-t pt-3">
          <button type="button" @click="addCustomer" class="px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">+ Add Passenger</button>
          <div class="text-sm font-medium">
            Total: <span class="text-lg font-bold text-blue-600">{{ form.job_customers.length }} passenger(s)</span>
          </div>
        </div>
      </section>

      <!-- Section 6: Inclusions/Exclusions -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">6. Inclusions / Exclusions</h2>
        <div v-for="(inc, idx) in form.job_inclusions" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-2 items-end">
          <div>
            <label class="block text-xs text-gray-500">Type</label>
            <select v-model="inc.inclusion_type" class="w-full p-2 border rounded text-sm">
              <option value="INCLUSION">Included</option>
              <option value="EXCLUSION">Not Included</option>
            </select>
          </div>
          <div class="md:col-span-2">
            <label class="block text-xs text-gray-500">Details</label>
            <input v-model="inc.description" type="text" class="w-full p-2 border rounded text-sm" placeholder="Details">
          </div>
          <button type="button" @click="removeInclusion(idx)" class="p-2 bg-red-100 text-red-600 rounded hover:bg-red-200">Delete</button>
        </div>
        <button type="button" @click="addInclusion" class="mt-2 mr-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">+ Add</button>
      </section>

      <!-- Section 7: Entrance Fees -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">7. Entrance Fees</h2>
        <div v-for="(fee, idx) in form.job_entrance_fees" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-2 items-end">
          <div>
            <label class="block text-xs text-gray-500">Attraction</label>
            <input v-model="fee.place_name" type="text" class="w-full p-2 border rounded text-sm" placeholder="Attraction">
          </div>
          <div>
            <label class="block text-xs text-gray-500">Thai (THB)</label>
            <input v-model.number="fee.thai_price" type="number" class="w-full p-2 border rounded text-sm">
          </div>
          <div>
            <label class="block text-xs text-gray-500">Foreigner (THB)</label>
            <input v-model.number="fee.foreigner_price" type="number" class="w-full p-2 border rounded text-sm">
          </div>
          <button type="button" @click="removeEntranceFee(idx)" class="p-2 bg-red-100 text-red-600 rounded hover:bg-red-200">Delete</button>
        </div>
        <button type="button" @click="addEntranceFee" class="mt-2 px-4 py-2 bg-green-100 text-green-700 rounded hover:bg-green-200">+ Add Entrance Fees</button>
      </section>

      <!-- Section 8: Remarks -->
      <section class="bg-white rounded-lg shadow p-4 mb-4">
        <h2 class="text-lg font-semibold mb-3 text-blue-600 border-b pb-2">8. Remarks</h2>
        <textarea v-model="form.note" rows="4" class="w-full p-2 border rounded" placeholder="หมายเหตุเพิ่มเติม..."></textarea>
      </section>

      <!-- Submit Button -->
      <div class="fixed bottom-0 left-0 right-0 bg-white border-t p-4 shadow-lg">
        <div class="max-w-4xl mx-auto flex justify-between items-center">
          <button type="button" @click="$router.back()" class="px-6 py-2 border rounded hover:bg-gray-100">cancel</button>
          <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold">Create job</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'

const API_BASE = '/api'

const languages = [
  { value: 'English', label: 'English' },
  { value: 'Thai', label: 'Thai' },
  { value: 'Mandarin', label: 'Mandarin' },
  { value: 'Korean', label: 'Korean' },
  { value: 'Japanese', label: 'Japanese' },
  { value: 'French', label: 'French' },
  { value: 'German', label: 'German' }
]

const toggleLanguage = (lang) => {
  const idx = form.job_required_languages.indexOf(lang)
  if (idx > -1) {
    form.job_required_languages.splice(idx, 1)
  } else {
    form.job_required_languages.push(lang)
  }
}

const form = reactive({
  job_title: '',
  job_description: '',
  job_start_date: '',
  job_end_date: '',
  job_required_vehicle_type: 'VAN',
  job_required_seat: 9,
  job_required_languages: [],
  driver_name: '',
  driver_phone: '',
  note: '',
  job_itineraries: [],
  job_pickups: [],
  job_customers: [],
  job_inclusions: [],
  job_entrance_fees: []
})

const addItinerary = () => form.job_itineraries.push({ place_name: '', start_time: '', end_time: '', note: '' })
const removeItinerary = (idx) => form.job_itineraries.splice(idx, 1)
const addPickup = () => form.job_pickups.push({ hotel_name: '', pickup_location: '', pickup_time: '', sequence: form.job_pickups.length + 1 })
const removePickup = (idx) => form.job_pickups.splice(idx, 1)
const addCustomer = () => form.job_customers.push({ customer_name: '', note: '' })
const removeCustomer = (idx) => form.job_customers.splice(idx, 1)
const addInclusion = () => form.job_inclusions.push({ inclusion_type: 'INCLUSION', description: '', sequence: form.job_inclusions.length + 1 })
const removeInclusion = (idx) => form.job_inclusions.splice(idx, 1)
const addEntranceFee = () => form.job_entrance_fees.push({ place_name: '', thai_price: 0, foreigner_price: 0, sequence: form.job_entrance_fees.length + 1 })
const removeEntranceFee = (idx) => form.job_entrance_fees.splice(idx, 1)

const generateId = (prefix) => prefix + Date.now().toString(36).toUpperCase()

const submitJob = async () => {
  try {
    const job_id = generateId('JOB')
    const payload = {
      job_id,
      em_id: localStorage.getItem('em_id') || 'EM001',
      ...form
    }

    const res = await fetch(`${API_BASE}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })

    if (res.ok) {
      alert('สร้างงานสำเร็จ!')
      location.reload()
    } else {
      const err = await res.json()
      alert('เกิดข้อผิดพลาด: ' + (err.error || err.message || 'unknown'))
    }
  } catch (e) {
    alert('เกิดข้อผิดพลาด: ' + e.message)
  }
}
</script>

<style scoped>
input, select, textarea { font-family: 'Kanit', sans-serif; }
</style>