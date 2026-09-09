<template>
  <AppLayout>
    <div class="px-5 pb-8">

      <!-- Top bar: Back only -->
      <div class="flex items-center justify-between flex-wrap gap-2 py-3 mb-5">
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

      <!-- Floating Matching / Applications toolbar - fixed top-right -->
      <div v-if="job" class="fixed top-20 right-6 z-40 flex items-center gap-2">
        <button
          class="group flex items-center justify-center gap-2 w-[150px] px-3 py-2 rounded-full text-[13px] font-bold bg-white border-2 border-violet-500 text-violet-700 hover:bg-violet-50 shadow-md transition-colors cursor-pointer"
          @click="showMatchingModal = true">
          <span class="w-6 h-6 rounded-full bg-violet-100 flex items-center justify-center shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          </span>
          Matching
          <span v-if="suggestedMatches.length" class="inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-violet-600 text-white text-[10px] font-bold">{{ suggestedMatches.length }}</span>
        </button>

        <button
          class="group flex items-center justify-center gap-2 w-[150px] px-3 py-2 rounded-full text-[13px] font-bold bg-white border-2 border-amber-500 text-amber-700 hover:bg-amber-50 shadow-md transition-colors cursor-pointer"
          @click="showApplicationModal = true">
          <span class="w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center shrink-0">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          </span>
          Applications
          <span v-if="applications.length" class="inline-flex items-center justify-center min-w-[18px] h-[18px] px-1 rounded-full bg-amber-600 text-white text-[10px] font-bold">{{ applications.length }}</span>
        </button>
      </div>

      <!-- Floating Edit / Cancel toolbar - fixed bottom-right -->
      <div v-if="job" class="fixed bottom-6 right-6 z-40 flex items-center gap-2">
        <template v-if="!editing">
          <button v-if="canCancel" @click="confirmCancel" :disabled="cancelling"
            class="flex items-center justify-center w-[140px] px-3 py-2.5 text-[13px] font-medium rounded-full bg-white border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] shadow-md transition disabled:opacity-50">
            {{ cancelling ? 'Cancelling…' : 'Cancel Tour' }}
          </button>
          <button v-if="canEdit" @click="startEditing"
            class="flex items-center justify-center gap-1.5 w-[140px] px-3 py-2.5 text-[13px] font-semibold rounded-full bg-white border-2 border-red-500 text-red-600 hover:bg-red-50 shadow-md transition">
            <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit Tour
          </button>
        </template>
        <template v-else>
          <button @click="cancelEditing"
            class="flex items-center justify-center w-[140px] px-3 py-2.5 text-[13px] font-medium rounded-full bg-white border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] shadow-md transition">
            Discard
          </button>
          <button @click="saveJob" :disabled="submitting"
            class="flex items-center justify-center w-[140px] px-3 py-2.5 text-[13px] font-semibold rounded-full bg-red-600 text-white hover:bg-red-700 shadow-md transition disabled:opacity-50">
            {{ submitting ? 'Saving…' : 'Save Changes' }}
          </button>
        </template>
      </div>

      <!-- Loading -->
      <div v-if="loading">
        <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-6 mb-4">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div class="flex-1 flex flex-col gap-2.5">
              <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
              <div class="animate-pulse bg-[#ebebeb] h-7 w-72 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3.5 w-36 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-full max-w-lg rounded"></div>
            </div>
            <div class="shrink-0 flex flex-col items-end gap-2">
              <div class="animate-pulse bg-[#ebebeb] h-2.5 w-10 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-9 w-32 rounded"></div>
            </div>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-[#f0f0f0]">
            <div v-for="i in 4" :key="i" class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 flex flex-col gap-1.5">
              <div class="animate-pulse bg-[#ebebeb] h-2 w-14 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-4 w-20 rounded"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="mt-20 text-center">
        <p class="text-red-500 font-medium mb-4">{{ error }}</p>
        <button @click="fetchJob" class="px-5 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700 transition">Retry</button>
      </div>

      <!-- Content -->
      <template v-else-if="job">

        <!-- Hero Card -->
        <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-6 mb-4 hover:shadow-md transition-shadow">
          <div class="flex items-start justify-between gap-4 mb-5">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2">
                <span class="badge" :class="job.job_status?.toLowerCase()">{{ statusLabel(job.job_status) }}</span>
                <span v-if="editing" class="badge" style="background:#fef3c7;color:#92400e;border:1px solid #fde68a">Editing</span>
              </div>
              <template v-if="editing">
                <input v-model="form.job_title" type="text" class="field-input text-[18px] font-bold w-full mb-1.5" placeholder="Tour Title *" />
              </template>
              <template v-else>
                <h1 class="text-[20px] font-bold text-[#111] leading-tight mb-1.5">{{ job.job_title }}</h1>
              </template>
              <p v-if="!editing && job.job_description" class="text-[13px] text-[#888] leading-relaxed mt-2 max-w-2xl">{{ job.job_description }}</p>
              <textarea v-if="editing" v-model="form.job_description" rows="2" class="field-input w-full mt-2 text-[13px]" placeholder="Description"></textarea>
            </div>
            <div class="text-right shrink-0">
              <div class="text-[11px] text-[#bbb] tracking-wide font-medium mb-1">Price (THB)</div>
              <template v-if="editing">
                <input v-model.number="form.job_price" type="number" class="field-input text-right text-[18px] font-bold w-32" placeholder="0" />
              </template>
              <template v-else>
                <div class="text-[26px] font-bold text-[#111]">{{ job.job_price ? "฿" + Number(job.job_price).toLocaleString() : "–" }}</div>
              </template>
            </div>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-[#f0f0f0]">
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 transition-colors">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Start Date</div>
              <template v-if="editing">
                <input v-model="form.job_start_date" type="date" class="field-input text-[13px] font-semibold w-full" />
              </template>
              <div v-else class="text-[14px] font-semibold text-[#222]">{{ formatDate(job.job_start_date) }}</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 transition-colors">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">End Date</div>
              <template v-if="editing">
                <input v-model="form.job_end_date" type="date" class="field-input text-[13px] font-semibold w-full" />
              </template>
              <div v-else class="text-[14px] font-semibold text-[#222]">{{ formatDate(job.job_end_date) }}</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 transition-colors">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Vehicle</div>
              <div class="text-[14px] font-semibold text-[#222]">VAN</div>
            </div>
            <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 transition-colors">
              <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Seats Required</div>
              <template v-if="editing">
                <div class="flex items-center gap-2 mt-0.5">
                  <button type="button" @click="form.job_required_seat = Math.max(1, form.job_required_seat - 1)"
                    class="w-7 h-7 rounded-md border border-[#e0e0e0] text-[#666] hover:bg-[#ebebeb] transition text-base font-medium flex items-center justify-center shrink-0">−</button>
                  <span class="text-[15px] font-bold text-[#222] w-6 text-center">{{ form.job_required_seat }}</span>
                  <button type="button" @click="form.job_required_seat = Math.min(13, form.job_required_seat + 1)"
                    class="w-7 h-7 rounded-md border border-[#e0e0e0] text-[#666] hover:bg-[#ebebeb] transition text-base font-medium flex items-center justify-center shrink-0">+</button>
                </div>
              </template>
              <div v-else class="text-[14px] font-semibold text-[#222]">{{ job.job_required_seat || "–" }}</div>
            </div>
          </div>
        </div>

        <!-- 2-col layout -->
        <div class="grid gap-4 grid-cols-1 lg:grid-cols-[320px_1fr] items-start">

          <!-- LEFT -->
          <div class="flex flex-col gap-3">

            <!-- Area Required -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Pickup Area</span>
              </div>

              <!-- View mode -->
              <div v-if="!editing" class="px-4 py-4 flex flex-wrap gap-1.5">
                <span v-if="job.job_area_name" class="info-tag area">{{ job.job_area_name }}</span>
                <span v-else class="text-[13px] text-[#bbb]">None specified</span>
              </div>

              <!-- Edit mode -->
              <div v-else class="px-4 py-4">
                <select v-model="form.job_area_id" class="field-input text-[13px] w-full">
                  <option :value="null">None specified</option>
                  <option v-for="a in areas" :key="a.area_id" :value="a.area_id">{{ a.area_name }}</option>
                </select>
              </div>
            </div>

            <!-- Languages Required -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Languages Required</span>
              </div>

              <!-- View mode -->
              <div v-if="!editing" class="px-4 py-4 flex flex-wrap gap-1.5">
                <span v-for="lang in job.job_required_languages" :key="lang" class="info-tag language">{{ lang }}</span>
                <span v-if="!job.job_required_languages?.length" class="text-[13px] text-[#bbb]">None specified</span>
              </div>

              <!-- Edit mode -->
              <div v-else class="px-4 py-4">
                <div class="flex flex-wrap gap-2">
                  <button v-for="lang in languages.slice(0, 5)" :key="lang.language_id" type="button"
                    @click="toggleLanguage(lang.language_name)"
                    :class="['px-3 py-1 rounded-full text-[12px] font-medium border transition-colors',
                      form.job_required_languages.includes(lang.language_name)
                        ? 'bg-red-600 text-white border-red-600'
                        : 'bg-white text-gray-600 border-gray-300 hover:border-red-400']">
                    {{ lang.language_name }}
                  </button>
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
                <!-- Custom (non-preset) language tags -->
                <div v-if="form.job_required_languages.some(l => !languages.slice(0,5).find(db => db.language_name === l))" class="flex flex-wrap gap-1.5 mt-2">
                  <span v-for="lang in form.job_required_languages.filter(l => !languages.slice(0,5).find(db => db.language_name === l))" :key="lang"
                    class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[12px] bg-red-600 text-white">
                    {{ lang }}<button type="button" @click="toggleLanguage(lang)" class="hover:opacity-70 ml-0.5">✕</button>
                  </span>
                </div>
              </div>
            </div>

            <!-- Pickup Areas -->
            <div v-if="pickups.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Pickup Areas</span>
              </div>
              <div class="px-4 py-4 flex flex-wrap gap-1.5">
                <span v-for="p in pickups" :key="p.area_id" class="info-tag area">{{ p.area_name }}</span>
              </div>
            </div>

            <!-- Assigned Driver -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Assigned Driver</span>
              </div>
              <div class="px-4 py-4">
                <div v-if="job.driver_name" class="flex items-center gap-2.5">
                  <div class="w-8 h-8 rounded-full text-sm font-bold flex items-center justify-center shrink-0" :style="avatarStyle(job.selected_fl_id, job.driver_name)">{{ initials2(job.driver_name) }}</div>
                  <div>
                    <div class="text-[14px] font-medium text-[#222]">{{ job.driver_name }}</div>
                    <div v-if="job.driver_phone" class="text-[12px] text-[#999]">{{ job.driver_phone }}</div>
                  </div>
                </div>
                <span v-else class="text-[13px] text-[#bbb]">Not assigned</span>
              </div>
            </div>

            <!-- Timeline -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Timeline</span>
              </div>
              <div class="px-4 py-3 flex flex-col gap-3">
                <div class="flex items-center gap-2.5">
                  <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                  <div>
                    <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Created</div>
                    <div class="text-[13px] font-medium text-[#222]">{{ formatDateTime(job.job_created_at) }}</div>
                  </div>
                </div>
                <div class="flex items-center gap-2.5">
                  <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/></svg>
                  <div>
                    <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last Updated</div>
                    <div class="text-[13px] font-medium text-[#222]">{{ formatDateTime(job.job_updated_at) }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Expenses -->
            <div v-if="editing || job.job_expenses?.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path stroke-linecap="round" stroke-linejoin="round" d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Expenses</span>
              </div>
              <div class="px-4 py-4">
                <template v-if="!editing">
                  <div class="flex flex-col divide-y divide-[#f0f0f0]">
                    <div v-for="(exp, idx) in sortedExpenses" :key="idx" class="flex items-center justify-between py-2 transition-colors px-1 rounded">
                      <span class="text-[13px] text-[#444]">{{ exp.item_name }}</span>
                      <span class="text-[13px] font-semibold text-[#222]">{{ exp.amount ? "฿" + Number(exp.amount).toLocaleString() : "–" }}</span>
                    </div>
                  </div>
                  <div class="flex items-center justify-between pt-3 mt-1 border-t-2 border-[#eee]">
                    <span class="text-[13px] font-bold text-[#111]">Total</span>
                    <span class="text-[15px] font-bold text-[#111]">฿{{ Number(sortedExpenses.reduce((s, e) => s + Number(e.amount || 0), 0)).toLocaleString() }}</span>
                  </div>
                </template>
                <template v-else>
                  <div v-for="(exp, idx) in form.job_expenses" :key="idx" class="grid gap-2 mb-2 items-end" style="grid-template-columns: 1fr 1fr auto">
                    <div><label class="field-label">Item Name</label><input v-model="exp.item_name" type="text" class="field-input" /></div>
                    <div><label class="field-label">Amount (THB)</label><input v-model.number="exp.amount" type="number" class="field-input" /></div>
                    <button type="button" @click="form.job_expenses.splice(idx, 1)"
                      class="mb-0.5 p-2 bg-red-50 text-red-400 rounded-lg hover:bg-red-100 transition">✕</button>
                  </div>
                  <button type="button" @click="form.job_expenses.push({ item_name: '', amount: 0 })"
                    class="px-3 py-1.5 bg-[#f5f5f5] text-[#555] rounded-lg text-xs hover:bg-[#ebebeb] transition">+ Add Expense</button>
                </template>
              </div>
            </div>

            <!-- Payment -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Payment</span>
              </div>
              <div class="px-4 py-4 flex flex-col gap-3">

                <!-- Current payment -->
                <template v-if="payment">
                  <div class="rounded-xl border border-[#e8e8e8] bg-[#f8f9fa] hover:border-[#ddd] hover:bg-[#f5f5f5] transition-colors overflow-hidden">
                    <div class="px-4 py-3 flex items-center justify-between">
                      <div class="flex items-center gap-2">
                        <div class="w-7 h-7 rounded-full text-xs font-bold flex items-center justify-center shrink-0" :style="avatarStyle(payment.fl_id, payment.driver_name)">{{ initials2(payment.driver_name || '?') }}</div>
                        <span class="text-[13px] font-medium text-[#222]">{{ payment.driver_name || '-' }}</span>
                      </div>
                      <span class="payment-badge" :class="payment.payment_status?.toLowerCase()">{{ payment.payment_status }}</span>
                    </div>
                    <div v-if="payment.paid_at || payment.confirmed_at || payment.reject_reason" class="px-4 pb-3 flex flex-col gap-1">
                      <div v-if="payment.paid_at" class="text-[11px] text-[#888]">Paid: {{ formatDateTime(payment.paid_at) }}</div>
                      <div v-if="payment.confirmed_at" class="text-[11px] text-[#888]">Confirmed: {{ formatDateTime(payment.confirmed_at) }}</div>
                      <div v-if="payment.reject_reason" class="text-[11px] text-red-600">Reason: {{ payment.reject_reason }}</div>
                    </div>
                    <div v-if="payment.slip_url" class="border-t border-[#eee]">
                      <div class="px-4 py-2 text-[10px] text-[#aaa] uppercase tracking-wide font-medium">Payment Slip</div>
                      <div class="h-[160px] bg-[#f0f0f0] overflow-hidden cursor-pointer hover:opacity-90 transition-opacity" @click="slipModalUrl = payment.slip_url">
                        <img :src="payment.slip_url" class="w-full h-full object-contain" />
                      </div>
                    </div>
                  </div>

                  <!-- Reupload when REJECTED -->
                  <template v-if="payment.payment_status === 'REJECTED'">
                    <div class="border border-red-100 rounded-xl p-4 bg-red-50">
                      <p class="text-[12px] font-semibold text-red-600 mb-2">Re-upload Slip</p>
                      <div class="border-2 border-dashed border-red-200 rounded-xl p-4 text-center hover:border-red-400 transition-colors cursor-pointer relative"
                        @click="$refs.reuploadInput.click()" @dragover.prevent @drop.prevent="onReuploadDrop">
                        <input ref="reuploadInput" type="file" accept="image/*" class="hidden" @change="onReuploadFileChange" />
                        <div v-if="!reuploadPreview">
                          <svg class="w-7 h-7 text-red-300 mx-auto mb-1.5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4-4 4 4 4-8 4 8"/><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
                          <p class="text-[13px] text-[#999]">Click to select a new slip</p>
                        </div>
                        <div v-else class="relative">
                          <img :src="reuploadPreview" class="max-h-32 mx-auto rounded-lg object-contain" />
                          <button type="button" @click.stop="clearReupload" class="absolute top-1 right-1 w-6 h-6 bg-red-600 text-white rounded-full text-xs flex items-center justify-center hover:bg-red-700">✕</button>
                        </div>
                      </div>
                      <button v-if="reuploadPreview" @click="submitReupload" :disabled="paymentSubmitting"
                        class="mt-2 w-full py-2 bg-red-600 text-white text-[13px] font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50">
                        {{ paymentSubmitting ? 'Uploading…' : 'Submit New Slip' }}
                      </button>
                    </div>
                  </template>
                </template>

                <!-- No payment yet -->
                <template v-else>
                  <p class="text-[13px] text-[#bbb]">No payment submitted yet.</p>
                  <div class="border-2 border-dashed border-[#e0e0e0] rounded-xl p-4 text-center hover:border-red-300 transition-colors cursor-pointer relative"
                    @click="$refs.slipInput.click()" @dragover.prevent @drop.prevent="onSlipDrop">
                    <input ref="slipInput" type="file" accept="image/*" class="hidden" @change="onSlipFileChange" />
                    <div v-if="!slipPreview">
                      <svg class="w-8 h-8 text-[#ccc] mx-auto mb-2" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4-4 4 4 4-8 4 8"/><rect x="3" y="3" width="18" height="18" rx="2"/></svg>
                      <p class="text-[13px] text-[#999]">Click or drag & drop file here</p>
                      <p class="text-[11px] text-[#ccc] mt-1">JPEG, PNG, WebP</p>
                    </div>
                    <div v-else class="relative">
                      <img :src="slipPreview" class="max-h-40 mx-auto rounded-lg object-contain" />
                      <button type="button" @click.stop="clearSlip" class="absolute top-1 right-1 w-6 h-6 bg-red-600 text-white rounded-full text-xs flex items-center justify-center hover:bg-red-700">✕</button>
                    </div>
                  </div>
                  <button v-if="slipPreview" @click="submitPayment" :disabled="paymentSubmitting"
                    class="w-full py-2 bg-red-600 text-white text-[13px] font-semibold rounded-lg hover:bg-red-700 transition disabled:opacity-50">
                    {{ paymentSubmitting ? 'Uploading…' : 'Submit Payment Slip' }}
                  </button>
                </template>

                <!-- Payment history -->
                <div v-if="paymentHistory.length">
                  <button class="flex items-center gap-1.5 text-[11px] text-[#999] hover:text-[#555] transition-colors mt-1 mb-2"
                    @click="showPaymentHistory = !showPaymentHistory">
                    <svg class="w-3 h-3 transition-transform" :class="showPaymentHistory ? 'rotate-90' : ''" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"/></svg>
                    {{ showPaymentHistory ? 'Hide' : 'Show' }} payment history ({{ paymentHistory.length }})
                  </button>
                  <div v-if="showPaymentHistory" class="flex flex-col gap-2">
                    <div v-for="pay in paymentHistory" :key="pay.payment_id"
                      class="rounded-xl border border-[#f0e0e0] bg-[#fff8f8] overflow-hidden opacity-70">
                      <div class="px-4 py-2.5 flex items-center justify-between">
                        <div class="flex items-center gap-2">
                          <div class="w-6 h-6 rounded-full text-xs font-bold flex items-center justify-center shrink-0" :style="avatarStyle(pay.fl_id, pay.driver_name)">{{ initials2(pay.driver_name || '?') }}</div>
                          <span class="text-[12px] text-[#666]">{{ pay.driver_name }}</span>
                        </div>
                        <span class="payment-badge" :class="pay.payment_status?.toLowerCase()">{{ pay.payment_status }}</span>
                      </div>
                      <div class="px-4 pb-2.5 flex flex-col gap-0.5">
                        <div v-if="pay.paid_at" class="text-[10px] text-[#aaa]">Paid: {{ formatDateTime(pay.paid_at) }}</div>
                        <div v-if="pay.reject_reason" class="text-[10px] text-red-400">Reason: {{ pay.reject_reason }}</div>
                      </div>
                      <div v-if="pay.slip_url" class="border-t border-[#f5e0e0]">
                        <div class="px-4 py-2 text-[10px] text-[#aaa] uppercase tracking-wide font-medium">Payment Slip</div>
                        <div class="h-[160px] bg-[#f8f0f0] overflow-hidden cursor-pointer hover:opacity-90 transition-opacity" @click="slipModalUrl = pay.slip_url">
                          <img :src="pay.slip_url" class="w-full h-full object-contain" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>

            <!-- Review from employer to freelancer -->
            <div v-if="jobReview" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Your Review</span>
                <div class="ml-auto flex items-center gap-0.5">
                  <span v-for="s in 5" :key="s" class="text-[13px]" :class="s <= jobReview.rating ? 'text-[#f9a825]' : 'text-[#e0e0e0]'">★</span>
                </div>
              </div>
              <div class="px-4 py-4">
                <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-1">To {{ jobReview.driver_name }}</div>
                <p v-if="jobReview.comment" class="text-[13px] text-[#444] leading-relaxed">{{ jobReview.comment }}</p>
                <p v-else class="text-[13px] text-[#bbb] italic">No comment</p>
                <div class="text-[11px] text-[#bbb] mt-2">{{ formatDate(jobReview.reviewed_at) }}</div>
              </div>
            </div>

            <!-- Review from freelancer to employer -->
            <div v-if="emReview" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Freelancer Review</span>
              </div>
              <div class="p-4">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-[13px] font-semibold text-[#222]">{{ emReview.driver_name }}</span>
                  <div class="flex items-center gap-0.5">
                    <svg v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= emReview.rating ? 'text-[#f9a825]' : 'text-[#ddd]'" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                    <span class="text-[12px] font-bold text-[#333] ml-1">{{ emReview.rating }}.0</span>
                  </div>
                </div>
                <p v-if="emReview.comment" class="text-[13px] text-[#555] leading-relaxed">{{ emReview.comment }}</p>
                <p v-else class="text-[13px] text-[#bbb] italic">No comment</p>
                <div class="text-[12px] text-[#bbb] mt-1.5">{{ formatDateTime(emReview.reviewed_at) }}</div>
              </div>
            </div>

          </div>

          <!-- RIGHT -->
          <div class="flex flex-col gap-3">

            <!-- Tour Schedule -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Tour Schedule</span>
              </div>
              <div class="px-4 py-4 flex flex-col gap-2">
                <template v-if="!editing">
                  <div v-for="(item, i) in job.job_itineraries" :key="i"
                    class="flex items-center px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] transition-colors">
                    <div class="w-6 h-6 rounded-full bg-[#f3e5f5] text-[#7b1fa2] text-[11px] font-bold flex items-center justify-center shrink-0 mr-3">{{ i + 1 }}</div>
                    <div class="min-w-0" style="flex: 3">
                      <div class="text-[13px] font-medium text-[#222]">{{ item.place_name }}</div>
                      <div v-if="item.note" class="text-[11px] text-[#999] mt-0.5">{{ item.note }}</div>
                    </div>
                    <div class="flex justify-center" style="flex: 2">
                      <span v-if="item.start_time || item.end_time" class="text-[12px] font-bold text-[#7b1fa2] bg-[#f3e5f5] px-2 py-0.5 rounded-md whitespace-nowrap">{{ item.start_time }} - {{ item.end_time }}</span>
                    </div>
                    <span v-if="item.itinerary_date" class="text-[12px] text-[#aaa] whitespace-nowrap shrink-0 w-20 text-left">{{ formatDate(item.itinerary_date) }}</span>
                  </div>
                  <p v-if="!job.job_itineraries?.length" class="text-[13px] text-[#bbb] px-1">No stops added</p>
                </template>
                <template v-else>
                  <div v-for="(item, idx) in form.job_itineraries" :key="idx"
                    class="grid items-end gap-2 mb-2"
                    style="grid-template-columns: 2fr 1fr 1fr 1fr auto">
                    <div><label class="field-label">Stop / Activity</label><input v-model="item.place_name" type="text" class="field-input" /></div>
                    <div><label class="field-label">Start</label><input v-model="item.start_time" type="time" class="field-input" /></div>
                    <div><label class="field-label">End</label><input v-model="item.end_time" type="time" class="field-input" /></div>
                    <div><label class="field-label">Date</label><input v-model="item.itinerary_date" type="date" class="field-input" /></div>
                    <button type="button" @click="form.job_itineraries.splice(idx, 1)"
                      class="mb-0.5 p-2 bg-red-50 text-red-400 rounded-lg hover:bg-red-100 transition">✕</button>
                    <div class="col-span-full"><label class="field-label">Note</label><input v-model="item.note" type="text" class="field-input" placeholder="Optional note" /></div>
                  </div>
                  <button type="button" @click="form.job_itineraries.push({ place_name: '', itinerary_date: '', start_time: '', end_time: '', note: '' })"
                    class="w-full px-4 py-2 bg-[#f5f5f5] text-[#555] rounded-lg text-sm hover:bg-[#ebebeb] transition mt-1">+ Add Stop</button>
                </template>
              </div>
            </div>

            <!-- Pick Up Points -->
            <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
              <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/></svg>
                <span class="text-[13px] font-bold text-[#444] tracking-wide">Pick Up Points</span>
                <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ job.job_passengers?.length ?? 0 }}</span>
              </div>
              <div class="px-4 py-4 flex flex-col gap-2">
                <template v-if="!editing">
                  <div v-for="(p, i) in job.job_passengers" :key="i"
                    class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] transition-colors">
                    <div class="w-6 h-6 rounded-full bg-[#e8f5e9] text-[#2e7d32] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
                    <div class="flex-1 min-w-0">
                      <div class="text-[13px] font-medium text-[#222]">{{ p.first_name }} {{ p.last_name }}</div>
                      <div class="text-[11px] text-[#999] mt-0.5">
                        <span v-if="p.hotel_name">{{ p.hotel_name }}</span>
                        <span v-if="p.hotel_name && p.note" class="mx-1 text-[#ddd]">·</span>
                        <span v-if="p.note">{{ p.note }}</span>
                      </div>
                    </div>
                    <span v-if="p.pickup_time" class="text-[12px] font-bold text-[#1976d2] bg-[#e3f2fd] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ formatPickupTime(p.pickup_time) }}</span>
                  </div>
                  <p v-if="!job.job_passengers?.length" class="text-[13px] text-[#bbb] px-1">No passengers added</p>
                </template>
                <template v-else>
                  <div v-for="(p, idx) in form.job_passengers" :key="idx" class="grid gap-2 mb-3 items-end" style="grid-template-columns: 1fr 1fr 1fr 1fr auto">
                    <div><label class="field-label">First Name</label><input v-model="p.first_name" type="text" class="field-input" /></div>
                    <div><label class="field-label">Last Name</label><input v-model="p.last_name" type="text" class="field-input" /></div>
                    <div><label class="field-label">Hotel</label><input v-model="p.hotel_name" type="text" class="field-input" /></div>
                    <div><label class="field-label">Pickup Time</label><input v-model="p.pickup_time" type="time" class="field-input" /></div>
                    <button type="button" @click="form.job_passengers.splice(idx, 1)"
                      class="mb-0.5 p-2 bg-red-50 text-red-400 rounded-lg hover:bg-red-100 transition">✕</button>
                    <div class="col-span-full"><label class="field-label">Note</label><input v-model="p.note" type="text" class="field-input" placeholder="Optional note" /></div>
                  </div>
                  <button type="button" @click="form.job_passengers.push({ first_name: '', last_name: '', hotel_name: '', pickup_time: '', note: '' })"
                    class="px-4 py-2 bg-[#f5f5f5] text-[#555] rounded-lg text-sm hover:bg-[#ebebeb] transition">+ Add Passenger</button>
                </template>
              </div>
            </div>

          </div>
        </div>

      </template>
    </div>

    <!-- Slip Image Modal -->
    <div v-if="slipModalUrl" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70" @click.self="slipModalUrl = null">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden max-w-xl w-full mx-4 flex flex-col" style="max-height:90vh" @click.stop>
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <span class="text-[15px] font-semibold text-[#111]">Payment Slip</span>
          <button class="text-[#999] hover:text-[#333] transition" @click="slipModalUrl = null">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="bg-[#111] flex items-center justify-center flex-1 overflow-auto">
          <img :src="slipModalUrl" class="max-w-full object-contain" style="max-height:calc(90vh - 56px)" />
        </div>
      </div>
    </div>
    <!-- Matching Modal -->
    <div v-if="showMatchingModal" class="fixed inset-0 z-50 flex items-start justify-center pt-16 bg-black/70" @click.self="showMatchingModal = false">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden w-full max-w-lg mx-4 flex flex-col" style="max-height:88vh">
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <div class="flex items-center gap-2">
            <span class="w-7 h-7 rounded-full bg-violet-100 flex items-center justify-center shrink-0">
              <svg class="w-3.5 h-3.5 text-violet-800" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            </span>
            <div>
              <div class="text-[15px] font-semibold text-[#111] leading-tight">Suggested Matches</div>
            </div>
          </div>
          <button class="text-[#999] hover:text-[#333] transition" @click="showMatchingModal = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <div class="overflow-y-auto px-5 py-4 flex flex-col gap-2.5">
          <div v-if="matchesLoading" class="flex flex-col gap-2.5">
            <div v-for="i in 3" :key="i" class="flex items-center gap-3 px-3.5 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8]">
              <span class="animate-pulse bg-[#ebebeb] w-9 h-9 rounded-full block shrink-0"></span>
              <div class="flex-1 flex flex-col gap-2">
                <span class="animate-pulse bg-[#ebebeb] h-3.5 w-2/5 rounded block"></span>
                <span class="animate-pulse bg-[#ebebeb] h-2.5 w-3/5 rounded block"></span>
              </div>
              <span class="animate-pulse bg-[#ebebeb] w-14 h-6 rounded-lg block shrink-0"></span>
            </div>
          </div>
          <div v-else-if="!suggestedMatches.length" class="text-center py-10">
            <p class="text-[13px] text-[#bbb]">No suggested matches for this tour yet.</p>
            <p class="text-[11px] text-[#ccc] mt-1">Freelancers must be verified, drive the right vehicle, and be available on these dates.</p>
          </div>
          <div v-for="cand in suggestedMatches" :key="cand.fl_id"
            class="flex items-center gap-3 px-3.5 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] hover:bg-[#f2f2f2] transition-all">
            <div class="w-9 h-9 rounded-full text-sm font-bold flex items-center justify-center shrink-0" :style="avatarStyle(cand.fl_id, cand.name)">{{ initials2(cand.name) }}</div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-1.5">
                <span class="text-[13px] font-semibold text-[#222] truncate">{{ cand.name }}</span>
                <span class="shrink-0 inline-flex items-center gap-1 bg-[#e8f5e9] text-[#2e7d32] text-[10px] font-bold px-1.5 py-0.5 rounded-full">
                  <svg class="w-2.5 h-2.5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                  {{ cand.matchScore }}% match
                </span>
              </div>
              <div class="flex flex-wrap gap-1 mt-1.5">
                <span v-for="tag in cand.reasons" :key="tag" :class="reasonClass(tag)">{{ tag }}</span>
              </div>
            </div>
            <div class="shrink-0 flex items-center gap-1.5">
              <button @click="miniModalFlId = cand.fl_id"
                class="px-2.5 py-1.5 text-[11px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-white hover:border-[#bbb] transition">
                View
              </button>
              <button class="flex items-center gap-1 text-[11px] font-semibold rounded-lg px-2.5 py-1.5 border-none transition-colors"
                :class="candidateStatus(cand.fl_id) === 'REJECTED'
                  ? 'text-red-400 bg-red-50 cursor-not-allowed'
                  : candidateStatus(cand.fl_id) === 'APPLIED'
                    ? 'text-blue-700 bg-blue-100 cursor-not-allowed'
                    : candidateStatus(cand.fl_id)
                      ? 'text-green-700 bg-green-100 cursor-default'
                      : 'text-violet-800 bg-violet-100 hover:bg-violet-200 cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-violet-100'"
                :disabled="inviting || candidateStatus(cand.fl_id) !== null || job?.job_status === 'MATCHED' || hasPendingInvite"
                @click="handleInviteCandidate(cand)">
                <svg v-if="candidateStatus(cand.fl_id) === 'PENDING' || candidateStatus(cand.fl_id) === 'ACCEPTED'" class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
                {{ candidateLabel(cand.fl_id) }}
              </button>
            </div>
          </div>
        </div>

        <div class="px-5 py-3 border-t border-[#f0f0f0] shrink-0">
          <p v-if="job?.job_status === 'MATCHED'" class="text-[11px] text-[#bbb] leading-relaxed">This tour is already matched - invites are locked.</p>
          <p v-else-if="hasPendingInvite" class="text-[11px] text-[#bbb] leading-relaxed">An invite is already pending for this tour - you can invite someone else once they respond.</p>
          <p v-else-if="hasAppliedCandidate" class="text-[11px] text-[#bbb] leading-relaxed">Some freelancers below have already applied on their own - you can accept them directly, or invite anyone else.</p>
          <p v-else class="text-[11px] text-[#bbb] leading-relaxed">You can invite one freelancer at a time - they'll show up as "Pending" until they respond.</p>
        </div>
      </div>
    </div>

    <!-- Applications Modal -->
    <div v-if="showApplicationModal" class="fixed inset-0 z-50 flex items-start justify-center pt-16 bg-black/70" @click.self="showApplicationModal = false">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden w-full max-w-lg mx-4 flex flex-col" style="max-height:88vh">
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <div class="flex items-center gap-2">
            <span class="w-7 h-7 rounded-full bg-amber-100 flex items-center justify-center shrink-0">
              <svg class="w-3.5 h-3.5 text-amber-800" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            </span>
            <div>
              <div class="text-[15px] font-semibold text-[#111] leading-tight">Applications</div>
            </div>
          </div>
          <button class="text-[#999] hover:text-[#333] transition" @click="showApplicationModal = false">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>

        <div class="overflow-y-auto px-5 py-4 flex flex-col gap-2.5">
          <div v-if="!applications.length" class="text-center py-10">
            <p class="text-[13px] text-[#bbb]">No applications yet.</p>
          </div>
          <div v-for="(app, idx) in applications" :key="app.job_application_id || idx"
            class="flex flex-col sm:flex-row sm:items-center gap-2 px-3.5 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] hover:bg-[#f2f2f2] transition-all">
            <div class="flex items-center gap-3 flex-1 min-w-0">
              <div class="w-9 h-9 rounded-full text-sm font-bold flex items-center justify-center shrink-0" :style="avatarStyle(app.fl_id, app.driver_name)">{{ initials2(app.driver_name || '?') }}</div>
              <div class="min-w-0">
                <div class="text-[13px] font-medium text-[#222]">{{ app.driver_name || "-" }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Applied {{ formatDate(app.applied_at) }}</div>
              </div>
              <span class="application-badge shrink-0 ml-auto sm:ml-0" :class="app.application_status?.toLowerCase()">{{ app.application_status }}</span>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <button @click="miniModalFlId = app.fl_id"
                class="px-2.5 py-1.5 text-[11px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-white hover:border-[#bbb] transition">
                View
              </button>
              <button @click="handleAccept(app)" title="Accept"
                :disabled="app.application_status !== 'APPLIED' || hasPendingInvite"
                class="w-8 h-8 flex items-center justify-center rounded-lg border border-green-200 bg-green-50 text-green-600 hover:bg-green-100 hover:border-green-300 transition disabled:opacity-30 disabled:cursor-not-allowed disabled:bg-[#f5f5f5] disabled:border-[#e0e0e0] disabled:text-[#aaa]">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
              </button>
              <button @click="handleReject(app)" title="Reject"
                :disabled="app.application_status !== 'APPLIED' || hasPendingInvite"
                class="w-8 h-8 flex items-center justify-center rounded-lg border border-red-200 bg-red-50 text-red-500 hover:bg-red-100 hover:border-red-300 transition disabled:opacity-30 disabled:cursor-not-allowed disabled:bg-[#f5f5f5] disabled:border-[#e0e0e0] disabled:text-[#aaa]">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
              </button>
            </div>
          </div>
        </div>

        <div v-if="hasPendingInvite" class="px-5 py-3 border-t border-[#f0f0f0] shrink-0">
          <p class="text-[11px] text-[#bbb] leading-relaxed">A Matching invite is pending - waiting for the freelancer to respond. Accept/Reject is locked for everyone (including the invited person) until then.</p>
        </div>
      </div>
    </div>
    <FreelancerMiniModal
      v-if="miniModalFlId"
      :fl-id="miniModalFlId"
      :job-id="job?.job_id"
      @close="miniModalFlId = null"
    />
  </AppLayout>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AppLayout from '@/components/AppLayout.vue'
import FreelancerMiniModal from '@/components/FreelancerMiniModal.vue'
import { useAvatar } from '@/composables/useAvatar'
import { useToast } from '@/components/useToast.js'

const { avatarStyle, initials2 } = useAvatar()
const { showToast } = useToast()

const API_BASE = import.meta.env.VITE_API_BASE || '/api'
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
const miniModalFlId = ref(null)
const showMatchingModal = ref(false)
const showApplicationModal = ref(false)

// Matching state
const matches = ref([])
const matchesLoading = ref(false)
// Pickup areas (from assigned freelancer)
const pickups = ref([])
const jobReview = ref(null)
const emReview = ref(null)

const payment = ref(null)
const paymentHistory = ref([])
const showPaymentHistory = ref(false)
const paymentSubmitting = ref(false)
const slipPreview = ref(null)
const slipFile = ref(null)
const reuploadPreview = ref(null)
const reuploadFile = ref(null)
const slipModalUrl = ref(null)

// Language DB fetch + search
const languages = ref([])
const otherLanguage = ref('')
const showSuggestions = ref(false)
const langSuggestions = ref([])
const exactMatch = ref(false)

// Areas DB fetch (for the job's own Area Required dropdown - distinct from
// `pickups`, which is the assigned freelancer's own coverage areas)
const areas = ref([])
const fetchAreas = async () => {
  try {
    const res = await fetch(`${API_BASE}/areas`)
    if (res.ok) areas.value = await res.json()
  } catch {}
}

const fetchLanguages = async () => {
  try {
    const res = await fetch(`${API_BASE}/languages`)
    if (res.ok) languages.value = await res.json()
  } catch {}
}

const onLangInput = () => {
  const q = otherLanguage.value.trim().toLowerCase()
  showSuggestions.value = true
  if (!q) { langSuggestions.value = []; exactMatch.value = false; return }
  langSuggestions.value = languages.value.filter(l => l.language_name.toLowerCase().includes(q)).slice(0, 6)
  exactMatch.value = languages.value.some(l => l.language_name.toLowerCase() === q)
}

const hideSuggestions = () => setTimeout(() => { showSuggestions.value = false }, 150)

const selectSuggestion = (langName) => {
  if (!form.job_required_languages.includes(langName)) form.job_required_languages.push(langName)
  otherLanguage.value = ''
  showSuggestions.value = false
}

const addTopSuggestion = () => {
  if (langSuggestions.value.length) selectSuggestion(langSuggestions.value[0].language_name)
  else addOtherLanguage()
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

const form = reactive({
  job_title: '',
  job_description: '',
  job_start_date: '',
  job_end_date: '',
  job_required_vehicle_type: 'VAN',
  job_required_seat: 9,
  job_area_id: null,
  job_price: null,
  job_required_languages: [],
  job_itineraries: [],
  job_passengers: [],
  job_expenses: [],
})

// Fetch tour
const fetchJob = async () => {
  loading.value = true
  error.value = ''
  const id = route.params.id
  try {
    const [jobRes, langRes, itinRes, passRes, expRes, appRes, payRes, histRes, revRes] = await Promise.all([
      fetch(`${API_BASE}/tours/${id}?em_id=${emId}`),
      fetch(`${API_BASE}/job-required-languages?job_id=${id}&limit=20`),
      fetch(`${API_BASE}/job-itineraries?job_id=${id}&limit=50`),
      fetch(`${API_BASE}/job-passengers?job_id=${id}&limit=50`),
      fetch(`${API_BASE}/job-expenses?job_id=${id}&limit=20`),
      fetch(`${API_BASE}/job-applications?job_id=${id}&limit=50`),
      fetch(`${API_BASE}/job-payments?job_id=${id}&limit=10`),
      fetch(`${API_BASE}/job-payments/${id}/history`),
      fetch(`${API_BASE}/fl-reviews?job_id=${id}&limit=10`),
    ])

    const [jobData, langData, itinData, passData, expData, appData, payData, histData, revData] = await Promise.all([
      jobRes.json(), langRes.json(), itinRes.json(), passRes.json(),
      expRes.json(), appRes.json(), payRes.json(), histRes.json(), revRes.json(),
    ])

    if (!jobRes.ok) throw new Error(jobData.detail || jobData.message || 'Failed to load tour.')

    job.value = jobData
    job.value.job_required_languages = (langData.items || []).map(l => l.language_name)
    job.value.job_itineraries = (itinData.items || []).sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
    job.value.job_passengers = passData.items || []
    job.value.job_expenses = (expData.items || []).sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))

    applications.value = (appData.items || []).sort((a, b) => new Date(b.applied_at) - new Date(a.applied_at))

    payment.value = (payData.items || []).find(p => p.is_latest) || null
    const allHistory = histData.history || []
    paymentHistory.value = allHistory.filter(p => !p.is_latest)
    jobReview.value = (revData.items || [])[0] || null

    // Pickup areas + em-reviews filtered by assigned freelancer
    if (jobData.selected_fl_id) {
      try {
        const emRevRes = await fetch(`${API_BASE}/em-reviews?job_id=${id}&limit=10`)
        const emRevData = await emRevRes.json()
        emReview.value = (emRevData.items || [])[0] || null
      } catch { emReview.value = null }
      try {
        const pickupRes = await fetch(`${API_BASE}/fl-pickup-areas?fl_id=${jobData.selected_fl_id}&limit=20`)
        const pickupData = await pickupRes.json()
        pickups.value = pickupData.items || []
      } catch { pickups.value = [] }
    }

  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
  fetchMatches()
}

const fetchMatches = async () => {
  const id = route.params.id
  matchesLoading.value = true
  try {
    const res = await fetch(`${API_BASE}/tours/${id}/matches?em_id=${emId}`)
    const data = await res.json()
    matches.value = res.ok ? (data.items || []) : []
  } catch {
    matches.value = []
  } finally {
    matchesLoading.value = false
  }
}

onMounted(() => {
  fetchJob()
  fetchLanguages()
  fetchAreas()
})

// Refresh payment only
const fetchPayment = async () => {
  const id = route.params.id
  try {
    const [payRes, histRes] = await Promise.all([
      fetch(`${API_BASE}/job-payments?job_id=${id}&limit=10`),
      fetch(`${API_BASE}/job-payments/${id}/history`),
    ])
    const [payData, histData] = await Promise.all([payRes.json(), histRes.json()])
    payment.value = (payData.items || []).find(p => p.is_latest) || null
    paymentHistory.value = (histData.history || []).filter(p => !p.is_latest)
  } catch { payment.value = null }
}

const uploadSlipToStorage = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${API_BASE}/upload/payment-slip`, { method: 'POST', body: formData })
  if (!res.ok) throw new Error('Upload failed')
  const data = await res.json()
  return data.url
}

const onSlipFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  slipFile.value = file
  slipPreview.value = URL.createObjectURL(file)
}
const onSlipDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (!file) return
  slipFile.value = file
  slipPreview.value = URL.createObjectURL(file)
}
const clearSlip = () => { slipFile.value = null; slipPreview.value = null }

const onReuploadFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  reuploadFile.value = file
  reuploadPreview.value = URL.createObjectURL(file)
}
const onReuploadDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (!file) return
  reuploadFile.value = file
  reuploadPreview.value = URL.createObjectURL(file)
}
const clearReupload = () => { reuploadFile.value = null; reuploadPreview.value = null }

const submitPayment = async () => {
  if (!slipFile.value) return
  if (!job.value?.selected_fl_id) {
    alert('Cannot submit payment: no freelancer has been assigned to this tour yet.')
    return
  }
  paymentSubmitting.value = true
  try {
    const slip_url = await uploadSlipToStorage(slipFile.value)
    const res = await fetch(`${API_BASE}/job-payments`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        job_id: route.params.id,
        em_id: emId,
        fl_id: job.value?.selected_fl_id || null,
        slip_url,
      }),
    })
    const data = await res.json()
    if (res.ok) {
      clearSlip()
      await fetchPayment()
    } else {
      alert(data.detail || data.error || 'Failed to submit payment.')
    }
  } catch (e) {
    alert('Error: ' + e.message)
  } finally {
    paymentSubmitting.value = false
  }
}

const submitReupload = async () => {
  if (!reuploadFile.value) return
  paymentSubmitting.value = true
  try {
    const slip_url = await uploadSlipToStorage(reuploadFile.value)
    const res = await fetch(`${API_BASE}/job-payments/${route.params.id}/reupload`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slip_url }),
    })
    const data = await res.json()
    if (res.ok) {
      clearReupload()
      await fetchPayment()
    } else {
      alert(data.detail || data.error || 'Failed to reupload.')
    }
  } catch (e) {
    alert('Error: ' + e.message)
  } finally {
    paymentSubmitting.value = false
  }
}

// Accept / Reject
const handleAccept = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/job-applications/${app.job_application_id}/accept`, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      app.application_status = 'ACCEPTED'
      job.value.job_status = 'MATCHED'
      job.value.selected_fl_id = app.fl_id
      job.value.driver_name = app.driver_name

      // get driver_phone from freelancer
      try {
        const flRes = await fetch(`${API_BASE}/freelancers/${app.fl_id}`)
        const flData = await flRes.json()
        if (flRes.ok) job.value.driver_phone = flData.fl_phone
      } catch {}

      // backend already rejects everyone else for this job atomically - mirror that locally
      applications.value.forEach(a => {
        if (a.job_application_id !== app.job_application_id && a.application_status !== 'ACCEPTED' && a.application_status !== 'REJECTED') {
          a.application_status = 'REJECTED'
        }
      })
    } else {
      const d = await res.json().catch(() => ({}))
      alert('Failed to accept: ' + (d.detail || res.status))
    }
  } catch { alert('Failed to accept application.') }
}

