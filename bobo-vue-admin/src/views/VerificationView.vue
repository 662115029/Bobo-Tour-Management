<template>
  <div>
    <BreadcrumbBar />

    <div class="tabs">
      <button class="tab" :class="{ active: activeTab === 'Freelancer' }" @click="switchTab('Freelancer')">Freelancer</button>
      <button class="tab" :class="{ active: activeTab === 'Employer' }" @click="switchTab('Employer')">Employer</button>
    </div>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search name..." class="search-input" @input="onSearch" />
    </div>

    <div class="table-container">
      <table class="table verify-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width:40%" @click="cycleSort('name')">
              <span class="th-inner">NAME
                <span class="sort-label">
                  <span v-if="!nameSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="nameSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th style="width:16%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">STATUS
                <button class="col-filter-btn" :class="{ active: statusFilter !== 'PENDING' }" @click.stop="toggleStatusDropdown($event)">
                  {{ statusFilter || 'PENDING' }} ▼
                </button>
              </span>
            </th>
            <th style="width:12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width:16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">SUBMITTED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-active">↑</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button v-if="nameSort || dateSort || search || statusFilter !== 'PENDING'" class="reset-btn ml-1.5"
                @click.stop="resetAllFilters" style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);">✕ Reset</button>
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
          <tr v-else-if="!isLoading && sortedList.length === 0">
            <td colspan="4" class="text-center text-muted py-6">No results found</td>
          </tr>
          <tr v-for="v in sortedList" :key="v.id">
            <td class="truncate-cell">
              <div class="user-cell">
              <UserAvatar :id="v.id" :name="v.name" :image-url="v.imageUrl" :size="28" />
                <span class="clickable-cell" :title="v.name" @click="openUserModal(v)">{{ v.name }}</span>
              </div>
            </td>
            <td><span class="badge" :class="v.status?.toLowerCase()">{{ formatVerifyStatus(v.status) }}</span></td>
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

    <!-- Pagination -->
    <PaginationBar :page="currentPage" :has-more="hasMore" :has-items="sortedList.length > 0"
      @prev="loadUsers(currentPage - 1)" @next="loadUsers(currentPage + 1)" />

    <!-- Column Filter Dropdown -->
    <div v-if="showStatusDropdown" class="col-dropdown min-w-[140px]" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setStatusFilter('VERIFIED')">Verified</button>
      <button class="col-dropdown-item" @click="setStatusFilter('PENDING')">Pending</button>
      <button class="col-dropdown-item" @click="setStatusFilter('NOT_VERIFIED')">Not Verified</button>
    </div>

    <UserMiniModal
      :data="userDetailModal"
      :type="activeTab === 'Freelancer' ? 'FREELANCER' : 'EMPLOYER'"
      :loading="userDetailLoading"
      @close="userDetailModal = null"
      @view-detail="goToUserDetail"
    />

    <DocReviewModal
      :user="selectedUser"
      :docs="selectedDocs"
      @close="selectedUser = null"
      @approve="(doc) => reviewDoc(doc, 'APPROVED')"
      @reject="(doc) => reviewDoc(doc, 'REJECTED')"
    />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import UserMiniModal from '../components/UserMiniModal.vue'
import DocReviewModal from '../components/DocReviewModal.vue'
import UserAvatar from '../components/UserAvatar.vue'
import PaginationBar from '../components/PaginationBar.vue'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime, groupDocsByLatest } from '../utils/formatDate'
import { API_BASE } from '../data/api'
import { formatVerifyStatus } from '../utils/statusClasses'

const router = useRouter()
const { avatarStyle, initials2 } = useAvatar()

const activeTab = ref('Freelancer')
const isLoading = ref(false)
const search = ref('')
const currentPage = ref(1)
const pageSize = 10
const hasMore = ref(false)
const pageCache = new Map()
const inFlight = new Map()
const nameSort = ref('')
const statusFilter = ref('PENDING')
const sortField = ref('fl_updated_at')
const sortOrder = ref('asc')

