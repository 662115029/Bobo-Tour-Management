<template>
  <div>
    <BreadcrumbBar />

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search action or target..." class="search-input" />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width: 17%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">ACTION
                <button class="col-filter-btn" :class="{ active: actionFilter !== 'All' }"
                  @click.stop="toggleActionDropdown($event)">
                  {{ actionFilter === "All" ? "All ▼"
                    : actionFilter === "APPROVE_DOCUMENT" ? "APPROVE DOC ▼"
                      : actionFilter === "REJECT_DOCUMENT" ? "REJECT DOC ▼"
                        : actionFilter === "VERIFY_FREELANCER" ? "VERIFY FL ▼"
                          : actionFilter === "VERIFY_EMPLOYER" ? "VERIFY EM ▼"
                            : actionFilter === "BAN_USER" ? "BAN ▼"
                              : actionFilter === "UNBAN_USER" ? "UNBAN ▼"
                                : actionFilter === "DELETE" ? "DELETE ▼"
                                  : actionFilter + " ▼" }}
                </button></span>
            </th>
            <th style="width: 13%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">TYPE
                <button class="col-filter-btn" :class="{ active: typeFilter !== 'All' }"
                  @click.stop="toggleTypeDropdown($event)">
                  {{ typeFilter === "All" ? "All ▼" : typeFilter === "FREELANCER" ? "FREELANCE ▼" : typeFilter ===
                    "EMPLOYER" ? "EMPLOYER ▼" : typeFilter === "DOCUMENT" ? "DOCUMENT ▼" : typeFilter === "JOB" ? "JOB ▼"
                  : typeFilter + " ▼" }}
                </button></span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': targetSort }" style="width: 18%"
              @click="cycleSort('target')">
              <span class="th-inner">
                TARGET
                <span class="sort-label">
                  <span v-if="!targetSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="targetSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th style="width: 20%">NOTE</th>
            <th style="width: 15%; white-space: nowrap;">ADMIN</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 17%;" @click="cycleSort('date')">
              <span class="th-inner" style="display:inline-flex;align-items:center;gap:6px;white-space:nowrap;">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
                <button v-if="actionFilter !== 'All' || typeFilter !== 'All' || targetSort || dateSort"
                  class="reset-btn" style="margin-left:6px;font-size:11px;padding:2px 8px;"
                  @click.stop="resetAllFilters">✕ Reset</button>
              </span>
            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 8" :key="'sk-' + i" class="skeleton-row">
              <td><span class="skeleton skeleton-badge" style="width:80px"></span></td>
              <td><span class="skeleton skeleton-badge" style="width:90px"></span></td>
              <td><span class="skeleton skeleton-text" style="width:70%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:85%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:60%"></span></td>
              <td><span class="skeleton skeleton-text" style="width:75%"></span></td>
            </tr>
          </template>
          <tr v-for="log in filteredLogs" :key="log.log_id">
            <td>
              <span class="action-badge" :class="getActionClass(log.action_type)">
                {{ log.action_type || "-" }}
              </span>
            </td>
            <td>
              <span class="type-tag" :class="getTypeClass(log.target_type)">
                {{ log.target_type || "-" }}
              </span>
            </td>
            <td class="truncate-cell" :title="log.target_name">
              {{ log.target_name || log.target_id || "-" }}
            </td>
            <td class="truncate-cell text-muted text-xs" :title="log.note">
              {{ log.note || "-" }}
            </td>
            <td>
              <div class="user-cell">
                <span class="user-avatar" :style="avatarStyle(log.admin_name, log.admin_name)">{{ initials2(log.admin_name) }}</span>
                {{ log.admin_name || "-" }}
              </div>
            </td>
            <td class="text-muted text-xs">{{ formatDateTime(log.created_at) }}</td>
          </tr>
          <tr v-if="filteredLogs.length === 0">
            <td colspan="6" class="empty">No logs found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdowns -->
    <div v-if="showActionDropdown" class="col-dropdown" :style="actionDropdownStyle">
      <button class="col-dropdown-item" @click="setActionFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setActionFilter('APPROVE_DOCUMENT')">Approve Document</button>
      <button class="col-dropdown-item" @click="setActionFilter('REJECT_DOCUMENT')">Reject Document</button>
      <button class="col-dropdown-item" @click="setActionFilter('VERIFY_FREELANCER')">Verify Freelancer</button>
      <button class="col-dropdown-item" @click="setActionFilter('VERIFY_EMPLOYER')">Verify Employer</button>
      <button class="col-dropdown-item" @click="setActionFilter('BAN_USER')">Ban</button>
      <button class="col-dropdown-item" @click="setActionFilter('UNBAN_USER')">Unban</button>
      <button class="col-dropdown-item" @click="setActionFilter('DELETE')">Delete Job</button>
    </div>

    <div v-if="showTypeDropdown" class="col-dropdown" :style="typeDropdownStyle">
      <button class="col-dropdown-item" @click="setTypeFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setTypeFilter('FREELANCER')">Freelancer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('EMPLOYER')">Employer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('JOB')">Job</button>
      <button class="col-dropdown-item" @click="setTypeFilter('DOCUMENT')">Document</button>
    </div>


  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { computed, onMounted, onUnmounted, ref } from "vue";
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime } from '../utils/formatDate'

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const { avatarStyle, initials2 } = useAvatar()
const search = ref("");
const typeFilter = ref(localStorage.getItem("logs_typeFilter") || "All");
const actionFilter = ref(localStorage.getItem("logs_actionFilter") || "All");
const targetSort = ref(localStorage.getItem("logs_targetSort") || "");
const showActionDropdown = ref(false);
const actionDropdownStyle = ref({});
const dateSort = ref(localStorage.getItem("logs_dateSort") || "");
const isLoading = ref(true);
const logs = ref([]);

