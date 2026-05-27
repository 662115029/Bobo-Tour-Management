<template>
  <div>
    <BreadcrumbBar />

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search job title..." class="search-input" @input="onSearchInput" />
      <div class="filter-group">
        <SelectDropdown v-model="yearFilter" :options="years.map(y => ({ label: String(y), value: y }))" @change="fetchJobs" />
        <SelectDropdown v-model="monthFilter" :options="monthOptions" @change="fetchJobs" />
      </div>
    </div>

    <div class="table-container">
      <table class="table jobs-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': titleSort }" style="width: 20%" @click="cycleSort('title')">
              <span class="th-inner">JOB TITLE
                <span class="sort-label">
                  <span v-if="!titleSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="titleSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': companySort }" style="width: 16%" @click="cycleSort('company')">
              <span class="th-inner">COMPANY
                <span class="sort-label">
                  <span v-if="!companySort" class="sort-label-dim">⇅</span>
                  <span v-else-if="companySort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': priceSort }" style="width: 10%" @click="cycleSort('price')">
              <span class="th-inner">PRICE
                <span class="sort-label">
                  <span v-if="!priceSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="priceSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th style="width: 16%; text-align: center;">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">STATUS
                <button class="col-filter-btn" :class="{ active: statusFilter !== 'All' }"
                  @click.stop="toggleStatusDropdown($event)">
                  {{ statusFilter === "All" ? "All ▼" : formatJobStatus(statusFilter) + " ▼" }}
                </button>
              </span>
            </th>
            <th style="width: 12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button v-if="titleSort || companySort || priceSort || statusFilter !== 'All' || dateSort"
                class="reset-btn ml-1.5" @click.stop="resetAllFilters"
                style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);">
                ✕ Reset
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-' + i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:70%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:60%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:50%"></span></td>
              <td><span class="skeleton skeleton-badge"></span></td>
              <td><div class="action-btns"><span class="skeleton skeleton-btn"></span><span class="skeleton skeleton-btn"></span></div></td>
              <td><span class="skeleton skeleton-text" style="width:80%"></span></td>
            </tr>
          </template>
          <template v-else>
            <tr v-if="filteredJobs.length === 0">
              <td colspan="6" class="text-center text-muted py-6">No jobs found.</td>
            </tr>
            <tr v-for="job in filteredJobs" :key="job.job_id" class="row-hover">
              <td class="truncate-cell clickable-cell" @click="openJobModal(job)">
                <div class="user-cell">
                  <span class="user-avatar" :style="jobIconStyle(job.job_id)" style="border-radius:6px;flex-shrink:0;">
                    <svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/><path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/></svg>
                  </span>
                  {{ job.job_title }}
                </div>
              </td>
              <td class="truncate-cell clickable-cell" @click="openCompanyModal(job)">
                <div class="user-cell">
                  <span class="user-avatar" :style="avatarStyle(job.em_id, job.company)">{{ initials2(job.company) }}</span>
                  {{ job.company }}
                </div>
              </td>
              <td>{{ job.job_price ? "฿" + Number(job.job_price).toLocaleString() : "-" }}</td>
              <td style="text-align: center;">
                <span class="badge" :class="job.job_status?.toLowerCase()">{{ formatJobStatus(job.job_status) }}</span>
              </td>
              <td>
                <div class="action-btns">
                  <button class="btn-action view" @click="viewJob(job.job_id)">View</button>
                  <button class="btn-action delete" @click="deleteJob(job.job_id)">Delete</button>
                </div>
              </td>
              <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <PaginationBar :page="page" :has-more="hasMore" :has-items="filteredJobs.length > 0"
      @prev="goToPage(page - 1)" @next="goToPage(page + 1)" />

    <!-- Column Filter Dropdowns -->
    <div v-if="showStatusDropdown" class="col-dropdown" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setStatusFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setStatusFilter('OPEN')">Open</button>
      <button class="col-dropdown-item" @click="setStatusFilter('PENDING')">Pending</button>
      <button class="col-dropdown-item" @click="setStatusFilter('MATCHED')">Matched</button>
      <button class="col-dropdown-item" @click="setStatusFilter('IN_PROGRESS')">In Progress</button>
      <button class="col-dropdown-item" @click="setStatusFilter('COMPLETED')">Completed</button>
      <button class="col-dropdown-item" @click="setStatusFilter('CANCELLED')">Cancelled</button>
    </div>

    <!-- Job Modal -->
    <JobMiniModal :data="jobModal" @close="jobModal = null"
      @view-detail="(id) => { viewJob(id); jobModal = null }" />

    <!-- Company Modal -->
    <UserMiniModal :data="companyModal" type="EMPLOYER" @close="companyModal = null"
      @view-detail="({ id }) => { router.push({ name: 'EmployerDetail', params: { id } }); companyModal = null }" />

    <!-- Delete Modal -->
    <DeleteJobModal :show="showDeleteModal" :title="deleteTargetTitle"
      @confirm="confirmDelete" @cancel="showDeleteModal = false" />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from "vue"
