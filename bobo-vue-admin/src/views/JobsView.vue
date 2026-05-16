<template>
  <div>
    <BreadcrumbBar />

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search job title..." class="search-input" />
      <div class="filter-group">
        <select v-model="yearFilter" class="filter-select-jobs">
          <option value="All">All Years</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
        <select v-model="monthFilter" class="filter-select-jobs">
          <option value="All">All Months</option>
          <option value="01">January</option>
          <option value="02">February</option>
          <option value="03">March</option>
          <option value="04">April</option>
          <option value="05">May</option>
          <option value="06">June</option>
          <option value="07">July</option>
          <option value="08">August</option>
          <option value="09">September</option>
          <option value="10">October</option>
          <option value="11">November</option>
          <option value="12">December</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="table jobs-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': titleSort }" style="width: 20%" @click="cycleSort('title')">
              <span class="th-inner">
                JOB TITLE
                <span class="sort-label">
                  <span v-if="!titleSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="titleSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': companySort }" style="width: 16%"
              @click="cycleSort('company')">
              <span class="th-inner">
                COMPANY
                <span class="sort-label">
                  <span v-if="!companySort" class="sort-label-dim">⇅</span>
                  <span v-else-if="companySort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': priceSort }" style="width: 10%" @click="cycleSort('price')">
              <span class="th-inner">
                PRICE
                <span class="sort-label">
                  <span v-if="!priceSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="priceSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th style="width: 16%; text-align: center;">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">STATUS
                <button class="col-filter-btn" :class="{ active: statusFilter !== 'All' }"
                  @click.stop="toggleStatusDropdown($event)">
                  {{ statusFilter === "All" ? "All ▼" : statusFilter + " ▼" }}
                </button></span>
            </th>
            <th style="width: 12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 16%; position: relative;"
              @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button v-if="titleSort || companySort || priceSort || statusFilter !== 'All' || dateSort"
                class="reset-btn ml-1.5" @click.stop="resetAllFilters"
                style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);">
                ✕ Reset
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in filteredJobs" :key="job.job_id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="openJobModal(job)">
              {{ job.job_title }}
            </td>
            <td class="truncate-cell clickable-cell" @click="openCompanyModal(job)">
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
            <td style="text-align: center;">
              <span class="badge" :class="job.job_status?.toLowerCase()">{{
                job.job_status
              }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewJob(job.job_id)">
                  View
                </button>
                <button class="btn-action delete" @click="deleteJob(job.job_id)">
                  Delete
                </button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-' + i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:70%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:60%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:50%"></span></td>
              <td><span class="skeleton skeleton-badge"></span></td>
              <td>
                <div class="action-btns">
                  <span class="skeleton skeleton-btn"></span>
                  <span class="skeleton skeleton-btn"></span>
                </div>
              </td>
              <td><span class="skeleton skeleton-text" style="width:80%"></span></td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdowns -->
    <div v-if="showStatusDropdown" class="col-dropdown" :style="statusDropdownStyle">
      <button class="col-dropdown-item" @click="setStatusFilter('All')">
        All
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('OPEN')">
        Open
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('MATCHING')">
        Matching
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('SELECTED')">
        Selected
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('IN_PROGRESS')">
        In Progress
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('COMPLETED')">
        Completed
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('CANCELLED')">
        Cancelled
      </button>
    </div>

    <!-- Job Modal -->
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

    <!-- Company Modal -->
    <div v-if="companyModal" class="modal-overlay" @click.self="companyModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content: flex-end; margin-bottom: 8px">
          <button class="close-btn" @click="companyModal = null">✕</button>
        </div>
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
            <span class="badge" :class="companyModal.em_verify_status?.toLowerCase()">{{ companyModal.em_verify_status
              }}</span>
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
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="
            router.push({
              name: 'EmployerDetail',
              params: { id: companyModal.em_id },
            });
          companyModal = null;
          ">
            View Full Detail →
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="mini-modal" style="text-align: center; padding: 32px">
        <div style="font-size: 36px; margin-bottom: 12px">🗑</div>
        <h3 style="margin: 0 0 12px">Delete Job</h3>
        <p style="color: #555; margin: 0 0 8px; line-height: 1.5">
          Are you sure you want to delete<br /><strong>"{{ deleteTargetTitle }}"</strong>?
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
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { API_BASE } from "../data/api";

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
const search = ref("");
const statusFilter = ref(localStorage.getItem("jobs_statusFilter") || "All");
const monthFilter = ref("All");
const yearFilter = ref("All");

const titleSort = ref(localStorage.getItem("jobs_titleSort") || "");
const companySort = ref(localStorage.getItem("jobs_companySort") || "");
const priceSort = ref(localStorage.getItem("jobs_priceSort") || "");
const dateSort = ref(localStorage.getItem("jobs_dateSort") || "");

const showStatusDropdown = ref(false);
const statusDropdownStyle = ref({});

const saveFilters = () => {
  localStorage.setItem("jobs_titleSort", titleSort.value);
  localStorage.setItem("jobs_companySort", companySort.value);
  localStorage.setItem("jobs_priceSort", priceSort.value);
  localStorage.setItem("jobs_statusFilter", statusFilter.value);
  localStorage.setItem("jobs_dateSort", dateSort.value);
};

// กดลูกศร: ไม่มี → asc → desc → ไม่มี (และ clear คอลัมน์อื่นทั้งหมด)
const cycleSort = (key) => {
  const current = { title: titleSort, company: companySort, price: priceSort, date: dateSort }[key];
  const next = current.value === "" ? "asc" : current.value === "asc" ? "desc" : "";
  titleSort.value = "";
  companySort.value = "";
  priceSort.value = "";
  dateSort.value = "";
  current.value = next;
  saveFilters();
};

const isLoading = ref(true);
const jobs = ref([]);
const allEmployers = ref([]);
const allFreelancers = ref([]);
const showDeleteModal = ref(false);
const deleteTargetId = ref(null);
const deleteTargetTitle = ref("");
const jobModal = ref(null);
const companyModal = ref(null);

const currentYear = new Date().getFullYear();
const years = Array.from({ length: 5 }, (_, i) => currentYear - 2 + i);

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

const filteredJobs = computed(() => {
  let result = jobs.value.filter((job) => {
    const matchSearch = (job.job_title || "")
      .toLowerCase()
      .includes(search.value.toLowerCase());
    const matchStatus =
      statusFilter.value === "All" || job.job_status === statusFilter.value;
    const d = job.job_start_date ? new Date(job.job_start_date) : null;
    const matchYear =
      yearFilter.value === "All" ||
      (d && String(d.getFullYear()) === String(yearFilter.value));
    const matchMonth =
      monthFilter.value === "All" ||
      (d && String(d.getMonth() + 1).padStart(2, "0") === monthFilter.value);
    return matchSearch && matchStatus && matchYear && matchMonth;
  });

  if (titleSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.job_title || "").localeCompare(b.job_title || "");
      return titleSort.value === "desc" ? -cmp : cmp;
    });
  } else if (companySort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.company || "").localeCompare(b.company || "");
      return companySort.value === "desc" ? -cmp : cmp;
    });
  } else if (priceSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (Number(a.job_price) || 0) - (Number(b.job_price) || 0);
      return priceSort.value === "desc" ? -cmp : cmp;
    });
  } else if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = new Date(a.job_updated_at) - new Date(b.job_updated_at);
      return dateSort.value === "desc" ? -cmp : cmp;
    });
  } else {
    // Default: ล่าสุดก่อน
    result = [...result].sort((a, b) => new Date(b.job_updated_at) - new Date(a.job_updated_at));
  }

  return result;
});

