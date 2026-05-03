<template>
  <div>
    <h1 class="title">Jobs Management</h1>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search job title..." class="search-input" />
      <div class="filter-group">
        <select v-model="yearFilter" class="filter-select">
          <option value="All">All Years</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
        <select v-model="monthFilter" class="filter-select">
          <option value="All">All Months</option>
          <option value="01">January</option>
          <option value="02">February</option>
          <option value="03">March</option>
          <option value="04">April</option>
          <option value="05">May</option>
          <option value="06">June</option>
          <option value="07">July</option>
          <option value="08">August</option>
          <option value="09">September</option>
          <option value="10">October</option>
          <option value="11">November</option>
          <option value="12">December</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width:28%">
              JOB TITLE
              <button class="col-filter-btn" :class="{ active: titleSort !== '' }" @click.stop="toggleTitleDropdown($event)">
                {{ titleSort === 'asc' ? 'A→Z ▼' : titleSort === 'desc' ? 'Z→A ▼' : 'All ▼' }}
              </button>
            </th>
            <th style="width:16%">
              COMPANY
              <button class="col-filter-btn" :class="{ active: companySort !== '' }" @click.stop="toggleCompanyDropdown($event)">
                {{ companySort === 'asc' ? 'A→Z ▼' : companySort === 'desc' ? 'Z→A ▼' : 'All ▼' }}
              </button>
            </th>
            <th style="width:10%">
              PRICE
              <button class="col-filter-btn" :class="{ active: priceSort !== '' }" @click.stop="togglePriceDropdown($event)">
                {{ priceSort === 'asc' ? '↑ ▼' : priceSort === 'desc' ? '↓ ▼' : 'All ▼' }}
              </button>
            </th>
            <th style="width:10%">
              STATUS
              <button class="col-filter-btn" :class="{ active: statusFilter !== 'All' }" @click.stop="toggleStatusDropdown($event)">
                {{ statusFilter === 'All' ? 'All ▼' : statusFilter + ' ▼' }}
              </button>
            </th>
            <th style="width:12%">ACTION</th>
            <th style="width:16%">
              LAST UPDATED
              <button class="col-filter-btn" :class="{ active: dateSort !== '' }" @click.stop="toggleDateDropdown($event)">
                {{ dateSort === 'desc' ? 'Latest ▼' : dateSort === 'asc' ? 'Oldest ▼' : 'All ▼' }}
              </button>
              <button v-if="titleSort || companySort || priceSort || statusFilter !== 'All' || dateSort" class="reset-btn" @click="resetAllFilters">Reset</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in filteredJobs" :key="job.job_id">
            <td class="truncate-cell">
              <span class="clickable-title" @click="openJobModal(job)" :title="job.job_title">
                {{ job.job_title }}
              </span>
            </td>
            <td class="truncate-cell">
              <span class="clickable-company" @click="openCompanyModal(job)" :title="job.company">
                {{ job.company }}
              </span>
            </td>
            <td>{{ job.job_price ? '฿' + Number(job.job_price).toLocaleString() : '-' }}</td>
            <td>
              <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewJob(job.job_id)">View</button>
                <button class="btn-action delete" @click="deleteJob(job.job_id)">Delete</button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
          <tr v-if="filteredJobs.length === 0">
            <td colspan="6" class="empty">No jobs found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdowns -->
    <div v-if="showTitleDropdown" class="col-dropdown" :style="titleDropdownStyle">
      <button class="col-dropdown-item" @click="setTitleSort('')">All</button>
      <button class="col-dropdown-item" @click="setTitleSort('asc')">A → Z</button>
      <button class="col-dropdown-item" @click="setTitleSort('desc')">Z → A</button>
    </div>

    <div v-if="showCompanyDropdown" class="col-dropdown" :style="companyDropdownStyle">
      <button class="col-dropdown-item" @click="setCompanySort('')">All</button>
      <button class="col-dropdown-item" @click="setCompanySort('asc')">A → Z</button>
      <button class="col-dropdown-item" @click="setCompanySort('desc')">Z → A</button>
    </div>

    <div v-if="showPriceDropdown" class="col-dropdown" :style="priceDropdownStyle">
      <button class="col-dropdown-item" @click="setPriceSort('')">All</button>
      <button class="col-dropdown-item" @click="setPriceSort('asc')">Low → High</button>
      <button class="col-dropdown-item" @click="setPriceSort('desc')">High → Low</button>
    </div>

    <div v-if="showStatusDropdown" class="col-dropdown" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setStatusFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setStatusFilter('OPEN')">Open</button>
      <button class="col-dropdown-item" @click="setStatusFilter('MATCHING')">Matching</button>
      <button class="col-dropdown-item" @click="setStatusFilter('SELECTED')">Selected</button>
      <button class="col-dropdown-item" @click="setStatusFilter('IN_PROGRESS')">In Progress</button>
      <button class="col-dropdown-item" @click="setStatusFilter('COMPLETED')">Completed</button>
      <button class="col-dropdown-item" @click="setStatusFilter('CANCELLED')">Cancelled</button>
    </div>

    <div v-if="showDateDropdown" class="col-dropdown" :style="dateDropdownStyle">
      <button class="col-dropdown-item" @click="setDateSort('')">All</button>
      <button class="col-dropdown-item" @click="setDateSort('desc')">Latest</button>
      <button class="col-dropdown-item" @click="setDateSort('asc')">Oldest</button>
    </div>

    <!-- Job Modal -->
    <div v-if="jobModal" class="modal-overlay" @click.self="jobModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content:space-between;">
          <h3 class="mini-modal-title">{{ jobModal.job_title }}</h3>
          <button class="close-btn" @click="jobModal = null">✕</button>
        </div>
        <p v-if="jobModal.job_description" class="mini-desc">{{ jobModal.job_description }}</p>
        <div class="mini-grid">
          <div class="mini-item"><label>Status</label>
            <span class="badge" :class="jobModal.job_status?.toLowerCase()">{{ jobModal.job_status }}</span>
          </div>
          <div class="mini-item"><label>Price</label>
            <span>{{ jobModal.job_price ? '฿' + Number(jobModal.job_price).toLocaleString() : '-' }}</span>
          </div>
          <div class="mini-item"><label>Company</label>
            <span>{{ jobModal.company || '-' }}</span>
          </div>
          <div class="mini-item"><label>Freelancer</label>
            <span>{{ jobModal.selected_fl_id || '-' }}</span>
          </div>
          <div class="mini-item"><label>Job Start</label>
            <span>{{ formatDate(jobModal.job_start_date) }}</span>
          </div>
          <div class="mini-item"><label>Job End</label>
            <span>{{ formatDate(jobModal.job_end_date) }}</span>
          </div>
          <div class="mini-item"><label>Vehicle</label>
            <span>{{ jobModal.job_required_vehicle_type || '-' }}</span>
          </div>
          <div class="mini-item"><label>Seats</label>
            <span>{{ jobModal.job_required_seat || '-' }}</span>
          </div>
          <div class="mini-item"><label>Created</label>
            <span class="text-muted">{{ formatDateTime(jobModal.job_created_at) }}</span>
          </div>
          <div class="mini-item"><label>Last Updated</label>
            <span class="text-muted">{{ formatDateTime(jobModal.job_updated_at) }}</span>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="viewJob(jobModal.job_id); jobModal = null">View Full Detail →</button>
        </div>
      </div>
    </div>

    <!-- Company Modal -->
    <div v-if="companyModal" class="modal-overlay" @click.self="companyModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px;">
          <button class="close-btn" @click="companyModal = null">✕</button>
        </div>
        <div class="profile-hero">
          <div class="profile-avatar em">
            <img v-if="companyModal.em_profile_image_url" :src="companyModal.em_profile_image_url" class="avatar-img" />
            <span v-else class="avatar-initial">{{ companyModal.em_name?.[0] || '?' }}</span>
          </div>
          <div class="profile-info">
            <h3 class="profile-name">{{ companyModal.em_name }}</h3>
            <p class="profile-bio" :class="{ muted: !companyModal.em_bio }">
              {{ companyModal.em_bio || 'No bio' }}
            </p>
          </div>
        </div>
        <div class="mini-grid">
          <div class="mini-item"><label>Status</label>
            <span class="badge" :class="companyModal.em_verify_status?.toLowerCase()">{{ companyModal.em_verify_status }}</span>
          </div>
          <div class="mini-item"><label>Active</label>
            <span>{{ companyModal.em_is_active ? '✅ Active' : '❌ Inactive' }}</span>
          </div>
          <div class="mini-item"><label>Phone</label>
            <span>{{ companyModal.em_phone || '-' }}</span>
          </div>
          <div class="mini-item"><label>Rating</label>
            <span>⭐ {{ companyModal.em_rating_avg ?? '-' }}</span>
          </div>
          <div class="mini-item"><label>Address</label>
            <span>{{ companyModal.em_address || '-' }}</span>
          </div>
          <div class="mini-item"><label>Created</label>
            <span class="text-muted">{{ formatDateTime(companyModal.em_created_at) }}</span>
          </div>
          <div class="mini-item"><label>Last Updated</label>
            <span class="text-muted">{{ formatDateTime(companyModal.em_updated_at) }}</span>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="router.push({ name: 'EmployerDetail', params: { id: companyModal.em_id } }); companyModal = null">View Full Detail →</button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="mini-modal" style="text-align:center; padding:32px;">
        <div style="font-size:36px; margin-bottom:12px;">🗑</div>
        <h3 style="margin:0 0 12px;">Delete Job</h3>
        <p style="color:#555; margin:0 0 8px; line-height:1.5;">Are you sure you want to delete<br><strong>"{{ deleteTargetTitle }}"</strong>?</p>
        <p style="font-size:12px; color:#dc3545; margin-bottom:24px;">This action cannot be undone.</p>
        <div style="display:flex; justify-content:center; gap:12px;">
          <button class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-confirm-delete" @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const router = useRouter()
