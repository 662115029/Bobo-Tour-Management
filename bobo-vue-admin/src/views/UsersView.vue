<template>
  <div>
    <h1 class="title">Users Management</h1>
    
    <div class="tabs">
      <button 
        class="tab" 
        :class="{ active: activeTab === 'Freelancer' }"
        @click="activeTab = 'Freelancer'"
      >
        Freelancer
      </button>
      <button 
        class="tab" 
        :class="{ active: activeTab === 'Employer' }"
        @click="activeTab = 'Employer'"
      >
        Employer
      </button>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>VERIFY</th>
            <th>ACTIVE</th>
            <th>RATING</th>
            <th>ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>
              <div class="user-cell">
                <span class="avatar">
                  <img v-if="user.imageUrl" :src="user.imageUrl" alt="" />
                  <span v-else>{{ user.initials }}</span>
                </span>
                <span>{{ user.name }}</span>
              </div>
            </td>
            <td>
              <span class="badge" :class="user.verifyStatus.toLowerCase()">{{ user.verifyStatus }}</span>
            </td>
            <td>{{ user.isActive ? 'YES' : 'NO' }}</td>
            <td>{{ user.rating.toFixed(1) }}</td>
            <td>{{ user.id }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'

const activeTab = ref('Freelancer')

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const employers = ref([])
const freelancers = ref([])

function initialsFromName(name) {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/).slice(0, 2)
  return parts.map(p => p[0]?.toUpperCase() || '').join('')
}

async function loadEmployers() {
  const res = await fetch(`${API_BASE}/admin/employers?limit=50&offset=0`)
  const data = await res.json()
  employers.value = (data.items || []).map(e => ({
    id: e.em_id,
    name: e.em_name || e.em_username || e.em_id,
    initials: initialsFromName(e.em_name || e.em_username || ''),
    verifyStatus: e.em_verify_status || 'UNKNOWN',
    isActive: !!e.em_is_active,
    rating: Number(e.em_rating_avg || 0),
    imageUrl: e.em_profile_image_url || ''
  }))
}

async function loadFreelancers() {
  const res = await fetch(`${API_BASE}/admin/freelancers?limit=50&offset=0`)
  const data = await res.json()
  freelancers.value = (data.items || []).map(f => ({
    id: f.fl_id,
    name: f.fl_name || f.fl_id,
    initials: initialsFromName(f.fl_name || ''),
    verifyStatus: f.fl_verify_status || 'UNKNOWN',
    isActive: !!f.fl_is_active,
    rating: Number(f.fl_rating_avg || 0),
    imageUrl: f.fl_profile_image_url || ''
  }))
}

const users = computed(() => (activeTab.value === 'Employer' ? employers.value : freelancers.value))

onMounted(async () => {
  await Promise.allSettled([loadEmployers(), loadFreelancers()])
})

watch(activeTab, async (tab) => {
  // refresh only the active list
  if (tab === 'Employer' && employers.value.length === 0) await loadEmployers()
  if (tab === 'Freelancer' && freelancers.value.length === 0) await loadFreelancers()
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
}

.tab {
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 14px;
  cursor: pointer;
  color: #666;
}

.tab.active {
  color: #06C755;
  border-bottom: 2px solid #06C755;
  margin-bottom: -2px;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: #f9f9f9;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #6c757d;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.verified { background: #e8f5e9; color: #2e7d32; }
.badge.pending { background: #fff3e0; color: #f57c00; }
.badge.not_verified { background: #ffebee; color: #c62828; }
.badge.unknown { background: #f5f5f5; color: #666; }

</style>