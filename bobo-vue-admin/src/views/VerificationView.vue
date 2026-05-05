<template>
  <div>
    <BreadcrumbBar />

    <div class="tabs">
      <button class="tab" :class="{ active: activeTab === 'Freelancer' }" @click="activeTab = 'Freelancer'">
        Freelancer
      </button>
      <button class="tab" :class="{ active: activeTab === 'Employer' }" @click="activeTab = 'Employer'">
        Employer
      </button>
    </div>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search name..." class="search-input" />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width:46%" @click="cycleSort('name')">
              <span class="th-inner">
                NAME
                <span class="sort-arrows">
                  <span :class="nameSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="nameSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th style="width:10%">
              STATUS
              <button class="col-filter-btn" :class="{ active: statusFilter !== '' }" @click.stop="toggleStatusDropdown($event)">
                {{ statusFilter ? statusFilter : 'All ▼' }}
              </button>
            </th>
            <th style="width:12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width:16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-arrows">
                  <span :class="dateSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="dateSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
              <button v-if="nameSort || statusFilter || dateSort" class="reset-btn" @click.stop="resetAllFilters" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);">✕ Reset</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-'+i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:60%"></span></td>
              <td><span class="skeleton skeleton-badge"></span></td>
              <td><div class="action-btns"><span class="skeleton skeleton-btn" style="width:72px"></span></div></td>
              <td><span class="skeleton skeleton-text" style="width:75%"></span></td>
            </tr>
          </template>
          <tr v-for="v in filteredList" :key="v.id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openUserModal(v)">
              {{ v.name }}
            </td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="openDocs(v)">View Docs</button>
              </div>
            </td>
            <td class="text-muted">{{ v.updated }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdown -->
    <div v-if="showStatusDropdown" class="col-dropdown" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setStatusFilter('')">All</button>
      <button class="col-dropdown-item" @click="setStatusFilter('VERIFIED')">Verified</button>
      <button class="col-dropdown-item" @click="setStatusFilter('PENDING')">Pending</button>
      <button class="col-dropdown-item" @click="setStatusFilter('NOT_VERIFIED')">Not Verified</button>
    </div>



    <!-- User Detail Modal -->
    <div v-if="userDetailModal" class="modal-overlay" @click.self="userDetailModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px;">
          <button class="close-btn" @click="userDetailModal = null">✕</button>
        </div>
        <div v-if="userDetailLoading" class="mini-loading">Loading...</div>
        <div v-else>
          <!-- Freelancer -->
          <div v-if="activeTab === 'Freelancer' && userDetailModal">
            <div class="profile-hero">
              <div class="profile-avatar fl">
                <img v-if="userDetailModal.fl_profile_image_url" :src="userDetailModal.fl_profile_image_url" class="avatar-img" />
                <span v-else class="avatar-initial">{{ userDetailModal.fl_name?.[0] || '?' }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ userDetailModal.fl_name }}</h3>
                <p v-if="userDetailModal.fl_bio" class="profile-bio">{{ userDetailModal.fl_bio }}</p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item"><label>Status</label>
                <span class="badge" :class="userDetailModal.fl_verify_status?.toLowerCase()">{{ userDetailModal.fl_verify_status }}</span>
              </div>
              <div class="mini-item"><label>Active</label><span>{{ userDetailModal.fl_is_active ? '✅ Active' : '❌ Inactive' }}</span></div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ userDetailModal.fl_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ userDetailModal.fl_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(userDetailModal.fl_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(userDetailModal.fl_updated_at) }}</span></div>
            </div>
          </div>
          <!-- Employer -->
          <div v-if="activeTab === 'Employer' && userDetailModal">
            <div class="profile-hero">
              <div class="profile-avatar em">
                <img v-if="userDetailModal.em_profile_image_url" :src="userDetailModal.em_profile_image_url" class="avatar-img" />
                <span v-else class="avatar-initial">{{ userDetailModal.em_name?.[0] || '?' }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ userDetailModal.em_name }}</h3>
                <p v-if="userDetailModal.em_bio" class="profile-bio">{{ userDetailModal.em_bio }}</p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item"><label>Status</label>
                <span class="badge" :class="userDetailModal.em_verify_status?.toLowerCase()">{{ userDetailModal.em_verify_status }}</span>
              </div>
              <div class="mini-item"><label>Active</label><span>{{ userDetailModal.em_is_active ? '✅ Active' : '❌ Inactive' }}</span></div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ userDetailModal.em_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Phone</label><span>{{ userDetailModal.em_phone || '-' }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ userDetailModal.em_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(userDetailModal.em_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(userDetailModal.em_updated_at) }}</span></div>
            </div>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="openDocsFromUser">View Documents →</button>
        </div>
      </div>
    </div>

    <!-- Document Modal -->
    <div v-if="selectedUser" class="modal-overlay" @click.self="selectedUser = null">
      <div class="docs-modal">
        <div class="modal-header">
          <div>
            <h3>{{ selectedUser.name }} - Documents</h3>
          </div>
          <button class="close-btn" @click="selectedUser = null">✕</button>
        </div>

        <div v-if="selectedDocs.length === 0" class="no-docs">No documents found.</div>

        <div v-else class="doc-list">
          <div v-for="doc in selectedDocs" :key="doc.id" class="doc-row">
            <div class="doc-type-cell">{{ doc.type }}</div>
            <div class="doc-file-cell">
              <img :src="doc.file_url" class="doc-thumbnail" :alt="doc.type" />
            </div>
            <div class="doc-status-cell">
              <span class="doc-badge" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
            </div>
            <div class="doc-uploaded-cell">{{ doc.uploaded }}</div>
            <div class="doc-actions-cell">
              <button class="btn-approve-row" :disabled="doc.status === 'APPROVED'" @click="reviewDoc(doc, 'APPROVED')">✅ Approve</button>
              <button class="btn-reject-row" :disabled="doc.status === 'REJECTED'" @click="reviewDoc(doc, 'REJECTED')">❌ Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const activeTab = ref('Freelancer')
