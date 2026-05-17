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
                  {{ statusFilter === "All" ? "All ▼" : (formatJobStatus(statusFilter)) + " ▼" }}
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
              <div class="user-cell">
                <span class="user-avatar" :style="jobIconStyle(job.job_id)" style="border-radius:6px;flex-shrink:0;">
                  <svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2c-2.5 3-4 6.5-4 10s1.5 7 4 10"/><path d="M12 2c2.5 3 4 6.5 4 10s-1.5 7-4 10"/></svg>
                </span>
                {{ job.job_title }}
              </div>
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
                formatJobStatus(job.job_status)
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
      <button class="col-dropdown-item" @click="setStatusFilter('PENDING')">
        Pending
      </button>
      <button class="col-dropdown-item" @click="setStatusFilter('MATCHED')">
        Matched
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
    <JobMiniModal
      :data="jobModal"
      @close="jobModal = null"
      @view-detail="(id) => { viewJob(id); jobModal = null }"
    />

    <!-- Company Modal -->
    <UserMiniModal
      :data="companyModal"
      type="EMPLOYER"
      @close="companyModal = null"
      @view-detail="({ id }) => { router.push({ name: 'EmployerDetail', params: { id } }); companyModal = null }"
    />

    <!-- Delete Modal -->
    <DeleteJobModal :show="showDeleteModal" :title="deleteTargetTitle"
      @confirm="confirmDelete" @cancel="showDeleteModal = false" />
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { API_BASE } from "../data/api";
import { useAvatar } from '../composables/useAvatar'
import { formatDate, formatDateTime } from '../utils/formatDate'
import { formatJobStatus } from '../utils/statusClasses'
import JobMiniModal from '../components/JobMiniModal.vue'
import UserMiniModal from '../components/UserMiniModal.vue'
import DeleteJobModal from '../components/DeleteJobModal.vue'

const router = useRouter();
const { avatarStyle, jobIconStyle, initials2 } = useAvatar()

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