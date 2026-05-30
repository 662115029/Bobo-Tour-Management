<template>
  <AppLayout>
    <div class="px-8 pt-6 pb-16 font-['DM_Sans',sans-serif]">

      <!-- Back button row -->
      <div class="mb-4">
        <button
          @click="$router.back()"
          class="flex items-center gap-1.5 text-sm font-medium text-gray-600 bg-white hover:bg-[#ffd8d8] hover:text-[#dc2626] px-4 py-2 rounded-full transition w-fit"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-32 text-gray-400">
        <svg class="animate-spin w-8 h-8 mb-3 text-red-500" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
        </svg>
        <span class="text-sm">Loading Tour Details…</span>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="mt-20 text-center">
        <p class="text-red-500 font-medium mb-4">{{ error }}</p>
        <button @click="fetchJob" class="px-5 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition">Retry</button>
      </div>

      <!-- Content -->
      <template v-else-if="job">

        <!-- ── Hero card ── -->
        <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-5">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2">
                <span :class="statusClass(job.job_status)" class="text-xs font-semibold px-2.5 py-0.5 rounded-full">
                  {{ statusLabel(job.job_status) }}
                </span>
                <span v-if="editing" class="text-xs font-semibold text-amber-600 bg-amber-50 border border-amber-200 px-2.5 py-0.5 rounded-full">Editing</span>
              </div>
              <h1 class="text-2xl font-bold text-gray-800 leading-snug">
                {{ editing ? form.job_title || 'Edit Tour' : job.job_title }}
              </h1>
              <p v-if="job.company" class="text-sm text-gray-400 mt-1 flex items-center gap-1.5">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
                {{ job.company }}
              </p>
              <p v-if="job.job_description" class="text-sm text-gray-500 mt-2 leading-relaxed">{{ job.job_description }}</p>
            </div>
            <div class="text-right shrink-0">
              <p class="text-xs text-gray-400 uppercase tracking-wide font-medium mb-1">Price</p>
              <p class="text-3xl font-bold text-gray-800">฿{{ Number(job.job_price).toLocaleString() }}</p>
            </div>
          </div>

          <!-- Date/Vehicle/Seats row -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
              <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Start Date</p>
              <p class="text-sm font-semibold text-gray-700">{{ formatDate(job.job_start_date) }}</p>
            </div>
            <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
              <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">End Date</p>
              <p class="text-sm font-semibold text-gray-700">{{ formatDate(job.job_end_date) }}</p>
            </div>
            <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
              <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Vehicle</p>
              <p class="text-sm font-semibold text-gray-700">{{ job.job_required_vehicle_type || '—' }}</p>
            </div>
            <div class="bg-gray-50 rounded-xl p-3 border border-gray-100">
              <p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wide mb-1">Seats Required</p>
              <p class="text-sm font-semibold text-gray-700">{{ job.job_required_seat ?? '—' }}</p>
            </div>
          </div>
        </div>

        <!-- ── Two-column body ── -->
        <div class="flex gap-5 items-start">

          <!-- LEFT column -->
          <div class="flex flex-col gap-4 w-72 shrink-0">

            <!-- Languages & Driver -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
                Languages & Driver
              </h2>

              <div class="mb-4">
                <p class="info-label mb-1">Required Languages</p>
                <template v-if="!editing">
                  <div v-if="job.job_required_languages?.length" class="flex flex-wrap gap-1.5">
                    <span v-for="lang in job.job_required_languages" :key="lang" class="px-2.5 py-0.5 bg-red-50 text-red-700 text-xs font-medium rounded-full border border-red-100">{{ lang }}</span>
                  </div>
                  <p v-else class="text-sm text-gray-400 italic">None specified</p>
                </template>
                <div v-else class="flex flex-wrap gap-2">
                  <button v-for="lang in allLanguages" :key="lang" type="button" @click="toggleLanguage(lang)"
                    :class="['px-3 py-1 rounded-full text-xs font-medium border transition-colors', form.job_required_languages.includes(lang) ? 'bg-red-600 text-white border-red-600' : 'bg-white text-gray-600 border-gray-300 hover:border-red-400']">
                    {{ lang }}
                  </button>
                </div>
              </div>

              <div>
                <p class="info-label mb-2">Assigned Driver</p>
                <template v-if="!editing">
                  <div v-if="job.driver_name" class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-full bg-[#fef2f2] text-[#dc2626] text-sm font-bold flex items-center justify-center shrink-0">
                      {{ job.driver_name.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-800">{{ job.driver_name }}</p>
                      <p v-if="job.driver_phone" class="text-xs text-gray-400">{{ job.driver_phone }}</p>
                    </div>
                  </div>
                  <p v-else class="text-sm text-gray-400 italic">Not assigned</p>
                </template>
                <template v-else>
                  <input v-model="form.driver_name" type="text" class="field-input mb-2" placeholder="Driver Name" />
                  <input v-model="form.driver_phone" type="tel" class="field-input" placeholder="08x xxx xxxx" />
                </template>
              </div>
            </div>

            <!-- Timeline -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2"/></svg>
                Timeline
              </h2>
              <div class="space-y-3">
                <div class="flex items-start gap-2.5">
                  <svg class="w-4 h-4 text-gray-300 mt-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6l4 2"/></svg>
                  <div>
                    <p class="info-label">Created</p>
                    <p class="text-sm text-gray-700">{{ formatDateTime(job.job_created_at) }}</p>
                  </div>
                </div>
                <div class="flex items-start gap-2.5">
                  <svg class="w-4 h-4 text-gray-300 mt-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
                  <div>
                    <p class="info-label">Last Updated</p>
                    <p class="text-sm text-gray-700">{{ formatDateTime(job.job_updated_at) }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Expenses -->
            <div v-if="editing || job.job_expenses?.length" class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                Expenses
              </h2>
              <template v-if="!editing">
                <div class="space-y-2 mb-3">
                  <div v-for="(exp, idx) in sortedExpenses" :key="idx" class="flex items-center justify-between">
                    <span class="text-sm text-gray-600">{{ exp.item_name }}</span>
                    <span class="text-sm font-medium text-gray-800">฿{{ Number(exp.amount).toLocaleString() }}</span>
                  </div>
                </div>
                <div class="border-t border-gray-100 pt-2 flex justify-between">
                  <span class="text-sm font-bold text-gray-800">Total</span>
                  <span class="text-sm font-bold text-gray-800">฿{{ sortedExpenses.reduce((s, e) => s + Number(e.amount || 0), 0).toLocaleString() }}</span>
                </div>
              </template>
              <template v-else>
                <div v-for="(exp, idx) in form.job_expenses" :key="idx" class="grid grid-cols-2 gap-2 mb-2 items-end">
                  <div><label class="field-label">Item Name</label><input v-model="exp.item_name" type="text" class="field-input" /></div>
                  <div><label class="field-label">Amount (THB)</label><input v-model.number="exp.amount" type="number" class="field-input" /></div>
                  <button type="button" @click="form.job_expenses.splice(idx, 1)" class="col-span-2 text-xs text-red-500 hover:underline text-left">Remove</button>
                </div>
                <button type="button" @click="form.job_expenses.push({ item_name: '', amount: 0 })" class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-xs hover:bg-gray-200">+ Add Expense</button>
              </template>
            </div>



          </div>

          <!-- RIGHT column -->
          <div class="flex-1 min-w-0 flex flex-col gap-4">

            <!-- Itinerary -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                Itinerary
              </h2>
              <template v-if="!editing">
                <div class="space-y-2">
                  <div v-for="(item, idx) in job.job_itineraries" :key="idx" class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                    <div class="w-7 h-7 rounded-full bg-purple-100 text-purple-700 text-xs font-bold flex items-center justify-center shrink-0">{{ idx + 1 }}</div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-800">{{ item.place_name }}</p>
                      <p v-if="item.note" class="text-xs text-gray-400">{{ item.note }}</p>
                    </div>
                    <span v-if="item.start_time || item.end_time" class="text-xs font-semibold text-purple-600 bg-purple-50 px-2.5 py-1 rounded-lg shrink-0">
                      {{ item.start_time }} – {{ item.end_time }}
                    </span>
                  </div>
                  <p v-if="!job.job_itineraries?.length" class="text-sm text-gray-400 italic">No stops added</p>
                </div>
              </template>
              <template v-else>
                <div v-for="(item, idx) in form.job_itineraries" :key="idx" class="grid grid-cols-1 md:grid-cols-5 gap-2 mb-3 items-end">
                  <div><label class="field-label">Start</label><input v-model="item.start_time" type="time" class="field-input" /></div>
                  <div><label class="field-label">End</label><input v-model="item.end_time" type="time" class="field-input" /></div>
                  <div class="md:col-span-2"><label class="field-label">Stop / Activity</label><input v-model="item.place_name" type="text" class="field-input" /></div>
                  <button type="button" @click="form.job_itineraries.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">✕</button>
                </div>
                <button type="button" @click="form.job_itineraries.push({ place_name: '', start_time: '', end_time: '', note: '' })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Stop</button>
              </template>
            </div>

            <!-- Passengers (pickup points) -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a4 4 0 00-4-4h-1M9 20H4v-2a4 4 0 014-4h1m4-4a4 4 0 100-8 4 4 0 000 8z"/></svg>
                Passengers
                <span class="ml-auto text-xs font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full normal-case tracking-normal">{{ job.job_pickups?.length ?? 0 }}</span>
              </h2>
              <template v-if="!editing">
                <div class="space-y-2">
                  <div v-for="(pickup, idx) in sortedPickups" :key="idx" class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100">
                    <div class="w-7 h-7 rounded-full bg-blue-100 text-blue-700 text-xs font-bold flex items-center justify-center shrink-0">{{ idx + 1 }}</div>
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-800">{{ pickup.pickup_location || pickup.hotel_name || '—' }}</p>
                      <p v-if="pickup.hotel_name && pickup.pickup_location" class="text-xs text-gray-400">{{ pickup.hotel_name }}</p>
                    </div>
                    <span v-if="pickup.pickup_time" class="text-xs font-semibold text-blue-600 bg-blue-50 px-2.5 py-1 rounded-lg shrink-0">{{ pickup.pickup_time }}</span>
                  </div>
                  <p v-if="!job.job_pickups?.length" class="text-sm text-gray-400 italic">No passengers added</p>
                </div>
              </template>
              <template v-else>
                <div v-for="(pickup, idx) in form.job_pickups" :key="idx" class="grid grid-cols-1 md:grid-cols-4 gap-2 mb-3 items-end">
                  <div><label class="field-label">Hotel</label><input v-model="pickup.hotel_name" type="text" class="field-input" /></div>
                  <div><label class="field-label">Name</label><input v-model="pickup.pickup_location" type="text" class="field-input" /></div>
                  <div><label class="field-label">Pickup Time</label><input v-model="pickup.pickup_time" type="time" class="field-input" /></div>
                  <button type="button" @click="form.job_pickups.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">✕</button>
                </div>
                <button type="button" @click="form.job_pickups.push({ hotel_name: '', pickup_location: '', pickup_time: '' })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Passenger</button>
              </template>
            </div>

            <!-- Customer list -->
            <div v-if="editing || job.job_customers?.length" class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                Customers
              </h2>
              <template v-if="!editing">
                <div class="divide-y divide-gray-100">
                  <div v-for="(c, idx) in job.job_customers" :key="idx" class="flex items-center justify-between py-2.5">
                    <div class="flex items-center gap-2.5">
                      <div class="w-7 h-7 rounded-full bg-gray-100 text-gray-500 text-xs font-bold flex items-center justify-center">{{ idx + 1 }}</div>
                      <span class="text-sm text-gray-700">{{ c.customer_name || 'Unnamed' }}</span>
                    </div>
                    <span v-if="c.note" class="text-xs text-gray-400 italic">{{ c.note }}</span>
                  </div>
                </div>
              </template>
              <template v-else>
                <div v-for="(c, idx) in form.job_customers" :key="idx" class="flex gap-2 mb-3 items-end">
                  <div class="flex-1"><label class="field-label">Name</label><input v-model="c.customer_name" type="text" class="field-input" /></div>
                  <div class="flex-1"><label class="field-label">Note</label><input v-model="c.note" type="text" class="field-input" /></div>
                  <button type="button" @click="form.job_customers.splice(idx, 1)" class="p-2 bg-red-50 text-red-500 rounded-lg hover:bg-red-100 text-sm">✕</button>
                </div>
                <button type="button" @click="form.job_customers.push({ customer_name: '', note: '' })" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm hover:bg-gray-200">+ Add Customer</button>
              </template>
            </div>

            <!-- ── Applications ── -->
            <div class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>
                Applications
                <span class="ml-auto text-xs font-bold text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full normal-case tracking-normal">{{ applications.length }}</span>
              </h2>

              <div v-if="appsLoading" class="text-center py-8 text-gray-400 text-sm">Loading applications…</div>

              <div v-else-if="applications.length === 0" class="text-center py-8 text-gray-400 text-sm">
                No applications yet.
              </div>

              <div v-else class="space-y-3">
                <div
                  v-for="(app, idx) in applications"
                  :key="app.application_id || idx"
                  class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100"
                >
                  <!-- Avatar -->
                  <div class="w-10 h-10 rounded-full bg-[#fef2f2] text-[#dc2626] text-sm font-bold flex items-center justify-center shrink-0">
                    {{ (app.guide_name || '?').charAt(0).toUpperCase() }}
                  </div>

                  <!-- Info -->
                  <div class="flex-1 min-w-0">
                    <p class="font-semibold text-gray-800 text-sm">{{ app.guide_name || '—' }}</p>
                    <div class="flex flex-wrap gap-2 mt-0.5 text-xs text-gray-400">
                      <span v-if="app.guide_phone">{{ app.guide_phone }}</span>
                      <span v-if="app.languages?.length">{{ app.languages.join(', ') }}</span>
                      <span v-if="app.vehicle_type">{{ app.vehicle_type }}</span>
                      <span v-if="app.applied_at">Applied {{ formatDate(app.applied_at) }}</span>
                    </div>
                  </div>

                  <!-- Status badge -->
                  <span
                    class="px-2.5 py-1 rounded-full text-xs font-semibold shrink-0"
                    :class="{
                      'bg-blue-100 text-blue-700': app.status === 'APPLIED',
                      'bg-yellow-100 text-yellow-700': app.status === 'PENDING',
                      'bg-green-100 text-green-700': app.status === 'ACCEPTED',
                      'bg-red-100 text-red-600': app.status === 'REJECTED',
                    }"
                  >{{ app.status }}</span>

                  <!-- Accept / Reject -->
                  <div class="flex items-center gap-1.5 shrink-0">
                    <button
                      @click="handleAccept(app)"
                      :disabled="app.status === 'ACCEPTED' || app.status === 'REJECTED'"
                      class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-400 hover:bg-green-50 hover:text-green-600 hover:border-green-200 transition disabled:opacity-30 disabled:cursor-not-allowed"
                      title="Accept"
                    >
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button
                      @click="handleReject(app)"
                      :disabled="app.status === 'ACCEPTED' || app.status === 'REJECTED'"
                      class="w-8 h-8 flex items-center justify-center rounded-lg border border-gray-200 text-gray-400 hover:bg-red-50 hover:text-red-600 hover:border-red-200 transition disabled:opacity-30 disabled:cursor-not-allowed"
                      title="Reject"
                    >
                      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Edit mode: general info fields -->
            <div v-if="editing" class="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
              <h2 class="section-title">Edit General Info</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="md:col-span-2"><label class="field-label">Tour Title *</label><input v-model="form.job_title" type="text" class="field-input" /></div>
                <div><label class="field-label">Start Date *</label><input v-model="form.job_start_date" type="date" class="field-input" /></div>
                <div><label class="field-label">End Date *</label><input v-model="form.job_end_date" type="date" class="field-input" /></div>
                <div><label class="field-label">Seats *</label><input v-model.number="form.job_required_seat" type="number" min="1" max="13" class="field-input" /></div>
                <div><label class="field-label">Rate (THB) *</label><input v-model.number="form.job_price" type="number" class="field-input" /></div>
                <div><label class="field-label">Vehicle Type *</label>
                  <select v-model="form.job_required_vehicle_type" class="field-input"><option value="VAN">Van</option><option value="CAR">Car</option></select>
                </div>
                <div class="md:col-span-2"><label class="field-label">Description</label><textarea v-model="form.job_description" rows="3" class="field-input"></textarea></div>
              </div>
            </div>

            <!-- ── Action buttons ── -->
            <div class="flex gap-3 mt-1">
              <template v-if="!editing">
                <button v-if="canEdit" @click="startEditing"
                  class="flex-1 py-2.5 border-2 border-red-500 text-red-600 font-semibold rounded-xl hover:bg-red-50 transition text-sm">
                  Edit Tour
                </button>
                <button v-if="canCancel" @click="confirmCancel" :disabled="cancelling"
                  class="px-6 py-2.5 border border-gray-300 text-gray-500 font-medium rounded-xl hover:bg-gray-50 transition text-sm disabled:opacity-50">
                  {{ cancelling ? 'Cancelling…' : 'Cancel Tour' }}
                </button>
              </template>
              <template v-else>
                <button @click="cancelEditing" class="px-6 py-2.5 border border-gray-300 text-gray-500 font-medium rounded-xl hover:bg-gray-50 transition text-sm">Discard</button>
                <button @click="saveJob" :disabled="submitting"
                  class="flex-1 py-2.5 bg-red-600 text-white font-semibold rounded-xl hover:bg-red-700 transition text-sm disabled:opacity-50">
                  {{ submitting ? 'Saving…' : 'Save Changes' }}
                </button>
              </template>
            </div>

          </div>
        </div>

      </template>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'

const API_BASE = '/api'
const router = useRouter()
const route = useRoute()
const emId = localStorage.getItem('em_id')

const job = ref(null)
const loading = ref(true)
const error = ref('')
const cancelling = ref(false)
const submitting = ref(false)
const editing = ref(false)

// Applications state
const applications = ref([])
const appsLoading = ref(false)

const allLanguages = ['English', 'Thai', 'Mandarin', 'Korean', 'Japanese', 'French', 'German']

const form = reactive({
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
  job_expenses: [],
})

// ── Fetch tour ─────────────────────────────────────────────────────────────
const fetchJob = async () => {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch(`${API_BASE}/tours/${route.params.id}?em_id=${emId}`)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.detail || data.message || 'Failed to load tour.')
    }
    job.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

// ── Fetch applications for this tour ──────────────────────────────────────
const fetchApplications = async () => {
  appsLoading.value = true
  try {
    const res = await fetch(`${API_BASE}/tours/${route.params.id}/applications?em_id=${emId}`)
    const data = await res.json()
    const list = Array.isArray(data) ? data : (data.applications || [])
    applications.value = list.sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))
  } catch {
    applications.value = []
  } finally {
    appsLoading.value = false
  }
}

