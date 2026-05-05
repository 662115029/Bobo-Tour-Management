<template>
  <div>
    <BreadcrumbBar />

    <div class="filter-row">
      <input
        type="text"
        v-model="search"
        placeholder="Search action or target..."
        class="search-input"
      />
      <button
        v-if="actionFilter !== 'All' || typeFilter !== 'All' || targetSort || dateSort"
        class="reset-btn"
        @click="resetAllFilters"
      >
        ✕ Reset
      </button>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width: 18%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">ACTION
              <button
                class="col-filter-btn"
                :class="{ active: actionFilter !== 'All' }"
                @click.stop="toggleActionDropdown($event)"
              >
                {{ actionFilter === "All" ? "All ▼" : actionFilter === "APPROVE_DOCUMENT" ? "APPROVE DOC ▼" : actionFilter === "VERIFY_FREELANCER" ? "VERIFY FL ▼" : actionFilter === "VERIFY_EMPLOYER" ? "VERIFY EM ▼" : actionFilter === "REJECT_DOCUMENT" ? "REJECT DOC ▼" : actionFilter + " ▼" }}
              </button></span>
            </th>
            <th style="width: 16%">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">TYPE
              <button
                class="col-filter-btn"
                :class="{ active: typeFilter !== 'All' }"
                @click.stop="toggleTypeDropdown($event)"
              >
                {{ typeFilter === "All" ? "All ▼" : typeFilter === "FREELANCER" ? "FREELANCE ▼" : typeFilter === "EMPLOYER" ? "EMPLOYER ▼" : typeFilter === "DOCUMENT" ? "DOCUMENT ▼" : typeFilter === "JOB" ? "JOB ▼" : typeFilter + " ▼" }}
              </button></span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': targetSort }" style="width: 22%" @click="cycleSort('target')">
              <span class="th-inner">
                TARGET
                <span class="sort-label">
                  <span v-if="!targetSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="targetSort === 'asc'" class="sort-label-active">↑AZ</span>
                  <span v-else class="sort-label-active">↓ZA</span>
                </span>
              </span>
            </th>
            <th style="width: 24%">NOTE</th>
            <th style="width: 12%">ADMIN</th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 16%;" @click="cycleSort('date')">
              <span class="th-inner">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
              </span>

            </th>
          </tr>
        </thead>
        <tbody>
          <template v-if="isLoading">
            <tr v-for="i in 8" :key="'sk-'+i" class="skeleton-row">
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
              <span
                class="action-badge"
                :class="getActionClass(log.action_type)"
              >
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
            <td class="truncate-cell text-muted" :title="log.note">
              {{ log.note || "-" }}
            </td>
            <td>{{ log.admin_name || "-" }}</td>
            <td class="text-muted">{{ formatDateTime(log.created_at) }}</td>
          </tr>
          <tr v-if="filteredLogs.length === 0">
            <td colspan="6" class="empty">No logs found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdowns -->
    <div
      v-if="showActionDropdown"
      class="col-dropdown"
      :style="actionDropdownStyle"
    >
      <button class="col-dropdown-item" @click="setActionFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setActionFilter('APPROVE_DOCUMENT')">Approve Document</button>
      <button class="col-dropdown-item" @click="setActionFilter('VERIFY_FREELANCER')">Verify Freelancer</button>
      <button class="col-dropdown-item" @click="setActionFilter('VERIFY_EMPLOYER')">Verify Employer</button>
      <button class="col-dropdown-item" @click="setActionFilter('REJECT')">Reject</button>
      <button class="col-dropdown-item" @click="setActionFilter('REJECT_DOCUMENT')">Reject Document</button>
      <button class="col-dropdown-item" @click="setActionFilter('BAN')">Ban</button>
      <button class="col-dropdown-item" @click="setActionFilter('UNBAN')">Unban</button>
      <button class="col-dropdown-item" @click="setActionFilter('DELETE')">Delete</button>
      <button class="col-dropdown-item" @click="setActionFilter('UPDATE')">Update</button>
    </div>

    <div
      v-if="showTypeDropdown"
      class="col-dropdown"
      :style="typeDropdownStyle"
    >
      <button class="col-dropdown-item" @click="setTypeFilter('All')">
        All
      </button>
      <button class="col-dropdown-item" @click="setTypeFilter('FREELANCER')">
        Freelancer
      </button>
      <button class="col-dropdown-item" @click="setTypeFilter('EMPLOYER')">
        Employer
      </button>
      <button class="col-dropdown-item" @click="setTypeFilter('JOB')">
        Job
      </button>
      <button class="col-dropdown-item" @click="setTypeFilter('ADMIN')">
        Admin
      </button>
    </div>


  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { computed, onMounted, onUnmounted, ref } from "vue";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
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

