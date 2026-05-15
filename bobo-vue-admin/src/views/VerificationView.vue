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
      <table class="table verify-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width:40%" @click="cycleSort('name')">
              <span class="th-inner">
                NAME
                <span class="sort-label">
                  <span v-if="!nameSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="nameSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th style="width:16%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">STATUS
              <button class="col-filter-btn" :class="{ active: statusFilter !== '' }" @click.stop="toggleStatusDropdown($event)">
                {{ statusFilter ? statusFilter + ' ▼' : 'All ▼' }}
              </button></span>
            </th>
            <th style="width:12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width:16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button v-if="nameSort || statusFilter || dateSort" class="reset-btn ml-1.5" @click.stop="resetAllFilters" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);">✕ Reset</button>
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
          <tr v-for="v in filteredList" :key="v.id">
            <td class="truncate-cell">
              <div class="user-cell">
                <span class="user-avatar" :style="avatarStyle(v.id, v.name)">{{ initials2(v.name) }}</span>
                <span class="clickable-cell" style="cursor:pointer" :title="v.name" @click="openUserModal(v)">{{ v.name }}</span>
              </div>
            </td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action verify-style" @click="openDocs(v)">View Docs</button>
              </div>
            </td>
            <td class="text-muted text-[13px]">{{ v.updated }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdown -->
    <div v-if="showStatusDropdown" class="col-dropdown min-w-[140px]" :style="statusDropdownStyle">
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
              <div class="profile-avatar-wrap">
                <img v-if="userDetailModal.fl_profile_image_url" :src="userDetailModal.fl_profile_image_url" class="w-12 h-12 rounded-full object-cover ring-2 ring-[#eee]" />
                <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ring-2 ring-[#eee]" :style="avatarStyle(userDetailModal.fl_id, userDetailModal.fl_name)">{{ initials2(userDetailModal.fl_name) }}</div>
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
              <div class="mini-item"><label>Active</label>
                <div style="display:flex;align-items:center;gap:6px;">
                  <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: userDetailModal.fl_is_active ? '#06c755' : '#bbb' }"></div>
                  <span :style="{ color: userDetailModal.fl_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">{{ userDetailModal.fl_is_active ? 'Active' : 'Inactive' }}</span>
                </div>
              </div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ userDetailModal.fl_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ userDetailModal.fl_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(userDetailModal.fl_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(userDetailModal.fl_updated_at) }}</span></div>
            </div>
          </div>
          <!-- Employer -->
          <div v-if="activeTab === 'Employer' && userDetailModal">
            <div class="profile-hero">
              <div class="profile-avatar-wrap">
                <img v-if="userDetailModal.em_profile_image_url" :src="userDetailModal.em_profile_image_url" class="w-12 h-12 rounded-full object-cover ring-2 ring-[#eee]" />
                <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ring-2 ring-[#eee]" :style="avatarStyle(userDetailModal.em_id, userDetailModal.em_name)">{{ initials2(userDetailModal.em_name) }}</div>
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
              <div class="mini-item"><label>Active</label>
                <div style="display:flex;align-items:center;gap:6px;">
                  <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: userDetailModal.em_is_active ? '#06c755' : '#bbb' }"></div>
                  <span :style="{ color: userDetailModal.em_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">{{ userDetailModal.em_is_active ? 'Active' : 'Inactive' }}</span>
                </div>
              </div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ userDetailModal.em_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Phone</label><span>{{ userDetailModal.em_phone || '-' }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ userDetailModal.em_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(userDetailModal.em_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(userDetailModal.em_updated_at) }}</span></div>
            </div>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="openDocsFromUser">ดูรายละเอียดทั้งหมด →</button>
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

const AVATAR_PALETTES = [
  { bg: '#e3f2fd', text: '#1565c0' }, { bg: '#fce4ec', text: '#ad1457' },
  { bg: '#e8f5e9', text: '#2e7d32' }, { bg: '#fff3e0', text: '#e65100' },
  { bg: '#f3e5f5', text: '#6a1b9a' }, { bg: '#e0f7fa', text: '#00695c' },
  { bg: '#fff8e1', text: '#f57f17' }, { bg: '#fbe9e7', text: '#bf360c' },
]
const avatarPalette = (id, name) => {
  const str = String(id || name || '?')
  let hash = 0; for (let i = 0; i < str.length; i++) hash = (hash * 31 + str.charCodeAt(i)) >>> 0
  return AVATAR_PALETTES[hash % AVATAR_PALETTES.length]
}
const avatarStyle = (id, name) => {
  const p = avatarPalette(id, name)
  return { backgroundColor: p.bg, color: p.text }
}
const initials2 = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/).slice(0, 2)
  return parts.map(p => p[0]?.toUpperCase() || '').join('')
}
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
      body: JSON.stringify({ status: newStatus, reviewed_by: localStorage.getItem('admin_id') || '' })
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