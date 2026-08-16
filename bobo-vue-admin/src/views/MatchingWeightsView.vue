<template>
  <div>
    <BreadcrumbBar />

    <div class="px-5 pb-10 pt-1">

      <!-- Page header -->
      <div class="flex items-start justify-between gap-4 flex-wrap py-4 mb-1">
        <div>
          <h1 class="text-[20px] font-bold text-[#111] leading-tight">Matching Score Weights</h1>
          <p class="text-[13px] text-[#888] mt-1 max-w-xl leading-relaxed">
            Set how much each factor counts toward a freelancer's match score. The four weights must add up to 100.
          </p>
        </div>
        <div class="text-right shrink-0">
          <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Last saved</div>
          <div class="text-[13px] font-semibold text-[#444] mt-0.5">{{ lastSavedLabel }}</div>
        </div>
      </div>

      <!-- Formula card -->
      <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-6 mb-4">
        <div class="flex items-center gap-2 mb-4">
          <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 7h6m-6 4h6m-2 5l-4-4h3V7"/></svg>
          <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Formula</span>
        </div>

        <div class="bg-[#f8f9fa] border border-[#eee] rounded-lg px-5 py-4 overflow-x-auto">
          <div class="flex items-center flex-wrap gap-x-2 gap-y-1.5 text-[15px] font-medium text-[#222] whitespace-nowrap">
            <span class="italic">Score</span>
            <span class="text-[#bbb]">=</span>
            <template v-for="(f, i) in factors" :key="f.key">
              <span v-if="i > 0" class="text-[#bbb]">+</span>
              <span class="inline-flex items-center gap-1 px-2 py-1 rounded-md" :style="{ background: f.bg, color: f.text }">
                W<sub class="text-[10px]">{{ f.short }}</sub>
                <span class="text-[#bbb] mx-0.5">×</span>
                S<sub class="text-[10px]">{{ f.short }}</sub>
              </span>
            </template>
          </div>
        </div>

        <!-- Weight balance bar — the signature element: literally the data, not decoration -->
        <div class="mt-5">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Weight distribution</span>
            <span class="text-[12px] font-bold" :class="isValidTotal ? 'text-green-600' : 'text-red-500'">
              {{ totalWeight }} / 100
            </span>
          </div>
          <div class="w-full h-3 rounded-full overflow-hidden bg-[#eee] flex">
            <div v-for="f in factors" :key="f.key"
              class="h-full transition-all duration-300"
              :style="{ width: (weights[f.key] / 100 * 100) + '%', background: f.solid }"
              :title="`${f.label}: ${weights[f.key]}`">
            </div>
          </div>
          <p v-if="!isValidTotal" class="text-[12px] text-red-500 mt-2 flex items-center gap-1">
            <svg class="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Weights add up to {{ totalWeight }}, not 100. Adjust below before saving.
          </p>
        </div>
      </div>

      <!-- Weight controls -->
      <div class="grid gap-3 mb-4" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
        <div v-for="f in factors" :key="f.key"
          class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm p-5 hover:shadow-md transition-shadow">
          <div class="flex items-center gap-2.5 mb-3">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" :style="{ background: f.bg, color: f.text }">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" v-html="f.icon"></svg>
            </span>
            <div class="flex-1 min-w-0">
              <div class="text-[13px] font-bold text-[#222] leading-tight">{{ f.label }}</div>
              <div class="text-[11px] text-[#999] leading-tight mt-0.5">{{ f.description }}</div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <input type="range" min="0" max="100" step="1" v-model.number="weights[f.key]"
              class="flex-1 cursor-pointer" :style="{ accentColor: f.solid }" />
            <div class="flex items-center shrink-0 border border-[#e0e0e0] rounded-lg overflow-hidden">
              <input type="number" min="0" max="100" step="1" v-model.number="weights[f.key]"
                class="w-14 text-center text-[13px] font-bold text-[#222] py-1.5 border-none focus:outline-none focus:ring-0" />
              <span class="text-[12px] text-[#999] pr-2.5">%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center justify-between flex-wrap gap-2 mb-6">
        <button @click="distributeEvenly"
          class="flex items-center gap-1.5 text-[13px] font-medium text-[#666] hover:text-[#333] transition">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/></svg>
          Split evenly (25 / 25 / 25 / 25)
        </button>

        <div class="flex items-center gap-2">
          <button v-if="isDirty" @click="revert"
            class="px-3.5 py-2 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition">
            Revert
          </button>
          <button @click="save" :disabled="!isValidTotal || !isDirty"
            class="px-5 py-2 text-[13px] font-semibold rounded-lg bg-[#1a1a2e] text-white hover:bg-[#111122] transition disabled:opacity-40 disabled:cursor-not-allowed">
            Save Weights
          </button>
        </div>
      </div>

      <!-- Live example -->
      <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
        <div class="px-5 py-3.5 border-b border-[#f0f0f0] flex items-center gap-2">
          <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Try it on a sample freelancer</span>
          <span class="ml-auto text-[11px] text-[#bbb]">Move the sliders to see the score change live</span>
        </div>

        <div class="p-5 grid gap-5" style="grid-template-columns: 1.3fr 1fr;">
          <div class="grid gap-4" style="grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));">
            <div v-for="f in factors" :key="f.key + '-sample'">
              <div class="flex items-center justify-between mb-1.5">
                <span class="text-[12px] font-semibold text-[#555]">{{ f.label }}</span>
                <span class="text-[12px] font-bold" :style="{ color: f.text }">{{ sample[f.key] }}%</span>
              </div>
              <input type="range" min="0" max="100" step="1" v-model.number="sample[f.key]"
                class="w-full cursor-pointer" :style="{ accentColor: f.solid }" />
            </div>
          </div>

          <div class="flex flex-col items-center justify-center bg-[#f8f9fa] border border-[#eee] rounded-lg py-6">
            <div class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium mb-1">Resulting match score</div>
            <div class="text-[40px] font-bold leading-none" :style="{ color: scoreColor }">{{ sampleScore }}%</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, computed, ref, watch, onMounted } from 'vue'
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { useToast } from '../components/useToast.js'