const handleReject = async (app) => {
  try {
    const res = await fetch(`${API_BASE}/job-applications/${app.job_application_id}/reject`, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) app.application_status = 'REJECTED'
    else {
      const d = await res.json().catch(() => ({}))
      alert('Failed to reject: ' + (d.detail || res.status))
    }
  } catch { alert('Failed to reject application.') }
}

// Edit helpers
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
    job_area_id: j.job_area_id ?? null,
    job_price: j.job_price ?? null,
    job_required_languages: [...(j.job_required_languages || [])],
    job_itineraries: (j.job_itineraries || []).map(i => ({ ...i })),
    job_passengers: (j.job_passengers || []).map(p => ({
      ...p,
      pickup_time: formatPickupTime(p.pickup_time) === '-' ? '' : formatPickupTime(p.pickup_time),
    })),
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

// Save
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
      // update local job state without full refetch
      Object.assign(job.value, {
        job_title: form.job_title,
        job_description: form.job_description,
        job_start_date: form.job_start_date,
        job_end_date: form.job_end_date,
        job_required_vehicle_type: form.job_required_vehicle_type,
        job_required_seat: form.job_required_seat,
        job_area_id: form.job_area_id,
        job_area_name: areas.value.find(a => a.area_id === form.job_area_id)?.area_name || null,
        job_price: form.job_price,
        job_required_languages: [...form.job_required_languages],
        job_itineraries: form.job_itineraries.map(i => ({ ...i })),
        job_passengers: form.job_passengers.map(p => ({ ...p })),
        job_expenses: form.job_expenses.map(e => ({ ...e })),
        job_updated_at: new Date().toISOString(),
      })
    } else {
      alert('Failed to save: ' + (data.error || data.message || data.detail || 'Unknown error'))
    }
  } catch (e) {
    alert('An error occurred: ' + e.message)
  } finally {
    submitting.value = false
  }
}

