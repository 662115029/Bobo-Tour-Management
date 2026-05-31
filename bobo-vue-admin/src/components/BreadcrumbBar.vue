<!-- components/BreadcrumbBar.vue -->
<template>
  <nav
    class="mb-[15px] flex items-center gap-1 bg-[#1a1a2e] px-5 py-[15px] text-[15px] font-medium tracking-wide text-white"
  >
    <span v-for="(crumb, i) in crumbs" :key="i" class="flex items-center gap-1">
      <router-link
        v-if="crumb.to"
        :to="crumb.to"
        class="text-[15px] font-medium text-[#aaa] no-underline hover:text-white"
      >
        {{ crumb.label }}
      </router-link>
      <span v-else class="text-[15px] font-medium text-white">{{ crumb.label }}</span>
      <span v-if="i < crumbs.length - 1" class="text-[15px] text-[#666]">›</span>
    </span>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { pageNames } from '../router/index'

const props = defineProps({
  label: { type: String, default: null }
})

const route = useRoute()

// Fallback parent for dynamic detail pages when navigated directly (refresh / share link)
const fallbackParent = {
  FreelancerDetail: { label: 'Verification', to: '/verification' },
  EmployerDetail:   { label: 'Verification', to: '/verification' },
}

const crumbs = computed(() => {
  if (route.meta?.parent) {
    const base = [{ label: route.meta.parent, to: route.meta.parentTo }]
    if (props.label) {
      base.push({ label: props.label, to: null })
    }
    return base
  }

  // Dynamic detail page accessed directly (no meta.parent set by beforeEach)
  const fb = fallbackParent[route.name]
  if (fb) {
    const base = [{ label: fb.label, to: fb.to }]
    if (props.label) {
      base.push({ label: props.label, to: null })
    }
    return base
  }

  return [{ label: pageNames[route.name] || route.name, to: null }]
})
</script>