import { useRouter } from "vue-router"
import { API_BASE } from "../data/api"
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime } from '../utils/formatDate'
import { formatJobStatus } from '../utils/statusClasses'
import JobMiniModal from '../components/JobMiniModal.vue'
import UserMiniModal from '../components/UserMiniModal.vue'
import DeleteJobModal from '../components/DeleteJobModal.vue'
import SelectDropdown from '../components/SelectDropdown.vue'
import PaginationBar from '../components/PaginationBar.vue'

const router = useRouter()
const { avatarStyle, jobIconStyle, initials2 } = useAvatar()

const now = new Date()
const currentYear = now.getFullYear()
const currentMonth = String(now.getMonth() + 1).padStart(2, '0')
const years = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i)
const monthOptions = [
  { label: 'January',   value: '01' }, { label: 'February',  value: '02' },
  { label: 'March',     value: '03' }, { label: 'April',     value: '04' },
  { label: 'May',       value: '05' }, { label: 'June',      value: '06' },
  { label: 'July',      value: '07' }, { label: 'August',    value: '08' },
  { label: 'September', value: '09' }, { label: 'October',   value: '10' },
  { label: 'November',  value: '11' }, { label: 'December',  value: '12' },
]

const search = ref("")
const statusFilter = ref(localStorage.getItem("jobs_statusFilter") || "All")
const monthFilter = ref(currentMonth)
const yearFilter = ref(currentYear)

const titleSort = ref(localStorage.getItem("jobs_titleSort") || "")
const companySort = ref(localStorage.getItem("jobs_companySort") || "")
const priceSort = ref(localStorage.getItem("jobs_priceSort") || "")
const dateSort = ref(localStorage.getItem("jobs_dateSort") || "")

const showStatusDropdown = ref(false)
const statusDropdownStyle = ref({})
const isLoading = ref(true)
const jobs = ref([])
const showDeleteModal = ref(false)
const deleteTargetId = ref(null)
const deleteTargetTitle = ref("")
const jobModal = ref(null)
const companyModal = ref(null)

const PAGE_SIZE = 10
const page = ref(1)
const totalCount = ref(0)
const hasMore = ref(false)
const totalPages = computed(() => Math.max(1, Math.ceil(totalCount.value / PAGE_SIZE)))

let searchTimer = null
const onSearchInput = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => { page.value = 1; fetchJobs() }, 400)
}

const saveFilters = () => {
  localStorage.setItem("jobs_titleSort", titleSort.value)
  localStorage.setItem("jobs_companySort", companySort.value)
  localStorage.setItem("jobs_priceSort", priceSort.value)
  localStorage.setItem("jobs_statusFilter", statusFilter.value)
  localStorage.setItem("jobs_dateSort", dateSort.value)
}

const cycleSort = (key) => {
  const current = { title: titleSort, company: companySort, price: priceSort, date: dateSort }[key]
  const next = current.value === "" ? "asc" : current.value === "asc" ? "desc" : ""
  titleSort.value = ""; companySort.value = ""; priceSort.value = ""; dateSort.value = ""
  current.value = next
  saveFilters()
  page.value = 1
  fetchJobs()
}

