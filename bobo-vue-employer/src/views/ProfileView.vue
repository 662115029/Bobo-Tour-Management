<template>
  <AppLayout>
    <div class="px-5 pb-10">
      <div class="flex items-center py-3 mb-5">
        <button @click="$router.back()"
          class="flex items-center gap-1.5 text-sm font-medium text-gray-600 bg-white hover:bg-[#ffd8d8] hover:text-[#dc2626] px-4 py-2 rounded-full transition w-fit">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/></svg>
          Back
        </button>
      </div>

      <div class="grid gap-4 grid-cols-1 lg:grid-cols-[260px_1fr] items-start">

        <!-- LEFT -->
        <div class="flex flex-col gap-3">

          <!-- Profile Hero -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 flex flex-col items-center text-center hover:shadow-md transition-shadow">
            <div class="w-20 h-20 rounded-full bg-[#fef2f2] overflow-hidden flex items-center justify-center mb-3 cursor-pointer group relative" @click="avatarModal = true">
              <img v-if="form.em_profile_url" :src="form.em_profile_url" class="w-full h-full object-cover" @error="form.em_profile_url = ''" />
              <svg v-else class="w-9 h-9 text-[#dc2626]" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z"/>
              </svg>
              <div class="absolute inset-0 rounded-full bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
              </div>
            </div>
            <div class="text-[15px] font-bold text-[#111] mb-1">{{ form.em_name || 'Your Name' }}</div>
            <div class="text-[12px] text-[#999] mb-2">@{{ form.em_username }}</div>
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold uppercase tracking-wide mb-1"
              :class="form.em_verify_status === 'VERIFIED' ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'">
              {{ form.em_verify_status || 'PENDING' }}
            </span>
            <div v-if="verifiedAt" class="text-[11px] text-[#bbb] mb-3">Verified {{ formatDateTime(verifiedAt) }}</div>
            <div v-else class="mb-3"></div>
            <p v-if="form.em_bio" class="text-[12px] text-[#777] leading-relaxed">{{ form.em_bio }}</p>
            <p v-else class="text-[12px] text-[#bbb] italic">No bio provided</p>
          </div>

          <!-- Stats -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Stats</span>
            </div>
            <div class="px-4 py-3 grid grid-cols-3 gap-2 text-center">
              <div>
                <div class="text-[18px] font-bold text-[#111] flex items-center justify-center gap-1">
                  {{ Number(form.em_rating_avg || 0).toFixed(1) }}
                  <svg class="w-4 h-4 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </div>
                <div class="text-[11px] text-[#999] mt-0.5">Rating</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ completedJobs }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Completed</div>
              </div>
              <div>
                <div class="text-[18px] font-bold text-[#111]">{{ totalJobs }}</div>
                <div class="text-[11px] text-[#999] mt-0.5">Total Jobs</div>
              </div>
            </div>
          </div>

          <!-- Change Password -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Information</span>
            </div>
            <div class="px-4 py-3 flex flex-col gap-3">
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                <div>
                  <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Created</div>
                  <div class="text-[13px] text-[#222] font-medium">{{ formatDateTime(form.em_created_at) }}</div>
                </div>
              </div>
              <div class="flex items-center gap-2.5">
                <svg class="w-3.5 h-3.5 text-[#ccc] shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/></svg>
                <div>
                  <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last Updated</div>
                  <div class="text-[13px] text-[#222] font-medium">{{ formatDateTime(form.em_updated_at) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Change Password -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-4 py-3 border-b border-[#f0f0f0] flex items-center gap-2">
              <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/></svg>
              <span class="text-[12px] font-bold text-[#444] uppercase tracking-wide">Change Password</span>
            </div>
            <div class="px-4 py-4">
              <div v-if="!pwOpen">
                <button @click="pwOpen = true" class="px-4 py-2 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#555] hover:bg-[#f5f5f5] transition">Change Password</button>
              </div>
              <div v-else class="flex flex-col gap-3">
                <div v-if="pwSuccess" class="px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-[13px] text-green-700">Password changed!</div>
                <div v-if="pwError" class="px-3 py-2 bg-red-50 border border-red-200 rounded-lg text-[13px] text-red-600">{{ pwError }}</div>
                <div>
                  <label class="field-label">Current Password</label>
                  <input v-model="pwForm.current" type="password" class="field-input" placeholder="Enter current password" />
                </div>
                <div>
                  <label class="field-label">New Password</label>
                  <input v-model="pwForm.newPw" type="password" minlength="6" class="field-input" placeholder="At least 6 characters" />
                </div>
                <div>
                  <label class="field-label">Confirm New Password</label>
                  <input v-model="pwForm.confirm" type="password" class="field-input" placeholder="Re-enter new password" @keyup.enter="changePassword" />
                </div>
                <div class="flex items-center justify-between">
                  <button @click="pwOpen = false; pwError = ''" class="text-[12px] text-[#bbb] hover:text-[#666]">Cancel</button>
                  <button @click="changePassword" :disabled="changingPw || !pwForm.current || !pwForm.newPw || !pwForm.confirm"
                    class="px-4 py-2 text-[13px] font-semibold rounded-lg bg-[#222] text-white hover:bg-[#444] transition disabled:opacity-50">
                    {{ changingPw ? 'Updating…' : 'Update Password' }}
                  </button>
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT -->
        <div class="flex flex-col gap-3">

          <!-- Edit Profile -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-5 py-3 border-b border-[#f0f0f0] flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Edit Profile</span>
              </div>
              <div class="flex items-center gap-2">
                <button v-if="!isEditing" @click="startEditing" class="px-3.5 py-1.5 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition">Edit</button>
                <button v-if="isEditing" @click="cancelEditing" class="px-3.5 py-1.5 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition">Cancel</button>
                <button v-if="isEditing" @click="handleSubmit" :disabled="saving"
                  class="px-4 py-1.5 text-[13px] font-semibold rounded-lg bg-red-600 text-white hover:bg-red-700 transition disabled:opacity-50">
                  {{ saving ? 'Saving…' : 'Save' }}
                </button>
              </div>
            </div>
            <div v-if="saveSuccess" class="mx-5 mt-4 px-4 py-2.5 bg-green-50 border border-green-200 rounded-lg text-[13px] text-green-700">Profile updated successfully!</div>
            <div v-if="saveError" class="mx-5 mt-4 px-4 py-2.5 bg-red-50 border border-red-200 rounded-lg text-[13px] text-red-600">{{ saveError }}</div>
            <div class="px-5 py-5 grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label class="field-label">Username</label>
                <div class="relative">
                  <input v-model="form.em_username" type="text" disabled class="field-input bg-[#f8f9fa] text-[#aaa] cursor-not-allowed pr-14" />
                  <span class="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-semibold text-[#bbb] uppercase tracking-wide">Fixed</span>
                </div>
              </div>
              <div>
                <label class="field-label">Full Name <span class="text-red-500">*</span></label>
                <input v-model="form.em_name" type="text" :disabled="!isEditing" @input="touched.em_name = true"
                  :class="isEditing ? 'bg-white' : 'bg-[#f8f9fa] text-[#666] cursor-default'" class="field-input" />
                <p v-if="isEditing && touched.em_name && !form.em_name" class="text-[11px] text-red-500 mt-1">Required</p>
              </div>
              <div>
                <label class="field-label">Phone <span class="text-red-500">*</span></label>
                <input v-model="form.em_phone" type="tel" :disabled="!isEditing" placeholder="08x xxx xxxx" @input="touched.em_phone = true"
                  :class="isEditing ? 'bg-white' : 'bg-[#f8f9fa] text-[#666] cursor-default'" class="field-input" />
                <p v-if="isEditing && touched.em_phone && !form.em_phone" class="text-[11px] text-red-500 mt-1">Required</p>
              </div>
              <div>
                <label class="field-label">Email <span class="text-red-500">*</span></label>
                <input v-model="form.em_email" type="email" :disabled="!isEditing" @input="touched.em_email = true"
                  :class="isEditing ? 'bg-white' : 'bg-[#f8f9fa] text-[#666] cursor-default'" class="field-input" />
                <p v-if="isEditing && touched.em_email && !form.em_email" class="text-[11px] text-red-500 mt-1">Required</p>
              </div>
              <div class="col-span-1 sm:col-span-2">
                <label class="field-label">Address <span class="text-red-500">*</span></label>
                <input v-model="form.em_address" type="text" :disabled="!isEditing" placeholder="e.g. Chiang Mai, Thailand" @input="touched.em_address = true"
                  :class="isEditing ? 'bg-white' : 'bg-[#f8f9fa] text-[#666] cursor-default'" class="field-input" />
                <p v-if="isEditing && touched.em_address && !form.em_address" class="text-[11px] text-red-500 mt-1">Required</p>
              </div>
              <div class="col-span-1 sm:col-span-2">
                <label class="field-label">Bio <span class="text-[#ccc] font-normal normal-case tracking-normal">(optional)</span></label>
                <textarea v-model="form.em_bio" rows="3" :disabled="!isEditing" placeholder="Brief description of your tour company..."
                  :class="isEditing ? 'bg-white' : 'bg-[#f8f9fa] text-[#666] cursor-default'" class="field-input resize-none"></textarea>
              </div>
            </div>
          </div>

          <!-- Verification + Documents -->
          <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden hover:shadow-md transition-shadow">
            <div class="px-5 py-3 border-b border-[#f0f0f0] flex items-center justify-between">
              <div class="flex items-center gap-2">
                <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>
                <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Verification</span>
              </div>
              <button @click="docEditMode = !docEditMode"
                class="flex items-center gap-1.5 px-3.5 py-1.5 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
                {{ docEditMode ? 'Done' : 'Edit' }}
              </button>
            </div>
            <div class="px-5 py-4 flex flex-col gap-4">
              <!-- Error loading verification status -->
              <div v-if="verifyLoadError" class="text-[12px] text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {{ verifyLoadError }}
              </div>

              <!-- Required-docs / progress message -->
              <div v-if="!documents.some(d => d.file_url)" class="text-[12px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
                Please upload your documents to complete verification.
              </div>
              <div v-else-if="documents.filter(d => d.file_url).length < 5" class="text-[12px] text-[#666]">
                {{ documents.filter(d => d.file_url).length }} of 5 documents submitted
              </div>

              <!-- Verification status row -->
              <div class="flex flex-wrap items-center gap-x-6 gap-y-2">
                <div class="flex items-center gap-2">
                  <span class="text-[12px] text-[#999] font-medium">Status:</span>
                  <span class="badge" :class="form.em_verify_status?.toLowerCase()">{{ form.em_verify_status || 'PENDING' }}</span>
                  <span v-if="form.em_verify_status === 'VERIFIED' && verifiedAt" class="text-[12px] text-[#999]">· {{ formatDateTime(verifiedAt) }}</span>
                  <span v-else-if="submittedAt" class="text-[12px] text-[#999]">· Submitted {{ formatDateTime(submittedAt) }}</span>
                </div>
              </div>

              <!-- Documents -->
              <div>
                <div class="text-[12px] font-bold text-[#444] uppercase tracking-wide mb-1">Documents</div>
                <p class="text-[12px] text-[#999] mb-1">All 5 documents are required to complete verification.</p>
                <p class="text-[11px] text-[#bbb] mb-3">Accepted formats: JPG, PNG, PDF · Max size: 5 MB</p>
                <div v-if="docsLoading" class="text-center py-4 text-[13px] text-[#bbb]">Loading…</div>
                <div v-else-if="documents.length === 0" class="text-center py-4 text-[13px] text-[#bbb] italic">No documents.</div>
                <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
                  <div v-for="doc in documents" :key="doc.em_doc_id"
                    class="rounded-xl border overflow-hidden bg-white flex flex-col transition-colors text-left"
                    :class="doc.file_url ? 'border-[#eee] cursor-pointer hover:border-[#aaa]' : 'border-dashed border-[#ddd] cursor-default'"
                    @click="docEditMode ? triggerDocUpload(doc) : (doc.file_url ? openDocModal(doc) : null)">
                    <div class="aspect-square bg-[#f5f5f5] relative overflow-hidden w-full">
                      <img v-if="doc.file_url" :src="doc.file_url" class="absolute inset-0 w-full h-full object-cover hover:opacity-90 transition-opacity"
                        @error="e => e.target.style.display='none'" />
                      <div v-if="!doc.file_url && !docEditMode" class="absolute inset-0 flex items-center justify-center flex-col gap-1">
                        <svg class="w-6 h-6 text-[#ddd]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                        <span class="text-[9px] text-[#ccc] font-medium">Not uploaded yet</span>
                      </div>
                      <div v-if="docEditMode" class="absolute inset-0 bg-black/40 flex flex-col items-center justify-center gap-1 px-1 text-center">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
                        <span class="text-[9px] text-white font-medium leading-tight">Click to upload from device</span>
                      </div>
                      <div v-if="doc.uploading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
                        <span class="text-[10px] text-[#888]">Uploading…</span>
                      </div>
                      <span v-if="doc.em_doc_status" class="absolute top-1.5 left-1.5 doc-badge" :class="doc.em_doc_status?.toLowerCase()">{{ doc.em_doc_status }}</span>
                    </div>
                    <div class="p-2 flex flex-col gap-0.5">
                      <span class="text-[11px] font-semibold text-[#222] leading-snug truncate">{{ formatDocType(doc.em_doc_type) }}</span>
                      <span class="text-[10px] text-[#bbb]">{{ doc.em_uploaded_at ? 'Uploaded ' + formatDate(doc.em_uploaded_at) : '–' }}</span>
                      <span v-if="doc.reviewed_at && doc.em_doc_status === 'APPROVED'" class="text-[10px] text-[#bbb]">Verified {{ formatDate(doc.reviewed_at) }}</span>
                      <span v-if="doc.reviewed_by_name && doc.em_doc_status === 'APPROVED'" class="text-[10px] text-[#bbb]">By {{ doc.reviewed_by_name }}</span>
                      <span v-if="doc.em_doc_status === 'REJECTED' && doc.reject_reason" class="text-[10px] text-red-400 leading-snug">Reason: {{ doc.reject_reason }}</span>
                    </div>
                    <input :id="'doc-input-' + doc.em_doc_id" type="file" accept="image/*,application/pdf" class="hidden"
                      @change="e => uploadDocument(e, doc)" />
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Log Out -->
          <div class="flex justify-end">
            <button @click="logout" class="px-6 py-2 border-2 border-red-500 text-red-600 text-[13px] font-semibold rounded-lg hover:bg-red-50 transition">
              Log Out
            </button>
          </div>

        </div>
      </div>
    </div>

    <!-- Avatar Action Modal -->
    <div v-if="avatarModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="avatarModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-72 overflow-hidden" @click.stop>
        <div class="px-5 py-4 border-b border-[#eee] flex items-center justify-between">
          <span class="text-[14px] font-semibold text-[#111]">Profile Photo</span>
          <button @click="avatarModal = false" class="text-[#bbb] hover:text-[#333]">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="py-2">
          <button @click="viewAvatar" :disabled="!form.em_profile_url"
            class="w-full flex items-center gap-3 px-5 py-3 text-[13px] text-[#222] hover:bg-[#f5f5f5] transition disabled:opacity-40 disabled:cursor-not-allowed">
            <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
            View Photo
          </button>
          <button @click="$refs.avatarInput.click()"
            class="w-full flex items-center gap-3 px-5 py-3 text-[13px] text-[#222] hover:bg-[#f5f5f5] transition">
            <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
            Update Profile Photo
            <span v-if="avatarUploading" class="text-[11px] text-[#bbb] ml-auto">Uploading…</span>
          </button>
          <input ref="avatarInput" type="file" accept="image/*" class="hidden" @change="uploadAvatar" />
        </div>
      </div>
    </div>

    <!-- Doc Lightbox — same format as admin -->
    <div v-if="modalDoc" class="fixed inset-0 z-50 flex items-center justify-center bg-black/60" @click.self="modalDoc = null">
      <div class="relative max-w-3xl w-full mx-4">
        <button class="absolute -top-10 right-0 text-white/80 hover:text-white transition border-none bg-transparent cursor-pointer" @click="modalDoc = null">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
        <div class="relative">
          <img :src="modalDoc.file_url" :alt="formatDocType(modalDoc.em_doc_type)"
            class="w-full max-h-[80vh] object-contain rounded-xl shadow-2xl" />
          <span v-if="modalDoc.em_doc_status" class="absolute top-3 left-3 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase"
            :class="{
              'bg-green-100 text-green-700': modalDoc.em_doc_status === 'APPROVED',
              'bg-amber-100 text-amber-700': modalDoc.em_doc_status === 'PENDING',
              'bg-red-100 text-red-600':    modalDoc.em_doc_status === 'REJECTED',
            }">{{ modalDoc.em_doc_status }}</span>
        </div>
        <div class="flex items-center justify-between mt-3 px-1">
          <div class="flex-1"></div>
          <div class="flex flex-col items-center gap-0.5 flex-1">
            <span class="text-white/90 text-[13px] font-semibold text-center">{{ formatDocType(modalDoc.em_doc_type) }}</span>
            <span v-if="modalDoc.em_doc_status === 'REJECTED' && modalDoc.reject_reason" class="text-red-400 text-[11px] text-center">Reason: {{ modalDoc.reject_reason }}</span>
          </div>
          <div class="flex flex-col items-end gap-0.5 flex-1">
            <span v-if="modalDoc.em_uploaded_at" class="text-white/40 text-[11px]">Uploaded {{ formatDateTime(modalDoc.em_uploaded_at) }}</span>
            <span v-if="modalDoc.reviewed_at && modalDoc.em_doc_status === 'APPROVED'" class="text-white/40 text-[11px]">Verified {{ formatDateTime(modalDoc.reviewed_at) }}</span>
            <span v-if="modalDoc.reviewed_by_name && modalDoc.em_doc_status === 'APPROVED'" class="text-white/40 text-[11px]">By {{ modalDoc.reviewed_by_name }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Avatar View Modal -->
    <div v-if="avatarViewModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70" @click.self="avatarViewModal = false">
      <div class="relative max-w-sm w-full mx-4">
        <button class="absolute -top-10 right-0 text-white/80 hover:text-white transition" @click="avatarViewModal = false">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
        <img :src="form.em_profile_url" class="w-full rounded-2xl shadow-2xl object-cover" />
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
// @ts-nocheck
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '../components/AppLayout.vue'
import { useToast } from '@/components/useToast.js'
import { useConfirm } from '@/components/useConfirm.js'
const { showToast } = useToast()
const { confirmDialog } = useConfirm()

const API_BASE = '/api'
const documents = ref([])
const docsLoading = ref(false)
const verifyLoadError = ref('')
const docEditMode = ref(false)
const modalDoc = ref(null)
const avatarModal = ref(false)
const avatarViewModal = ref(false)
const avatarUploading = ref(false)
const totalJobs = ref(0)
const completedJobs = ref(0)
const verifiedAt = ref('')
const submittedAt = ref('')
const router = useRouter()

const parseTS = (d) => {
  if (!d) return null
  const s = String(d)
  // MySQL returns "2026-06-01 07:00:00" without timezone — treat as UTC
  return new Date(s.includes('T') ? s : s.replace(' ', 'T') + 'Z')
}
const formatDate = (d) => {
  const dt = parseTS(d)
  if (!dt) return '—'
  return dt.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', timeZone: 'Asia/Bangkok' })
}
const formatDateTime = (d) => {
  const dt = parseTS(d)
  if (!dt) return '—'
  return dt.toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Bangkok' })
}

const form = reactive({
  em_username: '', em_name: '', em_phone: '', em_email: '',
  em_address: '', em_bio: '', em_verify_status: '',
  em_rating_avg: 0, em_created_at: '', em_updated_at: '', em_profile_url: '',
})

const touched = reactive({ em_name: false, em_phone: false, em_email: false, em_address: false })
const resetTouched = () => Object.keys(touched).forEach(k => touched[k] = false)
const saving = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')
const isEditing = ref(false)
let snapshot = {}

const startEditing = () => { snapshot = { ...form }; resetTouched(); isEditing.value = true }
const cancelEditing = () => { Object.assign(form, snapshot); isEditing.value = false; saveError.value = ''; resetTouched() }
const handleSubmit = () => {
  touched.em_name = true; touched.em_phone = true; touched.em_email = true; touched.em_address = true
  if (!form.em_name || !form.em_phone || !form.em_email || !form.em_address) return
  saveProfile()
}

const pwOpen = ref(false)
const changingPw = ref(false)
const pwSuccess = ref(false)
const pwError = ref('')
const pwForm = reactive({ current: '', newPw: '', confirm: '' })

const changePassword = async () => {
  pwError.value = ''
  if (pwForm.newPw !== pwForm.confirm) { pwError.value = 'Passwords do not match.'; return }
  changingPw.value = true
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}/password`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ current_password: pwForm.current, new_password: pwForm.newPw }),
    })
    if (res.ok) {
      pwSuccess.value = true; pwOpen.value = false
      pwForm.current = ''; pwForm.newPw = ''; pwForm.confirm = ''
      setTimeout(() => (pwSuccess.value = false), 3000)
    } else { const d = await res.json(); pwError.value = d.message || 'Failed to change password.' }
  } catch { pwError.value = 'Unable to connect.' }
  finally { changingPw.value = false }
}

const viewAvatar = () => { avatarModal.value = false; avatarViewModal.value = true }

const uploadAvatar = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  avatarUploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const uploadRes = await fetch(`${API_BASE}/upload/employer-profile`, { method: 'POST', body: formData })
    if (!uploadRes.ok) throw new Error('Upload failed')
    const { url } = await uploadRes.json()
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        em_name: form.em_name,
        em_email: form.em_email,
        em_phone: form.em_phone,
        em_address: form.em_address,
        em_bio: form.em_bio,
        em_profile_image_url: url,
      }),
    })
    if (res.ok) { form.em_profile_url = url }
    else {
      const err = await res.json().catch(() => ({}))
      alert('Failed to update profile photo: ' + (err.detail || err.message || res.status))
    }
  } catch { alert('Failed to upload photo.') }
  finally { avatarUploading.value = false; avatarModal.value = false; e.target.value = '' }
}

const triggerDocUpload = (doc) => {
  document.getElementById('doc-input-' + doc.em_doc_id)?.click()
}

const openDocModal = (doc) => { modalDoc.value = doc }

const uploadDocument = async (e, doc) => {
  const file = e.target.files[0]
  if (!file) return
  if (doc.em_doc_status === 'APPROVED') {
  const ok = await confirmDialog('Re-uploading this document will reset your verification status to PENDING until reviewed by an Admin. Do you want to continue?')
  if (!ok) { e.target.value = ''; return }
  }

  doc.uploading = true
  try {
    const em_id = localStorage.getItem('em_id')
    const formData = new FormData()
    formData.append('file', file)
    const res = await fetch(`${API_BASE}/em-documents/${em_id}/upload?doc_type=${doc.em_doc_type}`, {
      method: 'POST', body: formData,
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || err.error || '')
    }
    const data = await res.json()
    doc.file_url = data.file_url
    doc.em_doc_status = 'PENDING'
    doc.em_uploaded_at = new Date().toISOString()
    doc.reject_reason = null

    // Reset verification status to PENDING
    await fetch(`${API_BASE}/employers/${em_id}/resubmit-verification`, { method: 'POST' })
    form.em_verify_status = 'PENDING'
    verifiedAt.value = ''
    submittedAt.value = new Date().toISOString()

  showToast('Document uploaded successfully.', 'success')
  } catch (e) { showToast(e.message || 'Failed to upload document. Please try again.', 'error') }
  finally { doc.uploading = false; e.target.value = '' }
}

onMounted(async () => {
  const em_id = localStorage.getItem('em_id')
  docsLoading.value = true
  try {
    const [profileRes, docRes, jobsRes, verifyRes] = await Promise.all([
      fetch(`${API_BASE}/employers/${em_id}`),
      fetch(`${API_BASE}/em-documents?em_id=${em_id}`),
      fetch(`${API_BASE}/tours?em_id=${em_id}&limit=200`),
      fetch(`${API_BASE}/em-verification?em_id=${em_id}&is_latest=true&limit=1`),
    ])
    const [profileData, docData, jobsData, verifyData] = await Promise.all([profileRes.json(), docRes.json(), jobsRes.json(), verifyRes.json()])

    if (profileRes.ok) {
      form.em_username      = profileData.em_username      || ''
      form.em_name          = profileData.em_name          || ''
      form.em_phone         = profileData.em_phone         || ''
      form.em_email         = profileData.em_email         || ''
      form.em_address       = profileData.em_address       || ''
      form.em_bio           = profileData.em_bio           || ''
      form.em_verify_status = profileData.em_verify_status || ''
      form.em_rating_avg    = profileData.em_rating_avg    || 0
      form.em_created_at    = profileData.em_created_at    || ''
      form.em_updated_at    = profileData.em_updated_at    || ''
      form.em_profile_url   = profileData.em_profile_image_url || profileData.em_profile_url || ''
    }

    if (docRes.ok) {
      documents.value = Array.isArray(docData) ? docData : (docData.items || docData.documents || [])
    }

    const jobs = Array.isArray(jobsData) ? jobsData : (jobsData.items || jobsData.jobs || [])
    totalJobs.value = jobs.length
    completedJobs.value = jobs.filter(j => j.job_status === 'COMPLETED').length

    if (verifyRes.ok) {
        const verifyItems = verifyData.items || verifyData || []
        const latest = Array.isArray(verifyItems) ? verifyItems[0] : null
        if (latest?.em_verified_at) verifiedAt.value = latest.em_verified_at
        if (latest?.em_submitted_at) submittedAt.value = latest.em_submitted_at
      } else {
        verifyLoadError.value = 'Failed to load verification status. Please try again.'
      }

  } catch {
    form.em_name     = localStorage.getItem('em_name')     || ''
    form.em_email    = localStorage.getItem('em_email')    || ''
    form.em_username = localStorage.getItem('em_username') || ''
    verifyLoadError.value = 'Failed to load verification status. Please try again.'
  } finally {
    docsLoading.value = false
  }
})

const logout = () => {
  localStorage.removeItem('em_id'); localStorage.removeItem('em_name'); localStorage.removeItem('em_email')
  router.push('/login')
}

const saveProfile = async () => {
  saving.value = true; saveError.value = ''; saveSuccess.value = false
  try {
    const em_id = localStorage.getItem('em_id')
    const res = await fetch(`${API_BASE}/employers/${em_id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    })
    if (res.ok) {
      localStorage.setItem('em_name', form.em_name); localStorage.setItem('em_email', form.em_email)
      const updated = await res.json().catch(() => ({}))
      form.em_updated_at = updated.em_updated_at || new Date().toISOString()
      isEditing.value = false; resetTouched(); saveSuccess.value = true
      setTimeout(() => (saveSuccess.value = false), 3000)
    } else { const d = await res.json(); saveError.value = d.message || 'Failed to save.' }
  } catch { saveError.value = 'Unable to connect.' }
  finally { saving.value = false }
}

const formatDocType = (type) => ({
  COMPANY_REGISTRATION: 'Company Registration', BUSINESS_LICENSE: 'Business License',
  TOURISM_LICENSE: 'Tourism License', TAX_ID_DOCUMENT: 'Tax ID',
  AUTHORIZED_PERSON_ID: 'Authorized ID',
}[type] || type)
</script>