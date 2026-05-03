<template>
  <div>
    <h1 class="title">Dashboard</h1>

    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-label">TOTAL JOBS</span>
        <span class="stat-value">{{ stats.totalJobs.toLocaleString() }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">PENDING VERIFY</span>
        <span class="stat-value">{{ stats.pendingVerify }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">FREELANCERS</span>
        <span class="stat-value">{{ stats.freelancers }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">EMPLOYERS</span>
        <span class="stat-value">{{ stats.employers }}</span>
      </div>
    </div>

    <!-- Recent Jobs -->
    <section>
      <h2 class="section-title">Recent Jobs</h2>
      <table class="table">
        <thead>
          <tr>
            <th style="width:28%">JOB TITLE</th>
            <th style="width:16%">COMPANY</th>
            <th style="width:10%">PRICE</th>
            <th style="width:10%">STATUS</th>
            <th style="width:12%">ACTION</th>
            <th style="width:16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs.slice(0, 10)" :key="job.job_id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openJobModal(job)">
              {{ job.job_title }}
            </td>
            <td class="truncate-cell clickable-cell" @click="openCompanyModal(job)">
              {{ job.company }}
            </td>
            <td>{{ job.job_price ? '฿' + Number(job.job_price).toLocaleString() : '-' }}</td>
            <td>
              <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
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

    <!-- Recent Verifications -->
    <section>
      <h2 class="section-title">Recent Verifications</h2>
      <table class="table">
        <thead>
          <tr>
            <th style="width:28%">NAME</th>
            <th style="width:26%">TYPE</th>
            <th style="width:10%">STATUS</th>
            <th style="width:12%">ACTION</th>
            <th style="width:16%">LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in verifications.slice(0, 10)" :key="v.id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openVerifyModal(v)">
              {{ v.name }}
            </td>
            <td>
              <span class="type-tag" :class="v.type.toLowerCase()">{{ v.type }}</span>
            </td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="openVerifyDocs(v)">View Docs</button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(v.updated_at) }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Job Mini Modal -->
    <div v-if="jobModal" class="modal-overlay" @click.self="jobModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header">
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
          <div class="mini-item"><label>Company</label>
            <span>{{ jobModal.company || '-' }}</span>
          </div>
          <div class="mini-item"><label>Freelancer</label>
            <span>{{ jobModal.selected_fl_id || '-' }}</span>
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

    <!-- Company Mini Modal -->
    <div v-if="companyModal" class="modal-overlay" @click.self="companyModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px;">
          <button class="close-btn" @click="companyModal = null">✕</button>
        </div>
        <div v-if="companyLoading" class="mini-loading">Loading...</div>
        <div v-else>
          <div class="profile-hero">
            <div class="profile-avatar em">
              <img v-if="companyModal.em_profile_image_url" :src="companyModal.em_profile_image_url" class="avatar-img" />
              <span v-else class="avatar-initial">{{ companyModal.em_name?.[0] || '?' }}</span>
            </div>
            <div class="profile-info">
              <h3 class="profile-name">{{ companyModal.em_name }}</h3>
              <p v-if="companyModal.em_bio" class="profile-bio">{{ companyModal.em_bio }}</p>
              <p v-else class="profile-bio muted">No bio</p>
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
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="router.push({ name: 'EmployerDetail', params: { id: companyModal.em_id } }); companyModal = null">View Full Detail →</button>
        </div>
      </div>
    </div>

    <!-- Verification Mini Modal -->
    <div v-if="verifyModal" class="modal-overlay" @click.self="verifyModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content:flex-end; margin-bottom:8px;">
          <button class="close-btn" @click="verifyModal = null">✕</button>
        </div>
        <div v-if="verifyLoading" class="mini-loading">Loading...</div>
        <div v-else>
          <!-- Freelancer -->
          <div v-if="verifyModal.type === 'Freelancer' && verifyDetail">
            <div class="profile-hero">
              <div class="profile-avatar fl">
                <img v-if="verifyDetail.fl_profile_image_url" :src="verifyDetail.fl_profile_image_url" class="avatar-img" />
                <span v-else class="avatar-initial">{{ verifyDetail.fl_name?.[0] || '?' }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ verifyDetail.fl_name }}</h3>
                <p v-if="verifyDetail.fl_bio" class="profile-bio">{{ verifyDetail.fl_bio }}</p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item"><label>Status</label>
                <span class="badge" :class="verifyDetail.fl_verify_status?.toLowerCase()">{{ verifyDetail.fl_verify_status }}</span>
              </div>
              <div class="mini-item"><label>Active</label><span>{{ verifyDetail.fl_is_active ? '✅ Active' : '❌ Inactive' }}</span></div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ verifyDetail.fl_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Date of Birth</label><span>{{ formatDate(verifyDetail.fl_date_of_birth) }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ verifyDetail.fl_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(verifyDetail.fl_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(verifyDetail.fl_updated_at) }}</span></div>
            </div>
          </div>
          <!-- Employer -->
          <div v-if="verifyModal.type === 'Employer' && verifyDetail">
            <div class="profile-hero">
              <div class="profile-avatar em">
                <img v-if="verifyDetail.em_profile_image_url" :src="verifyDetail.em_profile_image_url" class="avatar-img" />
                <span v-else class="avatar-initial">{{ verifyDetail.em_name?.[0] || '?' }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ verifyDetail.em_name }}</h3>
                <p v-if="verifyDetail.em_bio" class="profile-bio">{{ verifyDetail.em_bio }}</p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item"><label>Status</label>
                <span class="badge" :class="verifyDetail.em_verify_status?.toLowerCase()">{{ verifyDetail.em_verify_status }}</span>
              </div>
              <div class="mini-item"><label>Active</label><span>{{ verifyDetail.em_is_active ? '✅ Active' : '❌ Inactive' }}</span></div>
              <div class="mini-item"><label>Rating</label><span>⭐ {{ verifyDetail.em_rating_avg ?? '-' }}</span></div>
              <div class="mini-item"><label>Phone</label><span>{{ verifyDetail.em_phone || '-' }}</span></div>
              <div class="mini-item"><label>Address</label><span>{{ verifyDetail.em_address || '-' }}</span></div>
              <div class="mini-item"><label>Created</label><span class="text-muted">{{ formatDateTime(verifyDetail.em_created_at) }}</span></div>
              <div class="mini-item"><label>Last Updated</label><span class="text-muted">{{ formatDateTime(verifyDetail.em_updated_at) }}</span></div>
            </div>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="goToVerifyDetail">View Full Detail →</button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="mini-modal" style="text-align:center; padding: 32px;">
        <div style="font-size:36px; margin-bottom:12px;">🗑</div>
        <h3 style="margin:0 0 12px;">Delete Job</h3>
        <p style="color:#555; margin:0 0 8px;">Are you sure you want to delete<br><strong>"{{ deleteTargetTitle }}"</strong>?</p>
        <p style="font-size:12px; color:#dc3545; margin-bottom:24px;">This action cannot be undone.</p>
        <div style="display:flex; justify-content:center; gap:12px;">
          <button class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-confirm-delete" @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>

    <!-- Verification Documents Modal -->
    <div v-if="selectedVerifyUser" class="modal-overlay" @click.self="selectedVerifyUser = null">
      <div class="docs-modal">
        <div class="modal-header">
          <div>
            <h3>{{ selectedVerifyUser.name }} - Documents</h3>
          </div>
          <button class="close-btn" @click="selectedVerifyUser = null">✕</button>
        </div>

        <div v-if="selectedVerifyDocs.length === 0" class="no-docs">No documents found.</div>

        <div v-else class="doc-list">
          <div v-for="doc in selectedVerifyDocs" :key="doc.id" class="doc-row">
            <div class="doc-type-cell">{{ doc.type }}</div>
            <div class="doc-file-cell">
              <img :src="doc.file_url" class="doc-thumbnail" :alt="doc.type" />
            </div>
            <div class="doc-status-cell">
              <span class="doc-badge" :class="doc.status?.toLowerCase()">{{ doc.status }}</span>
            </div>
            <div class="doc-uploaded-cell">{{ doc.uploaded }}</div>
            <div class="doc-actions-cell">
              <button class="btn-approve-row" :disabled="doc.status === 'APPROVED'" @click="reviewVerifyDoc(doc, 'APPROVED')">✅ Approve</button>
              <button class="btn-reject-row" :disabled="doc.status === 'REJECTED'" @click="reviewVerifyDoc(doc, 'REJECTED')">❌ Reject</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const router = useRouter()

