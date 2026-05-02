<template>
  <div>
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
          <p v-if="job.job_description" class="job-desc">{{ job.job_description }}</p>
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
          <div class="mini-grid">
            <div class="mini-item">
              <label>Languages</label>
              <div class="tag-row" style="margin-top:4px;">
                <span v-for="lang in languages" :key="lang.job_req_lg_id" class="tag blue">{{ lang.language_name }}</span>
                <span v-if="!languages.length" class="empty-val">-</span>
              </div>
            </div>
            <div class="mini-item"><label>Freelancer</label>
              <span>{{ freelancerName || 'Not assigned' }}</span>
            </div>
            <div class="mini-item"><label>Job Start</label>
              <span>{{ formatDate(job.job_start_date) }}</span>
            </div>
            <div class="mini-item"><label>Job End</label>
              <span>{{ formatDate(job.job_end_date) }}</span>
            </div>
            <div class="mini-item"><label>Vehicle</label>
              <span>{{ job.job_required_vehicle_type || '-' }}</span>
            </div>
            <div class="mini-item"><label>Seats</label>
              <span>{{ job.job_required_seat || '-' }}</span>
            </div>
            <div class="mini-item"><label>Created</label>
              <span class="text-muted">{{ formatDateTime(job.job_created_at) }}</span>
            </div>
            <div class="mini-item"><label>Last Updated</label>
              <span class="text-muted">{{ formatDateTime(job.job_updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- 2. Pickup Points -->
        <div class="section-card" v-if="pickups.length">
          <h3 class="section-title">📍 Pickup Points</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th style="width:18%">Time</th>
                <th>Location</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in pickups" :key="p.job_pickup_id">
                <td><span class="time-badge">{{ p.pickup_time }}</span></td>
                <td>{{ p.pickup_location }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 3. Itinerary -->
        <div class="section-card" v-if="itineraries.length">
          <h3 class="section-title">🗺️ Itinerary</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th style="width:22%">Time</th>
                <th style="width:38%">Place</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in itineraries" :key="item.job_itinerary_id">
                <td><span class="time-badge">{{ item.start_time }} – {{ item.end_time }}</span></td>
                <td>{{ item.place_name }}</td>
                <td class="text-muted">{{ item.note || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 4. Passengers -->
        <div class="section-card" v-if="passengers.length">
          <h3 class="section-title">🧍 Passengers <span class="count-badge">{{ passengers.length }}</span></h3>
          <table class="data-table">
            <thead>
              <tr>
                <th style="width:18%">Pickup Time</th>
                <th>Name</th>
                <th style="width:28%">Hotel</th>
                <th style="width:20%">Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in passengers" :key="p.job_passenger_id">
                <td><span class="time-badge">{{ formatPickupTime(p.pickup_time) }}</span></td>
                <td>{{ p.first_name }} {{ p.last_name }}</td>
                <td>{{ p.hotel_name || '-' }}</td>
                <td class="text-muted">{{ p.note || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 5. Inclusions -->
        <div class="section-card" v-if="inclusions.length">
          <h3 class="section-title">📋 Inclusions</h3>
          <div class="two-col">
            <div>
              <p class="col-label">✅ Included</p>
              <div class="inclusion-list">
                <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'INCLUDED')"
                  :key="inc.job_inclusion_id" class="inclusion-item green">{{ inc.description }}</div>
                <div v-if="!inclusions.filter(i => i.inclusion_type === 'INCLUDED').length" class="empty-val">-</div>
              </div>
            </div>
            <div>
              <p class="col-label">❌ Not Included</p>
              <div class="inclusion-list">
                <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED')"
                  :key="inc.job_inclusion_id" class="inclusion-item red">{{ inc.description }}</div>
                <div v-if="!inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED').length" class="empty-val">-</div>
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
                <th style="width:15%">Thai</th>
                <th style="width:15%">Foreigner</th>
                <th style="width:25%">Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="fee in entranceFees" :key="fee.job_entrance_fee_id">
                <td>{{ fee.place_name }}</td>
                <td>{{ fee.thai_price > 0 ? '฿' + Number(fee.thai_price).toLocaleString() : 'Free' }}</td>
                <td>{{ fee.foreigner_price > 0 ? '฿' + Number(fee.foreigner_price).toLocaleString() : 'Free' }}</td>
                <td class="text-muted">{{ fee.note || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 7. Expenses -->
        <div class="section-card" v-if="expenses.length">
          <h3 class="section-title">💰 Expenses</h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Item</th>
                <th style="width:25%">Amount</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="e in expenses" :key="e.job_expense_id">
                <td>{{ e.item_name }}</td>
                <td>{{ e.amount ? '฿' + Number(e.amount).toLocaleString() : '-' }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="total-row">
                <td><strong>Total</strong></td>
                <td><strong>฿{{ Number(expenses.reduce((s, e) => s + Number(e.amount || 0), 0)).toLocaleString() }}</strong></td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- 8. Customers -->
        <div class="section-card" v-if="customers.length">
          <h3 class="section-title">👥 Customers <span class="count-badge">{{ customers.length }}</span></h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Note</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in customers" :key="c.job_customer_id">
                <td>{{ c.customer_name }}</td>
                <td class="text-muted">{{ c.note || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 9. Applications -->
        <div class="section-card" v-if="applications.length">
          <h3 class="section-title">📨 Applications <span class="count-badge">{{ applications.length }}</span></h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Freelancer</th>
                <th style="width:15%">Status</th>
                <th style="width:22%">Applied At</th>
                <th style="width:22%">Selected At</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.job_application_id">
                <td>{{ getFreelancerName(app.fl_id) }}</td>
                <td>
                  <span class="tag" :class="{
                    green: app.application_status === 'ACCEPTED',
                    red: app.application_status === 'REJECTED',
                    gray: app.application_status === 'APPLIED'
                  }">{{ app.application_status }}</span>
                </td>
                <td class="text-muted">{{ formatDateTime(app.applied_at) }}</td>
                <td class="text-muted">{{ app.selected_at ? formatDateTime(app.selected_at) : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 10. Payment -->
        <div class="section-card" v-if="payments.length">
          <h3 class="section-title">💳 Payment</h3>
          <div v-for="pay in payments" :key="pay.payment_id" class="payment-card">
            <div class="mini-grid">
              <div class="mini-item"><label>Status</label>
                <span class="tag" :class="{
                  green: pay.payment_status === 'CONFIRMED',
                  orange: pay.payment_status === 'PAID',
                  red: pay.payment_status === 'REJECTED',
                  gray: pay.payment_status === 'PENDING'
                }">{{ pay.payment_status }}</span>
              </div>
              <div class="mini-item"><label>Freelancer</label>
                <span>{{ getFreelancerName(pay.fl_id) }}</span>
              </div>
              <div class="mini-item" v-if="pay.paid_at"><label>Paid At</label>
                <span class="text-muted">{{ formatDateTime(pay.paid_at) }}</span>
              </div>
              <div class="mini-item" v-if="pay.confirmed_at"><label>Confirmed At</label>
                <span class="text-muted">{{ formatDateTime(pay.confirmed_at) }}</span>
              </div>
              <div class="mini-item" v-if="pay.reject_reason"><label>Reject Reason</label>
                <span class="text-muted">{{ pay.reject_reason }}</span>
              </div>
              <div class="mini-item" v-if="pay.slip_url"><label>Slip</label>
                <a :href="pay.slip_url" target="_blank" class="link">View Slip →</a>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div v-else class="loading">Job not found.</div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="mini-modal" style="text-align:center; padding:32px;">
        <div style="font-size:36px; margin-bottom:12px;">🗑</div>
        <h3 style="margin:0 0 12px;">Delete Job</h3>
        <p style="color:#555; margin:0 0 8px; line-height:1.5;">Are you sure you want to delete<br><strong>"{{ job?.job_title }}"</strong>?</p>
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const route = useRoute()
const router = useRouter()
const job = ref(null)
const languages = ref([])
const pickups = ref([])
const itineraries = ref([])
const passengers = ref([])
const inclusions = ref([])
const entranceFees = ref([])
const expenses = ref([])
const customers = ref([])
const applications = ref([])
const payments = ref([])
const allFreelancers = ref([])
const loading = ref(true)
const showDeleteModal = ref(false)

const freelancerName = computed(() => {
  if (!job.value?.selected_fl_id) return null
  const fl = allFreelancers.value.find(f => f.fl_id === job.value.selected_fl_id)
  return fl?.fl_name || job.value.selected_fl_id
})

const getFreelancerName = (id) => {
  if (!id) return '-'
  const fl = allFreelancers.value.find(f => f.fl_id === id)
  return fl?.fl_name || id
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const formatPickupTime = (val) => {
  if (!val) return '-'
  // Handle integer seconds-since-midnight (e.g. 29700 = 08:15)
  if (typeof val === 'number' || /^\d+$/.test(String(val))) {
    const secs = Number(val)
    const h = Math.floor(secs / 3600)
    const m = Math.floor((secs % 3600) / 60)
    return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`
  }
  return val
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
      jobsRes, langRes, pickupsRes, itinRes, passRes,
      inclRes, feesRes, expRes, custRes, appRes, payRes, flRes
    ] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/job-required-languages?limit=500`),
      fetch(`${API_BASE}/job-pickups?limit=500`),
      fetch(`${API_BASE}/job-itineraries?limit=500`),
      fetch(`${API_BASE}/job-passengers?limit=500`),
      fetch(`${API_BASE}/job-inclusions?limit=500`),
      fetch(`${API_BASE}/job-entrance-fees?limit=500`),
      fetch(`${API_BASE}/job-expenses?limit=500`),
      fetch(`${API_BASE}/job-customers?limit=500`),
      fetch(`${API_BASE}/job-applications?limit=500`),
      fetch(`${API_BASE}/job-payments?limit=500`),
      fetch(`${API_BASE}/freelancers?limit=500`),
    ])

    const [
      jobsData, langData, pickupsData, itinData, passData,
      inclData, feesData, expData, custData, appData, payData, flData
    ] = await Promise.all([
      jobsRes.json(), langRes.json(), pickupsRes.json(), itinRes.json(), passRes.json(),
      inclRes.json(), feesRes.json(), expRes.json(), custRes.json(), appRes.json(), payRes.json(), flRes.json(),
    ])

    job.value          = (jobsData.items    || []).find(j => j.job_id === id) || null
    languages.value    = (langData.items    || []).filter(l => l.job_id === id)
    pickups.value      = (pickupsData.items || []).filter(p => p.job_id === id).sort((a, b) => a.sequence - b.sequence)
    itineraries.value  = (itinData.items    || []).filter(i => i.job_id === id)
    passengers.value   = (passData.items    || []).filter(p => p.job_id === id)
    inclusions.value   = (inclData.items    || []).filter(i => i.job_id === id).sort((a, b) => a.sequence - b.sequence)
    entranceFees.value = (feesData.items    || []).filter(f => f.job_id === id).sort((a, b) => a.sequence - b.sequence)
    expenses.value     = (expData.items     || []).filter(e => e.job_id === id).sort((a, b) => a.sequence - b.sequence)
    customers.value    = (custData.items    || []).filter(c => c.job_id === id)
    applications.value = (appData.items     || []).filter(a => a.job_id === id)
    payments.value     = (payData.items     || []).filter(p => p.job_id === id)
    allFreelancers.value = flData.items || []
  } catch (e) {
    console.error('Failed to load job detail:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
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
  display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;
}
.hero-left { display: flex; flex-direction: column; gap: 8px; flex: 1; padding-right: 24px; }
.job-title { font-size: 5px; margin: 0; color: #111; }
.company { color: #666; margin: 0; font-size: 14px; }
.job-desc { color: #888; font-size: 13px; line-height: 1.6; margin: 0; }
.price-box { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; flex-shrink: 0; }
.price-label { font-size: 11px; color: #999; font-weight: 600; text-transform: uppercase; }
.price-value { font-size: 26px; font-weight: 700; color: #111; }

/* Sections */
.sections { display: flex; flex-direction: column; gap: 16px; }
.section-card { background: white; border-radius: 12px; padding: 24px; }
.section-title {
  font-size: 14px; font-weight: 600; color: #444;
  margin: 0 0 20px; padding-bottom: 12px; border-bottom: 1px solid #eee;
  display: flex; align-items: center; gap: 8px;
}
.count-badge {
  display: inline-flex; align-items: center; justify-content: center;
  background: #f0f4ff; color: #3d5afe; border-radius: 20px;
  font-size: 11px; font-weight: 700; padding: 2px 8px;
}

/* Mini Grid */
.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.mini-item { display: flex; flex-direction: column; gap: 4px; }
.mini-item label { font-size: 10px; color: #999; font-weight: 600; text-transform: uppercase; }
.mini-item span { font-size: 13px; color: #222; }
.text-muted { color: #888 !important; font-size: 12px !important; }
.empty-val { font-size: 13px; color: #ccc; }
.link { color: #0066cc; font-size: 13px; }

/* Tags */
.tag-row { display: flex; flex-wrap: wrap; gap: 6px; }
.tag { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.tag.blue { background: #e3f2fd; color: #1976d2; }
.tag.green { background: #f0fdf4; color: #166534; }
.tag.orange { background: #fff3e0; color: #f57c00; }
.tag.red { background: #fef2f2; color: #991b1b; }
.tag.gray { background: #f5f5f5; color: #666; }

/* Table */
.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th {
  text-align: left; font-size: 11px; font-weight: 600; color: #999;
  text-transform: uppercase; padding: 8px 12px; border-bottom: 2px solid #eee;
}
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f5f5f5; color: #333; }
.data-table tr:last-child td { border-bottom: none; }
.total-row td {
  background: #f9f9f9; font-weight: 600;
  border-top: 2px solid #eee !important; color: #111; border-bottom: none !important;
}

.time-badge {
  display: inline-block; padding: 3px 8px; border-radius: 6px;
  background: #f0f4ff; color: #3d5afe; font-size: 12px; font-weight: 700; white-space: nowrap;
}

/* Inclusions */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.col-label { font-size: 12px; font-weight: 600; color: #666; margin: 0 0 10px; }
.inclusion-list { display: flex; flex-direction: column; gap: 6px; }
.inclusion-item { padding: 8px 12px; border-radius: 6px; font-size: 14px; }
.inclusion-item.green { background: #f0fdf4; color: #166534; }
.inclusion-item.red { background: #fef2f2; color: #991b1b; }

/* Payment */
.payment-card {
  padding: 16px; background: #fafafa; border-radius: 8px; border: 1px solid #eee;
}

/* Badge */
.badge {
  display: inline-block; padding: 4px 12px;
  border-radius: 12px; font-size: 12px; font-weight: 600; width: fit-content;
}
.badge.open { background: #e3f2fd; color: #1976d2; }
.badge.matching { background: #e0f2f1; color: #00695c; }
.badge.selected { background: #f3e5f5; color: #7b1fa2; }
.badge.in_progress { background: #fff3e0; color: #f57c00; }
.badge.completed { background: #f5f5f5; color: #666; }
.badge.cancelled { background: #ffebee; color: #c62828; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center; z-index: 100;
}
.mini-modal { background: white; border-radius: 12px; padding: 24px; width: 460px; max-height: 80vh; overflow-y: auto; }
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