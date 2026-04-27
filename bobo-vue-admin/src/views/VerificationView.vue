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
      <div class="filter-group">
        <select v-model="statusFilter" class="filter-select">
          <option value="All">All Status</option>
          <option value="VERIFIED">Verified</option>
          <option value="PENDING">Pending</option>
          <option value="NOT_VERIFIED">Not Verified</option>
        </select>
        <select v-model="sortOrder" class="filter-select">
          <option value="newest">Newest First</option>
          <option value="oldest">Oldest First</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>STATUS</th>
            <th>ACTION</th>
            <th>SUBMITTED</th>
            <th>LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in filteredList" :key="v.id">
            <td>{{ v.name }}</td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>
              <span class="action-link" @click="openDocs(v)">View Docs</span>
            </td>
            <td class="text-muted">{{ v.submitted }}</td>
            <td class="text-muted">{{ v.updated }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Document Modal -->
    <div v-if="selectedUser" class="modal-overlay" @click.self="selectedUser = null">
      <div class="modal">
        <div class="modal-header">
          <div>
            <h3>{{ selectedUser.name }}</h3>
            <span class="badge" :class="selectedUser.status?.toLowerCase()">{{ selectedUser.status }}</span>
          </div>
          <button class="close-btn" @click="selectedUser = null">✕</button>
        </div>

        <div v-if="selectedDocs.length === 0" class="no-docs">No documents found.</div>

        <div v-else class="doc-list">
          <div v-for="doc in selectedDocs" :key="doc.id" class="doc-item">
            <div class="doc-info">
              <span class="doc-type">{{ doc.type }}</span>
              <span class="doc-badge" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
            </div>
            <div class="doc-meta">
              Uploaded: {{ doc.uploaded }}
              <span v-if="doc.reviewed"> · Reviewed: {{ doc.reviewed }}</span>
            </div>
            <div class="doc-actions">
              <a :href="doc.file_url" target="_blank" class="btn-view">📄 View File</a>
              <button class="btn-approve" :disabled="doc.status === 'APPROVED'" @click="reviewDoc(doc, 'APPROVED')">✅
                Approve</button>
              <button class="btn-reject" :disabled="doc.status === 'REJECTED'" @click="reviewDoc(doc, 'REJECTED')">❌
                Reject</button>
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
const sortOrder = ref('newest')
const freelancers = ref([])
const employers = ref([])
const flDocs = ref([])
const emDocs = ref([])
const selectedUser = ref(null)
const selectedDocs = ref([])

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
    return sortOrder.value === 'newest' ? dateB - dateA : dateA - dateB
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
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 280px;
  font-size: 14px;
}

.filter-group {
  display: flex;
  gap: 8px;
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

.badge.not_verified {
  background: #ffebee;
  color: #c62828;
}

.action-link {
  color: #0066cc;
  cursor: pointer;
  font-size: 13px;
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

.modal {
  background: white;
  border-radius: 12px;
  padding: 28px;
  width: 520px;
  max-height: 80vh;
  overflow-y: auto;
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
}

.no-docs {
  color: #999;
  text-align: center;
  padding: 24px 0;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.doc-item {
  border: 1px solid #eee;
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.doc-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.doc-type {
  font-size: 14px;
  font-weight: 600;
  color: #222;
}

.doc-badge {
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
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

.doc-meta {
  font-size: 12px;
  color: #888;
}

.doc-actions {
  display: flex;
  gap: 10px;
  align-items: center;
}

.btn-view {
  padding: 7px 14px;
  border-radius: 6px;
  border: 1px solid #ddd;
  background: white;
  font-size: 13px;
  cursor: pointer;
  text-decoration: none;
  color: #333;
}

.btn-approve {
  padding: 7px 14px;
  border-radius: 6px;
  border: none;
  background: #e8f5e9;
  color: #2e7d32;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.btn-approve:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-reject {
  padding: 7px 14px;
  border-radius: 6px;
  border: none;
  background: #ffebee;
  color: #c62828;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}

.btn-reject:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}
</style>