const stats = ref({ totalJobs: 0, pendingVerify: 0, freelancers: 0, employers: 0 })
const jobs = ref([])
const verifications = ref([])
const allEmployers = ref([])
const allFreelancers = ref([])
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

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const viewJob = (id) => router.push({ name: 'JobDetail', params: { id } })

const deleteJob = (id, title) => {
  deleteTargetId.value = id
  deleteTargetTitle.value = title
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await fetch(`${API_BASE}/jobs/${deleteTargetId.value}`, { method: 'DELETE' })
    jobs.value = jobs.value.filter(j => j.job_id !== deleteTargetId.value)
    stats.value.totalJobs = Math.max(0, stats.value.totalJobs - 1)
  } catch (e) {
    console.error('Failed to delete job:', e)
  } finally {
    showDeleteModal.value = false
    deleteTargetId.value = null
    deleteTargetTitle.value = ''
  }
}

const openJobModal = (job) => { jobModal.value = job }

const openCompanyModal = async (job) => {
  companyLoading.value = true
  companyModal.value = { em_name: job.company }
  const em = allEmployers.value.find(e => e.em_id === job.em_id)
  companyModal.value = em || { em_name: job.company }
  companyLoading.value = false
}

const openVerifyModal = async (v) => {
  verifyModal.value = v
  verifyDetail.value = null
  verifyLoading.value = true
  if (v.type === 'Freelancer') {
    verifyDetail.value = allFreelancers.value.find(f => f.fl_id === v.id) || null
  } else {
    verifyDetail.value = allEmployers.value.find(e => e.em_id === v.id) || null
  }
  verifyLoading.value = false
}

