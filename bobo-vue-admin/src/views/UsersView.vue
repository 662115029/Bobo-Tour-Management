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

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search name..." class="search-input" />
      <div class="filter-group">
        <select v-model="verifyFilter" class="filter-select">
          <option value="All">All Status</option>
          <option value="VERIFIED">Verified</option>
          <option value="PENDING">Pending</option>
          <option value="NOT_VERIFIED">Not Verified</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width:28%">NAME</th>
            <th style="width:16%">RATING</th>
            <th style="width:10%">JOBS</th>
            <th style="width:10%">STATUS</th>
            <th style="width:12%">ACTION</th>
            <th style="width:16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="truncate-cell">
              <div class="user-cell">
                <span class="avatar">{{ user.initials }}</span>
                <span class="clickable-title" @click="viewUser(user)" :title="user.name">
                  {{ user.name }}
                </span>
              </div>
            </td>
            <td>⭐ {{ Number(user.rating || 0).toFixed(1) }}</td>
            <td>{{ jobsDoneById[user.id] || 0 }}</td>
            <td>
              <span class="badge" :class="user.verifyStatus?.toLowerCase()">{{ user.verifyStatus }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewUser(user)">View</button>
                <button class="btn-action" :class="user.isActive ? 'ban' : 'unban'" @click="openBanModal(user)">
                  {{ user.isActive ? 'Ban' : 'Unban' }}
                </button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(user.updatedAt) }}</td>
          </tr>
          <tr v-if="users.length === 0">
            <td colspan="6" class="empty">No users found.</td>
          </tr>
        </tbody>
      </table>
    </div>
  <!-- Ban Modal -->
  <div v-if="showBanModal" class="modal-overlay" @click.self="showBanModal = false">
    <div class="modal">
      <div class="modal-icon">{{ banTarget?.isActive ? '🚫' : '✅' }}</div>
      <h3>{{ banTarget?.isActive ? 'Ban User' : 'Unban User' }}</h3>
      <p>Are you sure you want to {{ banTarget?.isActive ? 'ban' : 'unban' }}<br>
        <strong>"{{ banTarget?.name }}"</strong>?</p>
      <p v-if="banTarget?.isActive" class="modal-warning">This user will not be able to accept any jobs.</p>
      <div class="modal-actions">
        <button class="btn-cancel" @click="showBanModal = false">Cancel</button>
        <button class="btn-confirm" :class="banTarget?.isActive ? 'ban' : 'unban'" @click="confirmBan">
          {{ banTarget?.isActive ? 'Ban' : 'Unban' }}
        </button>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const activeTab = ref('Freelancer')

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const router = useRouter()
const showBanModal = ref(false)
const banTarget = ref(null)
const jobsDoneByFreelancer = ref({})
const jobsDoneByEmployer = ref({})

const viewUser = (user) => {
  if (activeTab.value === 'Freelancer') {
    router.push({ name: 'FreelancerDetail', params: { id: user.id } })
  } else {
    router.push({ name: 'EmployerDetail', params: { id: user.id } })
  }
}

const openBanModal = (user) => {
  banTarget.value = user
  showBanModal.value = true
}

const confirmBan = async () => {
  const user = banTarget.value
  const endpoint = activeTab.value === 'Freelancer'
    ? `${API_BASE}/freelancers/${user.id}/ban`
    : `${API_BASE}/employers/${user.id}/ban`
  try {
    const res = await fetch(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: !user.isActive })
    })
    const data = await res.json()
    if (data.status === 'updated') {
      user.isActive = !user.isActive
    }
  } catch (e) {
    console.error('Failed to ban/unban user:', e)
  } finally {
    showBanModal.value = false
    banTarget.value = null
  }
}
const employers = ref([])
const freelancers = ref([])
const jobs = ref([])
const search = ref('')
const verifyFilter = ref('All')

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

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
    imageUrl: e.em_profile_image_url || '',
    createdAt: e.em_created_at || '',
    updatedAt: e.em_updated_at || ''
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
    imageUrl: f.fl_profile_image_url || '',
    createdAt: f.fl_created_at || '',
    updatedAt: f.fl_updated_at || ''
  }))
}

