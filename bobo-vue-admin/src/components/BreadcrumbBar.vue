<!-- components/BreadcrumbBar.vue -->
<template>
  <nav class="breadcrumb-bar">
    <span
      v-for="(crumb, i) in crumbs"
      :key="i"
      class="breadcrumb-segment"
    >
      <router-link v-if="crumb.to" :to="crumb.to" class="breadcrumb-link">
        {{ crumb.label }}
      </router-link>
      <span v-else class="breadcrumb-current">{{ crumb.label }}</span>
      <span v-if="i < crumbs.length - 1" class="breadcrumb-sep">›</span>
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

<style scoped>
.breadcrumb-bar {
  font-size: 15px;
  font-weight: 500;
  background: #1a1a2e;
  padding: 15px 20px;
  color: white;
  letter-spacing: 0.2px;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 4px;
}
.breadcrumb-segment {
  display: flex;
  align-items: center;
  gap: 4px;
}
.breadcrumb-link {
  color: #aaa;
  text-decoration: none;
  font-size: 15px;
  font-weight: 500;
}
.breadcrumb-link:hover {
  color: white;
}
.breadcrumb-current {
  color: white;
  font-size: 15px;
  font-weight: 500;
}
.breadcrumb-sep {
  color: #666;
  font-size: 15px;
}
</style>