const search = ref('')
const nameSort = ref(localStorage.getItem('verification_nameSort') || '')
const statusFilter = ref(localStorage.getItem('verification_statusFilter') || '')
const dateSort = ref(localStorage.getItem('verification_dateSort') || '')
const showStatusDropdown = ref(false)
const statusDropdownStyle = ref({})

const saveFilters = () => {
  localStorage.setItem('verification_nameSort', nameSort.value)
  localStorage.setItem('verification_statusFilter', statusFilter.value)
  localStorage.setItem('verification_dateSort', dateSort.value)
}

const isLoading = ref(true)
const freelancers = ref([])
const employers = ref([])
const allFreelancers = ref([])
const allEmployers = ref([])
const flDocs = ref([])
const emDocs = ref([])
const selectedUser = ref(null)
const selectedDocs = ref([])
const userDetailModal = ref(null)
const userDetailLoading = ref(false)

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const cycleSort = (key) => {
  const map = { name: nameSort, date: dateSort }
  const current = map[key]
  const next = current.value === '' ? 'asc' : current.value === 'asc' ? 'desc' : ''
  nameSort.value = ''
  dateSort.value = ''
  current.value = next
  saveFilters()
}

const toggleStatusDropdown = (e) => {
  closeAllDropdowns()
  showStatusDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  statusDropdownStyle.value = {
    position: 'fixed',
    top: (rect.bottom + window.scrollY) + 'px',
    left: rect.left + 'px'
  }
}

const setStatusFilter = (val) => {
  statusFilter.value = val
  showStatusDropdown.value = false
  saveFilters()
}

const closeAllDropdowns = () => {
  showStatusDropdown.value = false
}

const resetAllFilters = () => {
  nameSort.value = ''
  statusFilter.value = ''
  dateSort.value = ''
  saveFilters()
}

const handleOutsideClick = (e) => {
  if (!e.target.closest('.col-dropdown') && !e.target.closest('.col-filter-btn')) {
    closeAllDropdowns()
  }
}

