<template>
  <div>
    <div class="header">
      <h1 class="title">Verification</h1>
      <span class="more-icon">...</span>
    </div>
    
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

    <div class="filter-row">
      <select v-model="statusFilter" class="filter-select full">
        <option value="All">All Status</option>
        <option value="VERIFIED">Verified</option>
        <option value="PENDING">Pending</option>
        <option value="NOT_VERIFIED">Not Verified</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>STATUS</th>
            <th>SUBMITTED</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in filteredVerifications" :key="v.id">
            <td>{{ v.name }}</td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>{{ v.submitted }}</td>
            <td><span class="action-link">View</span></td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <p class="helper">Select a user to view details</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const activeTab = ref('Freelancer')
const statusFilter = ref('All')
const freelancers = ref([])
const employers = ref([])

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const filteredVerifications = computed(() => {
  const list = activeTab.value === 'Freelancer' ? freelancers.value : employers.value
  return list.filter(v => {
    const matchStatus = statusFilter.value === 'All' || v.status === statusFilter.value
    return matchStatus
  })
})

onMounted(async () => {
  try {
    const [flRes, emRes] = await Promise.all([
      fetch(`${API_BASE}/admin/freelancers`),
      fetch(`${API_BASE}/admin/employers`)
    ])
    const flData = await flRes.json()
    const emData = await emRes.json()
    
    freelancers.value = (flData.items || []).map(f => ({
      id: f.fl_id,
      name: f.fl_name || f.line_user_id,
      status: f.fl_verify_status,
      submitted: formatDate(f.fl_created_at)
    }))
    
    employers.value = (emData.items || []).map(e => ({
      id: e.em_id,
      name: e.em_name || e.em_username,
      status: e.em_verify_status,
      submitted: formatDate(e.em_created_at)
    }))
  } catch (e) {
    console.error('Failed to load verifications:', e)
  }
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.more-icon {
  font-size: 24px;
  cursor: pointer;
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

.filter-row {
  margin-bottom: 16px;
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.filter-select.full {
  width: 100%;
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

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.rejected, .badge.not_verified {
  background: #ffebee;
  color: #c62828;
}

.action-link {
  color: #0066cc;
  cursor: pointer;
}

.helper {
  margin-top: 12px;
  font-size: 12px;
  color: #999;
  text-align: right;
}
</style>