<template>
  <div>
    <BreadcrumbBar :label="em?.em_name" />
    <!-- Loading skeleton — mirrors real layout -->
    <div v-if="loading" class="px-5 pb-8">
      <!-- Top bar -->
      <div class="flex items-center justify-between py-3 mb-5">
        <div class="animate-pulse bg-[#ebebeb] h-4 w-16 rounded"></div>
        <div class="animate-pulse bg-[#ebebeb] h-8 w-32 rounded-lg"></div>
      </div>
      <!-- Grid -->
      <div class="grid gap-4" style="grid-template-columns: 260px 1fr; align-items: start;">
        <!-- LEFT skeleton -->
        <div class="flex flex-col gap-3">
          <!-- Profile card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col items-center gap-3">
            <div class="animate-pulse bg-[#ebebeb] w-20 h-20 rounded-full"></div>
            <div class="animate-pulse bg-[#ebebeb] h-4 w-28 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-36 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded"></div>
          </div>
          <!-- Stats card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-10 rounded"></div>
            </div>
            <div class="px-4 py-3 grid grid-cols-3 gap-3">
              <div v-for="i in 3" :key="i" class="flex flex-col items-center gap-1.5">
                <div class="animate-pulse bg-[#ebebeb] h-6 w-10 rounded"></div>
                <div class="animate-pulse bg-[#ebebeb] h-2.5 w-14 rounded"></div>
              </div>
            </div>
          </div>
          <!-- Account card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-16 rounded"></div>
            </div>
            <div class="px-4 py-3 flex flex-col gap-4">
              <div v-for="i in 3" :key="i" class="flex items-center gap-2.5">
                <div class="animate-pulse bg-[#ebebeb] w-3.5 h-3.5 rounded shrink-0"></div>
                <div class="flex flex-col gap-1 flex-1">
                  <div class="animate-pulse bg-[#ebebeb] h-2 w-14 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-32 rounded"></div>
                </div>
              </div>
            </div>
          </div>
          <!-- Info card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-20 rounded"></div>
            </div>
            <div class="px-4 py-3 flex flex-col gap-4">
              <div v-for="i in 3" :key="i" class="flex items-center gap-2.5">
                <div class="animate-pulse bg-[#ebebeb] w-3.5 h-3.5 rounded shrink-0"></div>
                <div class="flex flex-col gap-1 flex-1">
                  <div class="animate-pulse bg-[#ebebeb] h-2 w-16 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-28 rounded"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- RIGHT skeleton -->
        <div class="flex flex-col gap-3">
          <!-- Verification box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-4">
              <div class="flex items-center gap-6">
                <div class="animate-pulse bg-[#ebebeb] h-5 w-20 rounded-full"></div>
                <div class="animate-pulse bg-[#ebebeb] h-3 w-28 rounded"></div>
                <div class="animate-pulse bg-[#ebebeb] h-3 w-32 rounded"></div>
              </div>
              <div>
                <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded mb-3"></div>
                <div class="grid grid-cols-5 gap-2">
                  <div v-for="i in 4" :key="i" class="rounded-xl border border-[#eee] overflow-hidden">
                    <div class="animate-pulse bg-[#ebebeb] h-[90px] w-full"></div>
                    <div class="p-2 flex flex-col gap-1">
                      <div class="animate-pulse bg-[#ebebeb] h-2.5 w-full rounded"></div>
                      <div class="animate-pulse bg-[#ebebeb] h-4 w-14 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Jobs Posted box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-5 w-8 rounded-full ml-auto"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="i in 4" :key="i" class="flex items-center gap-3 px-4 py-3 rounded-lg border border-[#e8e8e8]">
                <div class="flex-1 flex flex-col gap-1.5">
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-48 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-2.5 w-32 rounded"></div>
                </div>
                <div class="flex flex-col items-end gap-1.5 shrink-0">
                  <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-3 w-12 rounded"></div>
                </div>
              </div>
            </div>
          </div>
          <!-- Reviews box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-44 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-5 w-8 rounded-full ml-auto"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="i in 3" :key="i" class="p-3.5 rounded-lg border border-[#e8e8e8]">
                <div class="flex items-center justify-between mb-2">
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-28 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-20 rounded"></div>
                </div>
                <div class="animate-pulse bg-[#ebebeb] h-3 w-4/5 rounded"></div>
                <div class="animate-pulse bg-[#ebebeb] h-2.5 w-40 rounded mt-2"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="!em" class="empty">Employer not found.</div>

    <div v-else class="px-5 pb-8">
      <!-- Top Bar -->
      <div class="flex items-center justify-between py-3 mb-5">
        <button class="flex items-center gap-1.5 text-[13px] text-[#555] hover:text-black cursor-pointer border-none bg-transparent" @click="router.back()">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          Back
        </button>
        <button class="btn-action !px-4 !py-2 !text-[13px] !rounded-lg flex items-center gap-1.5"
          :class="em.em_is_active ? 'ban' : 'unban'" @click="showBanModal = true">
          <svg v-if="em.em_is_active" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
          <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          {{ em.em_is_active ? "Ban Employer" : "Unban Employer" }}
        </button>
      </div>

      <div class="grid gap-4" style="grid-template-columns: 260px 1fr; align-items: start;">

        <!-- ── LEFT sidebar ── -->
        <div class="flex flex-col gap-3">

          <!-- Profile -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col items-center text-center hover:shadow-md transition-shadow">
            <div class="relative mb-3">
              <img v-if="em.em_profile_image_url" :src="em.em_profile_image_url" class="w-20 h-20 rounded-full object-cover ring-2 ring-[#eee]" />
              <div v-else class="w-20 h-20 rounded-full bg-[#f3e5f5] text-[#7b1fa2] flex items-center justify-center text-3xl font-bold ring-2 ring-[#eee]">{{ em.em_name?.[0] || "?" }}</div>
              <span class="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2 border-white" :class="em.em_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
            </div>
            <h2 class="text-[15px] font-bold text-[#111] mb-1.5">{{ em.em_name }}</h2>
            <span class="badge mb-3" :class="em.em_verify_status?.toLowerCase()">{{ em.em_verify_status }}</span>
            <p v-if="em.em_bio" class="text-[12px] text-[#777] leading-relaxed">{{ em.em_bio }}</p>
            <p v-else class="text-[12px] text-[#bbb] italic">No bio provided</p>
          </div>

          <!-- Stats -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Stats</span>
            </div>
            <div class="px-4 py-3 grid grid-cols-3 gap-3 text-center">
              <div>
                <div class="text-[18px] font-bold text-[#111] flex items-center justify-center gap-1">
                  {{ Number(em.em_rating_avg || 0).toFixed(1) }}
                  <svg class="w-4 h-4 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </div>
                <div class="text-[11px] text-[#999] mt-0.5">Rating</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ jobs.filter(j => j.job_status === 'COMPLETED').length }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Completed</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ jobs.length }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Total Jobs</div>
              </div>
            </div>
          </div>

          <!-- Account -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Account</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-if="em.em_username" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Username</div><div class="text-[13px] text-[#222] font-medium">{{ em.em_username }}</div></div>
              </div>
              <div v-if="em.em_email" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Email</div><div class="text-[13px] text-[#222] font-medium break-all">{{ em.em_email }}</div></div>
              </div>
              <div v-if="em.em_phone" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Phone</div><div class="text-[13px] text-[#222] font-medium">{{ em.em_phone }}</div></div>
              </div>
            </div>
          </div>

          <!-- Information -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Information</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-if="em.em_address" class="flex items-start gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Address</div><div class="text-[13px] text-[#222] font-medium leading-snug">{{ em.em_address }}</div></div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Joined</div><div class="text-[13px] text-[#222] font-medium">{{ formatDate(em.em_created_at) }}</div></div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last Updated</div><div class="text-[13px] text-[#222] font-medium">{{ formatDateTime(em.em_updated_at) }}</div></div>
              </div>
            </div>
          </div>

          <!-- Bank Account — icon header, no Primary badge -->
          <div v-if="bankAccounts.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 6l9-3 9 3M3 6v12a1 1 0 001 1h16a1 1 0 001-1V6M3 6h18M8 10v7m4-7v7m4-7v7"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Bank Account</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-for="b in bankAccounts" :key="b.em_bank_account_id" class="flex flex-col gap-0.5">
                <div class="text-[13px] font-semibold text-[#222]">{{ b.bank_name }}</div>
                <div class="text-[12px] text-[#555]">{{ b.account_name }}</div>
                <div class="text-[12px] text-[#888] tracking-wide">{{ b.account_number }}</div>
                <div class="text-[10px] text-[#bbb] mt-0.5">Updated {{ formatDate(b.updated_at) }}</div>
              </div>
            </div>
          </div>

        </div>

        <!-- ── RIGHT main ── -->
        <div class="flex flex-col gap-3">

          <!-- Verification + Documents -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Verification</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-4">
              <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
                <div class="flex items-center gap-2">
                  <span class="text-[12px] text-[#999] font-medium">Status:</span>
                  <span class="badge" :class="em.em_verify_status?.toLowerCase()">{{ em.em_verify_status }}</span>
                </div>
                <div v-if="verification?.em_verified_at" class="flex items-center gap-1.5">
                  <span class="text-[12px] text-[#999] font-medium">Verified:</span>
                  <span class="text-[13px] font-medium text-[#222]">{{ formatDate(verification.em_verified_at) }}</span>
                </div>
                <div v-if="verification?.reviewed_by_name" class="flex items-center gap-1.5">
                  <span class="text-[12px] text-[#999] font-medium">Reviewed by:</span>
                  <span class="text-[13px] font-medium text-[#222]">{{ verification.reviewed_by_name }}</span>
                </div>
              </div>
              <!-- Documents — 5 cols, click → modal -->
              <div>
                <div class="text-[12px] font-bold text-[#444] uppercase tracking-wide mb-3">Documents</div>
                <div class="grid grid-cols-5 gap-2">
                  <div v-for="d in documents" :key="d.em_doc_id"
                    class="rounded-xl border overflow-hidden bg-white flex flex-col transition-colors"
                    :class="d.file_url ? 'border-[#eee] cursor-pointer hover:border-[#aaa]' : 'border-dashed border-[#ddd] cursor-default'"
                    @click="d.file_url ? openDocModal(d) : null">
                    <div class="h-[90px] bg-[#f5f5f5] relative overflow-hidden">
                      <img v-if="d.file_url" :src="d.file_url" class="w-full h-full object-cover hover:opacity-90 transition-opacity"
                        @error="(e) => { e.target.style.display='none' }" />
                      <div class="absolute inset-0 flex items-center justify-center flex-col gap-1"
                        :style="d.file_url ? 'display:none' : ''">
                        <svg class="w-5 h-5 text-[#ddd]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                        <span class="text-[9px] text-[#ccc] font-medium">Not uploaded</span>
                      </div>
                    </div>
                    <div class="p-2 flex flex-col gap-0.5">
                      <span class="text-[11px] font-semibold text-[#222] leading-snug truncate">{{ formatDocType(d.em_doc_type) }}</span>
                      <span class="doc-badge self-start" :class="d.em_doc_status?.toLowerCase()">{{ d.em_doc_status }}</span>
                      <span class="text-[11px] text-[#bbb]">{{ d.em_uploaded_at ? formatDate(d.em_uploaded_at) : '–' }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Jobs Posted — clickable to job detail -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="jobs.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path stroke-linecap="round" stroke-linejoin="round" d="M16 3H8a2 2 0 00-2 2v2h12V5a2 2 0 00-2-2z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Jobs Posted</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ jobs.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="j in jobs" :key="j.job_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] cursor-pointer hover:border-[#aaa] hover:bg-[#f0f0f0] transition-all"
                @click="router.push({ name: 'JobDetail', params: { id: j.job_id } })">
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222] truncate">{{ j.job_title }}</div>
                  <div class="flex items-center gap-2 text-[12px] text-[#999] mt-0.5">
                    <span>{{ formatDate(j.job_start_date) }}</span>
                    <span v-if="j.selected_driver" class="text-[#ccc]">·</span>
                    <span v-if="j.selected_driver">{{ j.selected_driver }}</span>
                  </div>
                </div>
                <div class="flex flex-col items-end gap-1 shrink-0">
                  <span class="badge" :class="j.job_status?.toLowerCase()">{{ formatJobStatus(j.job_status) }}</span>
                  <span class="text-[12px] font-semibold text-[#333]">{{ j.job_price ? "฿" + Number(j.job_price).toLocaleString() : "–" }}</span>
                </div>
                <svg class="w-4 h-4 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>

          <!-- Reviews Given -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="reviewsGiven.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Reviews Given to Freelancers</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ reviewsGiven.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="r in reviewsGiven" :key="r.fl_review_id" class="p-3.5 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] transition-colors">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-[13px] font-semibold text-[#222]">{{ r.driver_name }}</span>
                  <div class="flex items-center gap-0.5">
                    <svg v-for="i in 5" :key="i" class="w-3.5 h-3.5" :class="i <= r.rating ? 'text-[#f9a825]' : 'text-[#ddd]'" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                    <span class="text-[12px] font-bold text-[#333] ml-1">{{ r.rating }}.0</span>
                  </div>
                </div>
                <p v-if="r.comment" class="text-[13px] text-[#555] leading-relaxed">{{ r.comment }}</p>
                <div class="text-[12px] text-[#bbb] mt-1.5">{{ formatDateTime(r.reviewed_at) }} · {{ r.job_title }}</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="modalDoc" class="modal-overlay" @click.self="modalDoc = null">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden max-w-3xl w-full mx-4 flex flex-col" style="max-height:90vh" @click.stop>
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <div class="flex items-center gap-2.5">
            <span class="text-[15px] font-semibold text-[#111]">{{ modalDoc.title || "Preview" }}</span>
            <span v-if="modalDoc.status" class="doc-badge" :class="modalDoc.status?.toLowerCase()">{{ modalDoc.status }}</span>
          </div>
          <button class="text-[#999] hover:text-[#333] border-none bg-transparent cursor-pointer" @click="modalDoc = null">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="bg-[#111] flex items-center justify-center overflow-auto flex-1" style="min-height:400px">
          <img :src="modalDoc.url" class="max-w-full object-contain" style="max-height:calc(90vh - 110px)" />
        </div>
        <div v-if="modalDoc.uploadedAt || modalDoc.reviewedBy" class="px-5 py-3 border-t border-[#eee] flex flex-wrap items-center gap-5 shrink-0 bg-white">
          <div v-if="modalDoc.uploadedAt" class="flex items-center gap-1.5 text-[12px] text-[#666]">
            <svg class="w-3.5 h-3.5 text-[#bbb]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
            Uploaded <strong class="text-[#333] ml-1">{{ formatDateTime(modalDoc.uploadedAt) }}</strong>
          </div>
          <div v-if="modalDoc.reviewedBy" class="flex items-center gap-1.5 text-[12px] text-[#666]">
            <svg class="w-3.5 h-3.5 text-[#bbb]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
            Reviewed by <strong class="text-[#333] ml-1">{{ modalDoc.reviewedBy }}</strong>
          </div>
        </div>
      </div>
    </div>

    <!-- Ban Modal -->
    <BanModal
      :show="showBanModal"
      :is-active="em?.em_is_active"
      :name="em?.em_name"
      user-type="Employer"
      @confirm="confirmBan"
      @cancel="showBanModal = false"
    />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import BanModal from '../components/BanModal.vue'
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { API_BASE } from "../data/api"
import { formatJobStatus } from '../utils/statusClasses'
import { formatDate, formatDateTime } from '../utils/formatDate'

const route = useRoute()
const router = useRouter()
const showBanModal = ref(false)

const em = ref(null)
const documents = ref([])
const jobs = ref([])
const bankAccounts = ref([])
const reviewsGiven = ref([])
const verification = ref(null)
const loading = ref(true)
const modalDoc = ref(null)

const openDocModal = (d) => {
  modalDoc.value = { url: d.file_url, title: formatDocType(d.em_doc_type), status: d.em_doc_status, uploadedAt: d.em_uploaded_at, reviewedBy: d.reviewed_by_name || null }
}

const formatDocType = (t) => ({ COMPANY_REGISTRATION: "Company Registration", BUSINESS_LICENSE: "Business License", TOURISM_LICENSE: "Tourism License", TAX_ID_DOCUMENT: "Tax ID Document", AUTHORIZED_PERSON_ID: "Authorized Person ID" }[t] || t)

const confirmBan = async () => {
  if (!em.value) return
  try {
    const res = await fetch(`${API_BASE}/employers/${em.value.em_id}/ban`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ is_active: !em.value.em_is_active, admin_id: localStorage.getItem("admin_id") || "" }) })
    const data = await res.json()
    if (data.status === "updated") em.value.em_is_active = !em.value.em_is_active
  } catch (e) { console.error(e) } finally { showBanModal.value = false }
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [emRes, docRes, jobsRes, bankRes, reviewRes, verifyRes] = await Promise.all([
      fetch(`${API_BASE}/employers/${id}`),
      fetch(`${API_BASE}/em-documents?limit=500`),
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/em-bank-accounts?limit=500`),
      fetch(`${API_BASE}/fl-reviews?limit=500`),
      fetch(`${API_BASE}/em-verification?limit=500`),
    ])
    const [emData, docData, jobsData, bankData, reviewData, verifyData] = await Promise.all([
      emRes.json(), docRes.json(), jobsRes.json(), bankRes.json(), reviewRes.json(), verifyRes.json(),
    ])
    em.value = emData.em_id ? emData : null
    const allDocs = (docData.items || []).filter(d => String(d.em_id) === String(id))
    // ใช้ is_latest=1 เป็นหลัก — หลีกเลี่ยงปัญหา new Date(null) = epoch
    const byType = {}
    allDocs.forEach(d => {
      const isLatest = d.is_latest === 1 || d.is_latest === true
      if (!byType[d.em_doc_type]) {
        byType[d.em_doc_type] = d
      } else if (isLatest && !(byType[d.em_doc_type].is_latest === 1 || byType[d.em_doc_type].is_latest === true)) {
        byType[d.em_doc_type] = d
      } else if (isLatest && d.em_uploaded_at && new Date(d.em_uploaded_at) > new Date(byType[d.em_doc_type].em_uploaded_at)) {
        byType[d.em_doc_type] = d
      }
    })
    // เติม slot ที่ขาดหายให้ครบ 5 ประเภท
    const EM_DOC_TYPES = ['COMPANY_REGISTRATION', 'BUSINESS_LICENSE', 'TOURISM_LICENSE', 'TAX_ID_DOCUMENT', 'AUTHORIZED_PERSON_ID']
    EM_DOC_TYPES.forEach(type => {
      if (!byType[type]) {
        byType[type] = { em_doc_id: `empty_${type}`, em_id: id, em_doc_type: type, file_url: null, em_doc_status: 'PENDING', em_uploaded_at: null, reviewed_by_name: null, is_latest: 1 }
      }
    })
    documents.value = EM_DOC_TYPES.map(t => byType[t])
    jobs.value = (jobsData.items || []).filter(j => String(j.em_id) === String(id))
    bankAccounts.value = (bankData.items || []).filter(b => String(b.em_id) === String(id))
    reviewsGiven.value = (reviewData.items || []).filter(r => String(r.em_id) === String(id))
    const verList = (verifyData.items || []).filter(v => String(v.em_id) === String(id) && (v.is_latest === true || v.is_latest === 1))
    verification.value = verList[0] || null
  } catch (e) { console.error(e) } finally { loading.value = false }
})
</script>