const toggleStatusDropdown = (e) => {
  showStatusDropdown.value = !showStatusDropdown.value;
  const rect = e.target.getBoundingClientRect();
  statusDropdownStyle.value = {
    position: "fixed",
    top: rect.bottom + window.scrollY + "px",
    left: rect.left + "px",
  };
};

const setStatusFilter = (val) => {
  statusFilter.value = val;
  showStatusDropdown.value = false;
  saveFilters();
};

const closeAllDropdowns = () => {
  showStatusDropdown.value = false;
};

const resetAllFilters = () => {
  titleSort.value = "";
  companySort.value = "";
  priceSort.value = "";
  statusFilter.value = "All";
  dateSort.value = "";
  saveFilters();
};

const handleOutsideClick = (e) => {
  if (!e.target.closest(".col-dropdown") && !e.target.closest(".col-filter-btn")) {
    closeAllDropdowns();
  }
};

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
  } catch (e) { }
};

const viewJob = (id) => {
  const job = jobs.value.find((j) => j.job_id === id);
  router.push({
    name: "JobDetail",
    params: { id },
    state: { jobTitle: job?.job_title || "" }
  });
};

const openJobModal = (job) => {
  jobModal.value = job;
};

const openCompanyModal = (job) => {
  const em = allEmployers.value.find((e) => e.em_id === job.em_id);
  companyModal.value = em || { em_name: job.company };
};

const deleteJob = (id) => {
  deleteTargetId.value = id;
  deleteTargetTitle.value =
    jobs.value.find((j) => j.job_id === id)?.job_title || id;
  showDeleteModal.value = true;
};

const confirmDelete = async () => {
  const title = deleteTargetTitle.value;
  const id = deleteTargetId.value;
  try {
    const adminId = localStorage.getItem('admin_id') || '';
    const res = await fetch(`${API_BASE}/jobs/${id}?admin_id=${adminId}`, { method: "DELETE" });
    if (res.ok) {
      jobs.value = jobs.value.filter((j) => j.job_id !== id);
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

onUnmounted(() => {
  document.removeEventListener("click", handleOutsideClick);
});

onMounted(async () => {
  document.addEventListener("click", handleOutsideClick);
  try {
    const [jobsRes, emRes, flRes] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/freelancers?limit=500`),
    ]);
    const [jobsData, emData, flData] = await Promise.all([
      jobsRes.json(),
      emRes.json(),
      flRes.json(),
    ]);
    jobs.value = jobsData.items || [];
    allEmployers.value = emData.items || [];
    allFreelancers.value = flData.items || [];
  } catch (e) {
    console.error("Failed to load jobs:", e);
  } finally {
    isLoading.value = false;
  }
});
</script>