const search = ref('')
const statusFilter = ref(localStorage.getItem('jobs_statusFilter') || 'All')
const monthFilter = ref('All')
const yearFilter = ref('All')

const titleSort = ref(localStorage.getItem('jobs_titleSort') || '')
const companySort = ref(localStorage.getItem('jobs_companySort') || '')
const priceSort = ref(localStorage.getItem('jobs_priceSort') || '')
const dateSort = ref(localStorage.getItem('jobs_dateSort') || '')

const showTitleDropdown = ref(false)
const showCompanyDropdown = ref(false)
const showPriceDropdown = ref(false)
const showStatusDropdown = ref(false)
const showDateDropdown = ref(false)

const titleDropdownStyle = ref({})
const companyDropdownStyle = ref({})
const priceDropdownStyle = ref({})
const statusDropdownStyle = ref({})
const dateDropdownStyle = ref({})

const saveFilters = () => {
  localStorage.setItem('jobs_titleSort', titleSort.value)
  localStorage.setItem('jobs_companySort', companySort.value)
  localStorage.setItem('jobs_priceSort', priceSort.value)
  localStorage.setItem('jobs_statusFilter', statusFilter.value)
  localStorage.setItem('jobs_dateSort', dateSort.value)
}

const jobs = ref([])
const allEmployers = ref([])
const showDeleteModal = ref(false)
const deleteTargetId = ref(null)
const deleteTargetTitle = ref('')
const jobModal = ref(null)
const companyModal = ref(null)

