<template>
  <AppLayout>
    <div class="px-5 pb-10">

      <div class="flex items-center flex-wrap gap-2 py-3 mb-4">
        <button type="button" @click="cancelAndLeave"
          class="flex items-center gap-1.5 text-sm font-medium text-gray-600 bg-white hover:bg-[#ffd8d8] hover:text-[#dc2626] px-4 py-2 rounded-full transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          Back
        </button>
        <button v-if="formHistory.length > 0" type="button" @click="undo"
          class="flex items-center gap-1.5 text-sm font-medium text-gray-500 bg-white hover:bg-gray-100 px-4 py-2 rounded-full border border-gray-200 transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 10h10a8 8 0 018 8v2M3 10l6 6M3 10l6-6"/></svg>
          Undo
        </button>
      </div>

      <div v-if="!isVerified" class="mb-4 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 flex items-start gap-2.5">
        <svg class="w-4 h-4 text-amber-500 shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/></svg>
        <div>
          <p class="text-[13px] font-semibold text-amber-700">Account not verified</p>
          <p class="text-[12px] text-amber-600 mt-0.5">Your account must be verified before creating tours.</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-5 items-start">

        <!-- LEFT -->
        <div>
          <!-- Step bar -->
          <div class="flex items-start justify-center flex-wrap gap-y-2 gap-0 mb-5">
            <div v-for="(s, i) in steps" :key="i" class="flex items-center">
              <div class="flex flex-col items-center gap-0.5" @click="currentStep = i + 1" style="cursor:pointer">
                <div class="w-6 h-6 rounded-full flex items-center justify-center text-[11px] font-bold transition-colors shrink-0"
                  :class="currentStep > i + 1 ? 'bg-red-600 text-white' : currentStep === i + 1 ? 'bg-red-600 text-white' : 'bg-gray-200 text-gray-400'">
                  <svg v-if="currentStep > i + 1" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="3" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                  <span v-else>{{ i + 1 }}</span>
                </div>
                <span class="text-[10px] font-medium text-center leading-tight max-w-[60px]"
                  :class="currentStep === i + 1 ? 'text-red-600' : 'text-gray-400'">{{ s }}</span>
              </div>
              <div v-if="i < steps.length - 1" class="h-px w-4 mx-1 mt-3" :class="currentStep > i + 1 ? 'bg-red-600' : 'bg-gray-200'"></div>
            </div>
          </div>

          <!-- STEP 1: General Info -->
          <div v-if="currentStep === 1" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col gap-4">
            <h2 class="text-[14px] font-bold text-[#333] border-b border-[#f0f0f0] pb-2.5">General Information</h2>
            <div>
              <label class="field-label">Tour Title <span class="text-red-500">*</span></label>
              <input v-model="form.job_title" type="text" class="field-input" placeholder="e.g. Chiang Mai Full Day Temple Tour" />
            </div>
            <div>
              <label class="field-label">Description</label>
              <textarea v-model="form.job_description" rows="2" class="field-input resize-none" placeholder="Brief description…"></textarea>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label class="field-label">Start Date <span class="text-red-500">*</span></label>
                <input v-model="form.job_start_date" type="date" class="field-input" @change="syncItineraryDates" />
              </div>
              <div>
                <label class="field-label">End Date <span class="text-red-500">*</span></label>
                <input v-model="form.job_end_date" type="date" class="field-input" />
              </div>
            </div>
            <div>
              <label class="field-label">Price (THB) <span class="text-red-500">*</span></label>
              <input v-model.number="form.job_price" type="number" min="0" class="field-input" placeholder="0" />
            </div>
            <div>
              <label class="field-label">Languages Required</label>
              <div class="flex flex-wrap gap-2 mt-1">
                <button v-for="lang in displayLanguages" :key="lang.language_id" type="button"
                  @click="toggleLanguage(lang.language_name)"
                  :class="['px-3 py-1 rounded-full text-[12px] font-medium border transition-colors',
                    form.job_required_languages.includes(lang.language_name)
                      ? 'bg-red-600 text-white border-red-600'
                      : 'bg-white text-gray-600 border-gray-300 hover:border-red-400']">
                  {{ lang.language_name }}
                </button>

                <!-- Autocomplete -->
                <div class="relative">
                  <input v-model="otherLanguage" type="text" placeholder="Other…"
                    class="px-2.5 py-1 rounded-full text-[12px] border border-dashed border-gray-300 focus:outline-none focus:border-red-400 w-24"
                    @input="onLangInput" @keyup.enter="addTopSuggestion" @blur="hideSuggestions" @focus="onLangInput" />
                  <div v-if="showSuggestions && (langSuggestions.length || otherLanguage.trim())"
                    class="absolute left-0 top-full mt-1 z-20 bg-white border border-[#e0e0e0] rounded-xl shadow-lg overflow-hidden min-w-[160px]">
                    <button v-for="s in langSuggestions" :key="s.language_id" type="button"
                      @mousedown.prevent="selectSuggestion(s.language_name)"
                      class="w-full text-left px-3 py-2 text-[13px] text-[#222] hover:bg-[#f5f5f5] transition">
                      {{ s.language_name }}
                    </button>
                    <button v-if="otherLanguage.trim() && !exactMatch" type="button"
                      @mousedown.prevent="addOtherLanguage"
                      class="w-full text-left px-3 py-2 text-[13px] text-red-600 hover:bg-red-50 transition border-t border-[#f0f0f0]">
                      + Add "{{ otherLanguage.trim() }}"
                    </button>
                  </div>
                </div>
              </div>

              <!-- Custom (non-preset) language badges -->
              <div v-if="form.job_required_languages.some(l => !languages.slice(0,5).find(db => db.language_name === l))" class="flex flex-wrap gap-1.5 mt-2">
                <span v-for="lang in form.job_required_languages.filter(l => !languages.slice(0,5).find(db => db.language_name === l))" :key="lang"
                  class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] bg-red-600 text-white">
                  {{ lang }}<button type="button" @click="toggleLanguage(lang)" class="hover:opacity-70 ml-0.5">✕</button>
                </span>
              </div>
            </div>
          </div>

          <!-- STEP 2: Vehicle -->
          <div v-if="currentStep === 2" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col gap-4">
            <h2 class="text-[14px] font-bold text-[#333] border-b border-[#f0f0f0] pb-2.5">Vehicle</h2>
            <div>
              <label class="field-label">Vehicle Type</label>
              <div class="flex items-center gap-2 px-3 py-2.5 border border-[#e0e0e0] rounded-lg bg-[#f8f9fa] text-[13px] text-[#666]">
                <svg class="w-4 h-4 text-[#bbb]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 17h8M3 9l2-4h14l2 4M3 9v6a1 1 0 001 1h1m12 0h1a1 1 0 001-1V9M3 9h18"/></svg>
                VAN
              </div>
            </div>
            <div>
              <label class="field-label">Number of Seats <span class="text-red-500">*</span></label>
              <div class="flex items-center gap-3 mt-1">
                <button type="button" @click="form.job_required_seat = Math.max(1, form.job_required_seat - 1)"
                  class="w-9 h-9 rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition text-lg font-medium flex items-center justify-center">−</button>
                <span class="text-[20px] font-bold text-[#222] w-8 text-center">{{ form.job_required_seat }}</span>
                <button type="button" @click="form.job_required_seat = Math.min(13, form.job_required_seat + 1)"
                  class="w-9 h-9 rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition text-lg font-medium flex items-center justify-center">+</button>
                <span class="text-[12px] text-[#bbb]">1 – 13 seats</span>
              </div>
            </div>
          </div>

          <!-- STEP 3: Tour Schedule -->
          <div v-if="currentStep === 3" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col gap-3">
            <h2 class="text-[14px] font-bold text-[#333] border-b border-[#f0f0f0] pb-2.5">Tour Schedule</h2>
            <div class="flex flex-col gap-2">
              <div v-for="(itin, idx) in form.job_itineraries" :key="idx"
                class="bg-[#f8f9fa] rounded-xl border border-[#e8e8e8] px-3 py-2.5 flex flex-col gap-2">
                <div class="flex items-center gap-2">
                  <span class="text-[10px] font-bold text-[#bbb] uppercase w-10 shrink-0">{{ idx + 1 }}</span>
                  <input v-model="itin.place_name" type="text" placeholder="Place name *"
                    class="flex-1 min-w-0 px-2.5 py-1.5 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-red-400 bg-white" />
                  <input v-model="itin.itinerary_date" type="date"
                    class="w-32 shrink-0 px-2 py-1.5 border border-[#e0e0e0] rounded-lg text-[12px] focus:outline-none focus:border-red-400 bg-white" />
                  <input v-model="itin.start_time" type="time" required
                    class="w-24 shrink-0 px-2 py-1.5 border border-[#e0e0e0] rounded-lg text-[12px] focus:outline-none focus:border-red-400 bg-white" />
                  <span class="text-[#bbb] text-[11px] shrink-0">–</span>
                  <input v-model="itin.end_time" type="time" required
                    class="w-24 shrink-0 px-2 py-1.5 border border-[#e0e0e0] rounded-lg text-[12px] focus:outline-none focus:border-red-400 bg-white" />
                  <button type="button" @click="removeItinerary(idx)" class="text-[#ccc] hover:text-red-500 transition shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>
                <input v-model="itin.note" type="text" placeholder="Note (optional)"
                  class="w-full px-2.5 py-1.5 border border-dashed border-[#e0e0e0] rounded-lg text-[12px] text-[#999] focus:outline-none focus:border-red-300 bg-white" />
              </div>
            </div>
            <button type="button" @click="addItinerary"
              class="w-full py-2 border-2 border-dashed border-[#e0e0e0] rounded-xl text-[13px] text-[#999] hover:border-red-300 hover:text-red-400 transition">
              + Add Stop
            </button>
          </div>

          <!-- STEP 4: Passengers + Expenses -->
          <div v-if="currentStep === 4" class="flex flex-col gap-4">

            <!-- Pick Up Points table -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col gap-3">
              <h2 class="text-[14px] font-bold text-[#333] border-b border-[#f0f0f0] pb-2.5">Pick Up Points</h2>
              <div class="flex flex-col gap-2">
                <div v-for="(p, idx) in form.job_passengers" :key="idx"
                  class="bg-[#f8f9fa] rounded-xl border border-[#e8e8e8] px-3 py-2.5 flex flex-col gap-2">
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] font-bold text-[#bbb] uppercase w-10 shrink-0">{{ idx + 1 }}</span>
                    <input v-model="p.first_name" type="text" placeholder="First name *"
                      class="flex-1 min-w-0 px-2.5 py-1.5 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-red-400 bg-white" />
                    <input v-model="p.last_name" type="text" placeholder="Last name"
                      class="flex-1 min-w-0 px-2.5 py-1.5 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-red-400 bg-white" />
                    <input v-model="p.hotel_name" type="text" placeholder="Hotel"
                      class="flex-1 min-w-0 px-2.5 py-1.5 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-red-400 bg-white" />
                    <input v-model="p.pickup_time" type="time"
                      class="w-24 shrink-0 px-2 py-1.5 border border-[#e0e0e0] rounded-lg text-[12px] focus:outline-none focus:border-red-400 bg-white" />
                    <button type="button" @click="removePassenger(idx)" class="text-[#ccc] hover:text-red-500 transition shrink-0">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                    </button>
                  </div>
                  <input v-model="p.note" type="text" placeholder="Note (optional)"
                    class="w-full px-2.5 py-1.5 border border-dashed border-[#e0e0e0] rounded-lg text-[12px] text-[#999] focus:outline-none focus:border-red-300 bg-white" />
                </div>
              </div>
              <button type="button" @click="addPassenger"
                class="w-full py-2 border-2 border-dashed border-[#e0e0e0] rounded-xl text-[13px] text-[#999] hover:border-red-300 hover:text-red-400 transition">
                + Add Pick Up Point
              </button>
            </div>

            <!-- Expenses table -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col gap-3">
              <h2 class="text-[14px] font-bold text-[#333] border-b border-[#f0f0f0] pb-2.5">Expenses</h2>
              <div class="flex flex-col gap-2">
                <div v-for="(exp, idx) in form.job_expenses" :key="idx"
                  class="flex items-center gap-2">
                  <span class="text-[12px] text-[#bbb] font-medium w-4 shrink-0">{{ idx + 1 }}</span>
                  <input v-model="exp.item_name" type="text" placeholder="e.g. Entrance fee"
                    class="flex-1 min-w-0 px-3 py-2 border border-[#e0e0e0] rounded-lg text-[13px] focus:outline-none focus:border-red-400" />
                  <div class="flex items-center border border-[#e0e0e0] rounded-lg overflow-hidden shrink-0">
                    <span class="px-2 py-2 text-[12px] text-[#bbb] bg-[#f8f9fa] border-r border-[#e0e0e0]">฿</span>
                    <input v-model.number="exp.amount" type="number" min="0" placeholder="0"
                      class="w-20 px-2 py-2 text-[13px] focus:outline-none" />
                  </div>
                  <button type="button" @click="removeExpense(idx)" class="text-[#ccc] hover:text-red-500 transition shrink-0">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  </button>
                </div>
              </div>
              <button type="button" @click="addExpense"
                class="w-full py-2 border-2 border-dashed border-[#e0e0e0] rounded-xl text-[13px] text-[#999] hover:border-red-300 hover:text-red-400 transition">
                + Add Expense
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between mt-4">
            <span class="text-[12px] text-[#bbb]">Step {{ currentStep }} of {{ steps.length }}</span>
            <div class="flex gap-2">
              <button v-if="currentStep > 1" type="button" @click="currentStep--"
                class="px-5 py-2.5 border border-[#e0e0e0] text-[#666] rounded-lg text-[13px] font-medium hover:bg-[#f5f5f5] transition">
                ← Prev
              </button>
              <button v-if="currentStep < steps.length" type="button" @click="nextStep"
                class="px-6 py-2.5 bg-red-600 text-white rounded-lg text-[13px] font-semibold hover:bg-red-700 transition">
                Next →
              </button>
              <button v-else type="button" @click="submitJob" :disabled="submitting || !isVerified"
                class="px-6 py-2.5 bg-red-600 text-white rounded-lg text-[13px] font-semibold hover:bg-red-700 transition disabled:opacity-50">
                {{ submitting ? 'Creating…' : 'Create Tour' }}
              </button>
            </div>
          </div>
        </div>

        <!-- RIGHT — Summary -->
        <div class="flex flex-col gap-3 lg:sticky lg:top-4 order-first lg:order-last">

          <!-- Templates -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center justify-between">
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Templates</span>
              <button type="button" @click="saveAsTemplate" class="text-[11px] text-red-600 hover:text-red-700 font-medium">+ Save</button>
            </div>
            <div class="px-4 py-3 flex flex-col gap-1.5 max-h-40 overflow-y-auto">
              <p v-if="templates.length === 0" class="text-[12px] text-[#bbb] text-center py-2">No templates yet</p>
              <div v-for="tpl in templates" :key="tpl.id"
                class="flex items-center justify-between gap-2 px-2.5 py-1.5 bg-[#f8f9fa] rounded-lg hover:bg-[#f0f0f0] transition group cursor-pointer"
                @click="confirmLoadTemplate(tpl)">
                <div class="min-w-0">
                  <p class="text-[12px] font-medium text-[#222] truncate">{{ tpl.name }}</p>
                  <p class="text-[10px] text-[#bbb] truncate">{{ tpl.subtitle }}</p>
                </div>
                <button type="button" @click.stop="confirmDeleteTemplate(tpl)" class="text-[#ddd] hover:text-red-500 transition opacity-0 group-hover:opacity-100 shrink-0">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Live Summary -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0]">
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Summary</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-2 text-[13px]">
              <div class="flex justify-between gap-2">
                <span class="text-[#999] shrink-0">Title</span>
                <span class="text-[#222] font-medium text-right truncate">{{ form.job_title || '—' }}</span>
              </div>
              <div class="flex justify-between gap-2">
                <span class="text-[#999] shrink-0">Date</span>
                <span class="text-[#222] font-medium text-right text-[12px]">
                  {{ form.job_start_date ? formatDate(form.job_start_date) : '—' }}
                  <span v-if="form.job_end_date && form.job_end_date !== form.job_start_date"> → {{ formatDate(form.job_end_date) }}</span>
                </span>
              </div>
              <div class="flex justify-between gap-2">
                <span class="text-[#999] shrink-0">Price</span>
                <span class="text-[#222] font-medium">{{ form.job_price ? '฿' + Number(form.job_price).toLocaleString() : '—' }}</span>
              </div>
              <div class="flex justify-between gap-2">
                <span class="text-[#999] shrink-0">Vehicle</span>
                <span class="text-[#222] font-medium">VAN · {{ form.job_required_seat }} seats</span>
              </div>
              <div v-if="form.job_required_languages.length" class="flex justify-between gap-2">
                <span class="text-[#999] shrink-0">Languages</span>
                <span class="text-[#222] font-medium text-right text-[12px]">{{ form.job_required_languages.join(', ') }}</span>
              </div>

              <div v-if="form.job_itineraries.length" class="mt-1">
                <div class="text-[11px] font-bold text-[#bbb] uppercase tracking-wide mb-1.5">Schedule</div>
                <div class="overflow-x-auto">
                  <table class="w-full text-[11px]">
                    <thead>
                      <tr class="text-[10px] text-[#bbb] uppercase tracking-wide border-b border-[#f0f0f0]">
                        <th class="text-left pb-1 font-medium pr-2">#</th>
                        <th class="text-left pb-1 font-medium pr-2">Place</th>
                        <th class="text-left pb-1 font-medium pr-2">Date</th>
                        <th class="text-left pb-1 font-medium pr-2">Start</th>
                        <th class="text-left pb-1 font-medium pr-2">End</th>
                        <th class="text-left pb-1 font-medium">Note</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(itin, i) in form.job_itineraries" :key="i" class="border-b border-[#f8f8f8]">
                        <td class="py-1 pr-2 text-[#bbb]">{{ i + 1 }}</td>
                        <td class="py-1 pr-2 text-[#222] font-medium max-w-[80px] truncate">{{ itin.place_name || '—' }}</td>
                        <td class="py-1 pr-2 text-[#666]">{{ itin.itinerary_date ? formatDate(itin.itinerary_date) : '—' }}</td>
                        <td class="py-1 pr-2 text-[#666]">{{ itin.start_time || '—' }}</td>
                        <td class="py-1 pr-2 text-[#666]">{{ itin.end_time || '—' }}</td>
                        <td class="py-1 text-[#bbb] max-w-[60px] truncate">{{ itin.note || '—' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              <div class="h-px bg-[#f0f0f0]"></div>
              <div class="flex justify-between gap-2">
                <span class="text-[#999]">Pick Up Points</span>
                <span class="text-[#222] font-medium">{{ form.job_passengers.length }}</span>
              </div>
              <div class="flex justify-between gap-2">
                <span class="text-[#999]">Expenses</span>
                <span class="text-[#222] font-medium">
                  {{ form.job_expenses.length > 0 ? '฿' + form.job_expenses.reduce((s, e) => s + (Number(e.amount) || 0), 0).toLocaleString() : '—' }}
                </span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Modal: Load Template -->
    <div v-if="modal.show && modal.type === 'loadTemplate'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-xl p-6 w-72 mx-4" @click.stop>
        <h3 class="text-[15px] font-semibold text-[#111] mb-2">Load template?</h3>
        <p class="text-[13px] text-[#888] mb-5">Replace current form with "<strong>{{ modal.target?.name }}</strong>".</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-[13px] text-[#666] border border-[#e0e0e0] rounded-lg hover:bg-[#f5f5f5] transition">Cancel</button>
          <button type="button" @click="doLoadTemplate" class="px-4 py-2 text-[13px] font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Load</button>
        </div>
      </div>
    </div>

    <!-- Modal: Delete Template -->
    <div v-if="modal.show && modal.type === 'deleteTemplate'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-xl p-6 w-72 mx-4" @click.stop>
        <h3 class="text-[15px] font-semibold text-[#111] mb-2">Delete template?</h3>
        <p class="text-[13px] text-[#888] mb-5">Delete "<strong>{{ modal.target?.name }}</strong>"?</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-[13px] text-[#666] border border-[#e0e0e0] rounded-lg hover:bg-[#f5f5f5] transition">Cancel</button>
          <button type="button" @click="doDeleteTemplate" class="px-4 py-2 text-[13px] font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Delete</button>
        </div>
      </div>
    </div>

    <!-- Modal: Unsaved -->
    <div v-if="modal.show && modal.type === 'unsaved'" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
      <div class="bg-white rounded-2xl shadow-xl p-6 w-72 mx-4" @click.stop>
        <h3 class="text-[15px] font-semibold text-[#111] mb-2">Leave without saving?</h3>
        <p class="text-[13px] text-[#888] mb-5">Your unsaved changes will be lost.</p>
        <div class="flex gap-3 justify-end">
          <button type="button" @click="closeModal" class="px-4 py-2 text-[13px] text-[#666] border border-[#e0e0e0] rounded-lg hover:bg-[#f5f5f5] transition">Stay</button>
          <button type="button" @click="dismissModalAndLeave" class="px-4 py-2 text-[13px] font-semibold text-white bg-red-600 hover:bg-red-700 rounded-lg transition">Leave</button>
        </div>
      </div>
    </div>

  </AppLayout>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter, onBeforeRouteLeave } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'

const API_BASE = '/api'
const router = useRouter()
const DRAFT_KEY = 'create_job_draft'

const steps = ['General Info', 'Vehicle', 'Tour Schedule', 'Pick Up & Expenses']
const currentStep = ref(1)
const submitting = ref(false)
const isVerified = ref(true)

const languages = ref([])
const otherLanguage = ref('')
const showSuggestions = ref(false)
const langSuggestions = ref([])
const exactMatch = ref(false)

// Show 5 preset slots: selected custom langs replace unselected presets to keep total = 5
const displayLanguages = computed(() => {
  const presets = languages.value.slice(0, 5)
  const customSelected = form.job_required_languages.filter(
    l => !languages.value.slice(0, 5).find(db => db.language_name === l)
  )
  if (!customSelected.length) return presets
  // Remove unselected presets from the end to make room for custom ones
  const unselectedPresets = presets.filter(p => !form.job_required_languages.includes(p.language_name))
  const slotsToRemove = Math.min(customSelected.length, unselectedPresets.length)
  const trimmedPresets = presets.filter(p =>
    form.job_required_languages.includes(p.language_name) ||
    !unselectedPresets.slice(-slotsToRemove).find(u => u.language_id === p.language_id)
  )
  return trimmedPresets
})

const onLangInput = () => {
  const q = otherLanguage.value.trim().toLowerCase()
  showSuggestions.value = true
  if (!q) { langSuggestions.value = []; exactMatch.value = false; return }
  langSuggestions.value = languages.value.filter(l => l.language_name.toLowerCase().includes(q)).slice(0, 6)
  exactMatch.value = languages.value.some(l => l.language_name.toLowerCase() === q)
}

const hideSuggestions = () => setTimeout(() => { showSuggestions.value = false }, 150)

const selectSuggestion = (langName) => {
  if (!form.job_required_languages.includes(langName))
    form.job_required_languages.push(langName)
  otherLanguage.value = ''
  showSuggestions.value = false
}

const addTopSuggestion = () => {
  if (langSuggestions.value.length) selectSuggestion(langSuggestions.value[0].language_name)
  else addOtherLanguage()
}

const fetchLanguages = async () => {
  try {
    const res = await fetch(`${API_BASE}/languages`)
    if (res.ok) languages.value = await res.json()
  } catch {}
}

const addOtherLanguage = async () => {
  const name = otherLanguage.value.trim()
  if (!name || form.job_required_languages.includes(name)) { otherLanguage.value = ''; return }
  try {
    const res = await fetch(`${API_BASE}/languages`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language_name: name }),
    })
    if (res.ok) {
      const lang = await res.json()
      if (!languages.value.find(l => l.language_id === lang.language_id)) {
        languages.value.push(lang)
        languages.value.sort((a, b) => a.language_name.localeCompare(b.language_name))
      }
      form.job_required_languages.push(lang.language_name)
    }
  } catch {}
  otherLanguage.value = ''
}

const defaultForm = () => ({
  job_title: '',
  job_description: '',
  job_start_date: '',
  job_end_date: '',
  job_required_vehicle_type: 'VAN',
  job_required_seat: 9,
  job_price: null,
  job_required_languages: [],
  job_itineraries: [],
  job_passengers: [],
  job_expenses: [],
})

const form = reactive(defaultForm())
const isDirty = ref(false)
const formHistory = ref([])

const saveHistory = () => {
  formHistory.value.push(JSON.parse(JSON.stringify(form)))
  if (formHistory.value.length > 20) formHistory.value.shift()
}

const undo = () => {
  if (!formHistory.value.length) return
  const prev = formHistory.value.pop()
  Object.assign(form, prev)
}

const syncItineraryDates = () => {
  if (form.job_start_date) {
    form.job_itineraries.forEach(itin => {
      if (!itin.itinerary_date) itin.itinerary_date = form.job_start_date
    })
  }
}

watch(form, () => {
  isDirty.value = true
}, { deep: true })

const DEFAULT_TEMPLATES = [
  {
    id: 'tpl_fullday', name: 'Full Day Temple Tour', subtitle: 'VAN · English, Thai',
    data: {
      job_title: 'Chiang Mai Full Day Temple Tour', job_required_vehicle_type: 'VAN', job_required_seat: 9,
      job_required_languages: ['English', 'Thai'],
      job_itineraries: [
        { place_name: 'Doi Suthep Temple', itinerary_date: '', start_time: '08:00', end_time: '10:00', note: '', sequence: 1 },
        { place_name: 'Pha Lat Temple', itinerary_date: '', start_time: '10:30', end_time: '12:00', note: '', sequence: 2 },
      ],
      job_passengers: [], job_expenses: [{ item_name: 'Entrance fee — Doi Suthep', amount: 30, sequence: 1 }],
    },
  },
  {
    id: 'tpl_night', name: 'Night Market Tour', subtitle: 'VAN · English, Thai',
    data: {
      job_title: 'Chiang Mai Night Market Tour', job_required_vehicle_type: 'VAN', job_required_seat: 9,
      job_required_languages: ['English', 'Thai'],
      job_itineraries: [
        { place_name: 'Warorot Market', itinerary_date: '', start_time: '17:00', end_time: '18:30', note: '', sequence: 1 },
        { place_name: 'Sunday Walking Street', itinerary_date: '', start_time: '19:00', end_time: '21:00', note: '', sequence: 2 },
      ],
      job_passengers: [], job_expenses: [],
    },
  },
]

const em_id = localStorage.getItem('em_id')
const templates = ref([])

const saveTemplatesToDB = async (list) => {
  try {
    await fetch(`${API_BASE}/employers/${em_id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_templates: JSON.stringify(list) }),
    })
  } catch {}
}

const modal = reactive({ show: false, type: '', target: null })
const openModal = (type, target = null) => { modal.show = true; modal.type = type; modal.target = target }
const closeModal = () => { modal.show = false; modal.type = ''; modal.target = null }

const confirmLoadTemplate = (tpl) => openModal('loadTemplate', tpl)
const confirmDeleteTemplate = (tpl) => openModal('deleteTemplate', tpl)

const doLoadTemplate = () => {
  Object.assign(form, defaultForm(), modal.target.data)
  if (form.job_start_date) syncItineraryDates()
  currentStep.value = 1; isDirty.value = true; closeModal()
}

const doDeleteTemplate = () => {
  templates.value = templates.value.filter(t => t.id !== modal.target.id)
  saveTemplatesToDB(templates.value); closeModal()
}

const saveAsTemplate = () => {
  const name = form.job_title?.trim() || 'Untitled Template'
  templates.value.unshift({
    id: 'tpl_' + Date.now(), name,
    subtitle: ['VAN', ...form.job_required_languages].join(' · ') || 'Custom',
    data: {
      job_title: form.job_title, job_required_vehicle_type: 'VAN',
      job_required_seat: form.job_required_seat,
      job_required_languages: [...form.job_required_languages],
      job_itineraries: form.job_itineraries.map(i => ({ ...i })),
      job_passengers: form.job_passengers.map(p => ({ ...p })),
      job_expenses: form.job_expenses.map(e => ({ ...e })),
    },
  })
  saveTemplatesToDB(templates.value)
}

let pendingNavResolve = null
onBeforeRouteLeave((_to, _from, next) => {
  if (!isDirty.value) { next(); return }
  openModal('unsaved'); pendingNavResolve = next
})
const cancelAndLeave = () => {
  if (isDirty.value) {
    openModal('unsaved')
    pendingNavResolve = () => router.push('/my-tours')
  } else {
    router.push('/my-tours')
  }
}

const dismissModalAndLeave = () => {
  isDirty.value = false
  localStorage.removeItem(DRAFT_KEY)
  closeModal()
  if (pendingNavResolve) { pendingNavResolve(); pendingNavResolve = null }
}

const toggleLanguage = (lang) => {
  const idx = form.job_required_languages.indexOf(lang)
  if (idx > -1) form.job_required_languages.splice(idx, 1)
  else form.job_required_languages.push(lang)
}

const nextStep = () => { if (currentStep.value < steps.length) currentStep.value++ }
const prevStep = () => { if (currentStep.value > 1) currentStep.value--; else router.back() }

const addItinerary = () => {
  saveHistory()
  form.job_itineraries.push({
    place_name: '', itinerary_date: form.job_start_date || '',
    start_time: '', end_time: '', note: '', sequence: form.job_itineraries.length + 1
  })
}
const removeItinerary = (idx) => { saveHistory(); form.job_itineraries.splice(idx, 1) }
const addPassenger = () => { saveHistory(); form.job_passengers.push({ first_name: '', last_name: '', hotel_name: '', pickup_time: '', note: '' }) }
const removePassenger = (idx) => { saveHistory(); form.job_passengers.splice(idx, 1) }
const addExpense = () => { saveHistory(); form.job_expenses.push({ item_name: '', amount: 0, sequence: form.job_expenses.length + 1 }) }
const removeExpense = (idx) => { saveHistory(); form.job_expenses.splice(idx, 1) }

const formatDate = (d) => {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const generateId = () => 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
  const r = Math.random() * 16 | 0; return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16)
})

const submitJob = async () => {
  if (!form.job_title?.trim()) { alert('Please fill in Tour Title'); currentStep.value = 1; return }
  if (!form.job_start_date) { alert('Please fill in Start Date'); currentStep.value = 1; return }
  if (!form.job_end_date) { alert('Please fill in End Date'); currentStep.value = 1; return }
  if (!form.job_price) { alert('Please fill in Price'); currentStep.value = 1; return }
  for (const [i, itin] of form.job_itineraries.entries()) {
    if (!itin.start_time || !itin.end_time) {
      alert(`Please fill in Start and End time for Stop ${i + 1}`); currentStep.value = 3; return
    }
  }
  submitting.value = true
  try {
    const payload = { em_id, ...form }
    const res = await fetch(`${API_BASE}/tours`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload),
    })
    let data = {}
    const text = await res.text()
    if (text) { try { data = JSON.parse(text) } catch {} }
    if (res.ok) { isDirty.value = false; localStorage.removeItem(DRAFT_KEY); router.push('/my-tours') }
    else alert('Error: ' + (data.detail || data.error || data.message || 'Unknown error'))
  } catch (e) { alert('Error: ' + e.message) }
  finally { submitting.value = false }
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/employers/${em_id}`)
    const data = await res.json()
    isVerified.value = data.em_verify_status === 'VERIFIED'
    if (data.job_templates) {
      const parsed = typeof data.job_templates === 'string' ? JSON.parse(data.job_templates) : data.job_templates
      templates.value = Array.isArray(parsed) ? parsed : [...DEFAULT_TEMPLATES]
    } else { templates.value = [...DEFAULT_TEMPLATES] }
  } catch { isVerified.value = true; templates.value = [...DEFAULT_TEMPLATES] }

  await fetchLanguages()
})
</script>