<template>
  <div>
    <BreadcrumbBar />

    <div class="tabs-wide">
      <button class="tab" :class="{ active: activeTab === 'Freelancer' }" @click="switchTab('Freelancer')">Freelancer</button>
      <button class="tab" :class="{ active: activeTab === 'Employer' }" @click="switchTab('Employer')">Employer</button>
    </div>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search name..." class="search-input" @input="onSearch" />
    </div>

    <div class="table-container overflow-x-auto touch-pan-x">
      <table class="table users-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width: 16%" @click="cycleSort('name')">
              <span class="th-inner">NAME
                <span class="sort-label">
                  <span v-if="!nameSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="nameSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': ratingSort }" style="width: 12%" @click="cycleSort('rating')">
              <span class="th-inner">RATING
                <span class="sort-label">
                  <span v-if="!ratingSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="ratingSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': jobsSort }" style="width: 15%" @click="cycleSort('jobs')">
              <span class="th-inner">JOBS
                <span class="sort-label">
                  <span v-if="!jobsSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="jobsSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th style="width: 16%">
              <span class="inline-flex items-center whitespace-nowrap gap-1">STATUS
                <button class="col-filter-btn" :class="{ active: verifyFilter !== 'All' }" @click.stop="toggleStatusDropdown($event)">
                  {{ verifyFilter === 'All' ? 'All ▼' : verifyFilter === 'NOT_VERIFIED' ? 'NOT VERIF. ▼' : verifyFilter + ' ▼' }}
                </button>
              </span>
            </th>
            <th style="width:11%" class="text-center">ACTION</th>
            <th class="th-sortable relative" :class="{ 'th-active': dateSort }" style="width:16%" @click="cycleSort('date')">
              <span class="th-inner">LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button v-if="nameSort || ratingSort || verifyFilter !== 'All' || dateSort || jobsSort || search"
                class="reset-btn ml-1.5 absolute right-3 top-1/2 -translate-y-1/2" @click.stop="resetAllFilters">✕ Reset</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-'+i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:65%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:40%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:40%"></span></td>
              <td><span class="skeleton skeleton-badge"></span></td>
              <td><div class="action-btns"><span class="skeleton skeleton-btn"></span><span class="skeleton skeleton-btn"></span></div></td>
              <td><span class="skeleton skeleton-text" style="width:80%"></span></td>
            </tr>
          </template>
          <tr v-else-if="!isLoading && sortedUsers.length === 0">
            <td colspan="6" class="text-center text-muted py-6">No results found</td>
          </tr>
          <tr v-for="user in sortedUsers" :key="user.id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openUserModal(user)">
              <div class="user-cell">
                <UserAvatar :id="user.id" :name="user.name" :image-url="user.imageUrl" :size="28" />
                <span :title="user.name">{{ user.name }}</span>
              </div>
            </td>
            <td>
              <div style="display:inline-flex;align-items:center;gap:4px;">
                {{ Number(user.rating || 0).toFixed(1) }}
                <svg style="width:16px;height:16px;color:#f9a825;" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
              </div>
            </td>
            <td>{{ jobsDoneById[user.id] || 0 }}</td>
            <td><span class="badge" :class="user.verifyStatus?.toLowerCase()">{{ formatVerifyStatus(user.verifyStatus) }}</span></td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewUser(user)">View</button>
                <button class="btn-action" :class="user.isActive ? 'ban' : 'unban'" @click="openBanModal(user)">
                  {{ user.isActive ? 'Ban' : 'Unban' }}
                </button>
              </div>
            </td>
            <td class="text-muted text-[13px]">{{ formatDateTime(user.updatedAt) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <PaginationBar :page="currentPage" :has-more="hasMore" :has-items="sortedUsers.length > 0"
      @prev="loadUsers(currentPage - 1)" @next="loadUsers(currentPage + 1)" />

    <!-- Column Filter Dropdown -->
    <div v-if="showStatusDropdown" class="col-dropdown" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setVerifyFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setVerifyFilter('VERIFIED')">Verified</button>
      <button class="col-dropdown-item" @click="setVerifyFilter('PENDING')">Pending</button>
      <button class="col-dropdown-item" @click="setVerifyFilter('NOT_VERIFIED')">Not Verified</button>
    </div>

    <!-- Ban Modal -->
    <BanModal :show="showBanModal" :is-active="banTarget?.isActive" :name="banTarget?.name"
      :user-type="activeTab === 'Employer' ? 'Employer' : 'Freelancer'"
      @confirm="confirmBan" @cancel="showBanModal = false" />

    <!-- User Modal -->
    <UserMiniModal :data="userModalMapped" :type="activeTab === 'Employer' ? 'EMPLOYER' : 'FREELANCER'"
      @close="userModal = null" @view-detail="goToFullDetail" />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime } from '../utils/formatDate'
import UserMiniModal from '../components/UserMiniModal.vue'
import BanModal from '../components/BanModal.vue'
import UserAvatar from '../components/UserAvatar.vue'
import PaginationBar from '../components/PaginationBar.vue'
import { API_BASE } from '../data/api'
import { formatVerifyStatus } from '../utils/statusClasses'

const router = useRouter()
defineOptions({ name: 'UsersView' })
const { avatarStyle, initials2 } = useAvatar()

const activeTab = ref('Freelancer')
const isLoading = ref(false)
const employers = ref([])
const freelancers = ref([])
const jobs = ref([])
const search = ref('')
const userModal = ref(null)
const showBanModal = ref(false)
const banTarget = ref(null)
const jobsDoneByFreelancer = ref({})
const jobsDoneByEmployer = ref({})

const currentPage = ref(1)
const pageSize = 10
const hasMore = ref(false)
const pageCache = new Map()
const inFlight = new Map()

const nameSort = ref('')
const ratingSort = ref('')
const verifyFilter = ref('All')
const dateSort = ref('')
const jobsSort = ref('')
// API sort params
const sortField = ref('fl_updated_at')
const sortOrder = ref('desc')

const SORT_FIELD_MAP = {
  Freelancer: { name: 'fl_name', rating: 'fl_rating_avg', date: 'fl_updated_at' },
  Employer:   { name: 'em_name', rating: 'em_rating_avg', date: 'em_updated_at' },
}
const showStatusDropdown = ref(false)
const statusDropdownStyle = ref({})

const getCacheKey = (page) =>
  `${activeTab.value}_${page}_${verifyFilter.value}_${search.value}_${sortField.value}_${sortOrder.value}`

// Debounce search → query API
let searchTimer = null
const onSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { pageCache.clear(); loadUsers(1) }, 300)
}

