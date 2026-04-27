<template>
  <div>
    <!-- Top Bar -->
    <div class="topbar">
      <span class="back-link" @click="router.back()">← Back to Jobs</span>
      <button v-if="job" class="btn-delete" @click="showDeleteModal = true">🗑 Delete Job</button>
    </div>

    <div v-if="loading" class="loading">⏳ Loading...</div>

    <div v-else-if="job">

      <!-- Hero Card -->
      <div class="hero-card">
        <div class="hero-left">
          <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
          <h2 class="job-title">{{ job.job_title }}</h2>
          <p class="company">🏢 {{ job.company }}</p>
        </div>
        <div class="price-box">
          <span class="price-label">PRICE</span>
          <span class="price-value">{{ job.job_price ? '฿' + Number(job.job_price).toLocaleString() : '-' }}</span>
        </div>
      </div>

      <div class="sections">

        <!-- 1. Job Info -->
        <div class="section-card">
          <h3 class="section-title">📋 Job Info</h3>
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
              <label>Vehicle Type</label>
              <span>{{ job.job_required_vehicle_type || '-' }}</span>
            </div>
            <div class="info-item">
              <label>Required Seats</label>
              <span>{{ job.job_required_seat || '-' }} seats</span>
            </div>
            <div class="info-item">
              <label>Selected Freelancer</label>
              <span>{{ job.selected_fl_id || 'Not assigned' }}</span>
            </div>
            <div class="info-item">
              <label>Job ID</label>
              <span class="muted">{{ job.job_id }}</span>
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

        <!-- 2. Required Languages -->
        <div class="section-card" v-if="languages.length">
          <h3 class="section-title">🌐 Required Languages</h3>
          <div class="tag-row">
            <span v-for="lang in languages" :key="lang.job_req_lg_id" class="tag blue">
              {{ lang.language_name }}
            </span>
          </div>
        </div>

        <!-- 3. Pickup Points -->
        <div class="section-card" v-if="pickups.length">
          <h3 class="section-title">📍 Pickup Points</h3>
          <div class="timeline">
            <div v-for="p in pickups" :key="p.job_pickup_id" class="timeline-item">
              <div class="timeline-dot orange"></div>
              <div class="timeline-content">
                <span class="timeline-time">{{ p.pickup_time }}</span>
                <span class="timeline-place">{{ p.pickup_location }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Itinerary -->
        <div class="section-card" v-if="itineraries.length">
          <h3 class="section-title">🗺️ Itinerary</h3>
          <div class="timeline">
            <div v-for="item in itineraries" :key="item.job_itinerary_id" class="timeline-item">
              <div class="timeline-dot blue"></div>
              <div class="timeline-content">
                <span class="timeline-time">{{ item.start_time }} – {{ item.end_time }}</span>
                <span class="timeline-place">{{ item.place_name }}</span>
                <span v-if="item.note" class="timeline-note">📝 {{ item.note }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. Inclusions -->
        <div class="section-card" v-if="inclusions.length">
          <h3 class="section-title">📋 Inclusions</h3>
          <div class="two-col">
            <div>
              <p class="col-label">✅ Included</p>
              <div class="inclusion-list">
                <div
                  v-for="inc in inclusions.filter(i => i.inclusion_type === 'INCLUDED')"
                  :key="inc.job_inclusion_id"
                  class="inclusion-item green"
                >{{ inc.description }}</div>
                <div v-if="!inclusions.filter(i => i.inclusion_type === 'INCLUDED').length" class="empty-text">-</div>
              </div>
            </div>
            <div>
              <p class="col-label">❌ Not Included</p>
              <div class="inclusion-list">
                <div
                  v-for="inc in inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED')"
                  :key="inc.job_inclusion_id"
                  class="inclusion-item red"
                >{{ inc.description }}</div>
                <div v-if="!inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED').length" class="empty-text">-</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 6. Entrance Fees -->
        <div class="section-card" v-if="entranceFees.length">
          <h3 class="section-title">🎫 Entrance Fees</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Place</th>
                <th>Thai</th>
                <th>Foreigner</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="fee in entranceFees" :key="fee.job_entrance_fee_id">
                <td>{{ fee.place_name }}</td>
                <td>{{ fee.thai_price > 0 ? '฿' + fee.thai_price : 'Free' }}</td>
                <td>{{ fee.foreigner_price > 0 ? '฿' + fee.foreigner_price : 'Free' }}</td>
                <td class="muted">{{ fee.note || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 7. Customers -->
        <div class="section-card" v-if="customers.length">
          <h3 class="section-title">👥 Customers ({{ customers.length }})</h3>
          <div class="customer-list">
            <div v-for="c in customers" :key="c.job_customer_id" class="customer-item">
              <span class="customer-name">{{ c.customer_name }}</span>
              <span v-if="c.note" class="customer-note">{{ c.note }}</span>
            </div>
          </div>
        </div>

        <!-- 8. Applications -->
        <div class="section-card" v-if="applications.length">
          <h3 class="section-title">📨 Applications ({{ applications.length }})</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Freelancer ID</th>
                <th>Status</th>
                <th>Applied At</th>
                <th>Selected At</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.job_application_id">
                <td>{{ app.fl_id }}</td>
                <td>
                  <span class="tag" :class="{
                    green: app.application_status === 'ACCEPTED',
                    red: app.application_status === 'REJECTED',
                    gray: app.application_status === 'APPLIED'
                  }">{{ app.application_status }}</span>
                </td>
                <td class="muted">{{ formatDateTime(app.applied_at) }}</td>
                <td class="muted">{{ app.selected_at ? formatDateTime(app.selected_at) : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 9. Payment -->
        <div class="section-card" v-if="payments.length">
          <h3 class="section-title">💳 Payment</h3>
          <div v-for="pay in payments" :key="pay.payment_id">
            <div class="info-grid">
              <div class="info-item">
                <label>Payment ID</label>
                <span class="muted">{{ pay.payment_id }}</span>
              </div>
              <div class="info-item">
                <label>Status</label>
                <span class="tag" :class="{
                  green: pay.payment_status === 'CONFIRMED',
                  orange: pay.payment_status === 'PAID',
                  red: pay.payment_status === 'REJECTED',
                  gray: pay.payment_status === 'PENDING'
                }">{{ pay.payment_status }}</span>
              </div>
              <div class="info-item" v-if="pay.paid_at">
                <label>Paid At</label>
                <span>{{ formatDateTime(pay.paid_at) }}</span>
              </div>
              <div class="info-item" v-if="pay.confirmed_at">
                <label>Confirmed At</label>
                <span>{{ formatDateTime(pay.confirmed_at) }}</span>
              </div>
              <div class="info-item" v-if="pay.reject_reason">
                <label>Reject Reason</label>
                <span class="muted">{{ pay.reject_reason }}</span>
              </div>
              <div class="info-item" v-if="pay.slip_url">
                <label>Slip</label>
                <a :href="pay.slip_url" target="_blank" class="link">View Slip</a>
              </div>
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
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const route = useRoute()
const router = useRouter()
const job = ref(null)
const languages = ref([])
const pickups = ref([])
const itineraries = ref([])
const inclusions = ref([])
const entranceFees = ref([])
const customers = ref([])
const applications = ref([])
const payments = ref([])
const loading = ref(true)
const showDeleteModal = ref(false)

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

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
  const id = route.params.id
  try {
    const [
      jobsRes, langRes, pickupsRes, itinRes,
      inclRes, feesRes, custRes, appRes, payRes
    ] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/job-required-languages?limit=500`),
      fetch(`${API_BASE}/job-pickups?limit=500`),
      fetch(`${API_BASE}/job-itineraries?limit=500`),
      fetch(`${API_BASE}/job-inclusions?limit=500`),
      fetch(`${API_BASE}/job-entrance-fees?limit=500`),
      fetch(`${API_BASE}/job-customers?limit=500`),
      fetch(`${API_BASE}/job-applications?limit=500`),
      fetch(`${API_BASE}/job-payments?limit=500`),
    ])

    const [
      jobsData, langData, pickupsData, itinData,
      inclData, feesData, custData, appData, payData
    ] = await Promise.all([
      jobsRes.json(), langRes.json(), pickupsRes.json(), itinRes.json(),
      inclRes.json(), feesRes.json(), custRes.json(), appRes.json(), payRes.json(),
    ])

    job.value         = (jobsData.items    || []).find(j => j.job_id === id) || null
    languages.value   = (langData.items    || []).filter(l => l.job_id === id)
    pickups.value     = (pickupsData.items || []).filter(p => p.job_id === id).sort((a, b) => a.sequence - b.sequence)
    itineraries.value = (itinData.items    || []).filter(i => i.job_id === id)
    inclusions.value  = (inclData.items    || []).filter(i => i.job_id === id).sort((a, b) => a.sequence - b.sequence)
    entranceFees.value= (feesData.items    || []).filter(f => f.job_id === id).sort((a, b) => a.sequence - b.sequence)
    customers.value   = (custData.items    || []).filter(c => c.job_id === id)
    applications.value= (appData.items     || []).filter(a => a.job_id === id)
    payments.value    = (payData.items     || []).filter(p => p.job_id === id)
  } catch (e) {
    console.error('Failed to load job detail:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.topbar {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 20px;
}
.back-link { color: #0066cc; cursor: pointer; font-size: 14px; }
.btn-delete {
  padding: 8px 16px; border: none; border-radius: 6px;
  background: #dc3545; color: white; font-size: 13px; cursor: pointer;
}
.btn-delete:hover { background: #b02a37; }
.loading { color: #999; padding: 40px 0; text-align: center; }

/* Hero */
.hero-card {
  background: white; border-radius: 12px; padding: 28px;
  display: flex; justify-content: space-between;
  align-items: flex-start; margin-bottom: 16px;
}
.hero-left { display: flex; flex-direction: column; gap: 8px; }
.job-title { font-size: 22px; margin: 0; color: #111; }
.company { color: #666; margin: 0; font-size: 14px; }
.price-box { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
.price-label { font-size: 11px; color: #999; font-weight: 600; text-transform: uppercase; }
.price-value { font-size: 26px; font-weight: 700; color: #111; }

/* Sections */
.sections { display: flex; flex-direction: column; gap: 16px; }
.section-card { background: white; border-radius: 12px; padding: 24px; }
.section-title {
  font-size: 14px; font-weight: 600; color: #444;
  margin: 0 0 20px; padding-bottom: 12px; border-bottom: 1px solid #eee;
}

/* Info Grid */
.info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.info-item { display: flex; flex-direction: column; gap: 5px; }
.info-item label { font-size: 11px; color: #999; font-weight: 600; text-transform: uppercase; }
.info-item span { font-size: 15px; color: #222; }
.muted { color: #888 !important; font-size: 13px !important; }
.link { color: #0066cc; font-size: 14px; }

/* Tags */
.tag-row { display: flex; flex-wrap: wrap; gap: 8px; }
.tag {
  display: inline-block; padding: 5px 12px;
  border-radius: 20px; font-size: 12px; font-weight: 500;
}
.tag.blue { background: #e3f2fd; color: #1976d2; }
.tag.green { background: #f0fdf4; color: #166534; }
.tag.orange { background: #fff3e0; color: #f57c00; }
.tag.red { background: #fef2f2; color: #991b1b; }
.tag.gray { background: #f5f5f5; color: #666; }

/* Timeline */
.timeline { display: flex; flex-direction: column; }
.timeline-item {
  display: flex; gap: 14px; padding: 12px 0;
  border-bottom: 1px solid #f5f5f5; align-items: flex-start;
}
.timeline-item:last-child { border-bottom: none; }
.timeline-dot {
  width: 10px; height: 10px; border-radius: 50%;
  margin-top: 5px; flex-shrink: 0;
}
.timeline-dot.orange { background: #f57c00; }
.timeline-dot.blue { background: #1976d2; }
.timeline-content { display: flex; flex-direction: column; gap: 3px; }
.timeline-time { font-size: 12px; font-weight: 700; color: #555; }
.timeline-place { font-size: 14px; color: #222; }
.timeline-note { font-size: 12px; color: #888; }

/* Two Col */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.col-label { font-size: 12px; font-weight: 600; color: #666; margin: 0 0 10px; }
.inclusion-list { display: flex; flex-direction: column; gap: 6px; }
.inclusion-item { padding: 8px 12px; border-radius: 6px; font-size: 14px; }
.inclusion-item.green { background: #f0fdf4; color: #166534; }
.inclusion-item.red { background: #fef2f2; color: #991b1b; }
.empty-text { color: #ccc; font-size: 13px; }

/* Table */
.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th {
  text-align: left; font-size: 11px; font-weight: 600;
  color: #999; text-transform: uppercase;
  padding: 8px 12px; border-bottom: 2px solid #eee;
}
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f5f5f5; color: #333; }
.data-table tr:last-child td { border-bottom: none; }

/* Customers */
.customer-list { display: flex; flex-direction: column; gap: 8px; }
.customer-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 10px 14px; background: #fafafa; border-radius: 8px;
}
.customer-name { font-size: 14px; color: #222; font-weight: 500; }
.customer-note { font-size: 12px; color: #888; }

/* Badge */
.badge {
  display: inline-block; padding: 4px 12px;
  border-radius: 12px; font-size: 12px; font-weight: 600; width: fit-content;
}
.badge.open, .badge.matching { background: #e3f2fd; color: #1976d2; }
.badge.selected { background: #e8f5e9; color: #2e7d32; }
.badge.in_progress { background: #fff3e0; color: #f57c00; }
.badge.completed { background: #f5f5f5; color: #666; }
.badge.cancelled { background: #ffebee; color: #c62828; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.modal { background: white; border-radius: 12px; padding: 32px; width: 380px; text-align: center; }
.modal-icon { font-size: 36px; margin-bottom: 12px; }
.modal h3 { font-size: 20px; margin: 0 0 12px; }
.modal p { color: #555; margin: 0 0 8px; line-height: 1.5; }
.modal-warning { font-size: 12px; color: #dc3545 !important; margin-bottom: 24px !important; }
.modal-actions { display: flex; justify-content: center; gap: 12px; }
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