const filteredList = computed(() => {
  const list = activeTab.value === 'Freelancer' ? freelancers.value : employers.value
  let result = list.filter(v => {
    const matchSearch = (v.name || '').toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === '' || v.status === statusFilter.value
    return matchSearch && matchStatus
  })

  if (nameSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.name || '').localeCompare(b.name || '')
      return nameSort.value === 'desc' ? -cmp : cmp
    })
  }

  if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.createdAt || 0)
      const dateB = new Date(b.createdAt || 0)
      return dateSort.value === 'desc' ? dateB - dateA : dateA - dateB
    })
  } else if (!nameSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.createdAt || 0)
      const dateB = new Date(b.createdAt || 0)
      return dateB - dateA
    })
  }

  return result
})

const openDocs = (v) => {
  selectedUser.value = v
  if (activeTab.value === 'Freelancer') {
    const allDocs = flDocs.value.filter(d => d.fl_id === v.id)
    const docsByType = {}
    allDocs.forEach(d => {
      if (!docsByType[d.fl_doc_type] || new Date(d.fl_uploaded_at) > new Date(docsByType[d.fl_doc_type].fl_uploaded_at)) {
        docsByType[d.fl_doc_type] = d
      }
    })
    selectedDocs.value = Object.values(docsByType).map(d => ({
      id: d.fl_doc_id,
      type: d.fl_doc_type,
      status: d.fl_doc_status,
      file_url: d.file_url,
      uploaded: formatDateTime(d.fl_uploaded_at),
      reviewed: d.reviewed_at ? formatDateTime(d.reviewed_at) : null,
      _type: 'fl'
    }))
  } else {
    const allDocs = emDocs.value.filter(d => d.em_id === v.id)
    const docsByType = {}
    allDocs.forEach(d => {
      if (!docsByType[d.em_doc_type] || new Date(d.em_uploaded_at) > new Date(docsByType[d.em_doc_type].em_uploaded_at)) {
        docsByType[d.em_doc_type] = d
      }
    })
    selectedDocs.value = Object.values(docsByType).map(d => ({
      id: d.em_doc_id,
      type: d.em_doc_type,
      status: d.em_doc_status,
      file_url: d.file_url,
      uploaded: formatDateTime(d.em_uploaded_at),
      reviewed: d.reviewed_at ? formatDateTime(d.reviewed_at) : null,
      _type: 'em'
    }))
  }
}

const openUserModal = (v) => {
  userDetailLoading.value = true
  if (activeTab.value === 'Freelancer') {
    userDetailModal.value = allFreelancers.value.find(f => f.fl_id === v.id) || null
  } else {
    userDetailModal.value = allEmployers.value.find(e => e.em_id === v.id) || null
  }
  userDetailLoading.value = false
}

const openDocsFromUser = () => {
  if (!userDetailModal.value) return
  const user = activeTab.value === 'Freelancer'
    ? { id: userDetailModal.value.fl_id, name: userDetailModal.value.fl_name }
    : { id: userDetailModal.value.em_id, name: userDetailModal.value.em_name }
  openDocs(user)
  userDetailModal.value = null
}

