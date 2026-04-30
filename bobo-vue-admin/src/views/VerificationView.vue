<template>
  <div>
    <h1 class="title">Verification</h1>

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
      <select v-model="statusFilter" class="filter-select">
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
            <th style="width:54%">NAME</th>
            <th style="width:10%">STATUS</th>
            <th style="width:12%">ACTION</th>
            <th style="width:16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in filteredList" :key="v.id">
            <td class="truncate-cell">
              <span class="clickable-title" @click="openUserModal(v)" :title="v.name">
                {{ v.name }}
              </span>
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

        <div v-else class="doc-grid">
          <div v-for="(doc, idx) in selectedDocs" :key="doc.id" class="doc-card">
            <div class="doc-title">{{ doc.type }}</div>
            <div class="doc-image-container">
              <a :href="doc.file_url" target="_blank" class="doc-image-link">
                <div class="doc-image">📄</div>
              </a>
            </div>
            <div class="doc-status">
              <span class="doc-badge" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
            </div>
            <div class="doc-actions-vertical">
              <button class="btn-approve-sm" :disabled="doc.status === 'APPROVED'" @click="reviewDoc(doc, 'APPROVED')">✅ Approve</button>
              <button class="btn-reject-sm" :disabled="doc.status === 'REJECTED'" @click="reviewDoc(doc, 'REJECTED')">❌ Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const activeTab = ref('Freelancer')
const search = ref('')
const statusFilter = ref('All')
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

const filteredList = computed(() => {
  const list = activeTab.value === 'Freelancer' ? freelancers.value : employers.value
  let result = list.filter(v => {
    const matchSearch = (v.name || '').toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === 'All' || v.status === statusFilter.value
    return matchSearch && matchStatus
  })
  return [...result].sort((a, b) => {
    const dateA = new Date(a.createdAt || 0)
    const dateB = new Date(b.createdAt || 0)
    return dateB - dateA
  })
})

const openDocs = (v) => {
  selectedUser.value = v
  if (activeTab.value === 'Freelancer') {
    selectedDocs.value = flDocs.value
      .filter(d => d.fl_id === v.id && d.is_latest)
      .map(d => ({
        id: d.fl_doc_id,
        type: d.fl_doc_type,
        status: d.fl_doc_status,
        file_url: d.file_url,
        uploaded: formatDateTime(d.fl_uploaded_at),
        reviewed: d.reviewed_at ? formatDateTime(d.reviewed_at) : null,
        _type: 'fl'
      }))
  } else {
    selectedDocs.value = emDocs.value
      .filter(d => d.em_id === v.id && d.is_latest)
      .map(d => ({
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
      // Update local state
      doc.status = newStatus
      doc.reviewed = formatDateTime(new Date().toISOString())

      // Update verify status in list
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

onMounted(async () => {
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
  }
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

.filter-row {
  margin-bottom: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  max-width: 280px;
}

.filter-group {
  display: flex;
  gap: 8px;
  flex: 1;
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 160px;
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
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
  overflow: hidden;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: #f9f9f9;
}

.truncate-cell {
  max-width: 0;
}

.clickable-title {
  display: block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer;
  color: #0066cc;
  font-size: 14px;
}

.clickable-title:hover {
  text-decoration: underline;
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

.badge.not_verified {
  background: #ffebee;
  color: #c62828;
}

.action-btns {
  display: flex;
  gap: 6px;
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

/* Modal */
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

.modal {
  background: white;
  border-radius: 12px;
  padding: 28px;
  width: 520px;
  max-height: 80vh;
  overflow-y: auto;
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

.mini-modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #111;
  margin: 0;
  flex: 1;
  padding-right: 12px;
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
  font-weight: 600;
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
  width: 1000px;
  max-height: 80vh;
  overflow-y: auto;
}

.doc-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.doc-card {
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}

.doc-title {
  font-size: 12px;
  font-weight: 600;
  color: #222;
  text-align: center;
  width: 100%;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
}

.doc-image-container {
  width: 100%;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  border-radius: 6px;
}

.doc-image-link {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.doc-image {
  font-size: 36px;
  cursor: pointer;
}

.doc-status {
  width: 100%;
  text-align: center;
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

.doc-actions-vertical {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
}

.btn-approve-sm {
  padding: 5px 8px;
  border-radius: 5px;
  border: none;
  background: #e8f5e9;
  color: #2e7d32;
  font-size: 11px;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
}

.btn-approve-sm:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-reject-sm {
  padding: 5px 8px;
  border-radius: 5px;
  border: none;
  background: #ffebee;
  color: #c62828;
  font-size: 11px;
  cursor: pointer;
  font-weight: 500;
  width: 100%;
}

.btn-reject-sm:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>