// Computed helpers
const sortedExpenses = computed(() =>
  [...(job.value?.job_expenses ?? [])].sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
)
const canEdit = computed(() => job.value?.job_status === 'OPEN')
const canCancel = computed(() => ['OPEN', 'PENDING', 'MATCHED'].includes(job.value?.job_status))
const canMatch = computed(() => ['OPEN', 'PENDING'].includes(job.value?.job_status))

// Matching
const suggestedMatches = computed(() => matches.value)
const inviting = ref(false)

// Single source of truth: any fl_id with a real application row (from either
// Applications or a Matching invite) is locked here too - synced both ways.
// REJECTED stays locked permanently, same as an ACCEPTED/PENDING one.
const candidateStatus = (fl_id) => {
  const app = applications.value.find(a => a.fl_id === fl_id)
  return app ? app.application_status : null
}

// PENDING = employer invited them (this Matching flow). APPLIED = they applied
// on their own via Job Opening, unrelated to being invited. Label each honestly.
const candidateLabel = (fl_id) => {
  const status = candidateStatus(fl_id)
  if (status === 'REJECTED') return 'Rejected'
  if (status === 'ACCEPTED') return 'Matched'
  if (status === 'PENDING') return 'Invited'
  if (status === 'APPLIED') return 'Applied'
  return 'Invite'
}

