<template>
  <div>
    <BreadcrumbBar :label="fl?.fl_name" />
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
              <div v-for="i in 4" :key="i" class="flex items-center gap-2.5">
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
                    <div class="animate-pulse bg-[#ebebeb] h-[90px] w-full rounded-none"></div>
                    <div class="p-2 flex flex-col gap-1">
                      <div class="animate-pulse bg-[#ebebeb] h-2.5 w-full rounded"></div>
                      <div class="animate-pulse bg-[#ebebeb] h-4 w-14 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <!-- Vehicle box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-16 rounded"></div>
            </div>
            <div class="px-4 py-4">
              <div class="grid grid-cols-4 gap-x-5 gap-y-4 mb-5">
                <div v-for="i in 5" :key="i" class="flex flex-col gap-1.5">
                  <div class="animate-pulse bg-[#ebebeb] h-2 w-12 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-4 w-20 rounded"></div>
                </div>
              </div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded mb-2"></div>
              <div class="grid grid-cols-5 gap-2">
                <div v-for="i in 4" :key="i" class="animate-pulse bg-[#ebebeb] aspect-square rounded-lg"></div>
              </div>
            </div>
          </div>
          <!-- Reviews box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-36 rounded"></div>
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
    <div v-else-if="!fl" class="empty">Freelancer not found.</div>

    <div v-else class="px-5 pb-8">
      <!-- Top Bar -->
      <div class="flex items-center justify-between py-3 mb-5">
        <button class="flex items-center gap-1.5 text-sm text-[#555] hover:text-black cursor-pointer border-none bg-transparent" @click="router.back()">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          Back
        </button>
        <button class="btn-action !px-4 !py-2 !text-[13px] !rounded-lg flex items-center gap-1.5"
          :class="fl.fl_is_active ? 'ban' : 'unban'" @click="showBanModal = true">
          <svg v-if="fl.fl_is_active" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
          <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          {{ fl.fl_is_active ? "Ban Freelancer" : "Unban Freelancer" }}
        </button>
      </div>

      <div class="grid gap-4" style="grid-template-columns: 260px 1fr; align-items: start;">

        <!-- ── LEFT sidebar ── -->
        <div class="flex flex-col gap-3">

          <!-- Profile -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col items-center text-center hover:shadow-md transition-shadow">
            <div class="relative mb-3">
              <img v-if="fl.fl_profile_image_url" :src="fl.fl_profile_image_url" class="w-20 h-20 rounded-full object-cover ring-2 ring-[#eee]" />
              <div v-else class="w-20 h-20 rounded-full bg-[#e3f2fd] text-[#1976d2] flex items-center justify-center text-3xl font-bold ring-2 ring-[#eee]">{{ fl.fl_name?.[0] || "?" }}</div>
              <span class="absolute -bottom-0.5 -right-0.5 w-4 h-4 rounded-full border-2 border-white" :class="fl.fl_is_active ? 'bg-[#4caf50]' : 'bg-[#bbb]'"></span>
            </div>
            <h2 class="text-[15px] font-bold text-[#111] mb-1.5">{{ fl.fl_name }}</h2>
            <span class="badge mb-3" :class="fl.fl_verify_status?.toLowerCase()">{{ fl.fl_verify_status }}</span>
            <p v-if="fl.fl_bio" class="text-[12px] text-[#777] leading-relaxed">{{ fl.fl_bio }}</p>
            <p v-else class="text-[12px] text-[#bbb] italic">No bio provided</p>
          </div>

          <!-- Stats — with icon header -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Stats</span>
            </div>
            <div class="px-4 py-3 grid grid-cols-3 gap-3 text-center">
              <div>
                <div class="text-[18px] font-bold text-[#111] flex items-center justify-center gap-1">
                  {{ Number(fl.fl_rating_avg || 0).toFixed(1) }}
                  <svg class="w-4 h-4 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </div>
                <div class="text-[11px] text-[#999] mt-0.5">Rating</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ jobsDone }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Completed</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ jobHistory.length }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Total Jobs</div>
              </div>
            </div>
          </div>

          <!-- Account — with icon header -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Account</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-if="fl.fl_username" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Username</div><div class="text-[13px] text-[#222] font-medium">{{ fl.fl_username }}</div></div>
              </div>
              <div v-if="fl.fl_email" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Email</div><div class="text-[13px] text-[#222] font-medium break-all">{{ fl.fl_email }}</div></div>
              </div>
              <div v-if="fl.fl_phone" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Phone</div><div class="text-[13px] text-[#222] font-medium">{{ fl.fl_phone }}</div></div>
              </div>
            </div>
          </div>

          <!-- Information — with icon header -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Information</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-if="fl.fl_date_of_birth" class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Date of Birth</div><div class="text-[13px] text-[#222] font-medium">{{ formatDate(fl.fl_date_of_birth) }}</div></div>
              </div>
              <div v-if="fl.fl_address" class="flex items-start gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0 mt-0.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Address</div><div class="text-[13px] text-[#222] font-medium leading-snug">{{ fl.fl_address }}</div></div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Joined</div><div class="text-[13px] text-[#222] font-medium">{{ formatDate(fl.fl_created_at) }}</div></div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last Updated</div><div class="text-[13px] text-[#222] font-medium">{{ formatDateTime(fl.fl_updated_at) }}</div></div>
              </div>
            </div>
          </div>

          <!-- Availability — above Languages -->
          <div v-if="availability.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Availability</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-2">
              <div v-for="a in availability" :key="a.fl_available_id"
                class="flex items-center gap-2 px-3 py-2 bg-[#f0fdf4] rounded-lg border border-[#bbf7d0]">
                <div class="shrink-0">
                  <div class="text-[10px] text-[#166534] uppercase tracking-wide font-semibold">Start</div>
                  <div class="text-[13px] font-semibold text-[#111] mt-0.5">{{ formatDate(a.fl_available_start_date) }}</div>
                </div>
                <svg class="w-3 h-3 text-[#86efac] shrink-0 mx-1" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                <div class="shrink-0">
                  <div class="text-[10px] text-[#166534] uppercase tracking-wide font-semibold">End</div>
                  <div class="text-[13px] font-semibold text-[#111] mt-0.5">{{ formatDate(a.fl_available_end_date) }}</div>
                </div>
                <span v-if="!a.is_active" class="ml-auto text-[10px] bg-[#f5f5f5] text-[#999] px-1.5 py-0.5 rounded-full">Inactive</span>
              </div>
            </div>
          </div>

          <!-- Languages & Areas — with icon header -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Languages</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div class="flex flex-wrap gap-1.5">
                <span v-for="l in languages" :key="l.fl_language_id" class="badge open">{{ l.fl_language_name }}</span>
                <span v-if="!languages.length" class="text-[13px] text-[#bbb]">–</span>
              </div>
              <div>
                <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-1.5">Pickup Areas</div>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="a in pickupAreas" :key="a.fl_area_id" class="badge in_progress">{{ a.fl_area_name }}</span>
                  <span v-if="!pickupAreas.length" class="text-[13px] text-[#bbb]">–</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Bank Account — with icon header, no Primary badge -->
          <div v-if="bankAccounts.length" class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 6l9-3 9 3M3 6v12a1 1 0 001 1h16a1 1 0 001-1V6M3 6h18M8 10v7m4-7v7m4-7v7"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Bank Account</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div v-for="b in bankAccounts" :key="b.fl_bank_account_id" class="flex flex-col gap-0.5">
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
              <!-- Inline verify row -->
              <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
                <div class="flex items-center gap-2">
                  <span class="text-[12px] text-[#999] font-medium">Status:</span>
                  <span class="badge" :class="fl.fl_verify_status?.toLowerCase()">{{ fl.fl_verify_status }}</span>
                </div>
                <div v-if="verification?.fl_verified_at" class="flex items-center gap-1.5">
                  <span class="text-[12px] text-[#999] font-medium">Verified:</span>
                  <span class="text-[13px] font-medium text-[#222]">{{ formatDate(verification.fl_verified_at) }}</span>
                </div>
                <div v-if="verification?.reviewed_by_name" class="flex items-center gap-1.5">
                  <span class="text-[12px] text-[#999] font-medium">Reviewed by:</span>
                  <span class="text-[13px] font-medium text-[#222]">{{ verification.reviewed_by_name }}</span>
                </div>
              </div>
              <!-- Documents — 5 cols, click → modal (no open file link) -->
              <div>
                <div class="text-[12px] font-bold text-[#444] uppercase tracking-wide mb-3">Documents</div>
                <div v-if="documents.length" class="grid grid-cols-5 gap-2">
                  <div v-for="d in documents" :key="d.fl_doc_id"
                    class="rounded-xl border border-[#eee] overflow-hidden bg-white flex flex-col cursor-pointer hover:border-[#aaa] transition-colors"
                    @click="openDocModal(d)">
                    <div class="h-[90px] bg-[#f5f5f5] relative overflow-hidden hover:opacity-90 transition-opacity">
                      <img :src="d.file_url" class="w-full h-full object-cover"
                        @error="(e) => { e.target.style.display='none'; e.target.nextElementSibling.style.display='flex' }" />
                      <div class="absolute inset-0 hidden items-center justify-center bg-[#f5f5f5]">
                        <svg class="w-5 h-5 text-[#ccc]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                      </div>
                    </div>
                    <div class="p-2 flex flex-col gap-0.5">
                      <span class="text-[11px] font-semibold text-[#222] leading-snug truncate">{{ formatDocType(d.fl_doc_type) }}</span>
                      <span class="badge self-start" :class="{ verified: d.fl_doc_status === 'APPROVED', cancelled: d.fl_doc_status === 'REJECTED', pending: d.fl_doc_status === 'PENDING' }">{{ d.fl_doc_status }}</span>
                      <span class="text-[10px] text-[#bbb]">{{ formatDate(d.fl_uploaded_at) }}</span>
                    </div>
                  </div>
                </div>
                <div v-else class="text-[13px] text-[#bbb]">No documents uploaded.</div>
              </div>
            </div>
          </div>

          <!-- Vehicle -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="vehicle">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="3" width="15" height="13" rx="2"/><path stroke-linecap="round" stroke-linejoin="round" d="M16 8h4l3 3v4h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Vehicle</span>
            </div>
            <div class="px-4 py-4">
              <div class="grid grid-cols-4 gap-x-5 gap-y-4 mb-5">
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Type</div><div class="text-[13px] font-medium text-[#222]">{{ vehicle.fl_vehicle_type }}</div></div>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Brand / Model</div><div class="text-[13px] font-medium text-[#222]">{{ vehicle.fl_vehicle_brand }} {{ vehicle.fl_vehicle_model }}</div></div>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Year</div><div class="text-[13px] font-medium text-[#222]">{{ vehicle.fl_vehicle_year }}</div></div>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Capacity</div><div class="text-[13px] font-medium text-[#222]">{{ vehicle.fl_vehicle_seat_capa }} seats</div></div>
                <div class="col-span-2"><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">License Plate</div><div class="text-[15px] font-bold text-[#222]">{{ vehicle.fl_vehicle_license_plate }}</div></div>
              </div>
              <!-- Vehicle Photos — 5 cols, full box, aspect-square -->
              <div v-if="vehicleImages.length">
                <div class="text-[12px] font-bold text-[#444] uppercase tracking-wide mb-2">Photos ({{ vehicleImages.length }})</div>
                <div class="grid grid-cols-5 gap-2">
                  <button v-for="img in vehicleImages" :key="img.fl_vehicle_image_id" type="button"
                    class="aspect-square rounded-lg overflow-hidden border border-[#ddd] hover:border-[#888] transition-colors bg-[#f5f5f5] cursor-pointer"
                    @click="openImgModal(img.fl_vehicle_image_url, 'Vehicle Photo')">
                    <div class="w-full h-full relative">
                      <img :src="img.fl_vehicle_image_url" class="absolute inset-0 w-full h-full object-cover"
                        @error="(e) => { e.target.style.display='none'; e.target.nextElementSibling.style.display='flex' }" />
                      <div class="absolute inset-0 hidden items-center justify-center bg-[#f0f0f0]">
                        <svg class="w-5 h-5 text-[#ccc]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Reviews -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="reviews.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Reviews from Employers</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ reviews.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="r in reviews" :key="r.fl_review_id" class="p-3.5 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] transition-colors">
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-[13px] font-semibold text-[#222]">{{ r.company }}</span>
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

          <!-- Job History — clickable to job detail -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="jobHistory.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path stroke-linecap="round" stroke-linejoin="round" d="M16 3H8a2 2 0 00-2 2v2h12V5a2 2 0 00-2-2z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Job History</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ jobHistory.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="j in jobHistory" :key="j.job_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] cursor-pointer hover:border-[#aaa] hover:bg-[#f0f0f0] transition-all"
                @click="router.push({ name: 'JobDetail', params: { id: j.job_id } })">
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222] truncate">{{ j.job_title }}</div>
                  <div class="text-[12px] text-[#999] mt-0.5">{{ j.company }} · {{ formatDate(j.job_start_date) }}</div>
                </div>
                <div class="flex flex-col items-end gap-1 shrink-0">
                  <span class="badge" :class="j.job_status?.toLowerCase()">{{ j.job_status }}</span>
                  <span class="text-[12px] font-semibold text-[#333]">{{ j.job_price ? "฿" + Number(j.job_price).toLocaleString() : "–" }}</span>
                </div>
                <svg class="w-4 h-4 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Image Modal (docs + vehicle photos) -->
    <div v-if="modalDoc" class="modal-overlay" @click.self="modalDoc = null">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden max-w-3xl w-full mx-4 flex flex-col" style="max-height:90vh" @click.stop>
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <div class="flex items-center gap-2.5">
            <span class="text-[15px] font-semibold text-[#111]">{{ modalDoc.title || "Preview" }}</span>
            <span v-if="modalDoc.status" class="badge" :class="{ verified: modalDoc.status === 'APPROVED', cancelled: modalDoc.status === 'REJECTED', pending: modalDoc.status === 'PENDING' }">{{ modalDoc.status }}</span>
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
    <div v-if="showBanModal" class="modal-overlay" @click.self="showBanModal = false">
      <div class="modal">
        <div class="modal-icon">
          <svg v-if="fl?.fl_is_active" class="w-10 h-10 mx-auto text-red-500" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
          <svg v-else class="w-10 h-10 mx-auto text-green-600" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <h3>{{ fl?.fl_is_active ? "Ban Freelancer" : "Unban Freelancer" }}</h3>
        <p>Are you sure you want to {{ fl?.fl_is_active ? "ban" : "unban" }} <strong>{{ fl?.fl_name }}</strong>?</p>
        <p v-if="fl?.fl_is_active" class="modal-warning">They will not be able to accept jobs or use the platform.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showBanModal = false">Cancel</button>
          <button class="btn-confirm" :class="fl?.fl_is_active ? 'ban' : 'unban'" @click="confirmBan">{{ fl?.fl_is_active ? "Ban" : "Unban" }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { API_BASE } from "../data/api"

const route = useRoute()
const router = useRouter()
const showBanModal = ref(false)
const fl = ref(null)
const languages = ref([])
const vehicle = ref(null)
const vehicleImages = ref([])
const pickupAreas = ref([])
const availability = ref([])
const documents = ref([])
const bankAccounts = ref([])
const reviews = ref([])
const jobHistory = ref([])
const verification = ref(null)
const loading = ref(true)
const modalDoc = ref(null)

const jobsDone = computed(() => jobHistory.value.filter(j => j.job_status === 'COMPLETED').length)

const openImgModal = (url, title = "") => {
  modalDoc.value = { url, title, status: null, uploadedAt: null, reviewedBy: null }
}
const openDocModal = (d) => {
  modalDoc.value = { url: d.file_url, title: formatDocType(d.fl_doc_type), status: d.fl_doc_status, uploadedAt: d.fl_uploaded_at, reviewedBy: d.reviewed_by_name || null }
}

const formatDate = (d) => { if (!d) return "–"; return new Date(d).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }) }
const formatDateTime = (d) => { if (!d) return "–"; return new Date(d).toLocaleString("en-GB", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }) }
const formatDocType = (t) => ({ PERSONAL_ID: "Personal ID", DRIVER_LICENSE: "Driver License", PUBLIC_DRIVER_LICENSE: "Public Driver License", VEHICLE_REGISTRATION: "Vehicle Registration", VEHICLE_INSPECTION: "Vehicle Inspection" }[t] || t)

