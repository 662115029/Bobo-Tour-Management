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
            <th style="width: 16%">COMPANY</th>
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
          <tr
            v-else
            v-for="job in jobs.slice(0, 10)"
            :key="job.job_id"
            class="row-hover"
          >
            <td class="truncate-cell clickable-cell" @click="openJobModal(job)">
              <div class="user-cell">
                <span class="user-avatar" :style="jobIconStyle(job.job_id)" style="border-radius:6px;flex-shrink:0;">
                  <svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/><path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/></svg>
                </span>
                {{ job.job_title }}
              </div>
            </td>
            <td
              class="truncate-cell clickable-cell"
              @click="openCompanyModal(job)"
            >
              <div class="user-cell">
                <span class="user-avatar" :style="avatarStyle(job.em_id, job.company)">{{ initials2(job.company) }}</span>
                {{ job.company }}
              </div>
            </td>
            <td>
              {{
                job.job_price
                  ? "฿" + Number(job.job_price).toLocaleString()
                  : "-"
              }}
            </td>
            <td>
              <span class="badge" :class="job.job_status?.toLowerCase()">{{
                formatJobStatus(job.job_status)
              }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewJob(job.job_id)">
                  View
                </button>
                <button
                  class="btn-action delete"
                  @click="deleteJob(job.job_id, job.job_title)"
                >
                  Delete
                </button>
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
          <tr
            v-else
            v-for="v in verifications.slice(0, 10)"
            :key="v.id"
            class="row-hover"
          >
            <td
              class="truncate-cell clickable-cell"
              @click="openVerifyModal(v)"
            >
              <div class="user-cell">
                <span class="user-avatar" :style="avatarStyle(v.id, v.name)">{{ initials2(v.name) }}</span>
                {{ v.name }}
              </div>
            </td>
            <td>
              <span class="type-tag" :class="getTypeClass(v.type)">{{
                v.type
              }}</span>
            </td>
            <td>
              <span class="badge" :class="v.status?.toLowerCase()">{{
                v.status
              }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action verify-style" @click="openVerifyDocs(v)">
                  View Docs
                </button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(v.updated_at) }}</td>
          </tr>
        </tbody>
      </table>
      </section>
    </div>

    <!-- Job Mini Modal -->
    <JobMiniModal
      :data="jobModal"
      @close="jobModal = null"
      @view-detail="(id) => { viewJob(id); jobModal = null }"
    />

    <!-- Company Mini Modal -->
    <UserMiniModal
      :data="companyModal"
      type="EMPLOYER"
      :loading="companyLoading"
      @close="companyModal = null"
      @view-detail="({ id }) => { router.push({ name: 'EmployerDetail', params: { id } }); companyModal = null }"
    />

    <!-- Verification Mini Modal -->
    <UserMiniModal
      :data="verifyDetailMapped"
      :type="verifyModal?.type === 'Freelancer' ? 'FREELANCER' : 'EMPLOYER'"
      :loading="verifyLoading"
      @close="verifyModal = null; verifyDetail = null"
      @view-detail="goToVerifyDetail"
    />
    <!-- Delete Modal -->
    <DeleteJobModal :show="showDeleteModal" :title="deleteTargetTitle"
      @confirm="confirmDelete" @cancel="showDeleteModal = false" />

    <!-- Verification Documents Modal -->
    <DocReviewModal
      :user="selectedVerifyUser"
      :docs="selectedVerifyDocs"
      @close="selectedVerifyUser = null"
      @approve="(doc) => reviewVerifyDoc(doc, 'APPROVED')"
      @reject="(doc) => reviewVerifyDoc(doc, 'REJECTED')"
    />
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
import BreadcrumbBar from '../components/BreadcrumbBar.vue';
import { useRouter } from "vue-router";
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime, groupDocsByLatest } from '../utils/formatDate'
import { formatJobStatus, getTypeClass } from '../utils/statusClasses'
import JobMiniModal from '../components/JobMiniModal.vue'
import UserMiniModal from '../components/UserMiniModal.vue'
import DeleteJobModal from '../components/DeleteJobModal.vue'
import DocReviewModal from '../components/DocReviewModal.vue'
import { API_BASE } from '../data/api'
import { useStats } from '../composables/useStats'

const { avatarStyle, jobIconStyle, initials2 } = useAvatar()

const router = useRouter();

const { stats, loadStats } = useStats();
const localTotalJobs = ref(0);
watch(() => stats.value.totalJobs, (val) => { localTotalJobs.value = val }, { immediate: true })
const isLoading = ref(true);
const jobs = ref([]);
const verifications = ref([]);
const allEmployers = ref([]);
const allFreelancers = ref([]);
const flDocs = ref([]);
const emDocs = ref([]);
const selectedVerifyUser = ref(null);
const selectedVerifyDocs = ref([]);

const showDeleteModal = ref(false);
const deleteTargetId = ref(null);
const deleteTargetTitle = ref("");

const jobModal = ref(null);
const companyModal = ref(null);
const companyLoading = ref(false);
const verifyModal = ref(null);
const verifyDetail = ref(null);
const verifyLoading = ref(false);

const viewJob = (id) => router.push({ name: "JobDetail", params: { id } });