const cycleSort = (key) => {
  const map = { name: nameSort, rating: ratingSort, date: dateSort, jobs: jobsSort }
  const current = map[key]
  const next = current.value === '' ? 'asc' : current.value === 'asc' ? 'desc' : ''
  nameSort.value = ratingSort.value = dateSort.value = jobsSort.value = ''
  current.value = next

  if (key !== 'jobs' && next !== '') {
    sortField.value = SORT_FIELD_MAP[activeTab.value][key]
    sortOrder.value = next
    pageCache.clear(); inFlight.clear()
    loadUsers(1)
  } else if (next === '') {
    sortField.value = activeTab.value === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
    sortOrder.value = 'desc'
    pageCache.clear(); inFlight.clear()
    loadUsers(1)
  }
}

const toggleStatusDropdown = (e) => {
  showStatusDropdown.value = !showStatusDropdown.value
  const rect = e.target.getBoundingClientRect()
  statusDropdownStyle.value = { position: 'fixed', top: rect.bottom + window.scrollY + 'px', left: rect.left + 'px' }
}

const setVerifyFilter = (val) => {
  verifyFilter.value = val
  showStatusDropdown.value = false
  pageCache.clear(); inFlight.clear()
  loadUsers(1)
}

const resetAllFilters = () => {
  nameSort.value = ratingSort.value = dateSort.value = jobsSort.value = ''
  verifyFilter.value = 'All'
  search.value = ''
  sortField.value = activeTab.value === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
  sortOrder.value = 'desc'
  pageCache.clear(); inFlight.clear()
  loadUsers(1)
}

