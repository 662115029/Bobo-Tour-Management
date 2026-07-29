<template>
  <div>
    <BreadcrumbBar />
    <div class="stats-row">
      <div class="stat-card stat-card--blue">
        <span class="stat-label">TOTAL JOBS</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ localTotalJobs.toLocaleString() }}</span>
      </div>
      <div class="stat-card stat-card--amber">
        <span class="stat-label">PENDING VERIFY</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.pendingVerify }}</span>
      </div>
      <div class="stat-card stat-card--sky">
        <span class="stat-label">FREELANCERS</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.freelancers }}</span>
      </div>
      <div class="stat-card stat-card--purple">
        <span class="stat-label">EMPLOYERS</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.employers }}</span>
      </div>
    </div>

    <!-- Recent Jobs -->
    <div class="table-container mb-6">
      <section>
        <h2 class="section-title">Recent Jobs</h2>
        <table class="table dash-table">
        <thead>
          <tr>
            <th style="width: 20%">JOB TITLE</th>
            <th style="width: 16%">EMPLOYER</th>
            <th style="width: 10%">PRICE</th>
            <th style="width: 10%">STATUS</th>
            <th style="width: 12%; text-align: center;">ACTION</th>
            <th style="width: 16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 5" :key="'jsk-'+i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:70%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:60%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:50%"></span></td>
              <td style="text-align:center"><span class="skeleton skeleton-badge"></span></td>
              <td><div class="action-btns"><span class="skeleton skeleton-btn"></span><span class="skeleton skeleton-btn"></span></div></td>
              <td><span class="skeleton skeleton-text" style="width:80%"></span></td>
            </tr>
          </template>
          <tr v-else v-for="job in jobs" :key="job.job_id" class="row-hover">
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
            <td>
              <span class="badge" :class="job.job_status?.toLowerCase()">{{ formatJobStatus(job.job_status) }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewJob(job.job_id)">View</button>
                <button class="btn-action delete" @click="deleteJob(job.job_id, job.job_title)">Delete</button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
        </tbody>
      </table>
      </section>
    </div>

    <!-- Recent Verifications -->
    <div class="table-container mb-6">
      <section>
      <h2 class="section-title">Recent Verifications</h2>
      <table class="table dash-table">
        <thead>
          <tr>
            <th style="width: 20%">NAME</th>
            <th style="width: 26%">TYPE</th>
            <th style="width: 10%" >STATUS</th>
            <th style="width: 12%; text-align: center;">ACTION</th>
            <th style="width: 16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 5" :key="'vsk-'+i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:65%"></span></td>
              <td style="text-align:center"><span class="skeleton skeleton-badge" style="width:80px"></span></td>
              <td style="text-align:center"><span class="skeleton skeleton-badge"></span></td>
              <td style="text-align:center"><div class="action-btns"><span class="skeleton skeleton-btn" style="width:72px"></span></div></td>
              <td style="text-align:center"><span class="skeleton skeleton-text" style="width:75%"></span></td>
            </tr>
          </template>
          <tr v-else v-for="v in verifications" :key="v.id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openVerifyModal(v)">
              <div class="user-cell">
                <span class="user-avatar" :style="avatarStyle(v.id, v.name)">{{ initials2(v.name) }}</span>
                {{ v.name }}
              </div>
            </td>
            <td><span class="type-tag" :class="getTypeClass(v.type)">{{ v.type }}</span></td>
            <td><span class="badge" :class="v.status?.toLowerCase()">{{ formatVerifyStatus(v.status) }}</span></td>
            <td>
              <div class="action-btns">
                <button class="btn-action verify-style" @click="openVerifyDocs(v)">View Docs</button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(v.updated_at) }}</td>
          </tr>
        </tbody>
      </table>
      </section>
    </div>

    <JobMiniModal :data="jobModal" @close="jobModal = null" @view-detail="(id) => { viewJob(id); jobModal = null }" />
    <UserMiniModal :data="companyModal" type="EMPLOYER" :loading="companyLoading"
      @close="companyModal = null"
      @view-detail="({ id }) => { router.push({ name: 'EmployerDetail', params: { id } }); companyModal = null }" />
    <UserMiniModal :data="verifyDetailMapped"
      :type="verifyModal?.type === 'Freelancer' ? 'FREELANCER' : 'EMPLOYER'"
      :loading="verifyLoading"
      @close="verifyModal = null; verifyDetail = null"
      @view-detail="goToVerifyDetail" />
    <DeleteJobModal :show="showDeleteModal" :title="deleteTargetTitle"
      @confirm="confirmDelete" @cancel="showDeleteModal = false" />
    <DocReviewModal v-if="selectedVerifyUser" :user="selectedVerifyUser" :docs="selectedVerifyDocs"
      @close="selectedVerifyUser = null"
      @approve="(doc) => reviewVerifyDoc(doc, 'APPROVED')"
      @reject="({ id, reason }) => { const doc = selectedVerifyDocs.find(d => Number(d.id) === Number(id)); if (doc) reviewVerifyDoc(doc, 'REJECTED', reason) }"
      @reset="(doc) => reviewVerifyDoc(doc, 'PENDING')" />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { useRouter } from 'vue-router'
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime, groupDocsByLatest } from '../utils/formatDate'
import { formatJobStatus, getTypeClass, formatVerifyStatus } from '../utils/statusClasses'
import JobMiniModal from '../components/JobMiniModal.vue'
import UserMiniModal from '../components/UserMiniModal.vue'
import DeleteJobModal from '../components/DeleteJobModal.vue'
import DocReviewModal from '../components/DocReviewModal.vue'
import { API_BASE } from '../data/api'
import { useStats } from '../composables/useStats'

