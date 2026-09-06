<template>
  <div>
    <BreadcrumbBar />

    <div class="px-5 pb-10 pt-1">

      <!-- Page header -->
      <div class="flex items-start justify-between gap-4 flex-wrap py-4 mb-1">
        <div>
          <h1 class="text-[20px] font-bold text-[#111] leading-tight">Matching Score Weights</h1>
          <p class="text-[13px] text-[#888] mt-1 max-w-xl leading-relaxed">
            Set how much each factor counts toward a freelancer's match score.
            Dragging one factor automatically adjusts the others — the total always stays at 100.
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

        <!-- Weight balance bar — always exactly 100 now, no invalid state possible -->
        <div class="mt-5">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-[11px] text-[#bbb] uppercase tracking-wide font-medium">Weight distribution</span>
            <span class="text-[12px] font-bold text-green-600">{{ totalWeight }} / 100</span>
          </div>
          <div class="w-full h-3 rounded-full overflow-hidden bg-[#eee] flex">
            <div v-for="f in factors" :key="f.key"
              class="h-full transition-all duration-300"
              :style="{ width: weights[f.key] + '%', background: f.solid }"
              :title="`${f.label}: ${weights[f.key]}`">
            </div>
          </div>
        </div>
      </div>

      <!-- Weight controls -->
      <div class="flex flex-col gap-3 mb-4">
        <div v-for="f in factors" :key="f.key"
          class="bg-white rounded-xl border shadow-sm p-5 transition-shadow"
          :class="locks[f.key] ? 'border-[#e0e0e0]' : 'border-[#e0e0e0] hover:shadow-md'">
          <div class="flex items-center gap-2.5 mb-4">
            <span class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0" :style="{ background: f.bg, color: f.text }">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" v-html="f.icon"></svg>
            </span>
            <div class="flex-1 min-w-0">
              <div class="text-[13px] font-bold text-[#222] leading-tight">{{ f.label }}</div>
              <div class="text-[11px] text-[#999] leading-tight mt-0.5">{{ f.description }}</div>
            </div>
            <button type="button" @click="toggleLock(f.key)"
              class="w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border transition-colors"
              :class="locks[f.key] ? 'border-transparent' : 'border-[#e0e0e0] text-[#bbb] hover:text-[#888] hover:border-[#ccc]'"
              :style="locks[f.key] ? { background: f.bg, color: f.text } : {}"
              :title="locks[f.key] ? 'Locked — click to unlock' : 'Lock this value'">
              <svg v-if="locks[f.key]" class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
              <svg v-else class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M7 11V7a5 5 0 019.9-1"/></svg>
            </button>
            <div class="flex items-center shrink-0 border border-[#e0e0e0] rounded-lg overflow-hidden"
              :class="locks[f.key] ? 'opacity-50' : ''">
              <input type="number" min="0" max="100" step="1" :value="weights[f.key]" :disabled="locks[f.key]"
                @input="redistribute(f.key, $event.target.valueAsNumber)"
                class="w-14 text-center text-[13px] font-bold text-[#222] py-1.5 border-none focus:outline-none focus:ring-0 disabled:cursor-not-allowed" />
              <span class="text-[12px] text-[#999] pr-2.5">%</span>
            </div>
          </div>

          <div class="relative flex items-center" style="height: 32px;" :class="locks[f.key] ? 'opacity-50' : ''">
            <input type="range" min="0" max="100" step="1" :value="weights[f.key]" :disabled="locks[f.key]"
              @input="redistribute(f.key, $event.target.valueAsNumber)"
              class="weight-slider w-full" :class="locks[f.key] ? 'cursor-not-allowed' : 'cursor-pointer'" :style="sliderStyle(f)" />
            <span v-for="n in 11" :key="n"
              class="absolute rounded-full pointer-events-none transition-colors duration-150"
              :class="(n - 1) % 2 === 0 ? 'w-3.5 h-3.5 border-2 border-white' : 'w-2 h-2'"
              :style="{
                left: (n - 1) * 10 + '%',
                top: '50%',
                transform: 'translate(-50%, -50%)',
                background: weights[f.key] >= (n - 1) * 10 ? f.solid : '#dcdcdc',
              }">
            </span>
          </div>

          <!-- Number labels every 20, positioned at the exact same % as their dot above -->
          <div class="relative text-[13px] text-[#999]" style="height: 18px; margin-top: 6px;">
            <span v-for="n in 6" :key="n" class="absolute"
              :style="{
                left: (n - 1) * 20 + '%',
                transform: n === 1 ? 'translateX(0)' : n === 6 ? 'translateX(-100%)' : 'translateX(-50%)',
              }">{{ (n - 1) * 20 }}</span>
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

        <div class="flex items-center gap-3">
          <span class="text-[12px] font-semibold text-green-600 flex items-center gap-1">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
            {{ totalWeight }} / 100
          </span>
          <button v-if="isDirty" @click="reset"
            class="px-3.5 py-2 text-[13px] font-medium rounded-lg border border-[#e0e0e0] text-[#666] hover:bg-[#f5f5f5] transition">
            Reset
          </button>
          <button @click="save" :disabled="!isDirty || saving"
            class="px-5 py-2 text-[13px] font-semibold rounded-lg bg-[#1a1a2e] text-white hover:bg-[#111122] transition disabled:opacity-40 disabled:cursor-not-allowed">
            {{ saving ? 'Saving…' : 'Save Weights' }}
          </button>
        </div>
      </div>

      <!-- Sample freelancers — fixed example profiles, no database needed -->
      <div class="bg-white rounded-xl border border-[#e0e0e0] shadow-sm overflow-hidden">
        <div class="px-5 py-3.5 border-b border-[#f0f0f0] flex items-center gap-2">
          <svg class="w-4 h-4 text-[#888]" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
          <span class="text-[13px] font-bold text-[#444] uppercase tracking-wide">Sample freelancers</span>
          <span class="ml-auto text-[11px] text-[#bbb]">Scores update instantly as you adjust the weights above</span>
        </div>

        <div class="divide-y divide-[#f0f0f0]">
          <div v-for="p in sampleProfiles" :key="p.name" class="px-5 py-4 flex items-center gap-4">
            <div class="flex-1 min-w-0">
              <div class="text-[13px] font-bold text-[#222]">{{ p.name }}</div>
              <div class="text-[11px] text-[#999] mt-0.5">{{ p.description }}</div>
              <div class="flex flex-wrap gap-1.5 mt-2">
                <span v-for="f in factors" :key="f.key"
                  class="text-[10px] font-semibold px-2 py-0.5 rounded-full"
                  :style="{ background: f.bg, color: f.text }">
                  {{ f.short }}: {{ formatCriterionScore(p.scores[f.key]) }}
                </span>
              </div>
            </div>
            <div class="text-right shrink-0 w-20">
              <div class="text-[24px] font-bold leading-none" :style="{ color: scoreColorFor(profileScore(p)) }">
                {{ profileScore(p) }}
              </div>
              <div class="text-[10px] text-[#bbb] uppercase tracking-wide mt-0.5">score</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, computed, ref, onMounted } from 'vue'
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { useToast } from '../components/useToast.js'