onMounted(async () => {
  await fetchJob()
  fetchApplications()
})

// ── Accept / Reject ────────────────────────────────────────────────────────
const handleAccept = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/applications/${app.application_id}/accept`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.status = 'ACCEPTED'
    else alert('Failed to accept application.')
  } catch {
    alert('Failed to accept application.')
  }
}

const handleReject = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/applications/${app.application_id}/reject`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.status = 'REJECTED'
    else alert('Failed to reject application.')
  } catch {
    alert('Failed to reject application.')
  }
}

// ── Edit helpers ───────────────────────────────────────────────────────────
const toDateInput = (d) => d ? new Date(d).toISOString().slice(0, 10) : ''

const startEditing = () => {
  const j = job.value
  Object.assign(form, {
    job_title: j.job_title || '',
    job_description: j.job_description || '',
    job_start_date: toDateInput(j.job_start_date),
    job_end_date: toDateInput(j.job_end_date),
    job_required_vehicle_type: j.job_required_vehicle_type || 'VAN',
    job_required_seat: j.job_required_seat ?? 9,
    job_price: j.job_price ?? null,
    job_required_languages: [...(j.job_required_languages || [])],
    driver_name: j.driver_name || '',
    driver_phone: j.driver_phone || '',
    note: j.note || '',
    job_itineraries: (j.job_itineraries || []).map(i => ({ ...i })),
    job_pickups: (j.job_pickups || []).map(p => ({ ...p })),
    job_customers: (j.job_customers || []).map(c => ({ ...c })),
    job_expenses: (j.job_expenses || []).map(e => ({ ...e })),
  })
  editing.value = true
}

