<template>
  <div>
    <BreadcrumbBar />

    <div class="tabs">
      <button
        class="tab"
        :class="{ active: activeTab === 'Freelancer' }"
        @click="activeTab = 'Freelancer'"
      >
        Freelancer
      </button>
      <button
        class="tab"
        :class="{ active: activeTab === 'Employer' }"
        @click="activeTab = 'Employer'"
      >
        Employer
      </button>
    </div>

    <div class="filter-row">
      <input
        type="text"
        v-model="search"
        placeholder="Search name..."
        class="search-input"
      />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width: 20%" @click="cycleSort('name')">
              <span class="th-inner">
                NAME
                <span class="sort-arrows">
                  <span :class="nameSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="nameSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': ratingSort }" style="width: 16%" @click="cycleSort('rating')">
              <span class="th-inner">
                RATING
                <span class="sort-arrows">
                  <span :class="ratingSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="ratingSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': jobsSort }" style="width: 10%" @click="cycleSort('jobs')">
              <span class="th-inner">
                JOBS
                <span class="sort-arrows">
                  <span :class="jobsSort === 'asc' ? 'arrow-active' : 'arrow-dim'">↑</span><span :class="jobsSort === 'desc' ? 'arrow-active' : 'arrow-dim'">↓</span>
                </span>
              </span>
            </th>
            <th style="width: 10%">
              STATUS
              <button
                class="col-filter-btn"
                :class="{ active: verifyFilter !== 'All' }"
                @click.stop="toggleStatusDropdown($event)"
              >
                {{ verifyFilter === "All" ? "All ▼" : verifyFilter + " ▼" }}
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
                v-if="nameSort || ratingSort || verifyFilter !== 'All' || dateSort || jobsSort"
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
          <tr v-for="user in filteredUsers" :key="user.id" class="row-hover">
            <td class="truncate-cell clickable-cell" @click="viewUser(user)">
              <div class="user-cell">
                <span class="avatar">{{ user.initials }}</span>
                <span :title="user.name">
                  {{ user.name }}
                </span>
              </div>
            </td>
            <td>⭐ {{ Number(user.rating || 0).toFixed(1) }}</td>
            <td>{{ jobsDoneById[user.id] || 0 }}</td>
            <td>
              <span class="badge" :class="user.verifyStatus?.toLowerCase()">{{
                user.verifyStatus
              }}</span>
            </td>
            <td>
              <div class="action-btns">
                <button class="btn-action view" @click="viewUser(user)">
                  View
                </button>
                <button
                  class="btn-action"
                  :class="user.isActive ? 'ban' : 'unban'"
                  @click="openBanModal(user)"
                >
                  {{ user.isActive ? "Ban" : "Unban" }}
                </button>
              </div>
            </td>
            <td class="text-muted">{{ formatDateTime(user.updatedAt) }}</td>
          </tr>
          <template v-if="isLoading">
            <tr v-for="i in 6" :key="'sk-'+i" class="skeleton-row">
              <td><span class="skeleton skeleton-text" style="width:65%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:40%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:40%"></span></td>
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
      <button class="col-dropdown-item" @click="setVerifyFilter('All')">
        All
      </button>
      <button class="col-dropdown-item" @click="setVerifyFilter('VERIFIED')">
        Verified
      </button>
      <button class="col-dropdown-item" @click="setVerifyFilter('PENDING')">
        Pending
      </button>
      <button
        class="col-dropdown-item"
        @click="setVerifyFilter('NOT_VERIFIED')"
      >
        Not Verified
      </button>
    </div>

    <!-- Ban Modal -->
    <div
      v-if="showBanModal"
      class="modal-overlay"
      @click.self="showBanModal = false">
      <div class="modal">
        <div class="modal-icon">{{ banTarget?.isActive ? "🚫" : "✅" }}</div>
        <h3>{{ banTarget?.isActive ? "Ban User" : "Unban User" }}</h3>
        <p>
          Are you sure you want to {{ banTarget?.isActive ? "ban" : "unban"
          }}<br />
          <strong>"{{ banTarget?.name }}"</strong>?
        </p>
        <p v-if="banTarget?.isActive" class="modal-warning">
          This user will not be able to accept any jobs.
        </p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showBanModal = false">
            Cancel
          </button>
          <button
            class="btn-confirm"
            :class="banTarget?.isActive ? 'ban' : 'unban'"
            @click="confirmBan"
          >
            {{ banTarget?.isActive ? "Ban" : "Unban" }}
          </button>
        </div>
      </div>
    </div>
    <!-- User Modal -->
    <div v-if="userModal" class="modal-overlay" @click.self="userModal = null">
      <div class="mini-modal">
        <div class="mini-modal-header" style="justify-content: space-between">
          <h3 class="mini-modal-title">{{ userModal.name }}</h3>
          <button class="close-btn" @click="userModal = null">✕</button>
        </div>
        <div class="profile-hero">
          <div class="profile-avatar">
            <img v-if="userModal.imageUrl" :src="userModal.imageUrl" class="avatar-img" />
            <span v-else class="avatar-initial">{{ userModal.initials }}</span>
          </div>
        </div>
        <div class="mini-grid">
          <div class="mini-item">
            <label>Status</label>
            <span class="badge" :class="userModal.verifyStatus?.toLowerCase()">{{ userModal.verifyStatus }}</span>
          </div>
          <div class="mini-item">
            <label>Active</label>
            <span>{{ userModal.isActive ? '✅ Active' : '❌ Inactive' }}</span>
          </div>
          <div class="mini-item">
            <label>Rating</label>
            <span>⭐ {{ Number(userModal.rating || 0).toFixed(1) }}</span>
          </div>
          <div class="mini-item">
            <label>Jobs Done</label>
            <span>{{ jobsDoneById[userModal.id] || 0 }}</span>
          </div>
          <div class="mini-item">
            <label>Created</label>
            <span class="text-muted">{{ formatDateTime(userModal.createdAt) }}</span>
          </div>
          <div class="mini-item">
            <label>Last Updated</label>
            <span class="text-muted">{{ formatDateTime(userModal.updatedAt) }}</span>
          </div>
        </div>
        <div class="mini-modal-footer">
          <button class="btn-full-view" @click="goToFullDetail">View Full Detail →</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";

