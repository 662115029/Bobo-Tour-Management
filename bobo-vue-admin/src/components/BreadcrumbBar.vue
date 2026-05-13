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

const props = defineProps({
  label: { type: String, default: null }
})

const route = useRoute()

const crumbs = computed(() => {
  if (route.meta?.parent) {
    const base = [{ label: route.meta.parent, to: route.meta.parentTo }]
    const dynamicLabel = props.label || history.state?.jobTitle
    if (dynamicLabel) {
      base.push({ label: dynamicLabel, to: null })
    }
    return base
  }

  const pageNames = {
    Jobs: 'Jobs Management',
    Verification: 'Verification',
    Users: 'Users',
    Logs: 'Admin Logs',
    Profile: 'Profile',
    Dashboard: 'Dashboard',
  }

  return [{ label: pageNames[route.name] || route.name, to: null }]
})
</script>