// Color-code the reason tags on each match card: Verified/Available on dates
// (green) and Not Verified (red) carry status info the employer should
// notice; everything else (e.g. Speaks...) stays a neutral gray pill.
const reasonClass = (tag) => {
  if (tag === 'Verified' || tag === 'Available on dates' || tag === 'Covers Pickup Area') {
    return 'text-[10px] font-semibold text-[#2e7d32] bg-white border border-[#e8e8e8] rounded-full px-2 py-0.5'
  }
  if (tag === 'Not Verified' || tag === 'Outside Pickup Area') {
    return 'text-[10px] font-semibold text-[#c62828] bg-white border border-[#e8e8e8] rounded-full px-2 py-0.5'
  }
  return 'text-[10px] text-[#888] bg-white border border-[#e8e8e8] rounded-full px-2 py-0.5'
}

// Only one freelancer can be invited per tour at a time - once someone has a
// pending invite, every other Invite button locks (cursor-not-allowed) until
// they respond (accepted/rejected).
const hasPendingInvite = computed(() => applications.value.some(a => a.application_status === 'PENDING'))

// True when at least one freelancer in the Suggested Matches list has applied
// on their own (via Job Opening) rather than being invited - surfaced in the
// modal footer so the employer notices without hunting for the "Applied" pill.
const hasAppliedCandidate = computed(() => suggestedMatches.value.some(c => candidateStatus(c.fl_id) === 'APPLIED'))