const SORT_FIELD_MAP = {
  Freelancer: { name: 'fl_name', date: 'fl_updated_at' },
  Employer:   { name: 'em_name', date: 'em_updated_at' },
}
const dateSort = ref('')
const showStatusDropdown = ref(false)
const statusDropdownStyle = ref({})

const freelancers = ref([])
const employers = ref([])
const flDocs = ref([])
const emDocs = ref([])
const selectedUser = ref(null)
const selectedDocs = ref([])
const userDetailModal = ref(null)
const userDetailLoading = ref(false)

const getCacheKey = (page) =>
  `${activeTab.value}_${page}_${statusFilter.value}_${search.value}_${sortField.value}_${sortOrder.value}`

// Debounce search
let searchTimer = null
const onSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { pageCache.clear(); loadUsers(1) }, 300)
}

const cycleSort = (key) => {
  const map = { name: nameSort, date: dateSort }
  const current = map[key]
  const next = current.value === '' ? 'asc' : current.value === 'asc' ? 'desc' : ''
  nameSort.value = ''
  dateSort.value = ''
  current.value = next
  if (next !== '') {
    sortField.value = SORT_FIELD_MAP[activeTab.value][key]
    sortOrder.value = next
  } else {
    sortField.value = activeTab.value === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
    sortOrder.value = 'asc'
  }
  pageCache.clear(); inFlight.clear()
  loadUsers(1)
}