const confirmBan = async () => {
  if (!fl.value) return
  try {
    const res = await fetch(`${API_BASE}/freelancers/${fl.value.fl_id}/ban`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ is_active: !fl.value.fl_is_active, admin_id: localStorage.getItem("admin_id") || "" }) })
    const data = await res.json()
    if (data.status === "updated") fl.value.fl_is_active = !fl.value.fl_is_active
  } catch (e) { console.error(e) } finally { showBanModal.value = false }
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [flRes, langRes, vehicleRes, imgRes, areaRes, availRes, docRes, bankRes, reviewRes, jobsRes, verifyRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers/${id}`),
      fetch(`${API_BASE}/fl-languages?limit=500`),
      fetch(`${API_BASE}/fl-vehicle?limit=500`),
      fetch(`${API_BASE}/fl-vehicle-images?limit=500`),
      fetch(`${API_BASE}/fl-pickup-areas?limit=500`),
      fetch(`${API_BASE}/fl-availability?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
      fetch(`${API_BASE}/fl-bank-accounts?limit=500`),
      fetch(`${API_BASE}/fl-reviews?limit=500`),
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/fl-verification?limit=500`),
    ])
    const [flData, langData, vehicleData, imgData, areaData, availData, docData, bankData, reviewData, jobsData, verifyData] = await Promise.all([
      flRes.json(), langRes.json(), vehicleRes.json(), imgRes.json(), areaRes.json(), availRes.json(), docRes.json(), bankRes.json(), reviewRes.json(), jobsRes.json(), verifyRes.json(),
    ])
    fl.value = flData.fl_id ? flData : null
    languages.value = (langData.items || []).filter(l => String(l.fl_id) === String(id))
    vehicle.value = (vehicleData.items || []).find(v => String(v.fl_id) === String(id)) || null
    const vId = vehicle.value?.fl_vehicle_id
    vehicleImages.value = vId ? (imgData.items || []).filter(i => i.fl_vehicle_id === vId) : []
    pickupAreas.value = (areaData.items || []).filter(a => String(a.fl_id) === String(id))
    availability.value = (availData.items || []).filter(a => String(a.fl_id) === String(id))
    const allDocs = (docData.items || []).filter(d => String(d.fl_id) === String(id))
    const byType = {}
    allDocs.forEach(d => { if (!byType[d.fl_doc_type] || new Date(d.fl_uploaded_at) > new Date(byType[d.fl_doc_type].fl_uploaded_at)) byType[d.fl_doc_type] = d })
    documents.value = Object.values(byType)
    bankAccounts.value = (bankData.items || []).filter(b => String(b.fl_id) === String(id))
    reviews.value = (reviewData.items || []).filter(r => String(r.fl_id) === String(id))
    jobHistory.value = (jobsData.items || []).filter(j => String(j.selected_fl_id) === String(id))
    const verList = (verifyData.items || []).filter(v => String(v.fl_id) === String(id) && (v.is_latest === true || v.is_latest === 1))
    verification.value = verList[0] || null
  } catch (e) { console.error(e) } finally { loading.value = false }
})
</script>