const reviewDoc = async (doc, newStatus) => {
  const endpoint = doc._type === 'fl'
    ? `${API_BASE}/fl-documents/${doc.id}`
    : `${API_BASE}/em-documents/${doc.id}`
  try {
    const res = await fetch(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus, reviewed_by: 'ad_001' })
    })
    const data = await res.json()
    if (data.status === 'updated') {
      doc.status = newStatus
      doc.reviewed = formatDateTime(new Date().toISOString())

      const list = activeTab.value === 'Freelancer' ? freelancers.value : employers.value
      const user = list.find(u => u.id === selectedUser.value.id)
      if (user) {
        const allApproved = selectedDocs.value.every(d => d.status === 'APPROVED')
        const anyRejected = selectedDocs.value.some(d => d.status === 'REJECTED')
        if (allApproved) user.status = 'VERIFIED'
        else if (anyRejected) user.status = 'NOT_VERIFIED'
        selectedUser.value.status = user.status
      }
    }
  } catch (e) {
    console.error('Failed to review doc:', e)
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  try {
    const [flRes, emRes, flDocRes, emDocRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
      fetch(`${API_BASE}/em-documents?limit=500`),
    ])
    const [flData, emData, flDocData, emDocData] = await Promise.all([
      flRes.json(), emRes.json(), flDocRes.json(), emDocRes.json()
    ])

    allFreelancers.value = flData.items || []
    allEmployers.value = emData.items || []

    freelancers.value = (flData.items || []).map(f => ({
      id: f.fl_id,
      name: f.fl_name || f.line_user_id,
      status: f.fl_verify_status,
      submitted: formatDateTime(f.fl_created_at),
      updated: formatDateTime(f.fl_updated_at),
      createdAt: f.fl_created_at || '',
    }))

    employers.value = (emData.items || []).map(e => ({
      id: e.em_id,
      name: e.em_name || e.em_username,
      status: e.em_verify_status,
      submitted: formatDateTime(e.em_created_at),
      updated: formatDateTime(e.em_updated_at),
      createdAt: e.em_created_at || '',
    }))

    flDocs.value = flDocData.items || []
    emDocs.value = emDocData.items || []
  } catch (e) {
    console.error('Failed to load verifications:', e)
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
.title {
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 2px 0;
  background: #1a1a2e;
  padding: 15px 20px;
  color: white;
  letter-spacing: 0.2px;
}

.tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
  padding: 0 20px;
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
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}



.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin: 0 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.table th,
.table td {
  padding: 15px 20px;
  text-align: left;
  border-bottom: 1px solid #eee;
  overflow: hidden;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: white;
  white-space: nowrap;
  position: relative;
}