const handleInviteCandidate = async (candidate) => {
  inviting.value = true
  try {
    const res = await fetch(`${API_BASE}/tours/${route.params.id}/invite`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ em_id: emId, fl_id: candidate.fl_id }),
    })
    const data = await res.json().catch(() => ({}))
    if (!res.ok) {
      showToast(data.detail || 'Failed to invite freelancer.', 'error')
      return
    }
    // reflect immediately in the Applications list/badge without a full refetch
    applications.value.unshift({
      job_application_id: data.job_application_id,
      fl_id: candidate.fl_id,
      driver_name: candidate.name,
      application_status: 'PENDING',
      applied_at: new Date().toISOString(),
    })
    showToast(`Invitation sent to ${candidate.name} - waiting for their response`)
  } catch {
    showToast('Cannot connect to the server.', 'error')
  } finally {
    inviting.value = false
  }
}

// Status display
const STATUS_MAP = {
  OPEN:        { label: 'Open'        },
  PENDING:     { label: 'Pending'     },
  MATCHED:     { label: 'Matched'     },
  IN_PROGRESS: { label: 'In Progress' },
  COMPLETED:   { label: 'Completed'   },
  CANCELLED:   { label: 'Cancelled'   },
}
const statusLabel = (s) => STATUS_MAP[s]?.label ?? s

// Formatters
const formatPickupTime = (val) => {
  if (!val) return '-'
  if (typeof val === 'number' || /^\d+$/.test(String(val))) {
    const secs = Number(val)
    return `${String(Math.floor(secs / 3600)).padStart(2, '0')}:${String(Math.floor((secs % 3600) / 60)).padStart(2, '0')}`
  }
  return val
}

const TZ = 'Asia/Bangkok'
const parseDate = (d) => {
  if (!d) return null
  return new Date(String(d).replace(' ', 'T'))
}
const formatDate = (d) => {
  const dt = parseDate(d)
  if (!dt) return '-'
  return dt.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: TZ })
}
const formatDateTime = (d) => {
  const dt = parseDate(d)
  if (!dt) return '-'
  return dt.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: TZ })
}

// Cancel tour
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