const { showToast } = useToast()

const API_BASE = 'http://localhost:8000'

const FIELD_MAP = {
  pickupArea: 'weight_pickup_area',
  availability: 'weight_availability',
  verification: 'weight_verification',
  language: 'weight_language',
}
const KEYS = Object.keys(FIELD_MAP)

const DEFAULT_WEIGHTS = { pickupArea: 40, availability: 30, verification: 20, language: 10 }

const factors = [
  {
    key: 'pickupArea', short: 'PA', label: 'Pickup Area',
    description: 'Freelancer\u2019s pickup zone matches the tour\u2019s area (1 = match, 0 = no match)',
    bg: '#e0f7fa', text: '#00838f', solid: '#00acc1',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a2 2 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>',
  },
  {
    key: 'availability', short: 'AV', label: 'Availability',
    description: 'How much of the tour\u2019s dates the freelancer\u2019s availability covers (0\u20131)',
    bg: '#e8f5e9', text: '#2e7d32', solid: '#43a047',
    icon: '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
  },
  {
    key: 'verification', short: 'VF', label: 'Verification',
    description: 'Account is verified (1) or not (0)',
    bg: '#fff3e0', text: '#e65100', solid: '#fb8c00',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>',
  },
  {
    key: 'language', short: 'LG', label: 'Language',
    description: 'Fraction of the tour\u2019s required languages the freelancer speaks (0\u20131)',
    bg: '#e8eaf6', text: '#3949ab', solid: '#5c6bc0',
    icon: '<path stroke-linecap="round" stroke-linejoin="round" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"/>',
  },
]