.search-input {
  padding: 10px 14px;
  border: 1.5px solid #bbb;
  border-radius: 8px;
  width: 280px;
  font-size: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.search-input:focus {
  border-color: #06c755;
  box-shadow: 0 0 0 3px rgba(6,199,85,0.12);
}

.table th.th-sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.15s, color 0.15s;
}
.table th.th-sortable:hover { background: #f0fdf4; color: #06c755; }
.table th.th-active { background: #f0fdf4; color: #06c755; }
.th-inner { display: inline-flex; align-items: center; gap: 6px; }
.sort-arrows { display: inline-flex; flex-direction: column; line-height: 1; font-size: 10px; gap: 0; margin-top: 1px; }
.arrow-dim { color: #ccc; }
.arrow-active { color: #06c755; font-weight: 700; }

@keyframes shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
.skeleton {
  display: inline-block;
  border-radius: 6px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 800px 100%;
  animation: shimmer 1.4s infinite;
}
.skeleton-text { height: 14px; display: block; border-radius: 4px; }
.skeleton-badge { height: 22px; width: 70px; border-radius: 12px; }
.skeleton-btn { height: 26px; width: 50px; border-radius: 5px; }
.skeleton-row td { padding-top: 18px; padding-bottom: 18px; }

.col-filter-btn {
  margin-left: 8px;
  padding: 4px 10px;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 11px;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-weight: 500;
}

.col-filter-btn:hover {
  border-color: #06C755;
  color: #06C755;
}

.col-filter-btn.active {
  border-color: #06C755;
  color: #06C755;
  font-weight: 600;
}

.reset-btn {
  margin-left: 6px; padding: 4px 8px; border: none;
  border-radius: 4px; font-size: 10px; background: #ffebee;
  color: #c62828; cursor: pointer; font-weight: 500;
}
.reset-btn:hover { background: #ffcdd2; }

.col-dropdown {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 50;
  min-width: 140px;
}

.col-dropdown-item {
  display: block;
  width: 100%;
  padding: 8px 14px;
  border: none;
  background: none;
  text-align: left;
  font-size: 13px;
  cursor: pointer;
}

.col-dropdown-item:hover {
  background: #f5f5f5;
}

.col-dropdown-item:first-child {
  border-radius: 6px 6px 0 0;
}

.col-dropdown-item:last-child {
  border-radius: 0 0 6px 6px;
}

.truncate-cell {
  max-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-hover:hover {
  background: #f5f5f5;
}

.clickable-cell {
  cursor: pointer;
  color: #000;
}

.clickable-cell:hover {
  color: #000;
  text-decoration: underline;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  width: fit-content;
}

.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.not_verified {
  background: #ffebee;
  color: #c62828;
}

@keyframes shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
.skeleton {
  display: inline-block;
  border-radius: 6px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 800px 100%;
  animation: shimmer 1.4s infinite;
}
.skeleton-text { height: 14px; display: block; border-radius: 4px; }
.skeleton-badge { height: 22px; width: 70px; border-radius: 12px; }
.skeleton-btn { height: 26px; width: 50px; border-radius: 5px; }
.skeleton-row td { padding-top: 18px; padding-bottom: 18px; }

.action-btns {
  display: flex;
  gap: 6px;
  justify-content: center;
}

.btn-action {
  padding: 4px 10px;
  border-radius: 5px;
  border: none;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
}

.btn-action.view {
  background: #e3f2fd;
  color: #1976d2;
}

.btn-action.view:hover {
  background: #bbdefb;
}

.text-muted {
  color: #999;
  font-size: 13px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.modal-header h3 {
  font-size: 18px;
  margin: 0 0 6px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #888;
  padding: 0;
  flex-shrink: 0;
}

.no-docs {
  color: #999;
  text-align: center;
  padding: 24px 0;
}

.mini-modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 460px;
  max-height: 80vh;
  overflow-y: auto;
}

.mini-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.mini-modal-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}

.btn-full-view {
  background: none;
  border: none;
  color: #0066cc;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.btn-full-view:hover {
  text-decoration: underline;
}

.mini-loading {
  color: #999;
  text-align: center;
  padding: 20px 0;
}

.profile-hero {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}

.profile-avatar.fl {
  background: #e3f2fd;
}

.profile-avatar.em {
  background: #f3e5f5;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.avatar-initial {
  font-size: 22px;
  font-weight: 700;
  color: #555;
}

.profile-info {
  flex: 1;
  min-width: 0;
}

.profile-name {
  font-size: 16px;
  font-weight: 100;
  margin: 0 0 4px;
  color: #111;
}

.profile-bio {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.profile-bio.muted {
  color: #bbb;
  font-style: italic;
}

.mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.mini-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.mini-item label {
  font-size: 10px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.mini-item span {
  font-size: 13px;
  color: #222;
}

.docs-modal {
  background: white;
  border-radius: 12px;
  padding: 28px;
  width: 1200px;
  max-height: 80vh;
  overflow-y: auto;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doc-row {
  border: 1px solid #eee;
  border-radius: 8px;
  padding: 14px;
  display: grid;
  grid-template-columns: 120px 150px 100px 150px 1fr;
  gap: 16px;
  align-items: center;
}

.doc-type-cell {
  font-weight: 600;
  color: #222;
  font-size: 14px;
}

.doc-file-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}

.doc-thumbnail {
  max-width: 120px;
  max-height: 100px;
  border-radius: 5px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.2s;
}

.doc-thumbnail:hover {
  transform: scale(1.05);
}

.doc-status-cell {
  text-align: center;
}

.doc-uploaded-cell {
  font-size: 12px;
  color: #666;
}

.doc-actions-cell {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.btn-approve-row {
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
  background: #e8f5e9;
  color: #2e7d32;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-approve-row:hover:not(:disabled) {
  background: #c8e6c9;
}

.btn-approve-row:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-reject-row {
  padding: 6px 12px;
  border-radius: 5px;
  border: none;
  background: #ffebee;
  color: #c62828;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-reject-row:hover:not(:disabled) {
  background: #ffcdd2;
}

.btn-reject-row:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.doc-badge {
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 600;
}

.doc-badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.doc-badge.approved {
  background: #e8f5e9;
  color: #2e7d32;
}

.doc-badge.rejected {
  background: #ffebee;
  color: #c62828;
}
</style>