const handleOutsideClick = (e) => {
  if (!e.target.closest('.col-dropdown') && !e.target.closest('.col-filter-btn')) {
    showStatusDropdown.value = false
  }
}

async function fetchPage(page) {
  const key = getCacheKey(page)
  if (pageCache.has(key)) return pageCache.get(key)
  if (inFlight.has(key)) return inFlight.get(key)
  const offset = (page - 1) * pageSize
  const statusParam = verifyFilter.value !== 'All' ? `&status=${verifyFilter.value}` : ''
  const searchParam = search.value ? `&search=${encodeURIComponent(search.value)}` : ''
  const base = activeTab.value === 'Employer' ? '/admin/employers' : '/admin/freelancers'
  const promise = fetch(`${API_BASE}${base}?limit=${pageSize+1}&offset=${offset}${statusParam}${searchParam}&sort_by=${sortField.value}&sort_order=${sortOrder.value}`)
    .then(r => r.json())
    .then(data => {
      const result = { allItems: data.items || [] }
      pageCache.set(key, result)
      inFlight.delete(key)
      return result
    })
    .catch(err => { inFlight.delete(key); throw err })
  inFlight.set(key, promise)
  return promise
}

async function loadUsers(page = 1) {
  if (activeTab.value === 'Employer') employers.value = []
  else freelancers.value = []
  isLoading.value = true
  currentPage.value = page
  try {
    const { allItems } = await fetchPage(page)
    hasMore.value = allItems.length > pageSize
    const items = allItems.slice(0, pageSize)

    if (activeTab.value === 'Employer') {
      employers.value = items.map(e => ({
        id: e.em_id, name: e.em_name || e.em_username || e.em_id,
        verifyStatus: e.em_verify_status || 'UNKNOWN',
        isActive: !!e.em_is_active, rating: Number(e.em_rating_avg || 0),
        imageUrl: e.em_profile_image_url || '', createdAt: e.em_created_at || '',
        updatedAt: e.em_updated_at || '', username: e.em_username || '',
        email: e.em_email || '', phone: e.em_phone || '',
        address: e.em_address || '', bio: e.em_bio || '',
      }))
    } else {
      freelancers.value = items.map(f => ({
        id: f.fl_id, name: f.fl_name || f.fl_id,
        verifyStatus: f.fl_verify_status || 'UNKNOWN',
        isActive: !!f.fl_is_active, rating: Number(f.fl_rating_avg || 0),
        imageUrl: f.fl_profile_image_url || '', createdAt: f.fl_created_at || '',
        updatedAt: f.fl_updated_at || '', username: f.fl_username || '',
        email: f.fl_email || '', phone: f.fl_phone || '',
        address: f.fl_address || '', bio: f.fl_bio || '',
        dateOfBirth: f.fl_date_of_birth || '',
      }))
    }

    if (hasMore.value) fetchPage(page + 1).catch(() => {})
  } catch (e) {
    console.error('Failed to load users:', e)
  } finally {
    isLoading.value = false
  }
}

