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
          <div class="aspect-square bg-[#f5f5f5] relative overflow-hidden w-full">
            <!-- มีรูป -->
            <img v-if="doc.file_url" :src="doc.file_url" :alt="doc.type"
              class="absolute inset-0 w-full h-full object-cover hover:opacity-90 transition-opacity"
              @error="(e) => { e.target.style.display='none' }" />
            <!-- ไม่มีรูป -->
            <div class="absolute inset-0 flex flex-col items-center justify-center gap-1.5"
              :style="doc.file_url ? 'display:none' : ''">
              <svg class="w-7 h-7 text-[#ddd]" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
                <rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/>
              </svg>
              <span class="text-[10px] text-[#ccc] font-medium">Not uploaded</span>
            </div>
          </div>

          <!-- Info -->
          <div class="p-2 flex flex-col gap-0.5">
            <span class="text-[11px] font-semibold text-[#222] leading-snug truncate">
              {{ doc.type?.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()) }}
            </span>
            <span class="doc-badge self-start" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
            <span class="text-[10px] text-[#bbb]">{{ doc.uploaded || '–' }}</span>
          </div>

          <!-- Actions — ซ่อนถ้ายังไม่ได้ upload -->
          <div v-if="doc.file_url" class="flex gap-1 px-2 pb-2 mt-auto">
            <button class="btn-approve-row !flex flex-1 justify-center !text-[11px] !px-1 !py-1"
              :disabled="doc.status === 'APPROVED'" @click="$emit('approve', doc)">
              <svg class="w-3 h-3 mr-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
              </svg>
              Approve
            </button>
            <button class="btn-reject-row !flex flex-1 justify-center !text-[11px] !px-1 !py-1"
              :disabled="doc.status === 'REJECTED'" @click="$emit('reject', doc)">
              <svg class="w-3 h-3 mr-0.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
              </svg>
              Reject
            </button>
          </div>
          
          <div v-else class="px-2 pb-2 mt-auto">
            <span class="text-[10px] text-[#ccc] italic">Awaiting upload</span>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  user: { type: Object, default: null },
  docs: { type: Array, default: () => [] },
  requiredCount: { type: Number, default: 5 }
})
defineEmits(['close', 'approve', 'reject'])

const approvedCount = computed(() =>
  props.docs.filter(d => d.status === 'APPROVED').length
)
const allApproved = computed(() => approvedCount.value >= props.requiredCount)
</script>