const activeTab = ref("Freelancer");

const userModal = ref(null)

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const router = useRouter();
const showBanModal = ref(false);
const banTarget = ref(null);
const jobsDoneByFreelancer = ref({});
const jobsDoneByEmployer = ref({});

// Sort states
const nameSort = ref(localStorage.getItem("users_nameSort") || "");
const ratingSort = ref(localStorage.getItem("users_ratingSort") || "");
const verifyFilter = ref(localStorage.getItem("users_verifyFilter") || "All");
const dateSort = ref(localStorage.getItem("users_dateSort") || "");
const jobsSort = ref(localStorage.getItem("users_jobsSort") || "");

const showStatusDropdown = ref(false);
const statusDropdownStyle = ref({});

const saveFilters = () => {
  localStorage.setItem("users_nameSort", nameSort.value);
  localStorage.setItem("users_ratingSort", ratingSort.value);
  localStorage.setItem("users_verifyFilter", verifyFilter.value);
  localStorage.setItem("users_dateSort", dateSort.value);
  localStorage.setItem("users_jobsSort", jobsSort.value);
};

// กดลูกศร: ไม่มี → asc → desc → ไม่มี (clear คอลัมน์อื่นอัตโนมัติ)
const cycleSort = (key) => {
  const map = { name: nameSort, rating: ratingSort, date: dateSort, jobs: jobsSort };
  const current = map[key];
  const next = current.value === "" ? "asc" : current.value === "asc" ? "desc" : "";
  nameSort.value = "";
  ratingSort.value = "";
  dateSort.value = "";
  jobsSort.value = "";
  current.value = next;
  saveFilters();
};

const toggleStatusDropdown = (e) => {
  showStatusDropdown.value = !showStatusDropdown.value;
  const rect = e.target.getBoundingClientRect();
  statusDropdownStyle.value = {
    position: "fixed",
    top: rect.bottom + window.scrollY + "px",
    left: rect.left + "px",
  };
};

const setVerifyFilter = (val) => {
  verifyFilter.value = val;
  showStatusDropdown.value = false;
  saveFilters();
};

const closeAllDropdowns = () => {
  showStatusDropdown.value = false;
};

const resetAllFilters = () => {
  nameSort.value = "";
  ratingSort.value = "";
  verifyFilter.value = "All";
  dateSort.value = "";
  jobsSort.value = "";
  saveFilters();
};

const handleOutsideClick = (e) => {
  if (
    !e.target.closest(".col-dropdown") &&
    !e.target.closest(".col-filter-btn")
  ) {
    closeAllDropdowns();
  }
};

const viewUser = (user) => {
  userModal.value = user
}

const goToFullDetail = () => {
  if (!userModal.value) return
  const route = activeTab.value === 'Employer'
    ? { name: 'EmployerDetail', params: { id: userModal.value.id } }
    : { name: 'FreelancerDetail', params: { id: userModal.value.id } }
  router.push(route)
  userModal.value = null
}

const openBanModal = (user) => {
  banTarget.value = user;
  showBanModal.value = true;
};