const { avatarStyle, jobIconStyle, initials2 } = useAvatar()
const router = useRouter()

const { stats, loadStats } = useStats()
const localTotalJobs = ref(0)
watch(() => stats.value.totalJobs, (val) => { localTotalJobs.value = val }, { immediate: true })

const isLoading = ref(true)
const jobs = ref([])
const verifications = ref([])
const flDocs = ref([])
const emDocs = ref([])
const selectedVerifyUser = ref(null)
const selectedVerifyDocs = ref([])

const showDeleteModal = ref(false)
const deleteTargetId = ref(null)
const deleteTargetTitle = ref('')

const jobModal = ref(null)
const companyModal = ref(null)
const companyLoading = ref(false)
const verifyModal = ref(null)
const verifyDetail = ref(null)
const verifyLoading = ref(false)

const allLanguages = ref([])
const verifyUserCache = ref({})

const viewJob = (id) => router.push({ name: 'JobDetail', params: { id } })

const deleteJob = (id, title) => {
  deleteTargetId.value = id
  deleteTargetTitle.value = title
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  const id = deleteTargetId.value
  try {
    const res = await fetch(`${API_BASE}/jobs/${id}`, {
      method: 'DELETE',
      headers: { 'X-Admin-ID': localStorage.getItem('admin_id') || '' },
    })
    if (res.ok) {
      jobs.value = jobs.value.filter(j => j.job_id !== id)
      localTotalJobs.value = Math.max(0, localTotalJobs.value - 1)
    }
  } catch (e) {
    console.error('Failed to delete job:', e)
  } finally {
    showDeleteModal.value = false
    deleteTargetId.value = null
    deleteTargetTitle.value = ''
  }
}

const openJobModal = async (job) => {
  if (!allLanguages.value.length) {
    try {
      const res = await fetch(`${API_BASE}/job-required-languages?job_id=${job.job_id}&limit=20`)
      const data = await res.json()
      allLanguages.value = data.items || []
    } catch {}
  }
  const langs = allLanguages.value
    .filter(l => l.job_id === job.job_id)
    .map(l => l.language_name)
  jobModal.value = { ...job, languages: langs }
}

const openCompanyModal = async (job) => {
  companyLoading.value = true
  companyModal.value = { em_name: job.company }
  try {
    const res = await fetch(`${API_BASE}/employers/${job.em_id}`)
    const em = await res.json()
    companyModal.value = em.em_id ? em : { em_name: job.company }
  } catch {
    companyModal.value = { em_name: job.company }
  } finally {
    companyLoading.value = false
  }
}

const openVerifyModal = async (v) => {
  verifyModal.value = v
  verifyDetail.value = null
  verifyLoading.value = true
  try {
    if (verifyUserCache.value[v.id]) {
      verifyDetail.value = verifyUserCache.value[v.id]
      return
    }
    const endpoint = v.type === 'Freelancer'
      ? `${API_BASE}/freelancers/${v.id}`
      : `${API_BASE}/employers/${v.id}`
    const res = await fetch(endpoint)
    const data = await res.json()
    verifyUserCache.value[v.id] = data
    verifyDetail.value = data
  } catch {} finally {
    verifyLoading.value = false
  }
}

const verifyDetailMapped = computed(() => {
  if (!verifyDetail.value || !verifyModal.value) return null
  return verifyDetail.value
})

const goToVerifyDetail = () => {
  if (!verifyModal.value) return
  const route = verifyModal.value.type === 'Freelancer'
    ? { name: 'FreelancerDetail', params: { id: verifyModal.value.id } }
    : { name: 'EmployerDetail', params: { id: verifyModal.value.id } }
  router.push(route)
  verifyModal.value = null
}

const openVerifyDocs = (v) => {
  selectedVerifyUser.value = v
  if (v.type === 'Freelancer') {
    const allDocs = flDocs.value.filter(d => Number(d.fl_id) === Number(v.id))
    selectedVerifyDocs.value = groupDocsByLatest(allDocs, 'fl', formatDateTime)
  } else {
    const allDocs = emDocs.value.filter(d => Number(d.em_id) === Number(v.id))
    selectedVerifyDocs.value = groupDocsByLatest(allDocs, 'em', formatDateTime)
  }
}

