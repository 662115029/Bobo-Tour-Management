<template>
  <div>
    <h1 class="title">Jobs Management</h1>
    
    <div class="filter-row">
      <input 
        type="text" 
        v-model="search" 
        placeholder="Search job title..." 
        class="search-input"
      />
      <div class="filter-group">
        <select v-model="statusFilter" class="filter-select">
          <option value="All">All Status</option>
          <option value="OPEN">Open</option>
          <option value="MATCHING">Matching</option>
          <option value="SELECTED">Selected</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
          <option value="CANCELLED">Cancelled</option>
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
          <tr v-for="job in filteredJobs" :key="job.job_id">
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
              <span class="action-link delete" @click="deleteJob(job.job_id)">Delete</span>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal">
        <h3>Confirm Delete</h3>
        <p>Are you sure you want to delete <strong>"{{ deleteTargetTitle }}"</strong>? This action cannot be undone.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-delete" @click="confirmDelete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const router = useRouter()
const search = ref('')
const statusFilter = ref('All')
const sortOrder = ref('newest')
const jobs = ref([])
const showDeleteModal = ref(false)
const deleteTargetId = ref(null)
const deleteTargetTitle = ref('')

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
    return matchSearch && matchStatus
  })
  result = [...result].sort((a, b) => {
    const dateA = new Date(a.job_created_at)
    const dateB = new Date(b.job_created_at)
    return sortOrder.value === 'newest' ? dateB - dateA : dateA - dateB
  })
  return result
})

const viewJob = (id) => {
  router.push({ name: 'JobDetail', params: { id } })
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
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/jobs`)
    const data = await res.json()
    jobs.value = data.items || []
  } catch (e) {
    console.error('Failed to load jobs:', e)
  }
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.filter-group {
  display: flex;
  gap: 8px;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 280px;
  font-size: 14px;
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 140px;
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

.badge.open, .badge.matching {
  background: #e3f2fd;
  color: #1976d2;
}

.badge.selected {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.in_progress {
  background: #fff3e0;
  color: #f57c00;
}

.badge.completed {
  background: #f5f5f5;
  color: #666;
}

.badge.cancelled {
  background: #ffebee;
  color: #c62828;
}

.action-link {
  color: #0066cc;
  cursor: pointer;
  margin-right: 12px;
}

.action-link.delete {
  color: #dc3545;
}

.text-muted {
  color: #999;
  font-size: 13px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  background: white;
  border-radius: 10px;
  padding: 28px;
  width: 360px;
}

.modal h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.modal p {
  color: #555;
  margin: 0 0 24px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-cancel {
  padding: 8px 18px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
}

.btn-delete {
  padding: 8px 18px;
  border: none;
  border-radius: 6px;
  background: #dc3545;
  color: white;
  cursor: pointer;
}
</style>