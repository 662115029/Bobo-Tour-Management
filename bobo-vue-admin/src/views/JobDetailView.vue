<template>
  <div>
    <BreadcrumbBar :label="job?.job_title" />

    <!-- Loading skeleton — mirrors real layout -->
    <div v-if="loading" class="px-5 pb-8">
      <!-- Top bar -->
      <div class="flex items-center justify-between py-3 mb-5">
        <div class="animate-pulse bg-[#ebebeb] h-4 w-16 rounded"></div>
        <div class="animate-pulse bg-[#ebebeb] h-8 w-28 rounded-lg"></div>
      </div>
      <!-- Hero card -->
      <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-6 mb-4">
        <div class="flex items-start justify-between gap-4 mb-5">
          <div class="flex-1 flex flex-col gap-2.5">
            <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
            <div class="animate-pulse bg-[#ebebeb] h-7 w-72 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3.5 w-36 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-full max-w-lg rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-3 w-4/5 max-w-md rounded"></div>
          </div>
          <div class="shrink-0 flex flex-col items-end gap-2">
            <div class="animate-pulse bg-[#ebebeb] h-2.5 w-10 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-9 w-32 rounded"></div>
          </div>
        </div>
        <div class="grid grid-cols-4 gap-3 pt-4 border-t border-[#f0f0f0]">
          <div v-for="i in 4" :key="i" class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 flex flex-col gap-1.5">
            <div class="animate-pulse bg-[#ebebeb] h-2 w-14 rounded"></div>
            <div class="animate-pulse bg-[#ebebeb] h-4 w-20 rounded"></div>
          </div>
        </div>
      </div>
      <!-- Two column grid -->
      <div class="grid gap-4" style="grid-template-columns: 320px 1fr; align-items: start;">
        <!-- LEFT skeleton -->
        <div class="flex flex-col gap-3">
          <!-- Languages card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-32 rounded"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-4">
              <div class="flex flex-col gap-2">
                <div class="animate-pulse bg-[#ebebeb] h-2.5 w-32 rounded"></div>
                <div class="flex gap-1.5">
                  <div v-for="i in 3" :key="i" class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full"></div>
                </div>
              </div>
              <div class="flex flex-col gap-2">
                <div class="animate-pulse bg-[#ebebeb] h-2.5 w-28 rounded"></div>
                <div class="flex items-center gap-2">
                  <div class="animate-pulse bg-[#ebebeb] w-7 h-7 rounded-full shrink-0"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-4 w-32 rounded"></div>
                </div>
              </div>
            </div>
          </div>
          <!-- Timeline card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-16 rounded"></div>
            </div>
            <div class="px-4 py-3 flex flex-col gap-4">
              <div v-for="i in 2" :key="i" class="flex items-center gap-2.5">
                <div class="animate-pulse bg-[#ebebeb] w-3.5 h-3.5 rounded shrink-0"></div>
                <div class="flex flex-col gap-1 flex-1">
                  <div class="animate-pulse bg-[#ebebeb] h-2 w-14 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-36 rounded"></div>
                </div>
              </div>
            </div>
          </div>
          <!-- Expenses card -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-18 rounded"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-0">
              <div v-for="i in 4" :key="i" class="flex items-center justify-between py-2 border-b border-[#f5f5f5]">
                <div class="animate-pulse bg-[#ebebeb] h-3.5 w-32 rounded"></div>
                <div class="animate-pulse bg-[#ebebeb] h-3.5 w-16 rounded"></div>
              </div>
              <div class="flex items-center justify-between pt-3">
                <div class="animate-pulse bg-[#ebebeb] h-4 w-10 rounded"></div>
                <div class="animate-pulse bg-[#ebebeb] h-4 w-20 rounded"></div>
              </div>
            </div>
          </div>
        </div>
        <!-- RIGHT skeleton -->
        <div class="flex flex-col gap-3">
          <!-- Pickup box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="i in 3" :key="i" class="flex items-center gap-3 px-4 py-3 rounded-lg border border-[#e8e8e8]">
                <div class="animate-pulse bg-[#ebebeb] w-6 h-6 rounded-full shrink-0"></div>
                <div class="flex-1 flex flex-col gap-1.5">
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-48 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-2.5 w-24 rounded"></div>
                </div>
                <div class="animate-pulse bg-[#ebebeb] h-6 w-14 rounded-md shrink-0"></div>
              </div>
            </div>
          </div>
          <!-- Itinerary box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-18 rounded"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="i in 4" :key="i" class="flex items-center gap-3 px-4 py-3 rounded-lg border border-[#e8e8e8]">
                <div class="animate-pulse bg-[#ebebeb] w-6 h-6 rounded-full shrink-0"></div>
                <div class="flex-1 flex flex-col gap-1.5">
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-40 rounded"></div>
                </div>
                <div class="animate-pulse bg-[#ebebeb] h-6 w-24 rounded-md shrink-0"></div>
              </div>
            </div>
          </div>
          <!-- Applications box -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <div class="animate-pulse bg-[#ebebeb] w-4 h-4 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-3 w-24 rounded"></div>
              <div class="animate-pulse bg-[#ebebeb] h-5 w-8 rounded-full ml-auto"></div>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="i in 3" :key="i" class="flex items-center gap-3 px-4 py-3 rounded-lg border border-[#e8e8e8]">
                <div class="animate-pulse bg-[#ebebeb] w-8 h-8 rounded-full shrink-0"></div>
                <div class="flex-1 flex flex-col gap-1.5">
                  <div class="animate-pulse bg-[#ebebeb] h-3.5 w-32 rounded"></div>
                  <div class="animate-pulse bg-[#ebebeb] h-2.5 w-44 rounded"></div>
                </div>
                <div class="animate-pulse bg-[#ebebeb] h-5 w-16 rounded-full shrink-0"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="!job" class="empty">Job not found.</div>

    <div v-else class="px-5 pb-8">
      <!-- Top Bar -->
      <div class="flex items-center justify-between py-3 mb-5">
        <button class="flex items-center gap-1.5 text-[13px] text-[#555] hover:text-black cursor-pointer border-none bg-transparent" @click="router.back()">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          Back
        </button>
        <button class="btn-action delete flex items-center gap-1.5 !px-3.5 !py-2 !text-[13px] !rounded-lg" @click="showDeleteModal = true">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"/><path stroke-linecap="round" stroke-linejoin="round" d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6m5 0V4a1 1 0 011-1h2a1 1 0 011 1v2"/></svg>
          Delete Job
        </button>
      </div>

      <!-- Hero Card -->
      <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-6 mb-4 hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between gap-4 mb-5">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-2">
              <span class="badge" :class="job.job_status?.toLowerCase()">{{ formatJobStatus(job.job_status) }}</span>
            </div>
            <h1 class="text-[20px] font-bold text-[#111] leading-tight mb-1.5">{{ job.job_title }}</h1>
            <div class="flex items-center gap-1.5 text-[13px] text-[#666]">
              <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0H3m14 0h2M3 21h2"/></svg>
              {{ job.company }}
            </div>
            <p v-if="job.job_description" class="text-[13px] text-[#888] leading-relaxed mt-2 max-w-2xl">{{ job.job_description }}</p>
          </div>
          <div class="text-right shrink-0">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-1">Price</div>
            <div class="text-[26px] font-bold text-[#111]">{{ job.job_price ? "฿" + Number(job.job_price).toLocaleString() : "–" }}</div>
          </div>
        </div>
        <!-- Quick info boxes inside hero -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-[#f0f0f0]">
          <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 hover:border-[#ddd] hover:bg-[#f0f0f0] transition-colors">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Start Date</div>
            <div class="text-[14px] font-semibold text-[#222]">{{ formatDate(job.job_start_date) }}</div>
          </div>
          <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 hover:border-[#ddd] hover:bg-[#f0f0f0] transition-colors">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">End Date</div>
            <div class="text-[14px] font-semibold text-[#222]">{{ formatDate(job.job_end_date) }}</div>
          </div>
          <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 hover:border-[#ddd] hover:bg-[#f0f0f0] transition-colors">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Vehicle</div>
            <div class="text-[14px] font-semibold text-[#222]">{{ job.job_required_vehicle_type || "–" }}</div>
          </div>
          <div class="bg-[#f8f9fa] rounded-lg border border-[#eee] px-3 py-2.5 hover:border-[#ddd] hover:bg-[#f0f0f0] transition-colors">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-0.5">Seats Required</div>
            <div class="text-[14px] font-semibold text-[#222]">{{ job.job_required_seat || "–" }}</div>
          </div>
        </div>
      </div>

      <!-- 2-col layout -->
      <div class="grid gap-4" style="grid-template-columns: 320px 1fr; align-items: start;">

        <!-- ── LEFT ── -->
        <div class="flex flex-col gap-3">

          <!-- Languages & Driver -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Languages & Driver</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-4">
              <div>
                <div class="text-[11px] text-[#aaa] uppercase tracking-wide font-semibold mb-2">Required Languages</div>
                <div class="flex flex-wrap gap-1.5">
                  <span v-for="lang in languages" :key="lang.job_req_lg_id" class="info-tag language">{{ lang.language_name }}</span>
                  <span v-if="!languages.length" class="text-[13px] text-[#bbb]">None specified</span>
                </div>
              </div>
              <div>
                <div class="text-[11px] text-[#aaa] uppercase tracking-wide font-semibold mb-2">Assigned Driver</div>
                <div v-if="job.selected_driver" class="flex items-center gap-2">
                  <div class="w-7 h-7 rounded-full bg-[#e3f2fd] flex items-center justify-center text-[12px] font-bold text-[#1976d2]">{{ job.selected_driver[0] }}</div>
                  <span class="text-[14px] font-medium text-[#222]">{{ job.selected_driver }}</span>
                </div>
                <span v-else class="text-[13px] text-[#bbb]">Not assigned</span>
              </div>
            </div>
          </div>

          <!-- Timeline -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Timeline</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Created</div><div class="text-[13px] font-medium text-[#222]">{{ formatDateTime(job.job_created_at) }}</div></div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/></svg>
                <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last Updated</div><div class="text-[13px] font-medium text-[#222]">{{ formatDateTime(job.job_updated_at) }}</div></div>
              </div>
            </div>
          </div>

          <!-- Entrance Fees -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="entranceFees.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Entrance Fees</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="fee in entranceFees" :key="fee.job_entrance_fee_id" class="p-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] transition-colors">
                <div class="text-[13px] font-semibold text-[#222] mb-2">{{ fee.place_name }}</div>
                <div class="grid grid-cols-2 gap-2">
                  <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Thai</div><div class="text-[13px] font-semibold text-[#222]">{{ fee.thai_price > 0 ? "฿" + Number(fee.thai_price).toLocaleString() : "Free" }}</div></div>
                  <div><div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Foreigner</div><div class="text-[13px] font-semibold text-[#222]">{{ fee.foreigner_price > 0 ? "฿" + Number(fee.foreigner_price).toLocaleString() : "Free" }}</div></div>
                </div>
                <div v-if="fee.note" class="text-[11px] text-[#999] mt-1.5">{{ fee.note }}</div>
              </div>
            </div>
          </div>

          <!-- Expenses -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="expenses.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="12" y1="1" x2="12" y2="23"/><path stroke-linecap="round" stroke-linejoin="round" d="M17 5H9.5a3.5 3.5 0 000 7h5a3.5 3.5 0 010 7H6"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Expenses</span>
            </div>
            <div class="px-4 py-4">
              <div class="flex flex-col divide-y divide-[#f0f0f0]">
                <div v-for="e in expenses" :key="e.job_expense_id" class="flex items-center justify-between py-2 hover:bg-[#fafafa] transition-colors px-1 rounded">
                  <span class="text-[13px] text-[#444]">{{ e.item_name }}</span>
                  <span class="text-[13px] font-semibold text-[#222]">{{ e.amount ? "฿" + Number(e.amount).toLocaleString() : "–" }}</span>
                </div>
              </div>
              <div class="flex items-center justify-between pt-3 mt-1 border-t-2 border-[#eee]">
                <span class="text-[13px] font-bold text-[#111]">Total</span>
                <span class="text-[15px] font-bold text-[#111]">฿{{ Number(expenses.reduce((s, e) => s + Number(e.amount || 0), 0)).toLocaleString() }}</span>
              </div>
            </div>
          </div>

          <!-- Customers -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="customers.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Customers</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ customers.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-1.5">
              <div v-for="c in customers" :key="c.job_customer_id" class="flex items-center justify-between py-1.5 px-2 rounded-lg border-b border-[#f5f5f5] last:border-0 hover:bg-[#fafafa] transition-colors">
                <span class="text-[13px] font-medium text-[#222]">{{ c.customer_name }}</span>
                <div class="flex items-center gap-1.5">
                  <span v-if="c.pax_count" class="text-[12px] text-[#555] bg-[#f0f4ff] px-2 py-0.5 rounded-full">{{ c.pax_count }} pax</span>
                  <span v-if="c.note" class="text-[11px] text-[#aaa]">{{ c.note }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment — slip shown inline -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="payments.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Payment</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-3">
              <div v-for="pay in payments" :key="pay.payment_id" class="rounded-xl border border-[#e8e8e8] bg-[#f8f9fa] hover:border-[#ddd] hover:bg-[#f5f5f5] transition-colors overflow-hidden">
                <div class="px-4 py-3 flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <div class="w-7 h-7 rounded-full bg-[#e3f2fd] flex items-center justify-center text-[12px] font-bold text-[#1976d2] shrink-0">{{ (pay.driver_name || "?")[0] }}</div>
                    <span class="text-[13px] font-medium text-[#222]">{{ pay.driver_name }}</span>
                  </div>
                  <span class="payment-badge" :class="pay.payment_status?.toLowerCase()">{{ pay.payment_status }}</span>
                </div>
                <div v-if="pay.paid_at || pay.confirmed_at || pay.reject_reason" class="px-4 pb-3 flex flex-col gap-1">
                  <div v-if="pay.paid_at" class="text-[11px] text-[#888]">Paid: {{ formatDateTime(pay.paid_at) }}</div>
                  <div v-if="pay.confirmed_at" class="text-[11px] text-[#888]">Confirmed: {{ formatDateTime(pay.confirmed_at) }}</div>
                  <div v-if="pay.reject_reason" class="text-[11px] text-red-600">Reason: {{ pay.reject_reason }}</div>
                </div>
                <!-- Slip image shown inline like document preview -->
                <div v-if="pay.slip_url" class="border-t border-[#eee]">
                  <div class="px-4 py-2 text-[10px] text-[#aaa] uppercase tracking-wide font-medium">Payment Slip</div>
                  <div class="h-[160px] bg-[#f0f0f0] overflow-hidden cursor-pointer hover:opacity-90 transition-opacity"
                    @click="openSlipModal(pay.slip_url)">
                    <img :src="pay.slip_url" class="w-full h-full object-contain"
                      @error="(e) => { e.target.style.display='none'; e.target.nextElementSibling.style.display='flex' }" />
                    <div class="hidden w-full h-full items-center justify-center flex-col gap-1.5">
                      <svg class="w-7 h-7 text-[#ccc]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                      <span class="text-[11px] text-[#bbb]">Tap to view</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- ── RIGHT ── -->
        <div class="flex flex-col gap-3">

          <!-- Pickup Points -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="pickups.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Pickup Points</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="(p, i) in pickups" :key="p.job_pickup_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] hover:bg-[#f2f2f2] transition-colors">
                <div class="w-6 h-6 rounded-full bg-[#e3f2fd] text-[#1976d2] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222]">{{ p.pickup_location }}</div>
                  <div v-if="p.hotel_name" class="text-[11px] text-[#999] mt-0.5">{{ p.hotel_name }}</div>
                </div>
                <span class="text-[12px] font-bold text-[#1976d2] bg-[#e3f2fd] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ p.pickup_time }}</span>
              </div>
            </div>
          </div>

          <!-- Itinerary -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="itineraries.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Itinerary</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="(item, i) in itineraries" :key="item.job_itinerary_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] hover:bg-[#f2f2f2] transition-colors">
                <div class="w-6 h-6 rounded-full bg-[#f3e5f5] text-[#7b1fa2] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222]">{{ item.place_name }}</div>
                  <div v-if="item.note" class="text-[11px] text-[#999] mt-0.5">{{ item.note }}</div>
                </div>
                <span class="text-[12px] font-bold text-[#7b1fa2] bg-[#f3e5f5] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ item.start_time }} – {{ item.end_time }}</span>
              </div>
            </div>
          </div>

          <!-- Passengers -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="passengers.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path stroke-linecap="round" stroke-linejoin="round" d="M23 21v-2a4 4 0 00-3-3.87m-4-12a4 4 0 010 7.75"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Passengers</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ passengers.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="(p, i) in passengers" :key="p.job_passenger_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] hover:border-[#ddd] hover:bg-[#f2f2f2] transition-colors">
                <div class="w-6 h-6 rounded-full bg-[#e8f5e9] text-[#2e7d32] text-[11px] font-bold flex items-center justify-center shrink-0">{{ i + 1 }}</div>
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222]">{{ p.first_name }} {{ p.last_name }}</div>
                  <div class="text-[11px] text-[#999] mt-0.5">
                    <span v-if="p.hotel_name">{{ p.hotel_name }}</span>
                    <span v-if="p.hotel_name && p.note" class="mx-1 text-[#ddd]">·</span>
                    <span v-if="p.note">{{ p.note }}</span>
                  </div>
                </div>
                <span class="text-[12px] font-bold text-[#1976d2] bg-[#e3f2fd] px-2 py-0.5 rounded-md whitespace-nowrap shrink-0">{{ formatPickupTime(p.pickup_time) }}</span>
              </div>
            </div>
          </div>

          <!-- Inclusions -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="inclusions.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Inclusions</span>
            </div>
            <div class="px-4 py-4 grid grid-cols-2 gap-4">
              <div>
                <div class="flex items-center gap-1.5 text-[11px] font-semibold text-[#2e7d32] uppercase tracking-wide mb-2">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
                  Included
                </div>
                <div class="flex flex-col gap-1.5">
                  <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'INCLUDED')" :key="inc.job_inclusion_id"
                    class="text-[13px] text-[#166534] bg-[#f0fdf4] px-3 py-2 rounded-lg border border-[#bbf7d0] hover:border-[#86efac] transition-colors">{{ inc.description }}</div>
                  <div v-if="!inclusions.filter(i => i.inclusion_type === 'INCLUDED').length" class="text-[13px] text-[#bbb]">None</div>
                </div>
              </div>
              <div>
                <div class="flex items-center gap-1.5 text-[11px] font-semibold text-[#c62828] uppercase tracking-wide mb-2">
                  <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                  Not Included
                </div>
                <div class="flex flex-col gap-1.5">
                  <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED')" :key="inc.job_inclusion_id"
                    class="text-[13px] text-[#991b1b] bg-[#fef2f2] px-3 py-2 rounded-lg border border-[#fecaca] hover:border-[#fca5a5] transition-colors">{{ inc.description }}</div>
                  <div v-if="!inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED').length" class="text-[13px] text-[#bbb]">None</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Applications — clickable to freelancer detail -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow" v-if="applications.length">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Applications</span>
              <span class="ml-auto inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{ applications.length }}</span>
            </div>
            <div class="px-4 py-4 flex flex-col gap-2">
              <div v-for="app in applications" :key="app.job_application_id"
                class="flex items-center gap-3 px-4 py-3 bg-[#f8f9fa] rounded-lg border border-[#e8e8e8] cursor-pointer hover:border-[#aaa] hover:bg-[#f0f0f0] transition-all"
                @click="app.fl_id && router.push({ name: 'FreelancerDetail', params: { id: app.fl_id } })">
                <div class="w-8 h-8 rounded-full bg-[#e3f2fd] flex items-center justify-center text-[13px] font-bold text-[#1976d2] shrink-0">{{ (app.driver_name || "?")[0] }}</div>
                <div class="flex-1 min-w-0">
                  <div class="text-[13px] font-medium text-[#222]">{{ app.driver_name }}</div>
                  <div class="text-[11px] text-[#999] mt-0.5">Applied {{ formatDateTime(app.applied_at) }}</div>
                </div>
                <span class="application-badge shrink-0" :class="app.application_status?.toLowerCase()">{{ app.application_status }}</span>
                <svg class="w-4 h-4 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/></svg>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Slip Image Modal -->
    <div v-if="slipModal" class="modal-overlay" @click.self="slipModal = null">
      <div class="bg-white rounded-2xl shadow-2xl overflow-hidden max-w-xl w-full mx-4 flex flex-col" style="max-height:90vh" @click.stop>
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#eee] shrink-0">
          <span class="text-[15px] font-semibold text-[#111]">Payment Slip</span>
          <button class="text-[#999] hover:text-[#333] border-none bg-transparent cursor-pointer" @click="slipModal = null">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="bg-[#111] flex items-center justify-center flex-1" style="min-height:400px">
          <img :src="slipModal" class="max-w-full object-contain" style="max-height:calc(90vh - 56px)" />
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <DeleteJobModal :show="showDeleteModal" :title="job?.job_title"
      @confirm="confirmDelete" @cancel="showDeleteModal = false" />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import DeleteJobModal from '../components/DeleteJobModal.vue'
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { API_BASE } from "../data/api"
import { formatDate, formatDateTime } from '../utils/formatDate'
import { formatJobStatus } from '../utils/statusClasses'

const route = useRoute()
const router = useRouter()

const job = ref(null)
const languages = ref([])
const pickups = ref([])
const itineraries = ref([])
const passengers = ref([])
const inclusions = ref([])
const entranceFees = ref([])
const expenses = ref([])
const customers = ref([])
const applications = ref([])
const payments = ref([])
const loading = ref(true)
const showDeleteModal = ref(false)
const slipModal = ref(null)

const openSlipModal = (url) => { slipModal.value = url }

const formatPickupTime = (val) => {
  if (!val) return "–"
  if (typeof val === "number" || /^\d+$/.test(String(val))) {
    const secs = Number(val)
    return `${String(Math.floor(secs / 3600)).padStart(2, "0")}:${String(Math.floor((secs % 3600) / 60)).padStart(2, "0")}`
  }
  return val
}

const confirmDelete = async () => {
  try {
    const adminId = localStorage.getItem("admin_id") || ""
    const res = await fetch(`${API_BASE}/jobs/${job.value.job_id}?admin_id=${adminId}`, { method: "DELETE" })
    if (res.ok || res.status === 404) {
      router.push({ name: "Jobs" })
    }
  } catch (e) { console.error(e) } finally { showDeleteModal.value = false }
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [jobsRes, langRes, pickupsRes, itinRes, passRes, inclRes, feesRes, expRes, custRes, appRes, payRes] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/job-required-languages?limit=500`),
      fetch(`${API_BASE}/job-pickups?limit=500`),
      fetch(`${API_BASE}/job-itineraries?limit=500`),
      fetch(`${API_BASE}/job-passengers?limit=500`),
      fetch(`${API_BASE}/job-inclusions?limit=500`),
      fetch(`${API_BASE}/job-entrance-fees?limit=500`),
      fetch(`${API_BASE}/job-expenses?limit=500`),
      fetch(`${API_BASE}/job-customers?limit=500`),
      fetch(`${API_BASE}/job-applications?limit=500`),
      fetch(`${API_BASE}/job-payments?limit=500`),
    ])
    const [jobsData, langData, pickupsData, itinData, passData, inclData, feesData, expData, custData, appData, payData] = await Promise.all([
      jobsRes.json(), langRes.json(), pickupsRes.json(), itinRes.json(), passRes.json(),
      inclRes.json(), feesRes.json(), expRes.json(), custRes.json(), appRes.json(), payRes.json(),
    ])
    const sid = String(id)
    job.value = (jobsData.items || []).find(j => String(j.job_id) === sid) || null
    languages.value = (langData.items || []).filter(l => String(l.job_id) === sid)
    pickups.value = (pickupsData.items || []).filter(p => String(p.job_id) === sid).sort((a, b) => a.sequence - b.sequence)
    itineraries.value = (itinData.items || []).filter(i => String(i.job_id) === sid).sort((a, b) => a.sequence - b.sequence)
    passengers.value = (passData.items || []).filter(p => String(p.job_id) === sid)
    inclusions.value = (inclData.items || []).filter(i => String(i.job_id) === sid).sort((a, b) => a.sequence - b.sequence)
    entranceFees.value = (feesData.items || []).filter(f => String(f.job_id) === sid).sort((a, b) => a.sequence - b.sequence)
    expenses.value = (expData.items || []).filter(e => String(e.job_id) === sid).sort((a, b) => a.sequence - b.sequence)
    customers.value = (custData.items || []).filter(c => String(c.job_id) === sid)
    applications.value = (appData.items || []).filter(a => String(a.job_id) === sid)
    payments.value = (payData.items || []).filter(p => String(p.job_id) === sid)
  } catch (e) { console.error(e) } finally { loading.value = false }
})
</script>