const reviewVerifyDoc = async (doc, newStatus, reason = '') => {
  const endpoint = doc._type === 'fl'
    ? `${API_BASE}/fl-documents/${doc.id}`
    : `${API_BASE}/em-documents/${doc.id}`
  try {
    const res = await fetch(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus, reviewed_by: localStorage.getItem('admin_id') || '', reason: reason || null }),
    })
    const data = await res.json()
    if (data.status === 'updated') {
      selectedVerifyDocs.value = selectedVerifyDocs.value.map(d => {
        if (Number(d.id) !== Number(doc.id)) return d
        return {
          ...d,
          status: newStatus,
          reviewed: newStatus !== 'PENDING' ? formatDateTime(new Date().toISOString()) : null,
          rejectReason: newStatus === 'REJECTED' ? (reason || null) : null,
          reviewedBy: newStatus !== 'PENDING' ? (localStorage.getItem('admin_name') || 'Admin') : null,
        }
      })
      if (doc._type === 'fl') {
        const raw = flDocs.value.find(d => d.fl_doc_id === doc.id)
        if (raw) raw.fl_doc_status = newStatus
      } else {
        const raw = emDocs.value.find(d => d.em_doc_id === doc.id)
        if (raw) raw.em_doc_status = newStatus
      }
      if (selectedVerifyUser.value) {
        const userId = selectedVerifyUser.value.id
        const userDocs = doc._type === 'fl'
          ? flDocs.value.filter(d => Number(d.fl_id) === Number(userId))
          : emDocs.value.filter(d => Number(d.em_id) === Number(userId))
        const statusKey = doc._type === 'fl' ? 'fl_doc_status' : 'em_doc_status'
        const approvedCount = userDocs.filter(d => d[statusKey] === 'APPROVED').length
        const rejectedCount = userDocs.filter(d => d[statusKey] === 'REJECTED').length
        const pendingCount = userDocs.filter(d => d[statusKey] === 'PENDING').length
        const newUserStatus = approvedCount >= 5 ? 'VERIFIED'
          : rejectedCount === userDocs.length && pendingCount === 0 && approvedCount === 0 ? 'NOT_VERIFIED'
          : 'PENDING'
        const entry = verifications.value.find(v => v.id === userId)
        if (entry) entry.status = newUserStatus
        selectedVerifyUser.value.status = newUserStatus
      }
    }
  } catch (e) {
    console.error('Failed to review doc:', e)
  }
}

onMounted(async () => {
  try {
    const [pingRes, jobsRes, flRes, emRes] = await Promise.all([
      fetch(`${API_BASE}/admin/db/ping`),
      fetch(`${API_BASE}/jobs?limit=10`),
      fetch(`${API_BASE}/freelancers?limit=10&status=PENDING&sort_by=fv.fl_submitted_at&sort_order=desc`),
      fetch(`${API_BASE}/employers?limit=10&status=PENDING&sort_by=ev.em_submitted_at&sort_order=desc`),
   ])

    const [ping, jobsData, flData, emData] = await Promise.all([
      pingRes.json(), jobsRes.json(), flRes.json(), emRes.json(),
    ])

    if (!ping.connected) console.error('DB error:', ping.error)
    jobs.value = jobsData.items || []

    const flItems = flData.items || []
    const emItems = emData.items || []
    const flIds = flItems.map(f => f.fl_id).join(',')
    const emIds = emItems.map(e => e.em_id).join(',')

    const [flDocRes, emDocRes] = await Promise.all([
      flIds ? fetch(`${API_BASE}/fl-documents?fl_ids=${flIds}&limit=50`) : Promise.resolve({ json: () => ({ items: [] }) }),
      emIds ? fetch(`${API_BASE}/em-documents?em_ids=${emIds}&limit=50`) : Promise.resolve({ json: () => ({ items: [] }) }),
    ])
    const [flDocData, emDocData] = await Promise.all([flDocRes.json(), emDocRes.json()])
    flDocs.value = flDocData.items || []
    emDocs.value = emDocData.items || []

    const allFl = flItems.map(f => ({
      id: f.fl_id,
      name: f.fl_name || f.line_user_id,
      type: 'Freelancer',
      status: f.fl_verify_status,
      updated_at: f.fl_submitted_at || f.fl_updated_at,
    }))
    const allEm = emItems.map(e => ({
      id: e.em_id,
      name: e.em_name || e.em_username,
      type: 'Employer',
      status: e.em_verify_status,
      updated_at: e.em_submitted_at || e.em_updated_at,
    }))
    verifications.value = [...allFl, ...allEm]
      .sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at))
      .slice(0, 10)
  } catch (e) {
    console.error(e)
  } finally {
    isLoading.value = false
  }
})
</script>