const confirmBan = async () => {
  const user = banTarget.value;
  const endpoint =
    activeTab.value === "Freelancer"
      ? `${API_BASE}/freelancers/${user.id}/ban`
      : `${API_BASE}/employers/${user.id}/ban`;
  try {
    const res = await fetch(endpoint, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ is_active: !user.isActive }),
    });
    const data = await res.json();
    if (data.status === "updated") {
      user.isActive = !user.isActive;
    }
  } catch (e) {
    console.error("Failed to ban/unban user:", e);
  } finally {
    showBanModal.value = false;
    banTarget.value = null;
  }
};
const isLoading = ref(true);
const employers = ref([]);
const freelancers = ref([]);
const jobs = ref([]);
const search = ref("");

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

function initialsFromName(name) {
  if (!name) return "?";
  const parts = name.trim().split(/\s+/).slice(0, 2);
  return parts.map((p) => p[0]?.toUpperCase() || "").join("");
}

async function loadEmployers() {
  const res = await fetch(`${API_BASE}/admin/employers?limit=50&offset=0`);
  const data = await res.json();
  employers.value = (data.items || []).map((e) => ({
    id: e.em_id,
    name: e.em_name || e.em_username || e.em_id,
    initials: initialsFromName(e.em_name || e.em_username || ""),
    verifyStatus: e.em_verify_status || "UNKNOWN",
    isActive: !!e.em_is_active,
    rating: Number(e.em_rating_avg || 0),
    imageUrl: e.em_profile_image_url || "",
    createdAt: e.em_created_at || "",
    updatedAt: e.em_updated_at || "",
  }));
}

async function loadFreelancers() {
  const res = await fetch(`${API_BASE}/admin/freelancers?limit=50&offset=0`);
  const data = await res.json();
  freelancers.value = (data.items || []).map((f) => ({
    id: f.fl_id,
    name: f.fl_name || f.fl_id,
    initials: initialsFromName(f.fl_name || ""),
    verifyStatus: f.fl_verify_status || "UNKNOWN",
    isActive: !!f.fl_is_active,
    rating: Number(f.fl_rating_avg || 0),
    imageUrl: f.fl_profile_image_url || "",
    createdAt: f.fl_created_at || "",
    updatedAt: f.fl_updated_at || "",
  }));
}

async function loadJobs() {
  try {
    const res = await fetch(`${API_BASE}/jobs?limit=500`);
    const data = await res.json();
    jobs.value = data.items || [];

    const flMap = {};
    const emMap = {};

    for (const j of jobs.value) {
      if (j?.job_status !== "COMPLETED") continue;
      const flId = j.selected_fl_id;
      const emId = j.em_id;
      if (flId) flMap[flId] = (flMap[flId] || 0) + 1;
      if (emId) emMap[emId] = (emMap[emId] || 0) + 1;
    }

    jobsDoneByFreelancer.value = flMap;
    jobsDoneByEmployer.value = emMap;
  } catch (e) {
    console.error("Failed to load jobs:", e);
    jobs.value = [];
    jobsDoneByFreelancer.value = {};
    jobsDoneByEmployer.value = {};
  }
}

const jobsDoneById = computed(() =>
  activeTab.value === "Employer"
    ? jobsDoneByEmployer.value
    : jobsDoneByFreelancer.value,
);

const filteredUsers = computed(() => {
  const list =
    activeTab.value === "Employer" ? employers.value : freelancers.value;
  let result = list.filter((u) => {
    const matchSearch = (u.name || "")
      .toLowerCase()
      .includes(search.value.toLowerCase());
    const matchStatus =
      verifyFilter.value === "All" || u.verifyStatus === verifyFilter.value;
    return matchSearch && matchStatus;
  });

  if (nameSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.name || "").localeCompare(b.name || "");
      return nameSort.value === "desc" ? -cmp : cmp;
    });
  }

  if (ratingSort.value) {
    result = [...result].sort((a, b) => {
      return ratingSort.value === "desc"
        ? b.rating - a.rating
        : a.rating - b.rating;
    });
  }

  if (jobsSort.value) {
    result = [...result].sort((a, b) => {
      const jobsA = jobsDoneById.value[a.id] || 0;
      const jobsB = jobsDoneById.value[b.id] || 0;
      return jobsSort.value === "desc" ? jobsB - jobsA : jobsA - jobsB;
    });
  }

  if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.updatedAt) || 0;
      const dateB = new Date(b.updatedAt) || 0;
      return dateSort.value === "desc" ? dateB - dateA : dateA - dateB;
    });
  } else if (!nameSort.value && !ratingSort.value && !jobsSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.updatedAt) || 0;
      const dateB = new Date(b.updatedAt) || 0;
      return dateB - dateA;
    });
  }

  return result;
});

onUnmounted(() => {
  document.removeEventListener("click", handleOutsideClick);
});

onMounted(async () => {
  document.addEventListener("click", handleOutsideClick);
  await Promise.allSettled([loadEmployers(), loadFreelancers(), loadJobs()]);
  isLoading.value = false;
});