const showTypeDropdown = ref(false);
const typeDropdownStyle = ref({});

const saveFilters = () => {
  localStorage.setItem("logs_actionFilter", actionFilter.value);
  localStorage.setItem("logs_targetSort", targetSort.value);
  localStorage.setItem("logs_typeFilter", typeFilter.value);
  localStorage.setItem("logs_dateSort", dateSort.value);
};

const cycleSort = (key) => {
  const map = { target: targetSort, date: dateSort };
  const current = map[key];
  const next = current.value === "" ? "asc" : current.value === "asc" ? "desc" : "";
  targetSort.value = "";
  dateSort.value = "";
  current.value = next;
  saveFilters();
};

const toggleActionDropdown = (e) => {
  const opening = !showActionDropdown.value;
  showActionDropdown.value = false;
  showTypeDropdown.value = false;
  if (opening) {
    showActionDropdown.value = true;
    const rect = e.target.getBoundingClientRect();
    actionDropdownStyle.value = { position: "fixed", top: rect.bottom + "px", left: rect.left + "px" };
  }
};
const setActionFilter = (val) => {
  actionFilter.value = val;
  showActionDropdown.value = false;
  saveFilters();
};

const toggleTypeDropdown = (e) => {
  closeAllDropdowns();
  showTypeDropdown.value = true;
  const rect = e.target.getBoundingClientRect();
  typeDropdownStyle.value = {
    position: "fixed",
    top: rect.bottom + window.scrollY + "px",
    left: rect.left + "px",
  };
};

const setTypeFilter = (val) => {
  typeFilter.value = val;
  showTypeDropdown.value = false;
  saveFilters();
};

const closeAllDropdowns = () => {
  showTypeDropdown.value = false;
  showActionDropdown.value = false;
};

const resetAllFilters = () => {
  actionFilter.value = "All";
  targetSort.value = "";
  typeFilter.value = "All";
  dateSort.value = "";
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

const getActionClass = (action) => {
  const a = (action || "").toUpperCase();
  if (a === "APPROVE_DOCUMENT") return "action-approve";
  if (a === "VERIFY_FREELANCER" || a === "VERIFY_EMPLOYER") return "action-verify";
  if (a === "REJECT_DOCUMENT") return "action-reject";
  if (a === "BAN_USER") return "action-ban";
  if (a === "UNBAN_USER") return "action-unban";
  if (a === "UPDATE") return "action-update";
  if (a === "VIEW") return "action-view";
  if (a === "DELETE" || a === "DELETE_JOB") return "action-delete";
  return "action-default";
};

const getTypeClass = (type) => {
  const t = (type || "").toUpperCase();
  if (t === "FREELANCER") return "type-freelancer";
  if (t === "EMPLOYER") return "type-employer";
  if (t === "JOB") return "type-job";
  if (t === "DOCUMENT") return "type-document";
  if (t === "USER") return "type-user";
  return "type-default";
};

const filteredLogs = computed(() => {
  let result = logs.value.filter((log) => {
    const matchSearch =
      search.value === "" ||
      (log.action_type || "")
        .toLowerCase()
        .includes(search.value.toLowerCase()) ||
      (log.target_name || "")
        .toLowerCase()
        .includes(search.value.toLowerCase()) ||
      (log.note || "").toLowerCase().includes(search.value.toLowerCase());
    const matchType =
      typeFilter.value === "All" ||
      (log.target_type || "").toUpperCase() === typeFilter.value;
    return matchSearch && matchType;
  });

  if (actionFilter.value !== "All") {
    result = result.filter((log) => {
      const a = (log.action_type || "").toUpperCase();
      if (actionFilter.value === "DELETE") return a === "DELETE" || a === "DELETE_JOB";
      return a === actionFilter.value;
    });
  }

  if (targetSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.target_name || "").localeCompare(b.target_name || "");
      return targetSort.value === "desc" ? -cmp : cmp;
    });
  }

  if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at) || 0;
      const dateB = new Date(b.created_at) || 0;
      return dateSort.value === "desc" ? dateB - dateA : dateA - dateB;
    });
  } else {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at) || 0;
      const dateB = new Date(b.created_at) || 0;
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
  try {
    const res = await fetch(`${API_BASE}/admin/logs?limit=500`);
    const data = await res.json();
    logs.value = data.items || [];
  } catch (e) {
    console.error("Failed to load logs:", e);
    logs.value = [];
  } finally {
    isLoading.value = false;
  }
});
</script>