const deleteJob = (id, title) => {
  deleteTargetId.value = id;
  deleteTargetTitle.value = title;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  const id = deleteTargetId.value;
  const title = deleteTargetTitle.value;
  try {
    const adminId = localStorage.getItem('admin_id') || '';
    const res = await fetch(`${API_BASE}/jobs/${id}?admin_id=${adminId}`, {
      method: "DELETE",
    });
    if (res.ok) {
      jobs.value = jobs.value.filter((j) => j.job_id !== id);
      localTotalJobs.value = Math.max(0, localTotalJobs.value - 1);
    } else {
      console.error("Delete failed:", res.status);
    }
  } catch (e) {
    console.error("Failed to delete job:", e);
  } finally {
    showDeleteModal.value = false;
    deleteTargetId.value = null;
    deleteTargetTitle.value = "";
  }
};

const allLanguages = ref([])

const openJobModal = async (job) => {
  if (!allLanguages.value.length) {
    try {
      const res = await fetch(`${API_BASE}/job-required-languages?limit=500`)
      const data = await res.json()
      allLanguages.value = data.items || []
    } catch {}
  }
  const langs = allLanguages.value
    .filter(l => l.job_id === job.job_id)
    .map(l => l.language_name)
  jobModal.value = { ...job, languages: langs }
};

const openCompanyModal = async (job) => {
  companyLoading.value = true;
  companyModal.value = { em_name: job.company };
  const em = allEmployers.value.find((e) => e.em_id === job.em_id);
  companyModal.value = em || { em_name: job.company };
  companyLoading.value = false;
};

const openVerifyModal = async (v) => {
  verifyModal.value = v;
  verifyDetail.value = null;
  verifyLoading.value = true;
  try {
    if (v.type === "Freelancer") {
      const fl = allFreelancers.value.find((f) => f.fl_id === v.id) || null;
      if (fl) {
        const flJobs = jobs.value.filter(j => j.selected_fl_id === fl.fl_id);
        verifyDetail.value = {
          ...fl,
          fl_total_jobs: flJobs.length,
          fl_completed_jobs: flJobs.filter(j => j.job_status === 'COMPLETED').length,
        };
      }
    } else {
      const em = allEmployers.value.find((e) => e.em_id === v.id) || null;
      if (em) {
        const emJobs = jobs.value.filter(j => j.em_id === em.em_id);
        verifyDetail.value = {
          ...em,
          em_total_jobs: emJobs.length,
          em_completed_jobs: emJobs.filter(j => j.job_status === 'COMPLETED').length,
        };
      }
    }
  } finally {
    verifyLoading.value = false;
  }
};

const verifyDetailMapped = computed(() => {
  if (!verifyDetail.value || !verifyModal.value) return null;
  return verifyDetail.value;
});

const goToVerifyDetail = () => {
  if (!verifyModal.value) return;
  if (verifyModal.value.type === "Freelancer") {
    router.push({
      name: "FreelancerDetail",
      params: { id: verifyModal.value.id },
    });
  } else {
    router.push({
      name: "EmployerDetail",
      params: { id: verifyModal.value.id },
    });
  }
  verifyModal.value = null;
};

const openVerifyDocs = (v) => {
  selectedVerifyUser.value = v;
  if (v.type === "Freelancer") {
    const allDocs = flDocs.value.filter((d) => d.fl_id === v.id);
    selectedVerifyDocs.value = groupDocsByLatest(allDocs, 'fl', formatDateTime);
  } else {
    const allDocs = emDocs.value.filter((d) => d.em_id === v.id);
    selectedVerifyDocs.value = groupDocsByLatest(allDocs, 'em', formatDateTime);
  }
};

const reviewVerifyDoc = async (doc, newStatus) => {
  const endpoint =
    doc._type === "fl"
      ? `${API_BASE}/fl-documents/${doc.id}`
      : `${API_BASE}/em-documents/${doc.id}`;
  try {
    const res = await fetch(endpoint, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus, reviewed_by: localStorage.getItem("admin_id") || "" }),
    });
    const data = await res.json();
    if (data.status === "updated") {
      doc.status = newStatus;
      doc.reviewed = formatDateTime(new Date().toISOString());
    }
  } catch (e) {
    console.error("Failed to review doc:", e);
  }
};

onMounted(async () => {
  try {
    const pingRes = await fetch(`${API_BASE}/admin/db/ping`);
    const ping = await pingRes.json();
    if (!ping.connected) console.error("DB error:", ping.error);
  } catch (e) {
    console.error(e);
  }

  try {
    const jobsRes = await fetch(`${API_BASE}/jobs?limit=500`);
    const jobsData = await jobsRes.json();
    jobs.value = jobsData.items || [];
  } catch {}

  try {
    const [flRes, emRes, flDocRes, emDocRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
      fetch(`${API_BASE}/em-documents?limit=500`),
    ]);
    const flData = await flRes.json();
    const emData = await emRes.json();
    const flDocData = await flDocRes.json();
    const emDocData = await emDocRes.json();
    allFreelancers.value = flData.items || [];
    allEmployers.value = emData.items || [];
    flDocs.value = flDocData.items || [];
    emDocs.value = emDocData.items || [];

    const pendingFl = allFreelancers.value
      .filter((f) => f.fl_verify_status === "PENDING")
      .map((f) => ({
        id: f.fl_id,
        name: f.fl_name || f.line_user_id,
        type: "Freelancer",
        status: f.fl_verify_status,
        created_at: f.fl_created_at,
        updated_at: f.fl_updated_at,
      }));
    const pendingEm = allEmployers.value
      .filter((e) => e.em_verify_status === "PENDING")
      .map((e) => ({
        id: e.em_id,
        name: e.em_name || e.em_username,
        type: "Employer",
        status: e.em_verify_status,
        created_at: e.em_created_at,
        updated_at: e.em_updated_at,
      }));
    verifications.value = [...pendingFl, ...pendingEm];
  } catch {}
  finally {
    isLoading.value = false;
  }
});
</script>