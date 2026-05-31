<template>
  <div v-if="user" class="modal-overlay" @click.self="$emit('close')">
    <div class="docs-modal">

      <!-- Header -->
      <div class="modal-header">
        <div>
          <h3>{{ user.name }} - Documents</h3>
          <div class="text-[12px] mt-0.5 font-medium"
            :class="allApproved ? 'text-[#2e7d32]' : 'text-[#999]'">
            {{ approvedCount }} / {{ requiredCount }} Approved
            <span v-if="allApproved"> ✓ Will be VERIFIED</span>
          </div>
        </div>
        <button class="close-btn" @click="$emit('close')">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
      </div>

      <!-- Empty -->
      <div v-if="docs.length === 0" class="no-docs">No documents found.</div>

      <!-- Doc list -->
      <div v-else class="doc-grid">
        <div v-for="doc in docs" :key="doc.id"
          class="w-[220px] shrink-0 rounded-xl overflow-hidden bg-white flex flex-col"
          :class="doc.file_url ? 'border border-[#eee]' : 'border border-dashed border-[#ddd]'">

          <!-- Image area -->
          <div class="aspect-square bg-[#f5f5f5] relative overflow-hidden w-full"
            :class="doc.file_url ? 'cursor-zoom-in' : ''"
            @click="doc.file_url && openLightbox(doc)">
            <img v-if="doc.file_url" :src="doc.file_url" :alt="doc.type"
              class="absolute inset-0 w-full h-full object-cover hover:opacity-90 transition-opacity"
              @error="(e) => { e.target.style.display='none' }" />
            <div class="absolute inset-0 flex flex-col items-center justify-center gap-1.5"
              :style="doc.file_url ? 'display:none' : ''">
              <svg class="w-7 h-7 text-[#ddd]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>
              </svg>
              <span class="text-[10px] text-[#ccc] font-medium">Not uploaded</span>
            </div>
            <span v-if="doc.status" class="absolute top-1.5 left-1.5 doc-badge" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
          </div>

          <!-- Info -->
          <div class="p-2 flex flex-col gap-0.5">
            <span class="text-[11px] font-semibold text-[#222] leading-snug truncate">
              {{ doc.type?.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}
            </span>
            <span class="text-[10px] text-[#bbb]">{{ doc.uploaded || '–' }}</span>
            <span v-if="doc.reviewedBy" class="text-[10px] text-[#bbb]">By {{ doc.reviewedBy }}</span>
            <span v-if="doc.status === 'REJECTED' && doc.rejectReason" class="text-[10px] text-red-400 leading-snug mt-0.5">Reason: {{ doc.rejectReason }}</span>
          </div>

          <!-- Actions -->
          <div v-if="doc.file_url" class="flex flex-col gap-1 px-2 pb-2 mt-auto">
            <div v-if="rejectingDoc == doc.id" class="flex flex-col gap-1">
              <div class="relative">
                <input
                  v-model="rejectReason"
                  type="text"
                  maxlength="255"
                  placeholder="Reason for rejection..."
                  class="w-full rounded-lg border border-[#eee] bg-[#f8f8f8] px-2.5 py-1.5 pr-12 text-[11px] outline-none focus:border-red-300 focus:ring-1 focus:ring-red-100"
                  @keydown.esc="rejectingDoc = null; rejectReason = ''"
                />
                <span class="absolute right-2 top-1/2 -translate-y-1/2 text-[10px] pointer-events-none"
                  :class="rejectReason.length >= 230 ? 'text-red-400 font-semibold' : 'text-[#bbb]'">
                  {{ 255 - rejectReason.length }}
                </span>
              </div>
              <div class="flex justify-end gap-1">
                <button class="btn-reject-row !flex !justify-center !text-[11px] !px-2 !py-1"
                  @click="confirmReject(doc)">Confirm</button>
                <button class="btn-cancel-sm !flex !text-[11px] !px-2 !py-1"
                  @click="rejectingDoc = null; rejectReason = ''">Cancel</button>
              </div>
            </div>
            <div v-else class="flex gap-1">
              <button class="btn-approve-row !flex flex-1 justify-center !text-[11px] !px-1 !py-1"
                :disabled="doc.status === 'APPROVED'"
                :class="{ 'opacity-40 cursor-not-allowed': doc.status === 'APPROVED' }"
                @click="$emit('approve', doc)">
                <svg class="w-3 h-3 mr-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
                </svg>
                Approve
              </button>
              <button class="btn-reject-row !flex flex-1 justify-center !text-[11px] !px-1 !py-1"
                :disabled="doc.status === 'REJECTED'"
                :class="{ 'opacity-40 cursor-not-allowed': doc.status === 'REJECTED' }"
                @click="doc.status !== 'REJECTED' && (rejectingDoc = doc.id, rejectReason = doc.rejectReason || '')">
                <svg class="w-3 h-3 mr-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
                </svg>
                Reject
              </button>
              <button class="btn-reset-row !flex !justify-center !text-[11px] !px-1.5 !py-1"
                :disabled="doc.status === 'PENDING'"
                :class="{ 'opacity-40 cursor-not-allowed': doc.status === 'PENDING' }"
                title="Reset to Pending"
                @click="doc.status !== 'PENDING' && $emit('reset', doc)">
                <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8 8 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8 8 0 01-15.357-2m15.357 2H15"/>
                </svg>
              </button>
            </div>
          </div>

          <div v-else class="px-2 pb-2 mt-auto">
            <span class="text-[10px] text-[#ccc] italic">Awaiting upload</span>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- Lightbox -->
  <Teleport to="body">
    <div v-if="lightboxDoc"
      class="fixed inset-0 z-[500] flex items-center justify-center bg-black/60"
      @click.self="lightboxDoc = null">
      <div class="relative max-w-3xl w-full mx-4">
        <button class="absolute -top-10 right-0 text-white/80 hover:text-white transition-colors border-none bg-transparent cursor-pointer"
          @click="lightboxDoc = null">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
          </svg>
        </button>
        <div class="relative">
          <img :src="lightboxDoc.file_url" :alt="lightboxDoc.type"
            class="w-full max-h-[80vh] object-contain rounded-xl shadow-2xl" />
          <span v-if="lightboxDoc.status" class="absolute top-3 left-3 doc-badge" :class="lightboxDoc.status?.toLowerCase()">{{ lightboxDoc.status }}</span>
        </div>
        <div class="flex items-center justify-between mt-3 px-1">
          <div class="flex-1"></div>
          <div class="flex flex-col items-center gap-0.5 flex-1">
            <span class="text-white/90 text-[13px] font-semibold text-center">
              {{ lightboxDoc.type?.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}
            </span>
            <span v-if="lightboxDoc.status === 'REJECTED' && lightboxDoc.rejectReason" class="text-red-400 text-[11px] text-center">
              Reason: {{ lightboxDoc.rejectReason }}
            </span>
          </div>
          <div class="flex flex-col items-end gap-0.5 flex-1">
            <span v-if="lightboxDoc.uploaded" class="text-white/40 text-[11px]">Uploaded {{ lightboxDoc.uploaded }}</span>
            <span v-if="lightboxDoc.reviewedBy" class="text-white/40 text-[11px]">By {{ lightboxDoc.reviewedBy }}</span>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
  docs: { type: Array, default: () => [] },
  requiredCount: { type: Number, default: 5 }
})
const emit = defineEmits(['close', 'approve', 'reject', 'reset'])

const lightboxDoc = ref(null)
const rejectingDoc = ref(null)
const rejectReason = ref('')

function openLightbox(doc) {
  lightboxDoc.value = doc
}

function confirmReject(doc) {
  const reason = rejectReason.value.trim()
  rejectingDoc.value = null
  rejectReason.value = ''
  emit('reject', { id: doc.id, _type: doc._type, reason })
}

const approvedCount = computed(() =>
  props.docs.filter(d => d.status === 'APPROVED').length
)
const allApproved = computed(() => approvedCount.value >= props.requiredCount)
</script>