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

    <section>
      <h2 class="section-title">Recent Jobs</h2>
      <table class="table">
        <thead>
          <tr>
            <th>JOB TITLE</th>
            <th>COMPANY</th>
            <th>JOB START</th>
            <th>JOB END</th>
            <th>PRICE</th>
            <th>STATUS</th>
            <th>ACTION</th>
            <th>LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in jobs.slice(0, 10)" :key="job.job_id">
            <td>{{ job.job_title }}</td>
            <td>{{ job.company }}</td>
            <td>{{ formatDate(job.job_start_date) }}</td>
            <td>{{ formatDate(job.job_end_date) }}</td>
            <td>{{ job.job_price ? '฿' + Number(job.job_price).toLocaleString() : '-' }}</td>
            <td>
              <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
            </td>
            <td>
              <span class="action-link" @click="viewJob(job.job_id)">View</span>
              <span class="action-link delete" @click="deleteJob(job.job_id, job.job_title)">Delete</span>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
        </tbody>
      </table>
    </section>

    <section>
      <h2 class="section-title">Recent Verifications</h2>
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>TYPE</th>
            <th>STATUS</th>
            <th>ACTION</th>
            <th>SUBMITTED</th>
            <th>LAST UPDATED</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="v in verifications.slice(0, 10)" :key="v.id">
            <td>{{ v.name }}</td>
            <td>{{ v.type }}</td>
            <td>
              <span class="badge" :class="v.status.toLowerCase()">{{ v.status }}</span>
            </td>
            <td>
              <span class="action-link" @click="router.push('/verification')">View</span>
            </td>
            <td class="text-muted">{{ formatDateTime(v.created_at) }}</td>
            <td class="text-muted">{{ formatDateTime(v.updated_at) }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  <!-- Delete Modal -->
  <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
    <div class="modal">
      <div class="modal-icon">🗑</div>
      <h3>Delete Job</h3>
      <p>Are you sure you want to delete<br><strong>"{{ deleteTargetTitle }}"</strong>?</p>
      <p class="modal-warning">This action cannot be undone.</p>
      <div class="modal-actions">
        <button class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
        <button class="btn-confirm-delete" @click="confirmDelete">Delete</button>
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
const showDeleteModal = ref(false)
const deleteTargetId = ref(null)
const deleteTargetTitle = ref('')

const viewJob = (id) => {
  router.push({ name: 'JobDetail', params: { id } })
}

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

const dbConnected = ref(null)
const dbError = ref('')
const jobs = ref([])
const verifications = ref([])

const stats = ref({
  totalJobs: 0,
  pendingVerify: 0,
  freelancers: 0,
  employers: 0
})

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const getLatestDate = (job) => {
  const created = new Date(job.job_created_at || 0)
  const updated = new Date(job.job_updated_at || 0)
  return updated > created ? updated : created
}

const isJobUpdated = (job) => {
  const created = new Date(job.job_created_at || 0)
  const updated = new Date(job.job_updated_at || 0)
  return updated > created
}

const getLatestVerificationDate = (v) => {
  const created = new Date(v.created_at || 0)
  const updated = new Date(v.updated_at || 0)
  return updated > created ? updated : created
}

const isVerificationUpdated = (v) => {
  const created = new Date(v.created_at || 0)
  const updated = new Date(v.updated_at || 0)
  return updated > created
}

onMounted(async () => {
  try {
    const pingRes = await fetch(`${API_BASE}/admin/db/ping`)
    const ping = await pingRes.json()
    dbConnected.value = !!ping.connected
    dbError.value = ping.connected ? '' : (ping.error || 'Unknown error')
  } catch (e) {
    dbConnected.value = false
    dbError.value = String(e)
  }

  try {
    const res = await fetch(`${API_BASE}/admin/stats`)
    const data = await res.json()
    stats.value.totalJobs = data.totalJobs ?? 0
    stats.value.pendingVerify = data.pendingVerify ?? 0
    stats.value.freelancers = data.freelancers ?? 0
    stats.value.employers = data.employers ?? 0
  } catch {
    // keep defaults
  }

  try {
    const jobsRes = await fetch(`${API_BASE}/jobs`)
    const jobsData = await jobsRes.json()
    jobs.value = jobsData.items || []
  } catch {
    // keep empty
  }

  try {
    const [flRes, emRes] = await Promise.all([
      fetch(`${API_BASE}/admin/freelancers`),
      fetch(`${API_BASE}/admin/employers`)
    ])
    const flData = await flRes.json()
    const emData = await emRes.json()
    const pendingFl = (flData.items || []).filter(f => f.fl_verify_status === 'PENDING').map(f => ({
      id: f.fl_id, name: f.fl_name || f.line_user_id, type: 'Freelancer', status: f.fl_verify_status, submitted: formatDate(f.fl_created_at), created_at: f.fl_created_at, updated_at: f.fl_updated_at
    }))
    const pendingEm = (emData.items || []).filter(e => e.em_verify_status === 'PENDING').map(e => ({
      id: e.em_id, name: e.em_name || e.em_username, type: 'Employer', status: e.em_verify_status, submitted: formatDate(e.em_created_at), created_at: e.em_created_at, updated_at: e.em_updated_at
    }))
    verifications.value = [...pendingFl, ...pendingEm]
  } catch {
    // keep empty
  }
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-label {
  font-size: 12px;
  color: #666;
  font-weight: 600;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #1a1a2e;
}

section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  margin-bottom: 16px;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
}

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.open {
  background: #e3f2fd;
  color: #1976d2;
}

.badge.selected {
  background: #f3e5f5;
  color: #7b1fa2;
}

.badge.matching {
  background: #e0f2f1;
  color: #00695c;
}

.badge.closed {
  background: #f5f5f5;
  color: #666;
}

.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}

.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.rejected {
  background: #ffebee;
  color: #c62828;
}

.text-muted {
  color: #999;
  font-size: 13px;
}

.update-info {
  font-size: 12px;
  color: #555;
  font-weight: 500;
}

.action-link {
  color: #0066cc;
  cursor: pointer;
  margin-right: 12px;
  font-size: 13px;
}

.action-link.delete {
  color: #dc3545;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 12px;
  padding: 32px;
  width: 380px;
  text-align: center;
}

.modal-icon { font-size: 36px; margin-bottom: 12px; }
.modal h3 { font-size: 20px; margin: 0 0 12px; }
.modal p { color: #555; margin: 0 0 8px; line-height: 1.5; }
.modal-warning { font-size: 12px; color: #dc3545 !important; margin-bottom: 24px !important; }
.modal-actions { display: flex; justify-content: center; gap: 12px; }

.btn-cancel {
  padding: 10px 24px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}

.btn-confirm-delete {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  background: #dc3545;
  color: white;
  cursor: pointer;
  font-size: 14px;
}

.btn-confirm-delete:hover { background: #b02a37; }
</style>