async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/jobs?limit=500`)
    const data = await res.json()
    jobs.value = data.items || []

    const flMap = {}
    const emMap = {}

    for (const j of jobs.value) {
      if (j?.job_status !== 'COMPLETED') continue
      const flId = j.selected_fl_id
      const emId = j.em_id
      if (flId) flMap[flId] = (flMap[flId] || 0) + 1
      if (emId) emMap[emId] = (emMap[emId] || 0) + 1
    }

    jobsDoneByFreelancer.value = flMap
    jobsDoneByEmployer.value = emMap
  } catch (e) {
    console.error('Failed to load jobs:', e)
    jobs.value = []
    jobsDoneByFreelancer.value = {}
    jobsDoneByEmployer.value = {}
  }
}

const jobsDoneById = computed(() => (
  activeTab.value === 'Employer' ? jobsDoneByEmployer.value : jobsDoneByFreelancer.value
))

const users = computed(() => {
  const list = activeTab.value === 'Employer' ? employers.value : freelancers.value
  let result = list.filter(u => {
    const matchSearch = (u.name || '').toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = verifyFilter.value === 'All' || u.verifyStatus === verifyFilter.value
    return matchSearch && matchStatus
  })
  return [...result].sort((a, b) => {
    const dateA = new Date(a.createdAt || 0)
    const dateB = new Date(b.createdAt || 0)
    return dateB - dateA
  })
})

onMounted(async () => {
  await Promise.allSettled([loadEmployers(), loadFreelancers(), loadJobs()])
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
  table-layout: fixed;
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
  min-width: 0;
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
.badge.rejected, .badge.not_verified {
  background: #ffebee;
  color: #c62828;
}.badge.unknown { background: #f5f5f5; color: #666; }

.truncate-cell { max-width: 0; }

.clickable-title {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
  color: #0066cc;
  font-size: 14px;
}
.clickable-title:hover { text-decoration: underline; }

.action-btns { display: flex; gap: 6px; }
.btn-action {
  padding: 4px 10px;
  border-radius: 5px;
  border: none;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
}
.btn-action.view { background: #e3f2fd; color: #1976d2; }
.btn-action.view:hover { background: #bbdefb; }
.btn-action.ban { background: #ffebee; color: #c62828; }
.btn-action.ban:hover { background: #ffcdd2; }
.btn-action.unban { background: #e8f5e9; color: #2e7d32; }
.btn-action.unban:hover { background: #c8e6c9; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal {
  background: white; border-radius: 12px; padding: 32px;
  width: 380px; text-align: center;
}
.modal-icon { font-size: 36px; margin-bottom: 12px; }
.modal h3 { font-size: 20px; margin: 0 0 12px; }
.modal p { color: #555; margin: 0 0 8px; line-height: 1.5; }
.modal-warning { font-size: 12px; color: #dc3545 !important; margin-bottom: 24px !important; }
.modal-actions { display: flex; justify-content: center; gap: 12px; margin-top: 20px; }
.btn-cancel {
  padding: 10px 24px; border: 1px solid #ddd;
  border-radius: 6px; background: white; cursor: pointer; font-size: 14px;
}
.btn-confirm {
  padding: 10px 24px; border: none;
  border-radius: 6px; color: white; cursor: pointer; font-size: 14px;
}
.btn-confirm.ban { background: #dc3545; }
.btn-confirm.ban:hover { background: #b02a37; }
.btn-confirm.unban { background: #2e7d32; }
.btn-confirm.unban:hover { background: #1b5e20; }

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 280px;
  font-size: 14px;
}

.text-muted { color: #999; font-size: 13px; }

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 140px;
}

.empty { text-align: center; color: #999; padding: 32px; }
</style>