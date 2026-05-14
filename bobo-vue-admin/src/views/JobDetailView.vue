<template>
  <div>
    <BreadcrumbBar />
    <div class="px-5 pb-6">

      <!-- Topbar -->
      <div class="flex items-center justify-between py-3 mb-4">
        <span class="text-sm cursor-pointer" @click="router.back()">← Back to Jobs</span>
        <button v-if="job" class="btn-action delete !px-3 !py-1.5 !text-[13px] !rounded-md"
          @click="showDeleteModal = true">
          🗑 Delete Job
        </button>
      </div>

      <div v-if="loading" class="empty">⏳ Loading...</div>

      <div v-else-if="job">

        <!-- Hero Card -->
        <div class="bg-white rounded-xl p-7 flex justify-between items-start mb-4">
          <div class="flex flex-col gap-2 flex-1 pr-6">
            <span class="badge" :class="job.job_status?.toLowerCase()">{{ job.job_status }}</span>
            <h2 class="text-xl font-semibold text-[#111] mt-1 mb-0">{{ job.job_title }}</h2>
            <p class="text-[#666] text-sm m-0">🏢 {{ job.company }}</p>
            <p v-if="job.job_description" class="text-[#888] text-[13px] leading-relaxed m-0">{{ job.job_description }}
            </p>
          </div>
          <div class="flex flex-col items-end gap-1 shrink-0">
            <span class="text-[11px] text-[#999] font-semibold uppercase tracking-wide">PRICE</span>
            <span class="text-[26px] font-bold text-[#111]">{{ job.job_price ? "฿" +
              Number(job.job_price).toLocaleString() : "-" }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-4">

          <!-- 1. Job Info -->
          <section>
            <h3 class="section-title">📋 Job Info</h3>
            <div class="mini-grid px-5 pt-4">
              <div class="mini-item">
                <label>Languages</label>
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span v-for="lang in languages" :key="lang.job_req_lg_id" class="badge open">{{ lang.language_name
                    }}</span>
                  <span v-if="!languages.length" class="text-[#ccc] text-[13px]">-</span>
                </div>
              </div>
              <div class="mini-item">
                <label>Freelancer</label>
                <span>{{ freelancerName || "Not assigned" }}</span>
              </div>
              <div class="mini-item">
                <label>Job Start</label>
                <span>{{ formatDate(job.job_start_date) }}</span>
              </div>
              <div class="mini-item">
                <label>Job End</label>
                <span>{{ formatDate(job.job_end_date) }}</span>
              </div>
              <div class="mini-item">
                <label>Vehicle</label>
                <span>{{ job.job_required_vehicle_type || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Seats</label>
                <span>{{ job.job_required_seat || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Created</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(job.job_created_at) }}</span>
              </div>
              <div class="mini-item">
                <label>Last Updated</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(job.job_updated_at) }}</span>
              </div>
            </div>
          </section>

          <!-- 2. Pickup Points -->
          <section v-if="pickups.length">
            <h3 class="section-title">📍 Pickup Points</h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:18%">Time</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Location</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in pickups" :key="p.job_pickup_id" class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5">
                      <span
                        class="inline-block px-2 py-0.5 rounded-md bg-[#f0f4ff] text-[#3d5afe] text-[12px] font-bold whitespace-nowrap">{{
                        p.pickup_time }}</span>
                    </td>
                    <td class="px-3 py-2.5 text-[#333]">{{ p.pickup_location }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 3. Itinerary -->
          <section v-if="itineraries.length">
            <h3 class="section-title">🗺️ Itinerary</h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:22%">Time</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:38%">Place</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Note</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in itineraries" :key="item.job_itinerary_id"
                    class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5">
                      <span
                        class="inline-block px-2 py-0.5 rounded-md bg-[#f0f4ff] text-[#3d5afe] text-[12px] font-bold whitespace-nowrap">{{
                        item.start_time }} – {{ item.end_time }}</span>
                    </td>
                    <td class="px-3 py-2.5 text-[#333]">{{ item.place_name }}</td>
                    <td class="px-3 py-2.5 text-muted">{{ item.note || "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 4. Passengers -->
          <section v-if="passengers.length">
            <h3 class="section-title flex items-center gap-2">
              🧍 Passengers
              <span
                class="inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{
                passengers.length }}</span>
            </h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:18%">Pickup Time</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Name</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:28%">Hotel</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:20%">Note</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="p in passengers" :key="p.job_passenger_id" class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5">
                      <span
                        class="inline-block px-2 py-0.5 rounded-md bg-[#f0f4ff] text-[#3d5afe] text-[12px] font-bold whitespace-nowrap">{{
                        formatPickupTime(p.pickup_time) }}</span>
                    </td>
                    <td class="px-3 py-2.5 text-[#333]">{{ p.first_name }} {{ p.last_name }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ p.hotel_name || "-" }}</td>
                    <td class="px-3 py-2.5 text-muted">{{ p.note || "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 5. Inclusions -->
          <section v-if="inclusions.length">
            <h3 class="section-title">📋 Inclusions</h3>
            <div class="px-5 pt-4 grid grid-cols-2 gap-5">
              <div>
                <p class="text-xs font-semibold text-[#666] mb-2.5">✅ Included</p>
                <div class="flex flex-col gap-1.5">
                  <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'INCLUDED')"
                    :key="inc.job_inclusion_id" class="px-3 py-2 rounded-md text-sm bg-[#f0fdf4] text-[#166534]">{{
                    inc.description }}</div>
                  <div v-if="!inclusions.filter(i => i.inclusion_type === 'INCLUDED').length"
                    class="text-[#ccc] text-[13px]">-</div>
                </div>
              </div>
              <div>
                <p class="text-xs font-semibold text-[#666] mb-2.5">❌ Not Included</p>
                <div class="flex flex-col gap-1.5">
                  <div v-for="inc in inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED')"
                    :key="inc.job_inclusion_id" class="px-3 py-2 rounded-md text-sm bg-[#fef2f2] text-[#991b1b]">{{
                    inc.description }}</div>
                  <div v-if="!inclusions.filter(i => i.inclusion_type === 'NOT_INCLUDED').length"
                    class="text-[#ccc] text-[13px]">-</div>
                </div>
              </div>
            </div>
          </section>

          <!-- 6. Entrance Fees -->
          <section v-if="entranceFees.length">
            <h3 class="section-title">🎫 Entrance Fees</h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Place</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:15%">Thai</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:15%">Foreigner</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:25%">Note</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fee in entranceFees" :key="fee.job_entrance_fee_id"
                    class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ fee.place_name }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ fee.thai_price > 0 ? "฿" +
                      Number(fee.thai_price).toLocaleString() : "Free" }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ fee.foreigner_price > 0 ? "฿" +
                      Number(fee.foreigner_price).toLocaleString() : "Free" }}</td>
                    <td class="px-3 py-2.5 text-muted">{{ fee.note || "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 7. Expenses -->
          <section v-if="expenses.length">
            <h3 class="section-title">💰 Expenses</h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Item</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:25%">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="e in expenses" :key="e.job_expense_id" class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ e.item_name }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ e.amount ? "฿" + Number(e.amount).toLocaleString() : "-" }}
                    </td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr class="border-t-2 border-[#eee]">
                    <td class="px-3 py-2.5 font-semibold text-[#111]">Total</td>
                    <td class="px-3 py-2.5 font-semibold text-[#111]">฿{{Number(expenses.reduce((s, e) => s +
                      Number(e.amount || 0), 0)).toLocaleString() }}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </section>

          <!-- 8. Customers -->
          <section v-if="customers.length">
            <h3 class="section-title flex items-center gap-2">
              👥 Customers
              <span
                class="inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{
                customers.length }}</span>
            </h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Name</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Note</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="c in customers" :key="c.job_customer_id" class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ c.customer_name }}</td>
                    <td class="px-3 py-2.5 text-muted">{{ c.note || "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 9. Applications -->
          <section v-if="applications.length">
            <h3 class="section-title flex items-center gap-2">
              📨 Applications
              <span
                class="inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{
                applications.length }}</span>
            </h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Freelancer</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:15%">Status</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:22%">Applied At</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:22%">Selected At</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="app in applications" :key="app.job_application_id"
                    class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ getFreelancerName(app.fl_id) }}</td>
                    <td class="px-3 py-2.5">
                      <span class="badge" :class="{
                        verified: app.application_status === 'ACCEPTED',
                        cancelled: app.application_status === 'REJECTED',
                        unknown: app.application_status === 'APPLIED',
                      }">{{ app.application_status }}</span>
                    </td>
                    <td class="px-3 py-2.5 text-muted text-[12px]">{{ formatDateTime(app.applied_at) }}</td>
                    <td class="px-3 py-2.5 text-muted text-[12px]">{{ app.selected_at ? formatDateTime(app.selected_at)
                      : "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 10. Payment -->
          <section v-if="payments.length">
            <h3 class="section-title">💳 Payment</h3>
            <div class="px-5 pt-4 flex flex-col gap-3">
              <div v-for="pay in payments" :key="pay.payment_id"
                class="p-4 bg-[#fafafa] rounded-lg border border-[#eee]">
                <div class="mini-grid">
                  <div class="mini-item">
                    <label>Status</label>
                    <span class="badge" :class="{
                      verified: pay.payment_status === 'CONFIRMED',
                      in_progress: pay.payment_status === 'PAID',
                      cancelled: pay.payment_status === 'REJECTED',
                      unknown: pay.payment_status === 'PENDING',
                    }">{{ pay.payment_status }}</span>
                  </div>
                  <div class="mini-item">
                    <label>Freelancer</label>
                    <span>{{ getFreelancerName(pay.fl_id) }}</span>
                  </div>
                  <div class="mini-item" v-if="pay.paid_at">
                    <label>Paid At</label>
                    <span class="text-muted text-[12px]">{{ formatDateTime(pay.paid_at) }}</span>
                  </div>
                  <div class="mini-item" v-if="pay.confirmed_at">
                    <label>Confirmed At</label>
                    <span class="text-muted text-[12px]">{{ formatDateTime(pay.confirmed_at) }}</span>
                  </div>
                  <div class="mini-item" v-if="pay.reject_reason">
                    <label>Reject Reason</label>
                    <span class="text-muted text-[12px]">{{ pay.reject_reason }}</span>
                  </div>
                  <div class="mini-item" v-if="pay.slip_url">
                    <label>Slip</label>
                    <a :href="pay.slip_url" target="_blank" class="text-[#0066cc] text-[13px]">View Slip →</a>
                  </div>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>

      <div v-else class="empty">Job not found.</div>

      <!-- Delete Modal -->
      <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
        <div class="modal">
          <div class="modal-icon">🗑</div>
          <h3>Delete Job</h3>
          <p>Are you sure you want to delete<br /><strong>"{{ job?.job_title }}"</strong>?</p>
          <p class="modal-warning">This action cannot be undone.</p>
          <div class="modal-actions">
            <button class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
            <button class="btn-confirm-delete" @click="confirmDelete">Delete</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { API_BASE } from "../data/api";

const route = useRoute();
const router = useRouter();
const job = ref(null);
const languages = ref([]);
const pickups = ref([]);
const itineraries = ref([]);
const passengers = ref([]);
const inclusions = ref([]);
const entranceFees = ref([]);
const expenses = ref([]);
const customers = ref([]);
const applications = ref([]);
const payments = ref([]);
const allFreelancers = ref([]);
const loading = ref(true);
const showDeleteModal = ref(false);
const jobTitle = history.state.jobTitle || "Job Detail";

const freelancerName = computed(() => {
  if (!job.value?.selected_fl_id) return null;
  const fl = allFreelancers.value.find((f) => f.fl_id === job.value.selected_fl_id);
  return fl?.fl_name || job.value.selected_fl_id;
});

const getFreelancerName = (id) => {
  if (!id) return "-";
  const fl = allFreelancers.value.find((f) => f.fl_id === id);
  return fl?.fl_name || id;
};

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
};