watch(activeTab, async (tab) => {
  // refresh only the active list
  if (tab === "Employer" && employers.value.length === 0) await loadEmployers();
  if (tab === "Freelancer" && freelancers.value.length === 0)
    await loadFreelancers();
});
</script>

<style scoped>
.title {
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 2px 0;
  background: #1a1a2e;
  padding: 15px 20px;
  color: white;
  letter-spacing: 0.2px;
}

.tabs {
  display: flex;
  gap: 25px;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
  padding: 0 20px;
}

.tab {
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 14px;
  cursor: pointer;
  color: #666;
}

.tab.active {
  color: #06c755;
  border-bottom: 2px solid #06c755;
  margin-bottom: -2px;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 0 20px;
}

.table {
  width: 100%;
  min-width: 900px;
  border-collapse: collapse;
  table-layout: fixed;
}

.table th,
.table td {
  padding: 15px 20px;
  text-align: left;
  border-bottom: 1px solid #eee;
  white-space: nowrap;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: white;
  position: sticky;
  top: 0;
  z-index: 10;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 0;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #6c757d;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  width: fit-content;
}

.badge.verified {
  background: #e8f5e9;
  color: #2e7d32;
}
.badge.pending {
  background: #fff3e0;
  color: #f57c00;
}
.badge.rejected,
.badge.not_verified {
  background: #ffebee;
  color: #c62828;
}
.badge.unknown {
  background: #f5f5f5;
  color: #666;
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
.btn-action.ban {
  background: #ffebee;
  color: #c62828;
}
.btn-action.ban:hover {
  background: #ffcdd2;
}
.btn-action.unban {
  background: #e8f5e9;
  color: #2e7d32;
}
.btn-action.unban:hover {
  background: #c8e6c9;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
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
  margin-top: 20px;
}
.btn-cancel {
  padding: 10px 24px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-size: 14px;
}
.btn-confirm {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-size: 14px;
}
.btn-confirm.ban {
  background: #dc3545;
}
.btn-confirm.ban:hover {
  background: #b02a37;
}
.btn-confirm.unban {
  background: #2e7d32;
}
.btn-confirm.unban:hover {
  background: #1b5e20;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 20px;
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
.skeleton-text { height: 14px; display: block; border-radius: 4px; }
.skeleton-badge { height: 22px; width: 70px; border-radius: 12px; }
.skeleton-btn { height: 26px; width: 50px; border-radius: 5px; }
.skeleton-row td { padding-top: 18px; padding-bottom: 18px; }

.text-muted {
  color: #999;
  font-size: 13px;
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
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 140px;
}

.empty {
  text-align: center;
  color: #999;
  padding: 32px;
}

.table th.th-sortable {
  cursor: pointer;
  user-select: none;
  transition: background 0.15s, color 0.15s;
}
.table th.th-sortable:hover { background: #f0fdf4; color: #06c755; }
.table th.th-active { background: #f0fdf4; color: #06c755; }
.th-inner { display: inline-flex; align-items: center; gap: 6px; }
.sort-arrows { display: inline-flex; flex-direction: column; line-height: 1; font-size: 10px; gap: 0; margin-top: 1px; }
.arrow-dim { color: #ccc; }
.arrow-active { color: #06c755; font-weight: 700; }

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

@media (max-width: 1024px) {
  .table th,
  .table td {
    padding: 12px 10px;
  }
  .table th {
    font-size: 11px;
  }
  .badge {
    padding: 3px 8px;
    font-size: 11px;
  }
  .btn-action {
    padding: 3px 8px;
    font-size: 11px;
  }
  .avatar {
    width: 28px;
    height: 28px;
    font-size: 10px;
  }
}

@media (max-width: 640px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }
  .search-input {
    width: 100%;
  }
  .title {
    font-size: 20px;
  }
  .tabs {
    gap: 16px;
  }
  .tab {
    font-size: 13px;
    padding: 10px 0;
  }
}

.mini-modal {
  background: white;
  border-radius: 12px;
  padding: 24px;
  width: 480px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
}

.mini-modal-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.mini-modal-title {
  margin: 0;
  font-size: 18px;
  color: #1a1a2e;
}

.close-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
  color: #999;
  padding: 0;
}
.profile-hero {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.profile-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #1a1a2e;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-initial {
  color: white;
  font-size: 20px;
  font-weight: 600;
}

.mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 16px;
}

.mini-item label {
  display: block;
  font-size: 11px;
  color: #999;
  text-transform: uppercase;
  margin-bottom: 4px;
  letter-spacing: 0.5px;
}

.mini-item span {
  font-size: 14px;
  color: #333;
}

.mini-modal-footer {
  border-top: 1px solid #eee;
  padding-top: 16px;
  text-align: right;
}

.btn-full-view {
  background: none;
  border: none;
  color: #1976d2;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-full-view:hover {
  text-decoration: underline;
}
</style>