<template>
  <div>
    <!-- Top Bar -->
    <div class="topbar">
      <span class="back-link" @click="router.back()">← Back to Jobs</span>
      <div class="topbar-actions" v-if="job">
        <button class="btn-delete" @click="showDeleteModal = true">🗑 Delete Job</button>
      </div>
    </div>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-else-if="job">

      <!-- Hero Card -->
      <div class="hero-card">
        <div class="hero-left">
          <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
          <h2 class="job-title">{{ job.job_title }}</h2>
          <p class="company">🏢 {{ job.company }}</p>
        </div>
        <div class="hero-right">
          <div class="price-box">
            <span class="price-label">PRICE</span>
            <span class="price-value">{{ job.job_price ? '฿' + Number(job.job_price).toLocaleString() : '-' }}</span>
          </div>
        </div>
      </div>

      <!-- Info Sections -->
      <div class="sections">

        <!-- Date & Schedule -->
        <div class="section-card">
          <h3 class="section-title">📅 Schedule</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Job Start</label>
              <span>{{ formatDate(job.job_start_date) }}</span>
            </div>
            <div class="info-item">
              <label>Job End</label>
              <span>{{ formatDate(job.job_end_date) }}</span>
            </div>
            <div class="info-item">
              <label>Created At</label>
              <span class="muted">{{ formatDateTime(job.job_created_at) }}</span>
            </div>
            <div class="info-item">
              <label>Last Updated</label>
              <span class="muted">{{ formatDateTime(job.job_updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Vehicle & Logistics -->
        <div class="section-card">
          <h3 class="section-title">🚐 Vehicle & Logistics</h3>
          <div class="info-grid">
            <div class="info-item">
              <label>Vehicle Type</label>
              <span>{{ job.job_required_vehicle_type || '-' }}</span>
            </div>
            <div class="info-item">
              <label>Required Seats</label>
              <span>{{ job.job_required_seat || '-' }} seats</span>
            </div>
            <div class="info-item">
              <label>Job ID</label>
              <span class="muted">{{ job.job_id }}</span>
            </div>
            <div class="info-item">
              <label>Selected Freelancer</label>
              <span>{{ job.selected_fl_id || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- Description -->
        <div class="section-card" v-if="job.job_description">
          <h3 class="section-title">📝 Description</h3>
          <div class="desc-parsed">

            <!-- Header -->
            <div v-if="parsed.header" class="desc-header">{{ parsed.header }}</div>

            <!-- Staff -->
            <div v-if="parsed.staff.length" class="desc-section">
              <div class="desc-section-label">👤 Staff</div>
              <div class="desc-tag-row">
                <span v-for="(s, i) in parsed.staff" :key="i" class="desc-tag">{{ s }}</span>
              </div>
            </div>

            <!-- Schedule -->
            <div v-if="parsed.schedule.length" class="desc-section">
              <div class="desc-section-label">🕐 Tour Schedule</div>
              <div class="desc-timeline">
                <div v-for="(s, i) in parsed.schedule" :key="i" class="desc-timeline-item">
                  <span class="time-slot">{{ s.time }}</span>
                  <span class="time-place">{{ s.place }}</span>
                </div>
              </div>
            </div>

            <!-- Including -->
            <div v-if="parsed.including.length" class="desc-section">
              <div class="desc-section-label">✅ Including</div>
              <div class="desc-list">
                <span v-for="(item, i) in parsed.including" :key="i" class="desc-list-item green">{{ item }}</span>
              </div>
            </div>

            <!-- Not Included -->
            <div v-if="parsed.notIncluded.length" class="desc-section">
              <div class="desc-section-label">❌ Not Included</div>
              <div class="desc-list">
                <span v-for="(item, i) in parsed.notIncluded" :key="i" class="desc-list-item red">{{ item }}</span>
              </div>
            </div>

            <!-- Remark -->
            <div v-if="parsed.remark" class="desc-section">
              <div class="desc-section-label">📌 Remark</div>
              <div class="desc-remark">{{ parsed.remark }}</div>
            </div>

            <!-- Fallback raw -->
            <div v-if="!parsed.header && !parsed.schedule.length" class="desc-raw">
              {{ job.job_description }}
            </div>

          </div>
        </div>

      </div>
    </div>

    <div v-else class="loading">Job not found.</div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal">
        <div class="modal-icon">🗑</div>
        <h3>Delete Job</h3>
        <p>Are you sure you want to delete<br><strong>"{{ job?.job_title }}"</strong>?</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const route = useRoute()
const router = useRouter()
const job = ref(null)
const loading = ref(true)
const showDeleteModal = ref(false)

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const parsed = computed(() => {
  const text = job.value?.job_description || ''
  const result = { header: '', staff: [], schedule: [], including: [], notIncluded: [], remark: '' }
  if (!text) return result

  // Extract header from [...] at the start
  const headerMatch = text.match(/^\[([^\]]+)\]/)
  if (headerMatch) result.header = headerMatch[1]

  // Extract staff lines (Driver, Guide patterns)
  const staffMatches = text.match(/(Driver|Guide|Leader|Manager)[^/\n]+(\/ \d+)/g) || []
  result.staff = staffMatches.map(s => s.trim())

  // Extract tour schedule (time ranges like 07:00-07:30 ...)
  const scheduleMatches = text.match(/\d{2}:\d{2}-\d{2}:\d{2} [^\d\n]+/g) || []
  result.schedule = scheduleMatches.map(s => {
    const m = s.match(/(\d{2}:\d{2}-\d{2}:\d{2})\s+(.+)/)
    return m ? { time: m[1], place: m[2].trim() } : { time: '', place: s.trim() }
  })

  // Extract Including section
  const includingMatch = text.match(/Including:\s*([\s\S]*?)(?=Not Included:|Remark:|$)/)
  if (includingMatch) {
    result.including = includingMatch[1].split('-').map(s => s.trim()).filter(s => s.length > 0)
  }

  // Extract Not Included section
  const notIncludedMatch = text.match(/Not Included:\s*([\s\S]*?)(?=Remark:|$)/)
  if (notIncludedMatch) {
    result.notIncluded = notIncludedMatch[1].split('-').map(s => s.trim()).filter(s => s.length > 0)
  }

  // Extract Remark
  const remarkMatch = text.match(/Remark:\s*(.+)/)
  if (remarkMatch) result.remark = remarkMatch[1].trim()

  return result
})

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const confirmDelete = async () => {
  try {
    await fetch(`${API_BASE}/jobs/${job.value.job_id}`, { method: 'DELETE' })
    router.push({ name: 'Jobs' })
  } catch (e) {
    console.error('Failed to delete job:', e)
  } finally {
    showDeleteModal.value = false
  }
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/jobs`)
    const data = await res.json()
    job.value = (data.items || []).find(j => j.job_id === route.params.id) || null
  } catch (e) {
    console.error('Failed to load job:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-link {
  color: #0066cc;
  cursor: pointer;
  font-size: 14px;
}

.topbar-actions {
  display: flex;
  gap: 10px;
}

.btn-delete {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  background: #dc3545;
  color: white;
  font-size: 13px;
  cursor: pointer;
}

.btn-delete:hover {
  background: #b02a37;
}

.loading {
  color: #999;
  padding: 40px 0;
  text-align: center;
}

/* Hero Card */
.hero-card {
  background: white;
  border-radius: 12px;
  padding: 28px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.hero-left {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.job-title {
  font-size: 22px;
  margin: 0;
  color: #111;
}

.company {
  color: #666;
  margin: 0;
  font-size: 14px;
}

.price-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}

.price-label {
  font-size: 11px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.price-value {
  font-size: 24px;
  font-weight: 700;
  color: #111;
}

/* Sections */
.sections {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #444;
  margin: 0 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.info-item label {
  font-size: 11px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}

.info-item span {
  font-size: 15px;
  color: #222;
}

.info-item span.muted {
  color: #888;
  font-size: 14px;
}

.desc-parsed { display: flex; flex-direction: column; gap: 16px; }
.desc-header {
  font-size: 15px;
  font-weight: 600;
  color: #222;
  padding: 10px 14px;
  background: #f0f4ff;
  border-radius: 8px;
  border-left: 4px solid #4a6cf7;
}
.desc-section { display: flex; flex-direction: column; gap: 8px; }
.desc-section-label {
  font-size: 12px;
  font-weight: 600;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.desc-tag-row { display: flex; flex-wrap: wrap; gap: 8px; }
.desc-tag {
  padding: 6px 12px;
  background: #f5f5f5;
  border-radius: 20px;
  font-size: 13px;
  color: #333;
}
.desc-timeline { display: flex; flex-direction: column; gap: 6px; }
.desc-timeline-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 3px solid #e0e0e0;
}
.time-slot {
  font-size: 12px;
  font-weight: 700;
  color: #555;
  white-space: nowrap;
  min-width: 100px;
}
.time-place { font-size: 14px; color: #333; }
.desc-list { display: flex; flex-direction: column; gap: 6px; }
.desc-list-item {
  padding: 7px 12px;
  border-radius: 6px;
  font-size: 14px;
}
.desc-list-item.green { background: #f0fdf4; color: #166534; }
.desc-list-item.red { background: #fef2f2; color: #991b1b; }
.desc-remark {
  padding: 10px 14px;
  background: #fffbeb;
  border-radius: 8px;
  border-left: 4px solid #f59e0b;
  font-size: 14px;
  color: #444;
}
.desc-raw { font-size: 14px; color: #444; line-height: 1.7; }

/* Badge */
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  width: fit-content;
}

.badge.open, .badge.matching { background: #e3f2fd; color: #1976d2; }
.badge.selected { background: #e8f5e9; color: #2e7d32; }
.badge.in_progress { background: #fff3e0; color: #f57c00; }
.badge.completed { background: #f5f5f5; color: #666; }
.badge.cancelled { background: #ffebee; color: #c62828; }

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

.modal-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.modal h3 {
  font-size: 20px;
  margin: 0 0 12px;
}

.modal p {
  color: #555;
  margin: 0 0 8px;
  line-height: 1.5;
}

.modal-warning {
  font-size: 12px;
  color: #dc3545 !important;
  margin-bottom: 24px !important;
}

.modal-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

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

.btn-confirm-delete:hover {
  background: #b02a37;
}
</style>