const { showToast } = useToast()

const STORAGE_KEY = 'matching_weights_v1'
const DEFAULT_WEIGHTS = { pickupArea: 25, availability: 25, verification: 25, language: 25 }

const factors = [
  {
    key: 'pickupArea', short: 'PA', label: 'Pickup Area',
    description: 'Freelancer\u2019s pickup zones overlap the tour\u2019s route',
    bg: '#e0f7fa', text: '#00838f', solid: '#00acc1',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>',
  },
  {
    key: 'availability', short: 'AV', label: 'Availability',
    description: 'Freelancer is free for the tour\u2019s full date range',
    bg: '#e8f5e9', text: '#2e7d32', solid: '#43a047',
    icon: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
  },
  {
    key: 'verification', short: 'VF', label: 'Verification',
    description: 'Account is verified, active, and in good standing',
    bg: '#fff3e0', text: '#e65100', solid: '#fb8c00',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>',
  },
  {
    key: 'language', short: 'LG', label: 'Language',
    description: 'Overlap between spoken languages and the tour\u2019s requirements',
    bg: '#e8eaf6', text: '#3949ab', solid: '#5c6bc0',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>',
  },
]

const weights = reactive({ ...DEFAULT_WEIGHTS })
const savedWeights = ref({ ...DEFAULT_WEIGHTS })
const lastSavedAt = ref(null)

const sample = reactive({ pickupArea: 80, availability: 90, verification: 100, language: 65 })

onMounted(() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw)
      if (parsed?.weights) {
        Object.assign(weights, parsed.weights)
        savedWeights.value = { ...parsed.weights }
      }
      if (parsed?.savedAt) lastSavedAt.value = parsed.savedAt
    }
  } catch {}
})

const totalWeight = computed(() =>
  factors.reduce((sum, f) => sum + (Number(weights[f.key]) || 0), 0)
)
const isValidTotal = computed(() => totalWeight.value === 100)
const isDirty = computed(() =>
  factors.some(f => Number(weights[f.key]) !== Number(savedWeights.value[f.key]))
)

const lastSavedLabel = computed(() => {
  if (!lastSavedAt.value) return 'Never — using defaults'
  return new Date(lastSavedAt.value).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
  })
})

const distributeEvenly = () => {
  Object.assign(weights, DEFAULT_WEIGHTS)
}

const revert = () => {
  Object.assign(weights, savedWeights.value)
}

const save = () => {
  if (!isValidTotal.value) return
  const payload = { weights: { ...weights }, savedAt: new Date().toISOString() }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload))
  savedWeights.value = { ...weights }
  lastSavedAt.value = payload.savedAt
  showToast('Matching weights saved')
  // TODO(backend): persist to a real settings endpoint, e.g. PUT /admin/matching-weights
}

// Clamp any out-of-range typed values
watch(weights, () => {
  factors.forEach(f => {
    const v = weights[f.key]
    if (v === '' || v === null || Number.isNaN(Number(v))) { weights[f.key] = 0; return }
    weights[f.key] = Math.min(100, Math.max(0, Math.round(Number(v))))
  })
}, { deep: true })

const sampleScore = computed(() => {
  const raw = factors.reduce((sum, f) => sum + (weights[f.key] / 100) * sample[f.key], 0)
  return Math.round(Math.min(100, Math.max(0, raw)))
})

const scoreColor = computed(() => {
  const s = sampleScore.value
  if (s >= 80) return '#2e7d32'
  if (s >= 50) return '#f9a825'
  return '#e53935'
})
</script>