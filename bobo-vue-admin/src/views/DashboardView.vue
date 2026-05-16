<template>
  <div>
    <BreadcrumbBar />
    <div class="stats-row">
      <div class="stat-card">
        <span class="stat-label">TOTAL JOBS</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.totalJobs.toLocaleString() }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">PENDING VERIFY</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.pendingVerify }}</span>
      </div>
      <div class="stat-card">
        <span class="stat-label">FREELANCERS</span>
        <span v-if="isLoading" class="skeleton skeleton-stat"></span>
        <span v-else class="stat-value">{{ stats.freelancers }}</span>
      </div>
      <div class="stat-card">
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
                job.job_status
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
              <span class="type-tag" :class="v.type.toLowerCase()">{{
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
                <button class="btn-action view" @click="openVerifyDocs(v)">
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
    <div
      v-if="verifyModal"
      class="modal-overlay"
      @click.self="verifyModal = null"
    >
      <div class="mini-modal">
        <div
          class="mini-modal-header"
          style="justify-content: flex-end; margin-bottom: 8px"
        >
          <button class="close-btn" @click="verifyModal = null">✕</button>
        </div>
        <div v-if="verifyLoading" class="mini-loading">
  <div v-for="i in 4" :key="'vl-'+i" style="display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #f5f5f5">
    <span class="skeleton skeleton-text" style="flex:1"></span>
    <span class="skeleton skeleton-badge"></span>
    <span class="skeleton skeleton-btn"></span>
  </div>
</div>
        <div v-else>
          <!-- Freelancer -->
          <div v-if="verifyModal.type === 'Freelancer' && verifyDetail">
            <div class="profile-hero">
              <div class="dash-profile-avatar fl">
                <img
                  v-if="verifyDetail.fl_profile_image_url"
                  :src="verifyDetail.fl_profile_image_url"
                  class="avatar-img"
                />
                <span v-else class="dash-avatar-initial">{{
                  verifyDetail.fl_name?.[0] || "?"
                }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ verifyDetail.fl_name }}</h3>
                <p v-if="verifyDetail.fl_bio" class="profile-bio">
                  {{ verifyDetail.fl_bio }}
                </p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item">
                <label>Status</label>
                <span
                  class="badge"
                  :class="verifyDetail.fl_verify_status?.toLowerCase()"
                  >{{ verifyDetail.fl_verify_status }}</span
                >
              </div>
              <div class="mini-item">
                <label>Active</label>
                <div style="display:flex;align-items:center;gap:6px;">
                  <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: verifyDetail.fl_is_active ? '#06c755' : '#bbb' }"></div>
                  <span :style="{ color: verifyDetail.fl_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">{{ verifyDetail.fl_is_active ? 'Active' : 'Inactive' }}</span>
                </div>
              </div>
              <div class="mini-item">
                <label>Rating</label>
                <span class="flex items-center gap-1">
                  <span class="font-semibold text-[#333]">{{ Number(verifyDetail.fl_rating_avg || 0).toFixed(1) }}</span>
                  <svg class="w-3.5 h-3.5 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </span>
              </div>
              <div class="mini-item">
                <label>Date of Birth</label
                ><span>{{ formatDate(verifyDetail.fl_date_of_birth) }}</span>
              </div>
              <div class="mini-item">
                <label>Address</label
                ><span>{{ verifyDetail.fl_address || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Created</label
                ><span class="text-muted">{{
                  formatDateTime(verifyDetail.fl_created_at)
                }}</span>
              </div>
              <div class="mini-item">
                <label>Last Updated</label
                ><span class="text-muted">{{
                  formatDateTime(verifyDetail.fl_updated_at)
                }}</span>
              </div>
            </div>
          </div>
          <!-- Employer -->
          <div v-if="verifyModal.type === 'Employer' && verifyDetail">
            <div class="profile-hero">
              <div class="dash-profile-avatar em">
                <img
                  v-if="verifyDetail.em_profile_image_url"
                  :src="verifyDetail.em_profile_image_url"
                  class="avatar-img"
                />
                <span v-else class="dash-avatar-initial">{{
                  verifyDetail.em_name?.[0] || "?"
                }}</span>
              </div>
              <div class="profile-info">
                <h3 class="profile-name">{{ verifyDetail.em_name }}</h3>
                <p v-if="verifyDetail.em_bio" class="profile-bio">
                  {{ verifyDetail.em_bio }}
                </p>
                <p v-else class="profile-bio muted">No bio</p>
              </div>
            </div>
            <div class="mini-grid">
              <div class="mini-item">
                <label>Status</label>
                <span
                  class="badge"
                  :class="verifyDetail.em_verify_status?.toLowerCase()"
                  >{{ verifyDetail.em_verify_status }}</span
                >
              </div>
              <div class="mini-item">
                <label>Active</label>
                <div style="display:flex;align-items:center;gap:6px;">
                  <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: verifyDetail.em_is_active ? '#06c755' : '#bbb' }"></div>
                  <span :style="{ color: verifyDetail.em_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">{{ verifyDetail.em_is_active ? 'Active' : 'Inactive' }}</span>
                </div>
              </div>
              <div class="mini-item">
                <label>Rating</label>
                <span class="flex items-center gap-1">
                  <span class="font-semibold text-[#333]">{{ Number(verifyDetail.em_rating_avg || 0).toFixed(1) }}</span>
                  <svg class="w-3.5 h-3.5 text-[#f9a825]" fill="currentColor" viewBox="0 0 24 24"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </span>
              </div>
              <div class="mini-item">
                <label>Phone</label
                ><span>{{ verifyDetail.em_phone || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Address</label
                ><span>{{ verifyDetail.em_address || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Created</label
                ><span class="text-muted">{{
                  formatDateTime(verifyDetail.em_created_at)
                }}</span>
              </div>
              <div class="mini-item">
                <label>Last Updated</label
                ><span class="text-muted">{{
                  formatDateTime(verifyDetail.em_updated_at)
                }}</span>
              </div>
            </div>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="goToVerifyDetail">
            View Full Detail →
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div
      v-if="showDeleteModal"
      class="modal-overlay"
      @click.self="showDeleteModal = false"
    >
      <div class="mini-modal" style="text-align: center; padding: 32px">
        <div style="font-size: 36px; margin-bottom: 12px">🗑</div>
        <h3 style="margin: 0 0 12px">Delete Job</h3>
        <p style="color: #555; margin: 0 0 8px">
          Are you sure you want to delete<br /><strong
            >"{{ deleteTargetTitle }}"</strong
          >?
        </p>
        <p style="font-size: 12px; color: #dc3545; margin-bottom: 24px">
          This action cannot be undone.
        </p>
        <div style="display: flex; justify-content: center; gap: 12px">
          <button class="btn-cancel" @click="showDeleteModal = false">
            Cancel
          </button>
          <button class="btn-confirm-delete" @click="confirmDelete">
            Delete
          </button>
        </div>
      </div>
    </div>

    <!-- Verification Documents Modal -->
    <div
      v-if="selectedVerifyUser"
      class="modal-overlay"
      @click.self="selectedVerifyUser = null"
    >
      <div class="docs-modal">
        <div class="modal-header">
          <div>
            <h3>{{ selectedVerifyUser.name }} - Documents</h3>
          </div>
          <button class="close-btn" @click="selectedVerifyUser = null">
            ✕
          </button>
        </div>

        <div v-if="selectedVerifyDocs.length === 0" class="no-docs">
          No documents found.
        </div>

        <div v-else class="doc-list">
          <div v-for="doc in selectedVerifyDocs" :key="doc.id" class="doc-row">
            <div class="doc-type-cell">{{ doc.type }}</div>
            <div class="doc-file-cell">
              <img :src="doc.file_url" class="doc-thumbnail" :alt="doc.type" />
            </div>
            <div class="doc-status-cell">
              <span class="doc-badge" :class="doc.status?.toLowerCase()">{{
                doc.status
              }}</span>
            </div>
            <div class="doc-uploaded-cell">{{ doc.uploaded }}</div>
            <div class="doc-actions-cell">
              <button
                class="btn-approve-row"
                :disabled="doc.status === 'APPROVED'"
                @click="reviewVerifyDoc(doc, 'APPROVED')"
              >
                ✅ Approve
              </button>
              <button
                class="btn-reject-row"
                :disabled="doc.status === 'REJECTED'"
                @click="reviewVerifyDoc(doc, 'REJECTED')"
              >
                ❌ Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import BreadcrumbBar from '../components/BreadcrumbBar.vue';
import { useRouter } from "vue-router";
import { useAvatar } from '../composables/useAvatar'
import { formatDate, formatDateTime } from '../utils/formatDate'
import JobMiniModal from '../components/JobMiniModal.vue'
import UserMiniModal from '../components/UserMiniModal.vue'

const { avatarStyle, jobIconStyle, initials2 } = useAvatar()

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const router = useRouter();

const stats = ref({
  totalJobs: 0,
  pendingVerify: 0,
  freelancers: 0,
  employers: 0,
});
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

// Helper: send log to backend
const logAction = async (action_type, target_type, target_id, target_name, note = null) => {
  const admin_id = localStorage.getItem('admin_id') || '';
  if (!admin_id) return;
  try {
    await fetch(`${API_BASE}/admin/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ admin_id, action_type, target_type, target_id, target_name, note })
    });
  } catch (e) {}
};

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
      stats.value.totalJobs = Math.max(0, stats.value.totalJobs - 1);
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
  if (v.type === "Freelancer") {
    verifyDetail.value =
      allFreelancers.value.find((f) => f.fl_id === v.id) || null;
  } else {
    verifyDetail.value =
      allEmployers.value.find((e) => e.em_id === v.id) || null;
  }
  verifyLoading.value = false;
};

const goToVerifyFull = (v) => {
  if (v.type === "Freelancer") {
    router.push({ name: "FreelancerDetail", params: { id: v.id } });
  } else {
    router.push({ name: "EmployerDetail", params: { id: v.id } });
  }
};

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
    const docsByType = {};
    allDocs.forEach((d) => {
      if (
        !docsByType[d.fl_doc_type] ||
        new Date(d.fl_uploaded_at) >
          new Date(docsByType[d.fl_doc_type].fl_uploaded_at)
      ) {
        docsByType[d.fl_doc_type] = d;
      }
    });
    selectedVerifyDocs.value = Object.values(docsByType).map((d) => ({
      id: d.fl_doc_id,
      type: d.fl_doc_type,
      status: d.fl_doc_status,
      file_url: d.file_url,
      uploaded: formatDateTime(d.fl_uploaded_at),
      reviewed: d.reviewed_at ? formatDateTime(d.reviewed_at) : null,
      _type: "fl",
    }));
  } else {
    const allDocs = emDocs.value.filter((d) => d.em_id === v.id);
    const docsByType = {};
    allDocs.forEach((d) => {
      if (
        !docsByType[d.em_doc_type] ||
        new Date(d.em_uploaded_at) >
          new Date(docsByType[d.em_doc_type].em_uploaded_at)
      ) {
        docsByType[d.em_doc_type] = d;
      }
    });
    selectedVerifyDocs.value = Object.values(docsByType).map((d) => ({
      id: d.em_doc_id,
      type: d.em_doc_type,
      status: d.em_doc_status,
      file_url: d.file_url,
      uploaded: formatDateTime(d.em_uploaded_at),
      reviewed: d.reviewed_at ? formatDateTime(d.reviewed_at) : null,
      _type: "em",
    }));
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
    const res = await fetch(`${API_BASE}/admin/stats`);
    const data = await res.json();
    stats.value.totalJobs = data.totalJobs ?? 0;
    stats.value.pendingVerify = data.pendingVerify ?? 0;
    stats.value.freelancers = data.freelancers ?? 0;
    stats.value.employers = data.employers ?? 0;
  } catch {}

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