const goToVerifyFull = (v) => {
  if (v.type === 'Freelancer') {
    router.push({ name: 'FreelancerDetail', params: { id: v.id } })
  } else {
    router.push({ name: 'EmployerDetail', params: { id: v.id } })
  }
}

const goToVerifyDetail = () => {
  if (!verifyModal.value) return
  if (verifyModal.value.type === 'Freelancer') {
    router.push({ name: 'FreelancerDetail', params: { id: verifyModal.value.id } })
  } else {
    router.push({ name: 'EmployerDetail', params: { id: verifyModal.value.id } })
  }
  verifyModal.value = null
}

const openVerifyDocs = (v) => {
  selectedVerifyUser.value = v
  if (v.type === 'Freelancer') {
    const allDocs = flDocs.value.filter(d => d.fl_id === v.id)
    const docsByType = {}
    allDocs.forEach(d => {
      if (!docsByType[d.fl_doc_type] || new Date(d.fl_uploaded_at) > new Date(docsByType[d.fl_doc_type].fl_uploaded_at)) {
        docsByType[d.fl_doc_type] = d
      }
    })
    selectedVerifyDocs.value = Object.values(docsByType).map(d => ({
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
    selectedVerifyDocs.value = Object.values(docsByType).map(d => ({
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

const reviewVerifyDoc = async (doc, newStatus) => {
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
    }
  } catch (e) {
    console.error('Failed to review doc:', e)
  }
}

onMounted(async () => {
  try {
    const pingRes = await fetch(`${API_BASE}/admin/db/ping`)
    const ping = await pingRes.json()
    if (!ping.connected) console.error('DB error:', ping.error)
  } catch (e) { console.error(e) }

  try {
    const res = await fetch(`${API_BASE}/admin/stats`)
    const data = await res.json()
    stats.value.totalJobs = data.totalJobs ?? 0
    stats.value.pendingVerify = data.pendingVerify ?? 0
    stats.value.freelancers = data.freelancers ?? 0
    stats.value.employers = data.employers ?? 0
  } catch { }

  try {
    const jobsRes = await fetch(`${API_BASE}/jobs?limit=500`)
    const jobsData = await jobsRes.json()
    jobs.value = jobsData.items || []
  } catch { }

  try {
    const [flRes, emRes, flDocRes, emDocRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
      fetch(`${API_BASE}/em-documents?limit=500`)
    ])
    const flData = await flRes.json()
    const emData = await emRes.json()
    const flDocData = await flDocRes.json()
    const emDocData = await emDocRes.json()
    allFreelancers.value = flData.items || []
    allEmployers.value = emData.items || []
    flDocs.value = flDocData.items || []
    emDocs.value = emDocData.items || []

    const pendingFl = allFreelancers.value.filter(f => f.fl_verify_status === 'PENDING').map(f => ({
      id: f.fl_id, name: f.fl_name || f.line_user_id, type: 'Freelancer',
      status: f.fl_verify_status, created_at: f.fl_created_at, updated_at: f.fl_updated_at
    }))
    const pendingEm = allEmployers.value.filter(e => e.em_verify_status === 'PENDING').map(e => ({
      id: e.em_id, name: e.em_name || e.em_username, type: 'Employer',
      status: e.em_verify_status, created_at: e.em_created_at, updated_at: e.em_updated_at
    }))
    verifications.value = [...pendingFl, ...pendingEm]
  } catch { }
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

.stats-row {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 16px; margin-bottom: 32px;
}
.stat-card {
  background: white; padding: 20px; border-radius: 8px;
  display: flex; flex-direction: column; gap: 8px;
}
.stat-label { font-size: 12px; color: #666; font-weight: 600; }
.stat-value { font-size: 28px; font-weight: bold; color: #1a1a2e; }

section {
  background: white; padding: 20px;
  border-radius: 8px; margin-bottom: 24px;
}
.section-title { font-size: 16px; margin-bottom: 16px; }

.table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.table th, .table td {
  padding: 12px; text-align: left; border-bottom: 1px solid #eee;
  overflow: hidden;
}
.table th { font-size: 12px; color: #666; font-weight: 600; }

.truncate-cell { max-width: 0; }

.row-hover:hover {
  background: #f5f5f5;
}

.clickable-cell {
  cursor: pointer;
  color: #000;
}

.clickable-cell:hover {
  color: #000;
}

/* Badge */
.badge {
  display: inline-block; padding: 3px 10px;
  border-radius: 12px; font-size: 11px; font-weight: 600;
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

.type-tag {
  display: inline-block; padding: 3px 10px;
  border-radius: 12px; font-size: 11px; font-weight: 600;
}
.type-tag.freelancer { background: #e3f2fd; color: #1976d2; }
.type-tag.employer { background: #f3e5f5; color: #7b1fa2; }

/* Action buttons */
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

/* Mini Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.4);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.mini-modal {
  background: white; border-radius: 12px; padding: 24px;
  width: 460px; max-height: 80vh; overflow-y: auto;
}
.mini-modal-header {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 16px;
}
.mini-modal-title {
  font-size: 16px; font-weight: 600; color: #111;
  margin: 0; flex: 1; padding-right: 12px;
}
.close-btn {
  background: none; border: none; font-size: 16px;
  cursor: pointer; color: #888; flex-shrink: 0;
}
.mini-loading { color: #999; text-align: center; padding: 20px 0; }

.profile-hero {
  display: flex; align-items: flex-start; gap: 14px;
  margin-bottom: 20px; padding-bottom: 16px; border-bottom: 1px solid #eee;
}
.profile-avatar {
  width: 56px; height: 56px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0; overflow: hidden;
}
.profile-avatar.fl { background: #e3f2fd; }
.profile-avatar.em { background: #f3e5f5; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.avatar-initial { font-size: 22px; font-weight: 700; color: #555; }
.profile-info { flex: 1; min-width: 0; }
.profile-name { font-size: 16px; font-weight: 600; margin: 0 0 4px; color: #111; }
.profile-bio {
  font-size: 12px; color: #666; margin: 0;
  line-height: 1.5; display: -webkit-box;
  -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.profile-bio.muted { color: #bbb; font-style: italic; }
.mini-desc {
  font-size: 13px; color: #666; line-height: 1.6;
  margin: 0 0 16px; padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.mini-grid {
  display: grid; grid-template-columns: 1fr 1fr; gap: 14px;
}
.mini-item { display: flex; flex-direction: column; gap: 3px; }
.mini-item label {
  font-size: 10px; color: #999;
  font-weight: 600; text-transform: uppercase;
}
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

.btn-cancel {
  padding: 10px 24px; border: 1px solid #ddd;
  border-radius: 6px; background: white; cursor: pointer; font-size: 14px;
}
.btn-confirm-delete {
  padding: 10px 24px; border: none; border-radius: 6px;
  background: #dc3545; color: white; cursor: pointer; font-size: 14px;
}
.btn-confirm-delete:hover { background: #b02a37; }

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

.no-docs {
  color: #999;
  text-align: center;
  padding: 24px 0;
}
</style>