const getActionClass = (action) => {
  const a = (action || "").toUpperCase();
  // approve family
  if (a === "APPROVE" || a === "APPROVE_DOCUMENT" || a === "APPROVE_EMPLOYER" || a === "APPROVE_FREELANCER") return "action-approve";
  // verify family
  if (a === "VERIFY_FREELANCER" || a === "VERIFY_EMPLOYER" || a === "VERIFY") return "action-verify";
  // unban / restore
  if (a === "UNBAN") return "action-unban";
  // update
  if (a === "UPDATE") return "action-update";
  // view
  if (a === "VIEW") return "action-view";
  // reject family
  if (a === "REJECT" || a === "REJECT_DOCUMENT") return "action-reject";
  // ban
  if (a === "BAN") return "action-ban";
  // delete
  if (a === "DELETE") return "action-delete";
  return "action-default";
};

const getTypeClass = (type) => {
  const t = (type || "").toUpperCase();
  if (t === "FREELANCER") return "type-freelancer";
  if (t === "EMPLOYER")   return "type-employer";
  if (t === "JOB")        return "type-job";
  if (t === "DOCUMENT")   return "type-document";
  if (t === "USER")       return "type-user";
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
  margin-bottom: 16px;
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.filter-group {
  display: flex;
  gap: 8px;
}
.search-input {
  padding: 10px 14px;
  border: 1.5px solid #999;
  border-radius: 8px;
  width: 280px;
  font-size: 14px;
  background: white;
  box-shadow: 0 1px 6px rgba(0,0,0,0.12);
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
  min-width: 130px;
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
.table th:has(.col-filter-btn) { white-space: nowrap; }

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: white;
  letter-spacing: 0.3px;
}

.truncate-cell {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.action-badge,
.type-tag {
  display: inline-flex;
  align-items: center;
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 600;
  width: fit-content;
}

/* ACTION colors */
.action-approve { background: #e8f5e9; color: #2e7d32; }
.action-verify  { background: #e0f7f1; color: #00796b; }
.action-unban   { background: #e3f2fd; color: #1565c0; }
.action-update  { background: #ede7f6; color: #5e35b1; }
.action-view    { background: #fff3e0; color: #e65100; }
.action-reject  { background: #fce4ec; color: #c2185b; }
.action-ban     { background: #fff8e1; color: #f57f17; }
.action-delete  { background: #fef2f2; color: #991b1b; }
.action-default { background: #f5f5f5; color: #666; }

/* TYPE colors (ไม่ซ้ำ ACTION เลย) */
.type-freelancer { background: #e0f2fe; color: #0369a1; }
.type-employer   { background: #fdf4ff; color: #7e22ce; }
.type-job        { background: #fff7ed; color: #9a3412; }
.type-document   { background: #f0fdf4; color: #166534; }
.type-user       { background: #fce4ec; color: #880e4f; }
.type-default    { background: #f5f5f5; color: #666; }

.text-muted {
  color: #999;
  font-size: 12px;
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
.table th.th-sortable:hover { background: #f0fdf4; color: #1a7a3f; }
.table th.th-active { background: #e6f9ef; color: #1a7a3f; border-bottom: 2px solid #06c755; }
.th-inner { display: inline-flex; align-items: center; gap: 6px; }
.sort-label { font-size: 11px; margin-left: 4px; }
.sort-label-dim { color: #bbb; }
.sort-label-active { color: #1a7a3f; font-weight: 700; }

@keyframes shimmer { 0%{background-position:-400px 0} 100%{background-position:400px 0} }
.skeleton {
  display: inline-block; border-radius: 6px;
  background: linear-gradient(90deg,#f0f0f0 25%,#e0e0e0 50%,#f0f0f0 75%);
  background-size: 800px 100%; animation: shimmer 1.4s infinite;
}
.skeleton-text { height: 14px; display: block; border-radius: 4px; }
.skeleton-badge { height: 22px; border-radius: 12px; display: inline-block; }
.skeleton-row td { padding-top: 18px; padding-bottom: 18px; }

.col-filter-btn {
  margin-left: 6px;
  padding: 3px 8px;
  border: 1px solid #ccc;
  border-radius: 20px;
  font-size: 11px;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-weight: 500;
  vertical-align: middle;
  line-height: 1;
  max-width: 110px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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
  margin-left: 12px;
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  background: #ffebee;
  color: #c62828;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
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
    padding: 10px 8px;
  }
  .table th {
    font-size: 11px;
  }
  .action-badge,
  .type-tag {
    padding: 2px 8px;
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
}
</style>