const cancelEditing = () => { editing.value = false }

const toggleLanguage = (lang) => {
  const idx = form.job_required_languages.indexOf(lang)
  if (idx > -1) form.job_required_languages.splice(idx, 1)
  else form.job_required_languages.push(lang)
}

// ── Save ───────────────────────────────────────────────────────────────────
const saveJob = async () => {
  submitting.value = true
  try {
    const res = await fetch(`${API_BASE}/tours/${route.params.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, em_id: emId }),
    })
    let data = {}
    const text = await res.text()
    if (text) { try { data = JSON.parse(text) } catch (_) {} }
    if (res.ok) {
      editing.value = false
      await fetchJob()
    } else {
      alert('Failed to save: ' + (data.error || data.message || data.detail || 'Unknown error'))
    }
  } catch (e) {
    alert('An error occurred: ' + e.message)
  } finally {
    submitting.value = false
  }
}

// ── Computed helpers ───────────────────────────────────────────────────────
const sortedPickups = computed(() =>
  [...(job.value?.job_pickups ?? [])].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
)
const sortedExpenses = computed(() =>
  [...(job.value?.job_expenses ?? [])].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
)
const canEdit = computed(() => ['OPEN', 'PENDING'].includes(job.value?.job_status))
const canCancel = computed(() => ['OPEN', 'PENDING', 'MATCHED'].includes(job.value?.job_status))

// ── Status display ─────────────────────────────────────────────────────────
const STATUS_MAP = {
  OPEN:        { label: 'Open',        cls: 'bg-green-100 text-green-700' },
  PENDING:     { label: 'Pending',     cls: 'bg-yellow-100 text-yellow-700' },
  MATCHED:     { label: 'Matched',     cls: 'bg-blue-100 text-blue-700' },
  IN_PROGRESS: { label: 'In Progress', cls: 'bg-amber-100 text-amber-700' },
  COMPLETED:   { label: 'Completed',   cls: 'bg-gray-100 text-gray-600' },
  CANCELLED:   { label: 'Cancelled',   cls: 'bg-red-100 text-red-600' },
}
const statusLabel = (s) => STATUS_MAP[s]?.label ?? s
const statusClass = (s) => STATUS_MAP[s]?.cls ?? 'bg-gray-100 text-gray-500'

// ── Formatters ─────────────────────────────────────────────────────────────
const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}
const formatDateTime = (d) => {
  if (!d) return '—'
  return new Date(d).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

// ── Cancel tour ────────────────────────────────────────────────────────────
const confirmCancel = async () => {
  if (!confirm('Are you sure you want to cancel this tour? This cannot be undone.')) return
  cancelling.value = true
  try {
    const res = await fetch(`${API_BASE}/tours/${route.params.id}/cancel?em_id=${emId}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
    })
    if (res.ok) {
      job.value.job_status = 'CANCELLED'
    } else {
      const data = await res.json().catch(() => ({}))
      alert(data.detail || data.message || 'Failed to cancel tour.')
    }
  } catch (e) {
    alert('Unable to connect.')
  } finally {
    cancelling.value = false
  }
}
</script>

<style scoped>
.section-title {
  @apply text-sm font-semibold text-gray-500 uppercase tracking-wide border-b border-gray-100 pb-2 mb-4 flex items-center gap-2;
}
.count-badge {
  @apply text-xs font-medium text-gray-400 normal-case tracking-normal;
}
.info-block { @apply flex flex-col gap-0.5; }
.info-label { @apply text-xs text-gray-400 font-medium uppercase tracking-wide; }
.info-value { @apply text-sm font-semibold text-gray-700; }
.field-label { @apply block text-xs text-gray-500 font-medium mb-1; }
.field-input { @apply w-full p-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-red-400; }
</style>