const currentYear = new Date().getFullYear()
const years = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i)

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const filteredJobs = computed(() => {
  let result = jobs.value.filter(job => {
    const matchSearch = (job.job_title || '').toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === 'All' || job.job_status === statusFilter.value
    const d = job.job_start_date ? new Date(job.job_start_date) : null
    const matchYear = yearFilter.value === 'All' || (d && String(d.getFullYear()) === String(yearFilter.value))
    const matchMonth = monthFilter.value === 'All' || (d && String(d.getMonth() + 1).padStart(2, '0') === monthFilter.value)
    return matchSearch && matchStatus && matchYear && matchMonth
  })

  if (titleSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.job_title || '').localeCompare(b.job_title || '')
      return titleSort.value === 'desc' ? -cmp : cmp
    })
  }

  if (companySort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.company || '').localeCompare(b.company || '')
      return companySort.value === 'desc' ? -cmp : cmp
    })
  }

  if (priceSort.value) {
    result = [...result].sort((a, b) => {
      const priceA = Number(a.job_price) || 0
      const priceB = Number(b.job_price) || 0
      return priceSort.value === 'desc' ? priceB - priceA : priceA - priceB
    })
  }

  if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.job_updated_at) || 0
      const dateB = new Date(b.job_updated_at) || 0
      return dateSort.value === 'desc' ? dateB - dateA : dateA - dateB
    })
  } else {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.job_updated_at) || 0
      const dateB = new Date(b.job_updated_at) || 0
      return dateB - dateA
    })
  }

  return result
})

