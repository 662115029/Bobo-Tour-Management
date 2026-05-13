<template>
  <div>
    <BreadcrumbBar />

    <div class="tabs-wide">
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

    <div class="table-container overflow-x-auto touch-pan-x">
      <table class="table users-table">
        <thead>
          <tr>
            <th class="th-sortable" :class="{ 'th-active': nameSort }" style="width: 16%" @click="cycleSort('name')">
              <span class="th-inner">
                NAME
                <span class="sort-label">
                  <span v-if="!nameSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="nameSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': ratingSort }" style="width: 12%" @click="cycleSort('rating')">
              <span class="th-inner">
                RATING
                <span class="sort-label">
                  <span v-if="!ratingSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="ratingSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': jobsSort }" style="width: 15%" @click="cycleSort('jobs')">
              <span class="th-inner">
                JOBS
                <span class="sort-label">
                  <span v-if="!jobsSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="jobsSort === 'asc'" class="sort-label-active">↑09</span>
                  <span v-else class="sort-label-active">↓90</span>
                </span>
              </span>
            </th>
            <th style="width: 16%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">STATUS
              <button
                class="col-filter-btn"
                :class="{ active: verifyFilter !== 'All' }"
                @click.stop="toggleStatusDropdown($event)"
              >
                {{ verifyFilter === "All" ? "All ▼" : verifyFilter === "NOT_VERIFIED" ? "NOT VERIF. ▼" : verifyFilter === "VERIFIED" ? "VERIFIED ▼" : verifyFilter === "PENDING" ? "PENDING ▼" : verifyFilter === "REJECTED" ? "REJECTED ▼" : verifyFilter + " ▼" }}
              </button></span>
            </th>
            <th style="width: 11%; text-align: center;">ACTION</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 16%; position: relative;" @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>
              <button
                v-if="nameSort || ratingSort || verifyFilter !== 'All' || dateSort || jobsSort"
                class="reset-btn ml-1.5"
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
            <td class="truncate-cell clickable-cell" @click="openUserModal(user)">
              <div class="user-cell">
                <span class="user-avatar">{{ user.initials }}</span>
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
            <td class="text-muted text-[13px]">{{ formatDateTime(user.updatedAt) }}</td>
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
        <div class="mini-modal-header">
          <button class="close-btn" @click="userModal = null" style="margin-left:auto">✕</button>
        </div>
        <div class="profile-hero">
          <div class="profile-avatar" :class="activeTab === 'Freelancer' ? 'fl' : 'em'">
            <img v-if="userModal.imageUrl" :src="userModal.imageUrl" class="avatar-img" />
            <span v-else class="avatar-initial">{{ userModal.initials }}</span>
          </div>
          <div class="profile-info">
            <h3 class="profile-name">{{ userModal.name }}</h3>
            <p v-if="userModal.bio" class="profile-bio">{{ userModal.bio }}</p>
            <p v-else class="profile-bio muted">No bio</p>
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

const openUserModal = (user) => {
  userModal.value = user
}

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

const viewUser = (user) => {
  const target_type = activeTab.value === 'Employer' ? 'EMPLOYER' : 'FREELANCER';
  logAction('VIEW', target_type, user.id, user.name);
  const route = activeTab.value === 'Employer'
    ? { name: 'EmployerDetail', params: { id: user.id }, state: { parent: 'Users', parentTo: '/users', userName: user.name } }
    : { name: 'FreelancerDetail', params: { id: user.id }, state: { parent: 'Users', parentTo: '/users', userName: user.name } }
  router.push(route)
}

const goToFullDetail = () => {
  if (!userModal.value) return
  const route = activeTab.value === 'Employer'
    ? { name: 'EmployerDetail', params: { id: userModal.value.id }, state: { parent: 'Users', parentTo: '/users', userName: userModal.value.name } }
    : { name: 'FreelancerDetail', params: { id: userModal.value.id }, state: { parent: 'Users', parentTo: '/users', userName: userModal.value.name } }
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
      body: JSON.stringify({ is_active: !user.isActive, admin_id: localStorage.getItem('admin_id') || '' }),
    });
    const data = await res.json();
    if (data.status === "updated") {
      const action = user.isActive ? 'BAN_USER' : 'UNBAN_USER';
      const target_type = activeTab.value === 'Employer' ? 'EMPLOYER' : 'FREELANCER';
      logAction(action, target_type, user.id, user.name);
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
  // Clear sort state on fresh load
  nameSort.value = "";
  ratingSort.value = "";
  dateSort.value = "";
  jobsSort.value = "";
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

