<template>
  <div>
    <BreadcrumbBar />

    <div class="filter-row">
      <input
        type="text"
        v-model="search"
        placeholder="Search job title..."
        class="search-input"
      />
      <div class="filter-group">
        <select v-model="yearFilter" class="filter-select">
          <option value="All">All Years</option>
          <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
        </select>
        <select v-model="monthFilter" class="filter-select">
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
      <table class="table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': titleSort }" style="width: 20%" @click="cycleSort('title')">
              <span class="th-inner">
                JOB TITLE
                <span class="sort-arrows">
                  <span :class="titleSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="titleSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': companySort }" style="width: 16%" @click="cycleSort('company')">
              <span class="th-inner">
                COMPANY
                <span class="sort-arrows">
                  <span :class="companySort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="companySort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': priceSort }" style="width: 10%" @click="cycleSort('price')">
              <span class="th-inner">
                PRICE
                <span class="sort-arrows">
                  <span :class="priceSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="priceSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th style="width: 10% ">
              STATUS
              <button
                class="col-filter-btn"
                :class="{ active: statusFilter !== 'All' }"
                @click.stop="toggleStatusDropdown($event)"
              >
                {{ statusFilter === "All" ? "All ▼" : statusFilter + " ▼" }}
              </button>
            </th>
            <th style="width: 12%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-arrows">
                  <span :class="dateSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="dateSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
              <button
                v-if="titleSort || companySort || priceSort || statusFilter !== 'All' || dateSort"
                class="reset-btn"
                @click.stop="resetAllFilters"
                style="position: absolute; right: 12px; top: 50%; transform: translateY(-50%);"
              >
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
            <td
              class="truncate-cell clickable-cell"
              @click="openCompanyModal(job)"
            >
              {{ job.company }}
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
                  @click="deleteJob(job.job_id)"
                >
                  Delete
                </button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(job.job_updated_at) }}</td>
          </tr>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-'+i" class="skeleton-row">
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
    <div
      v-if="showStatusDropdown"
      class="col-dropdown"
      :style="statusDropdownStyle"
    >
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
        <div class="mini-modal-header" style="justify-content: space-between">
          <h3 class="mini-modal-title">{{ jobModal.job_title }}</h3>
          <button class="close-btn" @click="jobModal = null">✕</button>
        </div>
        <p v-if="jobModal.job_description" class="mini-desc">
          {{ jobModal.job_description }}
        </p>
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
            <span>{{ jobModal.company || "-" }}</span>
          </div>
          <div class="mini-item">
            <label>Freelancer</label>
            <span>{{ jobModal.selected_fl_id || "-" }}</span>
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
          <button
            class="btn-full-view"
            @click="
              viewJob(jobModal.job_id);
              jobModal = null;
            "
          >
            View Full Detail →
          </button>
        </div>
      </div>
    </div>

    <!-- Company Modal -->
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
        <div class="profile-hero">
          <div class="profile-avatar em">
            <img
              v-if="companyModal.em_profile_image_url"
              :src="companyModal.em_profile_image_url"
              class="avatar-img"
            />
            <span v-else class="avatar-initial">{{
              companyModal.em_name?.[0] || "?"
            }}</span>
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
            <span>{{
              companyModal.em_is_active ? "✅ Active" : "❌ Inactive"
            }}</span>
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

    <!-- Delete Modal -->
    <div
      v-if="showDeleteModal"
      class="modal-overlay"
      @click.self="showDeleteModal = false"
    >
      <div class="mini-modal" style="text-align: center; padding: 32px">
        <div style="font-size: 36px; margin-bottom: 12px">🗑</div>
        <h3 style="margin: 0 0 12px">Delete Job</h3>
        <p style="color: #555; margin: 0 0 8px; line-height: 1.5">
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
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { API_BASE } from "../data/api";

const router = useRouter();
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
  try {
    await fetch(`${API_BASE}/jobs/${deleteTargetId.value}`, {
      method: "DELETE",
    });
    jobs.value = jobs.value.filter((j) => j.job_id !== deleteTargetId.value);
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
    const [jobsRes, emRes] = await Promise.all([
      fetch(`${API_BASE}/jobs?limit=500`),
      fetch(`${API_BASE}/employers?limit=500`),
    ]);
    const [jobsData, emData] = await Promise.all([
      jobsRes.json(),
      emRes.json(),
    ]);
    jobs.value = jobsData.items || [];
    allEmployers.value = emData.items || [];
  } catch (e) {
    console.error("Failed to load jobs:", e);
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.title {
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 15px 0;
  background: #1a1a2e;
  padding: 15px 20px;
  color: white;
  letter-spacing: 0.2px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 20px;
}
.filter-group {
  display: flex;
  gap: 8px;
}
.search-input {
  padding: 10px 14px;
  border: 1.5px solid #bbb;
  border-radius: 8px;
  width: 280px;
  font-size: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.search-input:focus {
  border-color: #06c755;
  box-shadow: 0 0 0 3px rgba(6,199,85,0.12);
}
.filter-select {
  padding: 10px 14px;
  border: 1.5px solid #bbb;
  border-radius: 8px;
  font-size: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  margin: 0 20px;
}

.table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}
.table th,
.table td {
  padding: 15px 20px;
  text-align: left;
  border-bottom: 1px solid #eee;
  overflow: hidden;
}
.table td:nth-child(2) {
  color: #888;
  font-size: 13px;
}
.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: #ffffff;
  position: relative;
}