// Fixed example profiles — no database needed. Each score is a real S_i value:
// pickupArea/verification are binary (0 or 1), availability/language are 0-1 fractions.
const sampleProfiles = [
  {
    name: 'Perfect match',
    description: 'Right area, fully available, verified, speaks every required language',
    scores: { pickupArea: 1, availability: 1, verification: 1, language: 1 },
  },
  {
    name: 'Verified, but wrong area',
    description: 'Everything else lines up, but is based outside the tour\u2019s pickup zone',
    scores: { pickupArea: 0, availability: 1, verification: 1, language: 1 },
  },
  {
    name: 'Right area, not yet verified',
    description: 'Great fit on paper, but verification is still pending',
    scores: { pickupArea: 1, availability: 1, verification: 0, language: 1 },
  },
  {
    name: 'Only partially available',
    description: 'Free for about half of the tour\u2019s date range',
    scores: { pickupArea: 1, availability: 0.5, verification: 1, language: 1 },
  },
  {
    name: 'Missing some languages',
    description: 'Tour needs 3 languages; this freelancer speaks only 1 of them',
    scores: { pickupArea: 1, availability: 1, verification: 1, language: 0.33 },
  },
  {
    name: 'Weakest candidate',
    description: 'Wrong area, unverified, only partially available and speaks 1 of 3 languages',
    scores: { pickupArea: 0, availability: 0.5, verification: 0, language: 0.33 },
  },
]

const weights = reactive({ ...DEFAULT_WEIGHTS })
const savedWeights = ref({ ...DEFAULT_WEIGHTS })
const lastSavedAt = ref(null)
const saving = ref(false)

const locks = reactive({ pickupArea: false, availability: false, verification: false, language: false })
const MAX_LOCKS = 2 // always leave at least 2 factors free to redistribute between

function toggleLock(key) {
  if (!locks[key] && Object.values(locks).filter(Boolean).length >= MAX_LOCKS) {
    showToast(`You can lock up to ${MAX_LOCKS} factors at a time`, 'error')
    return
  }
  locks[key] = !locks[key]
}

function sliderStyle(f) {
  const pct = weights[f.key]
  return {
    color: f.solid,
    '--slider-fill': `linear-gradient(to right, ${f.solid} 0%, ${f.solid} ${pct}%, #ececec ${pct}%, #ececec 100%)`,
  }
}

const toFrontendShape = (backendData) => ({
  pickupArea: backendData.weight_pickup_area,
  availability: backendData.weight_availability,
  verification: backendData.weight_verification,
  language: backendData.weight_language,
})

const fetchWeights = async () => {
  try {
    const res = await fetch(`${API_BASE}/admin/matching-config`)
    if (!res.ok) throw new Error('Failed to load matching config')
    const data = await res.json()
    const mapped = toFrontendShape(data)
    Object.assign(weights, mapped)
    savedWeights.value = { ...mapped }
    lastSavedAt.value = data.updated_at || null
  } catch (err) {
    showToast('Could not load matching weights — using defaults', 'error')
  }
}

onMounted(fetchWeights)