const toggleStatusDropdown = (e) => {
  showStatusDropdown.value = !showStatusDropdown.value
  const rect = e.target.getBoundingClientRect()
  statusDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setStatusFilter = (val) => {
  statusFilter.value = val
  showStatusDropdown.value = false
  pageCache.clear(); inFlight.clear()
  loadUsers(1)
}

const resetAllFilters = () => {
  nameSort.value = ''
  statusFilter.value = 'PENDING'
  dateSort.value = ''
  search.value = ''
  sortField.value = activeTab.value === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
  sortOrder.value = 'asc'
  pageCache.clear(); inFlight.clear()
  loadUsers(1)
}

const handleOutsideClick = (e) => {
  if (!e.target.closest('.col-dropdown') && !e.target.closest('.col-filter-btn')) {
    showStatusDropdown.value = false
  }
}

async function fetchPageData(page) {
  const key = getCacheKey(page)
  if (pageCache.has(key)) return pageCache.get(key)
  if (inFlight.has(key)) return inFlight.get(key)

  const offset = (page - 1) * pageSize
  const statusParam = statusFilter.value ? `&status=${statusFilter.value}` : ''
  const searchParam = search.value ? `&search=${encodeURIComponent(search.value)}` : ''
  const isFL = activeTab.value === 'Freelancer'
  const userUrl = isFL
    ? `${API_BASE}/freelancers?limit=${pageSize+1}&offset=${offset}${statusParam}${searchParam}&sort_by=${sortField.value}&sort_order=${sortOrder.value}`
    : `${API_BASE}/employers?limit=${pageSize+1}&offset=${offset}${statusParam}${searchParam}&sort_by=${sortField.value}&sort_order=${sortOrder.value}`

  const promise = (async () => {
    const userData = await fetch(userUrl).then(r => r.json())
    const userItems = (userData.items || []).slice(0, pageSize)
    const ids = isFL
      ? userItems.map(f => f.fl_id).join(',')
      : userItems.map(e => e.em_id).join(',')
    const docUrl = isFL
      ? `${API_BASE}/fl-documents?fl_ids=${ids}&limit=50`
      : `${API_BASE}/em-documents?em_ids=${ids}&limit=50`
    const docData = ids ? await fetch(docUrl).then(r => r.json()) : { items: [] }
    const result = {
      allItems: userData.items || [],
      docs: docData.items || [],
      type: isFL ? 'fl' : 'em'
    }
    pageCache.set(key, result)
    inFlight.delete(key)
    return result
  })().catch(err => { inFlight.delete(key); throw err })

  inFlight.set(key, promise)
  return promise
}

async function loadUsers(page = 1) {
  if (activeTab.value === 'Freelancer') freelancers.value = []
  else employers.value = []
  isLoading.value = true
  currentPage.value = page
  try {
    const { allItems, docs, type } = await fetchPageData(page)

    if (type === 'fl') {
      const allFlItems = allItems
      hasMore.value = allFlItems.length > pageSize
      const flItems = allFlItems.slice(0, pageSize)
      flDocs.value = docs
      freelancers.value = flItems.map(f => ({
        id: f.fl_id,
        name: f.fl_name || f.line_user_id,
        status: f.fl_verify_status,
        updated: formatDateTime(f.fl_updated_at),
        createdAt: f.fl_created_at || '',
        imageUrl: f.fl_profile_image_url || null,
        rawData: f,
      }))
    } else {
      const allEmItems = allItems
      hasMore.value = allEmItems.length > pageSize
      const emItems = allEmItems.slice(0, pageSize)
      emDocs.value = docs
      employers.value = emItems.map(e => ({
        id: e.em_id,
        name: e.em_name || e.em_username,
        status: e.em_verify_status,
        updated: formatDateTime(e.em_updated_at),
        createdAt: e.em_created_at || '',
        imageUrl: e.em_profile_image_url || null,
        rawData: e,
      }))
    }

    if (hasMore.value) fetchPageData(page + 1).catch(() => {})
  } catch (e) {
    console.error('Failed to load:', e)
  } finally {
    isLoading.value = false
  }
}

const currentList = computed(() =>
  activeTab.value === 'Freelancer' ? freelancers.value : employers.value
)

const sortedList = computed(() => currentList.value)

const openDocs = (v) => {
  selectedUser.value = v
  if (activeTab.value === 'Freelancer') {
    const allDocs = flDocs.value.filter(d => Number(d.fl_id) === Number(v.id))
    selectedDocs.value = groupDocsByLatest(allDocs, 'fl', formatDateTime)
  } else {
    const allDocs = emDocs.value.filter(d => Number(d.em_id) === Number(v.id))
    selectedDocs.value = groupDocsByLatest(allDocs, 'em', formatDateTime)
  }
}

const openUserModal = (v) => {
  userDetailLoading.value = true
  userDetailModal.value = v.rawData || null
  userDetailLoading.value = false
}

const goToUserDetail = ({ id, type }) => {
  if (type === 'FREELANCER') router.push({ name: 'FreelancerDetail', params: { id } })
  else router.push({ name: 'EmployerDetail', params: { id } })
  userDetailModal.value = null
}

const reviewDoc = async (doc, newStatus) => {
  const endpoint = doc._type === 'fl'
    ? `${API_BASE}/fl-documents/${doc.id}`
    : `${API_BASE}/em-documents/${doc.id}`
  try {
    const res = await fetch(endpoint, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus, reviewed_by: localStorage.getItem('admin_id') || '' })
    })
    const data = await res.json()
    if (data.status === 'updated') {
      doc.status = newStatus
      doc.reviewed = formatDateTime(new Date().toISOString())
      // Sync raw doc list
      if (doc._type === 'fl') {
        const raw = flDocs.value.find(d => d.fl_doc_id === doc.id)
        if (raw) raw.fl_doc_status = newStatus
      } else {
        const raw = emDocs.value.find(d => d.em_doc_id === doc.id)
        if (raw) raw.em_doc_status = newStatus
      }
      // Reload list to reflect status change
      pageCache.clear(); inFlight.clear()
      await loadUsers(currentPage.value)
    }
  } catch (e) {
    console.error('Failed to review doc:', e)
  }
}

const switchTab = async (tab) => {
  activeTab.value = tab
  search.value = ''
  statusFilter.value = 'PENDING'
  nameSort.value = ''
  dateSort.value = ''
  sortField.value = tab === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
  sortOrder.value = 'asc'
  pageCache.clear(); inFlight.clear()
  await loadUsers(1)
}

onUnmounted(() => document.removeEventListener('click', handleOutsideClick))
onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  await loadUsers()
})
</script>