const fetchJobs = async () => {
  isLoading.value = true
  try {
    const params = new URLSearchParams({
      limit: PAGE_SIZE + 1,
      offset: (page.value - 1) * PAGE_SIZE,
      year: yearFilter.value,
      month: monthFilter.value,
    })
    if (search.value) params.set('search', search.value)
    if (statusFilter.value !== 'All') params.set('status', statusFilter.value)

    const res = await fetch(`${API_BASE}/jobs?${params}`)
    const data = await res.json()
    const items = data.items || []
    hasMore.value = items.length === PAGE_SIZE + 1
    jobs.value = items.slice(0, PAGE_SIZE)
    if (hasMore.value) {
      totalCount.value = page.value * PAGE_SIZE + 1
    } else {
      totalCount.value = (page.value - 1) * PAGE_SIZE + jobs.value.length
    }
  } catch (e) {
    console.error("Failed to load jobs:", e)
  } finally {
    isLoading.value = false
  }
}

const filteredJobs = computed(() => {
  let result = [...jobs.value]
  if (titleSort.value) result.sort((a, b) => { const c = (a.job_title||'').localeCompare(b.job_title||''); return titleSort.value === 'desc' ? -c : c })
  else if (companySort.value) result.sort((a, b) => { const c = (a.company||'').localeCompare(b.company||''); return companySort.value === 'desc' ? -c : c })
  else if (priceSort.value) result.sort((a, b) => { const c = (Number(a.job_price)||0) - (Number(b.job_price)||0); return priceSort.value === 'desc' ? -c : c })
  else if (dateSort.value) result.sort((a, b) => { const c = new Date(a.job_updated_at) - new Date(b.job_updated_at); return dateSort.value === 'desc' ? -c : c })
  else result.sort((a, b) => new Date(b.job_updated_at) - new Date(a.job_updated_at))
  return result
})

const goToPage = (p) => { page.value = p; fetchJobs() }

const toggleStatusDropdown = (e) => {
  showStatusDropdown.value = !showStatusDropdown.value
  const rect = e.target.getBoundingClientRect()
  statusDropdownStyle.value = { position: "fixed", top: rect.bottom + window.scrollY + "px", left: rect.left + "px" }
}

const setStatusFilter = (val) => {
  statusFilter.value = val
  showStatusDropdown.value = false
  saveFilters()
  page.value = 1
  fetchJobs()
}

const resetAllFilters = () => {
  titleSort.value = ""; companySort.value = ""; priceSort.value = ""
  statusFilter.value = "All"; dateSort.value = ""
  saveFilters()
  page.value = 1
  fetchJobs()
}

const handleOutsideClick = (e) => {
  if (!e.target.closest(".col-dropdown") && !e.target.closest(".col-filter-btn")) showStatusDropdown.value = false
}

const viewJob = (id) => {
  const job = jobs.value.find((j) => j.job_id === id)
  router.push({ name: "JobDetail", params: { id }, state: { jobTitle: job?.job_title || "" } })
}

const openJobModal = async (job) => {
  try {
    const res = await fetch(`${API_BASE}/job-required-languages?job_id=${job.job_id}&limit=20`)
    const data = await res.json()
    jobModal.value = { ...job, languages: (data.items || []).map(l => l.language_name) }
  } catch { jobModal.value = { ...job, languages: [] } }
}

const openCompanyModal = async (job) => {
  companyModal.value = { em_name: job.company }
  try {
    const res = await fetch(`${API_BASE}/employers/${job.em_id}`)
    const data = await res.json()
    companyModal.value = data.em_id ? data : { em_name: job.company }
  } catch {}
}

const deleteJob = (id) => {
  deleteTargetId.value = id
  deleteTargetTitle.value = jobs.value.find((j) => j.job_id === id)?.job_title || id
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  const id = deleteTargetId.value
  try {
    const res = await fetch(`${API_BASE}/jobs/${id}`, {
      method: "DELETE",
      headers: { "X-Admin-ID": localStorage.getItem('admin_id') || '' },
    })
    if (res.ok) { jobs.value = jobs.value.filter((j) => j.job_id !== id) }
    else console.error("Delete failed:", res.status)
  } catch (e) { console.error("Failed to delete job:", e) }
  finally { showDeleteModal.value = false; deleteTargetId.value = null; deleteTargetTitle.value = "" }
}

onMounted(() => { document.addEventListener("click", handleOutsideClick); fetchJobs() })
onUnmounted(() => { document.removeEventListener("click", handleOutsideClick) })
</script>