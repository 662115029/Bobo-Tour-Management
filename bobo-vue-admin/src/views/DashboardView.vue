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
              {{ job.job_title }}
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
    <div v-if="jobModal" class="modal-overlay" @click.self="jobModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header">
          <button class="close-btn" @click="jobModal = null" style="margin-left:auto">✕</button>
        </div>
        <div class="profile-hero">
          <div class="w-12 h-12 rounded-xl flex items-center justify-center text-lg font-bold ring-2 ring-[#eee] flex-shrink-0" style="background:#f0f4ff;color:#3b5bdb;">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 00-2-2h-4a2 2 0 00-2 2v2"/></svg>
          </div>
          <div class="profile-info">
            <h3 class="profile-name">{{ jobModal.job_title }}</h3>
            <p class="profile-bio" :class="{ muted: !jobModal.job_description }">{{ jobModal.job_description || 'No description' }}</p>
          </div>
        </div>
        <div class="mini-grid">
          <div class="mini-item">
            <label>Status</label>
            <span class="badge" :class="jobModal.job_status?.toLowerCase()">{{
              jobModal.job_status
            }}</span>
          </div>
          <div class="mini-item">
            <label>Price</label>
            <span>{{
              jobModal.job_price
                ? "฿" + Number(jobModal.job_price).toLocaleString()
                : "-"
            }}</span>
          </div>
          <div class="mini-item">
            <label>Job Start</label>
            <span>{{ formatDate(jobModal.job_start_date) }}</span>
          </div>
          <div class="mini-item">
            <label>Job End</label>
            <span>{{ formatDate(jobModal.job_end_date) }}</span>
          </div>
          <div class="mini-item">
            <label>Vehicle</label>
            <span>{{ jobModal.job_required_vehicle_type || "-" }}</span>
          </div>
          <div class="mini-item">
            <label>Seats</label>
            <span>{{ jobModal.job_required_seat || "-" }}</span>
          </div>
          <div class="mini-item">
            <label>Company</label>
            <div class="user-cell" style="gap:5px;">
              <span class="user-avatar" style="width:18px;height:18px;font-size:9px;flex-shrink:0;" :style="avatarStyle(jobModal.em_id, jobModal.company)">{{ initials2(jobModal.company) }}</span>
              <span>{{ jobModal.company || "-" }}</span>
            </div>
          </div>
          <div class="mini-item">
            <label>Freelancer</label>
            <span>{{
              jobModal.selected_fl_id
                ? (allFreelancers.find(f => f.fl_id === jobModal.selected_fl_id)?.fl_name || jobModal.selected_fl_id)
                : '-'
            }}</span>
          </div>
          <div class="mini-item">
            <label>Created</label>
            <span class="text-muted">{{
              formatDateTime(jobModal.job_created_at)
            }}</span>
          </div>
          <div class="mini-item">
            <label>Last Updated</label>
            <span class="text-muted">{{
              formatDateTime(jobModal.job_updated_at)
            }}</span>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="viewJob(jobModal.job_id); jobModal = null;">
            View Full Detail →
          </button>
        </div>
      </div>
    </div>

    <!-- Company Mini Modal -->
    <div
      v-if="companyModal"
      class="modal-overlay"
      @click.self="companyModal = null"
    >
      <div class="mini-modal">
        <div
          class="mini-modal-header"
          style="justify-content: flex-end; margin-bottom: 8px"
        >
          <button class="close-btn" @click="companyModal = null">✕</button>
        </div>
        <div v-if="companyLoading" class="mini-loading">
          <div v-for="i in 4" :key="'cl-'+i" style="display:flex;gap:10px;padding:10px 0;border-bottom:1px solid #f5f5f5">
            <span class="skeleton skeleton-text" style="flex:1"></span>
            <span class="skeleton skeleton-badge"></span>
            <span class="skeleton skeleton-btn"></span>
          </div>
        </div>
        <div v-else>
          <div class="profile-hero">
            <div class="profile-avatar-wrap">
              <img v-if="companyModal.em_profile_image_url" :src="companyModal.em_profile_image_url" class="w-12 h-12 rounded-full object-cover ring-2 ring-[#eee]" />
              <div v-else class="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold ring-2 ring-[#eee]" :style="avatarStyle(companyModal.em_id, companyModal.em_name)">{{ initials2(companyModal.em_name) }}</div>
            </div>
            <div class="profile-info">
              <h3 class="profile-name">{{ companyModal.em_name }}</h3>
              <p class="profile-bio" :class="{ muted: !companyModal.em_bio }">
                {{ companyModal.em_bio || "No bio" }}
              </p>
            </div>
          </div>
          <div class="mini-grid">
            <div class="mini-item">
              <label>Status</label>
              <span
                class="badge"
                :class="companyModal.em_verify_status?.toLowerCase()"
                >{{ companyModal.em_verify_status }}</span
              >
            </div>
            <div class="mini-item">
              <label>Active</label>
              <div style="display:flex;align-items:center;gap:6px;">
                <div style="width:8px;height:8px;border-radius:50%;" :style="{ background: companyModal.em_is_active ? '#06c755' : '#bbb' }"></div>
                <span :style="{ color: companyModal.em_is_active ? '#2e7d32' : '#999', fontWeight: 500 }">{{ companyModal.em_is_active ? 'Active' : 'Inactive' }}</span>
              </div>
            </div>
            <div class="mini-item">
              <label>Phone</label>
              <span>{{ companyModal.em_phone || "-" }}</span>
            </div>
            <div class="mini-item">
              <label>Rating</label>
              <span>⭐ {{ companyModal.em_rating_avg ?? "-" }}</span>
            </div>
            <div class="mini-item">
              <label>Address</label>
              <span>{{ companyModal.em_address || "-" }}</span>
            </div>
            <div class="mini-item">
              <label>Created</label>
              <span class="text-muted">{{
                formatDateTime(companyModal.em_created_at)
              }}</span>
            </div>
            <div class="mini-item">
              <label>Last Updated</label>
              <span class="text-muted">{{
                formatDateTime(companyModal.em_updated_at)
              }}</span>
            </div>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button
            class="btn-full-view"
            @click="
              router.push({
                name: 'EmployerDetail',
                params: { id: companyModal.em_id },
              });
              companyModal = null;
            "
          >
            View Full Detail →
          </button>
        </div>
      </div>
    </div>

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
                <label>Active</label
                ><span>{{
                  verifyDetail.fl_is_active ? "✅ Active" : "❌ Inactive"
                }}</span>
              </div>
              <div class="mini-item">
                <label>Rating</label
                ><span>⭐ {{ verifyDetail.fl_rating_avg ?? "-" }}</span>
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
                <label>Active</label
                ><span>{{
                  verifyDetail.em_is_active ? "✅ Active" : "❌ Inactive"
                }}</span>
              </div>
              <div class="mini-item">
                <label>Rating</label
                ><span>⭐ {{ verifyDetail.em_rating_avg ?? "-" }}</span>
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

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const router = useRouter();

const AVATAR_PALETTES = [
  { bg: '#e3f2fd', text: '#1565c0' }, { bg: '#fce4ec', text: '#ad1457' },
  { bg: '#e8f5e9', text: '#2e7d32' }, { bg: '#fff3e0', text: '#e65100' },
  { bg: '#f3e5f5', text: '#6a1b9a' }, { bg: '#e0f7fa', text: '#00695c' },
  { bg: '#fff8e1', text: '#f57f17' }, { bg: '#fbe9e7', text: '#bf360c' },
]
const avatarPalette = (id, name) => {
  const str = String(id || name || '?')
  let hash = 0; for (let i = 0; i < str.length; i++) hash = (hash * 31 + str.charCodeAt(i)) >>> 0
  return AVATAR_PALETTES[hash % AVATAR_PALETTES.length]
}
const avatarStyle = (id, name) => {
  const p = avatarPalette(id, name)
  return { backgroundColor: p.bg, color: p.text }
}
const initials2 = (name) => {
  if (!name) return '?'
  const parts = name.trim().split(/\s+/).slice(0, 2)
  return parts.map(p => p[0]?.toUpperCase() || '').join('')
}

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

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
};

const formatDateTime = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
};

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

const openJobModal = (job) => {
  jobModal.value = job;
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