.col-filter-btn {
  margin-left: 8px;
  padding: 4px 10px;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 11px;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-weight: 500;
}
.col-filter-btn:hover {
  border-color: #06c755;
  color: #06c755;
}
.col-filter-btn.active {
  border-color: #06c755;
  color: #06c755;
  font-weight: 600;
}

.table th.th-sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.15s, color 0.15s;
}
.table th.th-sortable:hover { background: #f0fdf4; color: #06c755; }
.table th.th-active { background: #f0fdf4; color: #06c755; }
.th-inner {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.sort-arrows {
  display: inline-flex;
  flex-direction: column;
  line-height: 1;
  font-size: 10px;
  gap: 0px;
  margin-top: 1px;
}
.arrow-dim {
  color: #ccc;
}
.arrow-active {
  color: #06c755;
  font-weight: 700;
}

.reset-btn {
  margin-left: 6px;
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  font-size: 10px;
  background: #ffebee;
  color: #c62828;
  cursor: pointer;
  font-weight: 500;
}
.reset-btn:hover {
  background: #ffcdd2;
}

.col-dropdown {
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 50;
  min-width: 120px;
}
.col-dropdown-item {
  display: block;
  width: 100%;
  padding: 8px 14px;
  border: none;
  background: none;
  text-align: left;
  font-size: 13px;
  cursor: pointer;
}
.col-dropdown-item:hover {
  background: #f5f5f5;
}
.col-dropdown-item:first-child {
  border-radius: 6px 6px 0 0;
}
.col-dropdown-item:last-child {
  border-radius: 0 0 6px 6px;
}

.truncate-cell {
  max-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.row-hover:hover {
  background: #f5f5f5;
}

.clickable-cell {
  cursor: pointer;
  color: #000;
}

.clickable-cell:hover {
  color: #000;
  text-decoration: underline;
}

.badge {
  display: inline-flex;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  width: fit-content;
}
.badge.open {
  background: #e3f2fd;
  color: #1976d2;
}
.badge.matching {
  background: #e0f2f1;
  color: #00695c;
}
.badge.selected {
  background: #f3e5f5;
  color: #7b1fa2;
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
.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}
.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}
.badge.not_verified {
  background: #ffebee;
  color: #c62828;
}

.action-btns {
  display: flex;
  gap: 6px;
  justify-content: center;
}
.btn-action {
  padding: 4px 10px;
  border-radius: 5px;
  border: none;
  font-size: 12px;
  cursor: pointer;
  font-weight: 500;
}
.btn-action.view {
  background: #e0f7f1;
  color: #00796b;
  font-weight: 600;
}
.btn-action.view:hover {
  background: #b2dfdb;
}
.btn-action.delete {
  background: #ffebee;
  color: #c62828;
}
.btn-action.delete:hover {
  background: #ffcdd2;
}

@keyframes shimmer {
  0% { background-position: -400px 0; }
  100% { background-position: 400px 0; }
}
.skeleton {
  display: inline-block;
  border-radius: 6px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 800px 100%;
  animation: shimmer 1.4s infinite;
}
.skeleton-text {
  height: 14px;
  display: block;
  border-radius: 4px;
}
.skeleton-badge {
  height: 22px;
  width: 70px;
  border-radius: 12px;
}
.skeleton-btn {
  height: 26px;
  width: 50px;
  border-radius: 5px;
}
.skeleton-row td {
  padding-top: 18px;
  padding-bottom: 18px;
}

.text-muted {
  color: #999;
  font-size: 12px;
}
.empty {
  text-align: center;
  color: #999;
  padding: 32px;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}
.mini-modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 460px;
  max-height: 80vh;
  overflow-y: auto;
}
.mini-modal-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 16px;
}
.mini-modal-title {
  font-size: 16px;
  font-weight: 600;
  color: #111;
  margin: 0;
  flex: 1;
  padding-right: 12px;
}
.close-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #888;
  flex-shrink: 0;
}
.mini-desc {
  font-size: 13px;
  color: #666;
  line-height: 1.6;
  margin: 0 0 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}
.mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.mini-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.mini-item label {
  font-size: 10px;
  color: #999;
  font-weight: 600;
  text-transform: uppercase;
}
.mini-item span {
  font-size: 13px;
  color: #222;
}
.mini-modal-footer {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
}
.btn-full-view {
  background: none;
  border: none;
  color: #0066cc;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}
.btn-full-view:hover {
  text-decoration: underline;
}

.profile-hero {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}
.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;
}
.profile-avatar.em {
  background: #f3e5f5;
}
.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}
.avatar-initial {
  font-size: 22px;
  font-weight: 700;
  color: #555;
}
.profile-info {
  flex: 1;
  min-width: 0;
}
.profile-name {
  font-size: 16px;
  font-weight: 600;
  margin: 0 0 4px;
  color: #111;
}
.profile-bio {
  font-size: 12px;
  color: #666;
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.profile-bio.muted {
  color: #bbb;
  font-style: italic;
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