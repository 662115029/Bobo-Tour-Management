<template>
  <AppLayout>

    <div class="flex gap-8 px-8 pt-6 pb-10 min-h-screen items-start">

      <!-- ── Left Panel (persistent) ── -->
      <aside class="hidden lg:flex flex-col gap-4 w-80 shrink-0 sticky top-20">

        <!-- Templates block -->
        <div class="bg-white rounded-2xl border border-gray-100 shadow-md p-5">
          <h3 class="text-sm font-semibold text-gray-700 mb-3 flex items-center gap-2">
            <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Templates
          </h3>
          <div class="space-y-2">
            <div
              v-for="tpl in templates" :key="tpl.id"
              class="flex items-center gap-1 rounded-xl border border-gray-200 hover:border-red-300 hover:bg-red-50 transition-colors group"
            >
              <button
                type="button"
                @click="confirmLoadTemplate(tpl)"
                class="flex-1 text-left px-4 py-3 min-w-0"
              >
                <p class="text-sm font-semibold text-gray-700 group-hover:text-red-600 truncate">{{ tpl.name }}</p>
                <p class="text-sm text-gray-400 mt-0.5 truncate">{{ tpl.subtitle }}</p>
              </button>
              <button
                type="button"
                @click.stop="confirmDeleteTemplate(tpl)"
                class="p-2 mr-2 text-gray-300 hover:text-red-500 transition-colors shrink-0"
                title="Delete template"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
            <p v-if="templates.length === 0" class="text-xs text-gray-400 text-center py-3">No templates yet</p>
          </div>
        </div>

      </aside>

      <!-- ── Right: Main Form ── -->
      <div class="flex-1 min-w-0 max-w-3xl mr-16">
        <div class="flex items-center justify-between mb-6 mt-4">
          <h1 class="text-2xl font-bold text-gray-800">Create New Tour</h1>
          <div class="flex items-center gap-2">
            <button
              type="button"
              @click="saveAsTemplate"
              class="flex items-center gap-1.5 text-xs font-medium text-gray-600 bg-white border border-gray-300 hover:border-gray-400 hover:bg-gray-50 px-3 py-1.5 rounded-lg transition"
            >
              <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              Save as Template
            </button>
          </div>
        </div>

        <!-- ── Progress Bar ── -->
        <div class="flex items-center mb-10">
          <template v-for="(s, i) in steps" :key="i">
            <div class="flex flex-col items-center">
              <div
                class="w-9 h-9 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-all"
                :class="
                  currentStep > i + 1
                    ? 'bg-red-600 border-red-600 text-white'
                    : currentStep === i + 1
                    ? 'bg-white border-red-600 text-red-600'
                    : 'bg-white border-gray-300 text-gray-400'
                "
              >
                <svg v-if="currentStep > i + 1" class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                </svg>
                <span v-else>{{ i + 1 }}</span>
              </div>
              <span
                class="mt-1 text-xs font-semibold tracking-wide uppercase"
                :class="currentStep >= i + 1 ? 'text-red-600' : 'text-gray-400'"
              >{{ s }}</span>
            </div>
            <div
              v-if="i < steps.length - 1"
              class="flex-1 h-0.5 mx-2 mb-5 transition-all"
              :class="currentStep > i + 1 ? 'bg-red-600' : 'bg-gray-200'"
            />
          </template>
        </div>

        <!-- ── STEP 1: General Information ── -->
        <section v-if="currentStep === 1" class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
          <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">General Information</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="md:col-span-2">
              <label class="block text-sm font-medium mb-1">Tour Title *</label>
              <input v-model="form.job_title" type="text" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="e.g. Chiang Mai Full Day Temple Tour" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Start Date *</label>
              <input v-model="form.job_start_date" type="date" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">End Date *</label>
              <input v-model="form.job_end_date" type="date" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Number of Seats *</label>
              <input v-model.number="form.job_required_seat" type="number" min="1" max="13" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="0" />
            </div>
            <div>
              <label class="block text-sm font-medium mb-1">Rate (THB) *</label>
              <input v-model.number="form.job_price" type="number" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="0.00" />
            </div>
            <div class="md:col-span-2">
              <label class="block text-sm font-medium mb-2">Languages Required</label>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="lang in languages" :key="lang.value"
                  type="button"
                  @click="toggleLanguage(lang.value)"
                  :class="[
                    'px-4 py-1.5 rounded-full text-sm font-medium border transition-colors',
                    form.job_required_languages.includes(lang.value)
                      ? 'bg-red-600 text-white border-red-600'
                      : 'bg-white text-gray-600 border-gray-300 hover:border-red-400',
                  ]"
                >{{ lang.label }}</button>
              </div>
            </div>
          </div>
        </section>

        <!-- ── STEP 2: Logistics ── -->
        <section v-if="currentStep === 2" class="space-y-6">
          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Driver & Vehicle</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium mb-1">Driver Name</label>
                <input v-model="form.driver_name" type="text" class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="Driver Name" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Phone Number</label>
                <input v-model="form.driver_phone" type="tel" class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="08x xxx xxxx" />
              </div>
              <div>
                <label class="block text-sm font-medium mb-1">Vehicle Type *</label>
                <select v-model="form.job_required_vehicle_type" required class="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-400">
                  <option value="VAN">Van</option>
                  <option value="CAR">Car</option>
                </select>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Pickup Points</h2>
            <div v-for="(pickup, idx) in form.job_pickups" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Hotel Name</label>
                <input v-model="pickup.hotel_name" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Hotel" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Group / Customer</label>
                <input v-model="pickup.pickup_location" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Name" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Pickup Time</label>
                <input v-model="pickup.pickup_time" type="time" class="w-full p-2 border border-gray-300 rounded-lg text-sm" />
              </div>
              <button type="button" @click="removePickup(idx)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="addPickup" class="mt-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Pickup Point</button>
          </div>
        </section>

        <!-- ── STEP 3: Tour Details ── -->
        <section v-if="currentStep === 3" class="space-y-6">
          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Tour Schedule</h2>
            <div v-for="(item, idx) in form.job_itineraries" :key="idx" class="grid grid-cols-1 md:grid-cols-5 gap-2 mb-3 items-end">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Start Time</label>
                <input v-model="item.start_time" type="time" class="w-full p-2 border border-gray-300 rounded-lg text-sm" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">End Time</label>
                <input v-model="item.end_time" type="time" class="w-full p-2 border border-gray-300 rounded-lg text-sm" />
              </div>
              <div class="md:col-span-2">
                <label class="block text-xs text-gray-500 mb-1">Stop / Activity</label>
                <input v-model="item.place_name" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="e.g. Doi Suthep Temple" />
              </div>
              <button type="button" @click="removeItinerary(idx)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="addItinerary" class="mt-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Stop</button>
          </div>

          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Passenger List</h2>
            <div v-for="(customer, idx) in form.job_customers" :key="idx" class="flex gap-2 mb-3 items-end">
              <div class="flex-1">
                <label class="block text-xs text-gray-500 mb-1">Passenger Name</label>
                <input v-model="customer.customer_name" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Full Name" />
              </div>
              <div class="flex-1">
                <label class="block text-xs text-gray-500 mb-1">Note</label>
                <input v-model="customer.note" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="e.g. Wheelchair" />
              </div>
              <button type="button" @click="removeCustomer(idx)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="addCustomer" class="mt-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Passenger</button>
          </div>

          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Inclusions & Exclusions</h2>
            <div v-for="(inc, idx) in form.job_inclusions" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Type</label>
                <select v-model="inc.inclusion_type" class="w-full p-2 border border-gray-300 rounded-lg text-sm">
                  <option value="INCLUSION">Included</option>
                  <option value="EXCLUSION">Not Included</option>
                </select>
              </div>
              <div class="md:col-span-2">
                <label class="block text-xs text-gray-500 mb-1">Details</label>
                <input v-model="inc.description" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Details" />
              </div>
              <button type="button" @click="removeInclusion(idx)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="addInclusion" class="mt-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Item</button>
          </div>

          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-5 border-b pb-3">Entrance Fees</h2>
            <div v-for="(fee, idx) in form.job_entrance_fees" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
              <div>
                <label class="block text-xs text-gray-500 mb-1">Attraction</label>
                <input v-model="fee.place_name" type="text" class="w-full p-2 border border-gray-300 rounded-lg text-sm" placeholder="Attraction" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Thai (THB)</label>
                <input v-model.number="fee.thai_price" type="number" class="w-full p-2 border border-gray-300 rounded-lg text-sm" />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">Foreigner (THB)</label>
                <input v-model.number="fee.foreigner_price" type="number" class="w-full p-2 border border-gray-300 rounded-lg text-sm" />
              </div>
              <button type="button" @click="removeEntranceFee(idx)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">Delete</button>
            </div>
            <button type="button" @click="addEntranceFee" class="mt-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Entrance Fee</button>
          </div>
        </section>

        <!-- ── STEP 4: Review & Submit ── -->
        <section v-if="currentStep === 4" class="space-y-5">
          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-4 border-b pb-3">Review Your Tour</h2>
            <div class="space-y-3 text-sm text-gray-700">
              <div class="flex justify-between"><span class="text-gray-500">Title</span><span class="font-medium">{{ form.job_title || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Start Date</span><span>{{ form.job_start_date || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">End Date</span><span>{{ form.job_end_date || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Seats</span><span>{{ form.job_required_seat }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Rate</span><span>฿{{ form.job_price?.toLocaleString() || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Languages</span><span>{{ form.job_required_languages.join(', ') || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Driver</span><span>{{ form.driver_name || '—' }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Vehicle</span><span>{{ form.job_required_vehicle_type }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Pickup Points</span><span>{{ form.job_pickups.length }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Schedule Stops</span><span>{{ form.job_itineraries.length }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Passengers</span><span>{{ form.job_customers.length }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Inclusions/Exclusions</span><span>{{ form.job_inclusions.length }}</span></div>
              <div class="flex justify-between"><span class="text-gray-500">Entrance Fees</span><span>{{ form.job_entrance_fees.length }}</span></div>
            </div>
          </div>

          <div class="bg-white rounded-2xl shadow-xl border border-gray-100 p-6">
            <h2 class="text-base font-semibold text-gray-700 mb-3 border-b pb-3">Remarks</h2>
            <textarea v-model="form.note" rows="4" class="w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400" placeholder="Additional remarks or special instructions..."></textarea>
          </div>

        </section>

        <!-- ── Step Navigation (inline) ── -->
        <div class="mt-6 bg-white rounded-2xl shadow-xl border border-gray-100 p-4">
          <div class="flex justify-between items-center">
            <button
              type="button"
              @click="prevStep"
              class="px-6 py-2 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50 transition"
            >
              {{ currentStep === 1 ? 'Cancel' : '← Back' }}
            </button>
            <span class="text-xs text-gray-400">Step {{ currentStep }} of {{ steps.length }}</span>
            <button
              v-if="currentStep < steps.length"
              type="button"
              @click="nextStep"
              class="px-6 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition"
            >
              Next →
            </button>
            <button
              v-else
              type="button"
              @click="submitJob"
              :disabled="submitting"
              class="px-6 py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition disabled:opacity-50"
            >
              {{ submitting ? 'Creating...' : 'Create Tour' }}
            </button>
          </div>
        </div>

      </div> <!-- end right column -->
    </div> <!-- end flex row -->

    <!-- ── Modal: Load Template ── -->
    <div v-if="modal.show && modal.type === 'loadTemplate'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-9 h-9 rounded-full bg-red-100 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-base font-semibold text-gray-800">Load this template?</h3>
        </div>
        <p class="text-sm text-gray-500 mb-1"><span class="font-medium text-gray-700">{{ modal.target?.name }}</span></p>
        <p class="text-sm text-gray-400 mb-5">This will overwrite your current form data.</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-sm font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition">Cancel</button>
          <button type="button" @click="doLoadTemplate" class="px-4 py-2 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Yes, Load</button>
        </div>
      </div>
    </div>

    <!-- ── Modal: Delete Template ── -->
    <div v-if="modal.show && modal.type === 'deleteTemplate'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-9 h-9 rounded-full bg-red-100 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </div>
          <h3 class="text-base font-semibold text-gray-800">Delete this template?</h3>
        </div>
        <p class="text-sm text-gray-500 mb-5">"<span class="font-medium text-gray-700">{{ modal.target?.name }}</span>" will be permanently removed.</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-sm font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition">Cancel</button>
          <button type="button" @click="doDeleteTemplate" class="px-4 py-2 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Delete</button>
        </div>
      </div>
    </div>

    <!-- ── Modal: Unsaved Changes ── -->
    <div v-if="modal.show && modal.type === 'unsaved'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm mx-4">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-9 h-9 rounded-full bg-amber-100 flex items-center justify-center shrink-0">
            <svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" />
            </svg>
          </div>
          <h3 class="text-base font-semibold text-gray-800">Your information will be lost</h3>
        </div>
        <p class="text-sm text-gray-500 mb-5">Are you sure you want to leave? Your unsaved changes will be lost.</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-sm font-medium text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition">Stay</button>
          <button type="button" @click="dismissModalAndLeave" class="px-4 py-2 text-sm font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Leave</button>
        </div>
      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { reactive, ref, watch, onMounted } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'
const router = useRouter()

const DRAFT_KEY = 'create_job_draft'

const steps = ['General Info', 'Logistics', 'Tour Details', 'Review']
const currentStep = ref(1)
const submitting = ref(false)

const languages = [
  { value: 'English', label: 'English' },
  { value: 'Thai', label: 'Thai' },
  { value: 'Mandarin', label: 'Mandarin' },
  { value: 'Korean', label: 'Korean' },
  { value: 'Japanese', label: 'Japanese' },
  { value: 'French', label: 'French' },
  { value: 'German', label: 'German' },
]

const defaultForm = () => ({
  job_title: '',
  job_description: '',
  job_start_date: '',
  job_end_date: '',
  job_required_vehicle_type: 'VAN',
  job_required_seat: 9,
  job_price: null,
  job_required_languages: [],
  driver_name: '',
  driver_phone: '',
  note: '',
  job_itineraries: [],
  job_pickups: [],
  job_customers: [],
  job_inclusions: [],
  job_entrance_fees: [],
})

const form = reactive(defaultForm())

// ── Restore form on mount ──────────────────────────────────────────────────
onMounted(() => {
  try {
    const saved = localStorage.getItem(DRAFT_KEY)
    if (saved) {
      const { step, data } = JSON.parse(saved)
      Object.assign(form, data)
      currentStep.value = step || 1
    }
  } catch (e) {
    localStorage.removeItem(DRAFT_KEY)
  }

})

// ── Dirty tracking ─────────────────────────────────────────────────────────
const isDirty = ref(false)
const formSnapshot = () => JSON.stringify({
  ...form,
  job_required_languages: [...form.job_required_languages],
  job_itineraries: [...form.job_itineraries],
  job_pickups: [...form.job_pickups],
  job_customers: [...form.job_customers],
  job_inclusions: [...form.job_inclusions],
  job_entrance_fees: [...form.job_entrance_fees],
})
let lastSavedSnapshot = formSnapshot()

watch(() => formSnapshot(), (newVal) => {
  if (newVal !== lastSavedSnapshot) isDirty.value = true
  // Auto-persist to localStorage so data survives a page refresh
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({ step: currentStep.value, data: { ...form } }))
  } catch (_) {}
}, { deep: true })

watch(currentStep, (step) => {
  try {
    localStorage.setItem(DRAFT_KEY, JSON.stringify({ step, data: { ...form } }))
  } catch (_) {}
})

// ── Unified modal state ────────────────────────────────────────────────────
const modal = reactive({ show: false, type: '', target: null })
const openModal = (type, target = null) => { modal.show = true; modal.type = type; modal.target = target }
const closeModal = () => { modal.show = false; modal.type = ''; modal.target = null }

// ── Templates ──────────────────────────────────────────────────────────────
const templates = ref([
  {
    id: 'tpl_chiangmai_temple',
    name: 'Chiang Mai Temple Tour',
    subtitle: 'Full day · Van · English',
    data: {
      job_title: 'Chiang Mai Full Day Temple Tour',
      job_required_vehicle_type: 'VAN',
      job_required_seat: 9,
      job_required_languages: ['English'],
      job_itineraries: [
        { place_name: 'Doi Suthep Temple', start_time: '08:00', end_time: '10:00', note: '' },
        { place_name: 'Wat Chedi Luang', start_time: '11:00', end_time: '12:30', note: '' },
      ],
      job_inclusions: [
        { inclusion_type: 'INCLUSION', description: 'English-speaking guide', sequence: 1 },
        { inclusion_type: 'EXCLUSION', description: 'Entrance fees', sequence: 2 },
      ],
    },
  },
  {
    id: 'tpl_night_market',
    name: 'Night Market Run',
    subtitle: 'Evening · Van · Thai, English',
    data: {
      job_title: 'Chiang Mai Night Market Tour',
      job_required_vehicle_type: 'VAN',
      job_required_seat: 9,
      job_required_languages: ['English', 'Thai'],
      job_itineraries: [
        { place_name: 'Warorot Market', start_time: '17:00', end_time: '18:30', note: '' },
        { place_name: 'Sunday Walking Street', start_time: '19:00', end_time: '21:00', note: '' },
      ],
      job_inclusions: [],
    },
  },
])

const confirmLoadTemplate = (tpl) => openModal('loadTemplate', tpl)
const confirmDeleteTemplate = (tpl) => openModal('deleteTemplate', tpl)

const doLoadTemplate = () => {
  Object.assign(form, defaultForm(), modal.target.data)
  currentStep.value = 1
  isDirty.value = true
  closeModal()
}

const doDeleteTemplate = () => {
  templates.value = templates.value.filter(t => t.id !== modal.target.id)
  closeModal()
}

const saveAsTemplate = () => {
  const name = prompt('Enter a name for this template:')
  if (!name) return
  const newTpl = {
    id: 'tpl_' + Date.now(),
    name,
    subtitle: [form.job_required_vehicle_type, ...form.job_required_languages].filter(Boolean).join(' · ') || 'Custom',
    data: {
      job_title: form.job_title,
      job_required_vehicle_type: form.job_required_vehicle_type,
      job_required_seat: form.job_required_seat,
      job_required_languages: [...form.job_required_languages],
      job_itineraries: form.job_itineraries.map(i => ({ ...i })),
      job_inclusions: form.job_inclusions.map(i => ({ ...i })),
    },
  }
  templates.value.unshift(newTpl)
}

// ── Navigation guard ───────────────────────────────────────────────────────
let pendingNavResolve = null

onBeforeRouteLeave((_to, _from, next) => {
  if (!isDirty.value) { next(); return }
  openModal('unsaved')
  pendingNavResolve = next
})

const dismissModalAndLeave = () => {
  isDirty.value = false
  closeModal()
  if (pendingNavResolve) { pendingNavResolve(); pendingNavResolve = null }
}

// ── Misc helpers ───────────────────────────────────────────────────────────
const clearForm = () => { localStorage.removeItem(DRAFT_KEY) }

const toggleLanguage = (lang) => {
  const idx = form.job_required_languages.indexOf(lang)
  if (idx > -1) form.job_required_languages.splice(idx, 1)
  else form.job_required_languages.push(lang)
}

const nextStep = () => { if (currentStep.value < steps.length) currentStep.value++ }
const prevStep = () => { if (currentStep.value > 1) currentStep.value--; else router.back() }

const addItinerary    = () => form.job_itineraries.push({ place_name: '', start_time: '', end_time: '', note: '' })
const removeItinerary = (idx) => form.job_itineraries.splice(idx, 1)
const addPickup       = () => form.job_pickups.push({ hotel_name: '', pickup_location: '', pickup_time: '', sequence: form.job_pickups.length + 1 })
const removePickup    = (idx) => form.job_pickups.splice(idx, 1)
const addCustomer     = () => form.job_customers.push({ customer_name: '', note: '' })
const removeCustomer  = (idx) => form.job_customers.splice(idx, 1)
const addInclusion    = () => form.job_inclusions.push({ inclusion_type: 'INCLUSION', description: '', sequence: form.job_inclusions.length + 1 })
const removeInclusion = (idx) => form.job_inclusions.splice(idx, 1)
const addEntranceFee  = () => form.job_entrance_fees.push({ place_name: '', thai_price: 0, foreigner_price: 0, sequence: form.job_entrance_fees.length + 1 })
const removeEntranceFee = (idx) => form.job_entrance_fees.splice(idx, 1)

const generateId = (_prefix) => {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
    const r = Math.random() * 16 | 0
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
  })
}

const submitJob = async () => {
  submitting.value = true
  try {
    const job_id = generateId('JOB')
    const payload = { job_id, em_id: localStorage.getItem('em_id') || 'EM001', ...form }
    const res = await fetch(`${API_BASE}/jobs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    let data = {}
    const text = await res.text()
    if (text) { try { data = JSON.parse(text) } catch (_) {} }
    if (res.ok) {
      isDirty.value = false
      clearForm()
      router.push('/my-tours')
    } else {
      alert('An error occurred: ' + (data.error || data.message || data.detail || 'Unknown error'))
    }
  } catch (e) {
    alert('An error occurred: ' + e.message)
  } finally {
    submitting.value = false
  }
}
</script>