const totalWeight = computed(() => KEYS.reduce((sum, k) => sum + weights[k], 0))

const isDirty = computed(() => KEYS.some(k => weights[k] !== savedWeights.value[k]))

const lastSavedLabel = computed(() => {
  if (!lastSavedAt.value) return 'Never — using defaults'
  return new Date(lastSavedAt.value).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit',
  })
})

const distributeEvenly = () => {
  Object.assign(weights, { pickupArea: 25, availability: 25, verification: 25, language: 25 })
}

const reset = () => {
  Object.assign(weights, DEFAULT_WEIGHTS)
  Object.keys(locks).forEach(k => { locks[k] = false })
}

const save = async () => {
  saving.value = true
  const payload = {}
  for (const [feKey, beKey] of Object.entries(FIELD_MAP)) {
    payload[beKey] = weights[feKey]
  }

  try {
    const res = await fetch(`${API_BASE}/admin/matching-config`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
    const data = await res.json()
    if (!res.ok) {
      showToast(data.detail || 'Failed to save matching weights', 'error')
      return
    }
    savedWeights.value = { ...weights }
    lastSavedAt.value = new Date().toISOString()
    showToast('Matching weights saved')
  } catch (err) {
    showToast('Could not reach the server — weights not saved', 'error')
  } finally {
    saving.value = false
  }
}

const formatCriterionScore = (v) => (Number.isInteger(v) ? v : v.toFixed(2))

const profileScore = (profile) => {
  const raw = KEYS.reduce((sum, k) => sum + (weights[k] / 100) * profile.scores[k] * 100, 0)
  return Math.round(Math.min(100, Math.max(0, raw)))
}

const scoreColorFor = (score) => {
  if (score >= 80) return '#2e7d32'
  if (score >= 50) return '#f9a825'
  return '#e53935'
}

// Auto-redistribute: when one factor's weight changes, scale the *unlocked*
// others proportionally so the total always stays at exactly 100. Locked
// factors keep their current value untouched and are excluded entirely.
let isRedistributing = false

function redistribute(changedKey, rawValue) {
  if (isRedistributing) return
  if (locks[changedKey]) return // shouldn't happen (input is disabled), but stay safe
  if (rawValue === '' || rawValue === null || Number.isNaN(rawValue)) return
  isRedistributing = true

  const others = factors.map(f => f.key).filter(k => k !== changedKey)
  const lockedOthers = others.filter(k => locks[k])
  const unlockedOthers = others.filter(k => !locks[k])
  const lockedSum = lockedOthers.reduce((sum, k) => sum + weights[k], 0)

  // never let the changed value eat into what's reserved for locked factors
  const maxAllowed = Math.max(0, 100 - lockedSum)
  const newValue = Math.min(maxAllowed, Math.max(0, Math.round(rawValue)))
  const remaining = 100 - newValue - lockedSum

  if (unlockedOthers.length > 0) {
    const oldUnlockedSum = unlockedOthers.reduce((sum, k) => sum + weights[k], 0)
    let newUnlocked
    if (oldUnlockedSum === 0) {
      const base = Math.floor(remaining / unlockedOthers.length)
      newUnlocked = unlockedOthers.map(() => base)
      let leftover = remaining - base * unlockedOthers.length
      for (let i = 0; leftover > 0; i++, leftover--) newUnlocked[i % unlockedOthers.length]++
    } else {
      newUnlocked = unlockedOthers.map(k => Math.round((weights[k] * remaining) / oldUnlockedSum))
      const diff = remaining - newUnlocked.reduce((a, b) => a + b, 0)
      if (diff !== 0) {
        const maxIdx = newUnlocked.indexOf(Math.max(...newUnlocked))
        newUnlocked[maxIdx] += diff
      }
    }
    unlockedOthers.forEach((k, i) => { weights[k] = Math.max(0, Math.min(100, newUnlocked[i])) })
  }

  weights[changedKey] = newValue

  isRedistributing = false
}
</script>