async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/jobs?limit=50`)
    const data = await res.json()
    jobs.value = data.items || []
    const flMap = {}, emMap = {}
    for (const j of jobs.value) {
      if (j.selected_fl_id) flMap[j.selected_fl_id] = (flMap[j.selected_fl_id] || 0) + 1
      if (j.em_id) emMap[j.em_id] = (emMap[j.em_id] || 0) + 1
    }
    jobsDoneByFreelancer.value = flMap
    jobsDoneByEmployer.value = emMap
  } catch (e) {
    console.error('Failed to load jobs:', e)
    jobs.value = []
  }
}

const jobsDoneById = computed(() =>
  activeTab.value === 'Employer' ? jobsDoneByEmployer.value : jobsDoneByFreelancer.value
)

const currentList = computed(() =>
  activeTab.value === 'Employer' ? employers.value : freelancers.value
)

const sortedUsers = computed(() => {
  let result = [...currentList.value]

  if (jobsSort.value) {
    result.sort((a, b) => {
      const ja = jobsDoneById.value[a.id] || 0, jb = jobsDoneById.value[b.id] || 0
      return jobsSort.value === 'desc' ? jb - ja : ja - jb
    })
  }
  return result
})

const openUserModal = async (user) => {
  userModal.value = user

  if (jobs.value.length === 0) await loadJobs()
}
const viewUser = (user) => {
  const route = activeTab.value === 'Employer'
    ? { name: 'EmployerDetail', params: { id: user.id }, state: { parent: 'Users', parentTo: '/users', userName: user.name } }
    : { name: 'FreelancerDetail', params: { id: user.id }, state: { parent: 'Users', parentTo: '/users', userName: user.name } }
  router.push(route)
}

const userModalMapped = computed(() => {
  if (!userModal.value) return null
  const u = userModal.value
  if (activeTab.value === 'Employer') {
    return {
      em_id: u.id, em_name: u.name, em_bio: u.bio,
      em_profile_image_url: u.imageUrl, em_verify_status: u.verifyStatus,
      em_is_active: u.isActive, em_rating_avg: u.rating,
      em_created_at: u.createdAt, em_updated_at: u.updatedAt,
      em_username: u.username, em_email: u.email, em_phone: u.phone, em_address: u.address,
    }
  }
  return {
    fl_id: u.id, fl_name: u.name, fl_bio: u.bio,
    fl_profile_image_url: u.imageUrl, fl_verify_status: u.verifyStatus,
    fl_is_active: u.isActive, fl_rating_avg: u.rating,
    fl_created_at: u.createdAt, fl_updated_at: u.updatedAt,
    fl_username: u.username, fl_email: u.email, fl_phone: u.phone, fl_address: u.address,
    fl_date_of_birth: u.dateOfBirth,
  }
})

const goToFullDetail = () => {
  if (!userModal.value) return
  const route = activeTab.value === 'Employer'
    ? { name: 'EmployerDetail', params: { id: userModal.value.id } }
    : { name: 'FreelancerDetail', params: { id: userModal.value.id } }
  router.push(route)
  userModal.value = null
}

const openBanModal = (user) => { banTarget.value = user; showBanModal.value = true }
const confirmBan = async () => {
  const user = banTarget.value
  const endpoint = activeTab.value === 'Freelancer'
    ? `${API_BASE}/freelancers/${user.id}/ban`
    : `${API_BASE}/employers/${user.id}/ban`
  try {
    const res = await fetch(endpoint, {
      method: 'PATCH', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ is_active: !user.isActive, admin_id: localStorage.getItem('admin_id') || '' })
    })
    const data = await res.json()
    if (data.status === 'updated') {
      user.isActive = !user.isActive
      pageCache.clear(); inFlight.clear()
      await loadUsers(currentPage.value)
    }
  } catch (e) {
    console.error('Failed to ban/unban:', e)
  } finally {
    showBanModal.value = false
    banTarget.value = null
  }
}

const switchTab = async (tab) => {
  activeTab.value = tab
  search.value = ''
  verifyFilter.value = 'All'
  nameSort.value = ratingSort.value = dateSort.value = jobsSort.value = ''
  sortField.value = tab === 'Employer' ? 'em_updated_at' : 'fl_updated_at'
  sortOrder.value = 'desc'
  pageCache.clear(); inFlight.clear()
  await loadUsers(1)
}

onUnmounted(() => document.removeEventListener('click', handleOutsideClick))

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  await loadUsers()
})
</script>