const formatDateTime = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString("en-GB", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
};

const formatPickupTime = (val) => {
  if (!val) return "-";
  if (typeof val === "number" || /^\d+$/.test(String(val))) {
    const secs = Number(val);
    const h = Math.floor(secs / 3600);
    const m = Math.floor((secs % 3600) / 60);
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}`;
  }
  return val;
};

const confirmDelete = async () => {
  try {
    await fetch(`${API_BASE}/jobs/${job.value.job_id}`, { method: "DELETE" });
    router.push({ name: "Jobs" });
  } catch (e) {
    console.error("Failed to delete job:", e);
  } finally {
    showDeleteModal.value = false;
  }
};

onMounted(async () => {
  const id = route.params.id;
  try {
    const [jobsRes, langRes, pickupsRes, itinRes, passRes, inclRes, feesRes, expRes, custRes, appRes, payRes, flRes] = await Promise.all([
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
    ]);
    const [jobsData, langData, pickupsData, itinData, passData, inclData, feesData, expData, custData, appData, payData, flData] = await Promise.all([
      jobsRes.json(), langRes.json(), pickupsRes.json(), itinRes.json(), passRes.json(),
      inclRes.json(), feesRes.json(), expRes.json(), custRes.json(), appRes.json(), payRes.json(), flRes.json(),
    ]);
    job.value = (jobsData.items || []).find((j) => j.job_id === id) || null;
    languages.value = (langData.items || []).filter((l) => l.job_id === id);
    pickups.value = (pickupsData.items || []).filter((p) => p.job_id === id).sort((a, b) => a.sequence - b.sequence);
    itineraries.value = (itinData.items || []).filter((i) => i.job_id === id);
    passengers.value = (passData.items || []).filter((p) => p.job_id === id);
    inclusions.value = (inclData.items || []).filter((i) => i.job_id === id).sort((a, b) => a.sequence - b.sequence);
    entranceFees.value = (feesData.items || []).filter((f) => f.job_id === id).sort((a, b) => a.sequence - b.sequence);
    expenses.value = (expData.items || []).filter((e) => e.job_id === id).sort((a, b) => a.sequence - b.sequence);
    customers.value = (custData.items || []).filter((c) => c.job_id === id);
    applications.value = (appData.items || []).filter((a) => a.job_id === id);
    payments.value = (payData.items || []).filter((p) => p.job_id === id);
    allFreelancers.value = flData.items || [];
  } catch (e) {
    console.error("Failed to load job detail:", e);
  } finally {
    loading.value = false;
  }
});
</script>