const toggleTitleDropdown = (e) => {
  closeAllDropdowns()
  showTitleDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  titleDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setTitleSort = (val) => { titleSort.value = val; showTitleDropdown.value = false; saveFilters() }

const toggleCompanyDropdown = (e) => {
  closeAllDropdowns()
  showCompanyDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  companyDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setCompanySort = (val) => { companySort.value = val; showCompanyDropdown.value = false; saveFilters() }

const togglePriceDropdown = (e) => {
  closeAllDropdowns()
  showPriceDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  priceDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setPriceSort = (val) => { priceSort.value = val; showPriceDropdown.value = false; saveFilters() }

const toggleStatusDropdown = (e) => {
  closeAllDropdowns()
  showStatusDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  statusDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setStatusFilter = (val) => { statusFilter.value = val; showStatusDropdown.value = false; saveFilters() }

const toggleDateDropdown = (e) => {
  closeAllDropdowns()
  showDateDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  dateDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setDateSort = (val) => { dateSort.value = val; showDateDropdown.value = false; saveFilters() }

const closeAllDropdowns = () => {
  showTitleDropdown.value = false
  showCompanyDropdown.value = false
  showPriceDropdown.value = false
  showStatusDropdown.value = false
  showDateDropdown.value = false
}

const resetAllFilters = () => {
  titleSort.value = ''
  companySort.value = ''
  priceSort.value = ''
  statusFilter.value = 'All'
  dateSort.value = ''
  saveFilters()
}

const handleOutsideClick = (e) => {
  if (!e.target.closest('.col-dropdown') && !e.target.closest('.col-filter-btn')) {
    closeAllDropdowns()
  }
}

const viewJob = (id) => router.push({ name: 'JobDetail', params: { id } })

const openJobModal = (job) => { jobModal.value = job }

const openCompanyModal = (job) => {
  const em = allEmployers.value.find(e => e.em_id === job.em_id)
  companyModal.value = em || { em_name: job.company }
}

const deleteJob = (id) => {
  deleteTargetId.value = id
  deleteTargetTitle.value = jobs.value.find(j => j.job_id === id)?.job_title || id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await fetch(`${API_BASE}/jobs/${deleteTargetId.value}`, { method: 'DELETE' })
    jobs.value = jobs.value.filter(j => j.job_id !== deleteTargetId.value)
  } catch (e) {
    console.error('Failed to delete job:', e)
  } finally {
    showDeleteModal.value = false
    deleteTargetId.value = null
    deleteTargetTitle.value = ''
  }
}

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  try {
    const [jobsRes, emRes] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`)
    ])
    const [jobsData, emData] = await Promise.all([jobsRes.json(), emRes.json()])
    jobs.value = jobsData.items || []
    allEmployers.value = emData.items || []
  } catch (e) {
    console.error('Failed to load jobs:', e)
  }
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin: 0 0 24px -24px;
  background: #1a1a2e;
  padding: 24px 40px;
  color: white;
}

.filter-row {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 16px;
}
.filter-group { display: flex; gap: 8px; }
.search-input {
  padding: 10px 14px; border: 1px solid #ddd;
  border-radius: 6px; width: 280px; font-size: 14px;
}
.filter-select {
  padding: 10px 14px; border: 1px solid #ddd;
  border-radius: 6px; font-size: 14px;
}

.table-container { background: white; border-radius: 8px; overflow: hidden; }
.table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.table th, .table td {
  padding: 12px 14px; text-align: left;
  border-bottom: 1px solid #eee; overflow: hidden;
}
.table th { font-size: 12px; color: #666; font-weight: 600; background: #f9f9f9; position: relative; }

.col-filter-btn {
  margin-left: 8px; padding: 4px 10px; border: 1px solid #ccc;
  border-radius: 20px; font-size: 11px; background: transparent; color: #666;
  cursor: pointer; font-weight: 500;
}
.col-filter-btn:hover { border-color: #06C755; color: #06C755; }
.col-filter-btn.active { border-color: #06C755; color: #06C755; font-weight: 600; }

.reset-btn {
  margin-left: 6px; padding: 4px 8px; border: none;
  border-radius: 4px; font-size: 10px; background: #ffebee;
  color: #c62828; cursor: pointer; font-weight: 500;
}
.reset-btn:hover { background: #ffcdd2; }

.col-dropdown {
  background: white; border: 1px solid #ddd; border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 50; min-width: 120px;
}
.col-dropdown-item {
  display: block; width: 100%; padding: 8px 14px; border: none;
  background: none; text-align: left; font-size: 13px; cursor: pointer;
}
.col-dropdown-item:hover { background: #f5f5f5; }
.col-dropdown-item:first-child { border-radius: 6px 6px 0 0; }
.col-dropdown-item:last-child { border-radius: 0 0 6px 6px; }

.truncate-cell { max-width: 0; }
.clickable-title {
  display: block; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; cursor: pointer; color: #0066cc; font-size: 14px;
}
.clickable-title:hover { text-decoration: underline; }
.clickable-company {
  display: block; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; cursor: pointer; color: #0066cc; font-size: 13px;
}

.badge {
  display: inline-flex; padding: 3px 10px;
  border-radius: 12px; font-size: 11px; font-weight: 600; width: fit-content;
}
.badge.open { background: #e3f2fd; color: #1976d2; }
.badge.matching { background: #e0f2f1; color: #00695c; }
.badge.selected { background: #f3e5f5; color: #7b1fa2; }
.badge.in_progress { background: #fff3e0; color: #f57c00; }
.badge.completed { background: #f5f5f5; color: #666; }
.badge.cancelled { background: #ffebee; color: #c62828; }
.badge.pending { background: #fff3e0; color: #f57c00; }
.badge.verified { background: #e8f5e9; color: #2e7d32; }
.badge.not_verified { background: #ffebee; color: #c62828; }

.action-btns { display: flex; gap: 6px; }
.btn-action {
  padding: 4px 10px; border-radius: 5px; border: none;
  font-size: 12px; cursor: pointer; font-weight: 500;
}
.btn-action.view { background: #e3f2fd; color: #1976d2; }
.btn-action.view:hover { background: #bbdefb; }
.btn-action.delete { background: #ffebee; color: #c62828; }
.btn-action.delete:hover { background: #ffcdd2; }

.text-muted { color: #999; font-size: 12px; }
.empty { text-align: center; color: #999; padding: 32px; }

.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.mini-modal {
  background: white; border-radius: 12px; padding: 24px;
  width: 460px; max-height: 80vh; overflow-y: auto;
}
.mini-modal-header {
  display: flex; align-items: flex-start; margin-bottom: 16px;
}
.mini-modal-title {
  font-size: 16px; font-weight: 600; color: #111;
  margin: 0; flex: 1; padding-right: 12px;
}
.close-btn {
  background: none; border: none; font-size: 16px;
  cursor: pointer; color: #888; flex-shrink: 0;
}
.mini-desc {
  font-size: 13px; color: #666; line-height: 1.6;
  margin: 0 0 16px; padding-bottom: 16px; border-bottom: 1px solid #eee;
}
.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.mini-item { display: flex; flex-direction: column; gap: 3px; }
.mini-item label { font-size: 10px; color: #999; font-weight: 600; text-transform: uppercase; }
.mini-item span { font-size: 13px; color: #222; }
.mini-modal-footer {
  margin-top: 20px; padding-top: 16px; border-top: 1px solid #eee;
  display: flex; justify-content: flex-end;
}
.btn-full-view {
  background: none; border: none; color: #0066cc;
  font-size: 13px; cursor: pointer; font-weight: 500;
}
.btn-full-view:hover { text-decoration: underline; }

.profile-hero {
  display: flex; align-items: flex-start; gap: 14px;
  margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eee;
}
.profile-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; overflow: hidden;
}
.profile-avatar.em { background: #f3e5f5; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.avatar-initial { font-size: 22px; font-weight: 700; color: #555; }
.profile-info { flex: 1; min-width: 0; }
.profile-name { font-size: 16px; font-weight: 600; margin: 0 0 4px; color: #111; }
.profile-bio {
  font-size: 12px; color: #666; margin: 0; line-height: 1.5;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.profile-bio.muted { color: #bbb; font-style: italic; }

.btn-cancel {
  padding: 10px 24px; border: 1px solid #ddd;
  border-radius: 6px; background: white; cursor: pointer; font-size: 14px;
}
.btn-confirm-delete {
  padding: 10px 24px; border: none; border-radius: 6px;
  background: #dc3545; color: white; cursor: pointer; font-size: 14px;
}
.btn-confirm-delete:hover { background: #b02a37; }
</style>