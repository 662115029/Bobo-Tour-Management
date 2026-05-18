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
                                  : actionFilter === "DELETE_JOB" ? "DELETE ▼"
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
            <th class="th-sortable" :class="{ 'th-active': targetSort }" style="width: 22%"
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
            <th style="width: 14%">NOTE</th>
            <th style="width: 18%; white-space: nowrap;">
              <span style="display:inline-flex;align-items:center;white-space:nowrap;gap:4px;">ADMIN
                <button class="col-filter-btn" :class="{ active: adminFilter !== 'All' }"
                  @click.stop="toggleAdminDropdown($event)">
                  {{ adminFilter === 'All' ? 'All ▼' : adminFilter + ' ▼' }}
                </button></span>
            </th>
            <th class="th-sortable" :class="{ 'th-active': dateSort }" style="width: 17%;" @click="cycleSort('date')">
              <span class="th-inner" style="display:inline-flex;align-items:center;gap:6px;white-space:nowrap;">
                LAST UPDATED
                <span class="sort-label">
                  <span v-if="!dateSort" class="sort-label-dim">⇅</span>
                  <span v-else-if="dateSort === 'asc'" class="sort-label-active">↑</span>
                  <span v-else class="sort-label-active">↓</span>
                </span>
                <button v-if="actionFilter !== 'All' || typeFilter !== 'All' || adminFilter !== 'All' || targetSort || dateSort"
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
              <template v-if="['DOCUMENT'].includes((log.target_type||'').toUpperCase()) || ((log.target_id || log.target_name) && ['FREELANCER','EMPLOYER','JOB'].includes((log.target_type||'').toUpperCase()))">
                <span class="cursor-pointer underline underline-offset-[2px]" @click="openTargetModal(log)">{{ log.target_name || log.target_id || '-' }}</span>
              </template>
              <span v-else>{{ log.target_name || log.target_id || "-" }}</span>
            </td>
            <td class="truncate-cell text-muted text-[11px]" :title="log.note">
              {{ log.note || "-" }}
            </td>
            <td class="truncate-cell">
              <div class="user-cell flex-nowrap min-w-0">
                <span class="user-avatar shrink-0" :style="avatarStyle(log.admin_name, log.admin_name)">{{ initials2(log.admin_name) }}</span>
                <span class="overflow-hidden text-ellipsis whitespace-nowrap">{{ log.admin_name || "-" }}</span>
              </div>
            </td>
            <td class="text-muted text-[11px]">{{ formatDateTime(log.created_at) }}</td>
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
      <button class="col-dropdown-item" @click="setActionFilter('DELETE_JOB')">Delete Job</button>
    </div>

    <div v-if="showTypeDropdown" class="col-dropdown" :style="typeDropdownStyle">
      <button class="col-dropdown-item" @click="setTypeFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setTypeFilter('FREELANCER')">Freelancer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('EMPLOYER')">Employer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('JOB')">Job</button>
      <button class="col-dropdown-item" @click="setTypeFilter('DOCUMENT')">Document</button>
    </div>


    <div v-if="showAdminDropdown" class="col-dropdown" :style="adminDropdownStyle">
      <button class="col-dropdown-item" @click="setAdminFilter('All')">All</button>
      <button
        v-for="name in uniqueAdmins"
        :key="name"
        class="col-dropdown-item"
        @click="setAdminFilter(name)">
        {{ name }}
      </button>
    </div>

    <!-- Target Modals: Loading / FL / EM -->
    <UserMiniModal
      :data="targetModal && (targetModalType === 'FREELANCER' || targetModalType === 'EMPLOYER') ? targetModal : null"
      :type="targetModalType"
      :loading="targetModalLoading"
      @close="targetModal = null"
      @view-detail="({ id, type }) => { router.push({ name: type === 'FREELANCER' ? 'FreelancerDetail' : 'EmployerDetail', params: { id } }); targetModal = null }"
    />

    <!-- Target Modal: Job -->
    <JobMiniModal
      v-if="targetModal && targetModalType === 'JOB'"
      :data="targetModal"
      @close="targetModal = null"
      @view-detail="(id) => { router.push({ name: 'JobDetail', params: { id } }); targetModal = null }"
    />

    <!-- Deleted Job Modal: Loading skeleton -->
    <div v-if="deletedJobModalLoading" class="modal-overlay">
      <div class="w-[380px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col overflow-hidden">
        <div class="flex items-center justify-between px-5 py-3.5 border-b border-[#f0f0f0]">
          <span class="skeleton w-20 h-5 rounded-full block"></span>
          <span class="skeleton w-7 h-7 rounded-full block"></span>
        </div>
        <div class="px-5 pt-5 pb-4 flex flex-col gap-3">
          <div v-for="i in 4" :key="i" class="flex items-center justify-between bg-[#fafafa] rounded-xl px-4 py-3">
            <span class="skeleton h-3 w-1/4 rounded block"></span>
            <span class="skeleton h-3.5 w-2/5 rounded block"></span>
          </div>
        </div>
        <div class="px-5 pb-5 pt-1"><span class="skeleton w-full h-11 rounded-xl block"></span></div>
      </div>
    </div>

    <!-- Deleted Job Modal -->
    <div v-else-if="deletedJobModal" class="modal-overlay" @click.self="deletedJobModal = null">
      <div class="w-[380px] rounded-2xl bg-white shadow-[0_16px_56px_rgba(0,0,0,0.18)] flex flex-col overflow-hidden">

        <!-- Topbar -->
        <div class="relative flex items-center justify-center px-5 py-3.5 border-b border-[#f0f0f0]">
          <span class="text-[11px] font-bold uppercase tracking-widest text-[#e53935]">Job</span>
          <button
            class="absolute right-4 w-7 h-7 rounded-full bg-[#f5f5f5] text-[#888] text-[13px] flex items-center justify-center border-none cursor-pointer hover:bg-[#ebebeb] hover:text-[#111] transition-colors"
            @click="deletedJobModal = null">✕</button>
        </div>

        <!-- Icon + Title -->
        <div class="flex flex-col items-center px-6 pt-7 pb-5">
          <div class="w-16 h-16 rounded-2xl bg-[#fdecea] flex items-center justify-center mb-4 shadow-sm">
            <svg width="30" height="30" fill="none" viewBox="0 0 24 24" stroke="#e53935" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </div>
          <div class="text-[17px] font-bold text-[#111] text-center leading-snug">This job has been deleted</div>
          <div class="text-[13px] text-[#999] text-center mt-1.5 leading-relaxed">This job no longer exists in the system.</div>
        </div>

        <!-- Divider -->
        <div class="h-px bg-[#f5f5f5] mx-5"></div>

        <!-- Info rows -->
        <div class="px-5 py-4 flex flex-col gap-3">
          <div class="flex items-center justify-between bg-[#fafafa] rounded-xl px-4 py-3">
            <span class="text-[11px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Job Name</span>
            <span class="text-[13px] font-semibold text-[#222] max-w-[190px] truncate text-right">{{ deletedJobModal.target_name || deletedJobModal.target_id || '—' }}</span>
          </div>
          <div class="flex items-center justify-between bg-[#fafafa] rounded-xl px-4 py-3">
            <span class="text-[11px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Deleted by</span>
            <span class="text-[13px] font-semibold text-[#222]">{{ deletedJobModal.admin_name || '—' }}</span>
          </div>
          <div class="flex items-center justify-between bg-[#fafafa] rounded-xl px-4 py-3">
            <span class="text-[11px] font-semibold uppercase tracking-[0.08em] text-[#bbb]">Deleted at</span>
            <span class="text-[13px] font-semibold text-[#222]">{{ formatDateTime(deletedJobModal.created_at) }}</span>
          </div>
          <div v-if="deletedJobModal.note" class="flex items-start justify-between bg-[#fafafa] rounded-xl px-4 py-3 gap-3">
            <span class="text-[11px] font-semibold uppercase tracking-[0.08em] text-[#bbb] shrink-0 mt-0.5">Note</span>
            <span class="text-[13px] text-[#555] text-right leading-relaxed">{{ deletedJobModal.note }}</span>
          </div>
        </div>

        <!-- Footer -->
        <div class="px-5 pb-5 pt-1">
          <button
            class="w-full py-3 bg-[#f5f5f5] text-[#666] text-[13px] font-semibold rounded-xl border-none cursor-pointer transition-colors hover:bg-[#ebebeb] active:scale-[0.98]"
            @click="deletedJobModal = null">Close</button>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { computed, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { API_BASE } from "../data/api";
import { useAvatar } from '../composables/useAvatar'
import { formatDateTime } from '../utils/formatDate'
import { getActionClass, getTypeClass } from '../utils/statusClasses'
import UserMiniModal from '../components/UserMiniModal.vue'
import JobMiniModal from '../components/JobMiniModal.vue'

const router = useRouter();
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
const admins = ref([]);

const showTypeDropdown = ref(false);
const typeDropdownStyle = ref({});
const adminFilter = ref(localStorage.getItem("logs_adminFilter") || "All");
const showAdminDropdown = ref(false);
const adminDropdownStyle = ref({});

const saveFilters = () => {
  localStorage.setItem("logs_actionFilter", actionFilter.value);
  localStorage.setItem("logs_targetSort", targetSort.value);
  localStorage.setItem("logs_typeFilter", typeFilter.value);
  localStorage.setItem("logs_dateSort", dateSort.value);
  localStorage.setItem("logs_adminFilter", adminFilter.value);
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
    actionDropdownStyle.value = { position: "fixed", top: rect.bottom + window.scrollY + "px", left: rect.left + "px" };
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

const toggleAdminDropdown = (e) => {
  closeAllDropdowns();
  showAdminDropdown.value = true;
  const rect = e.target.getBoundingClientRect();
  adminDropdownStyle.value = {
    position: "fixed",
    top: rect.bottom + window.scrollY + "px",
    left: rect.left + "px",
  };
};

const setAdminFilter = (val) => {
  adminFilter.value = val;
  showAdminDropdown.value = false;
  saveFilters();
};

const closeAllDropdowns = () => {
  showTypeDropdown.value = false;
  showActionDropdown.value = false;
  showAdminDropdown.value = false;
};

const resetAllFilters = () => {
  actionFilter.value = "All";
  targetSort.value = "";
  typeFilter.value = "All";
  dateSort.value = "";
  adminFilter.value = "All";
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

const uniqueAdmins = computed(() => {
  return admins.value.map(a => a.name).filter(Boolean).sort();
});

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
      (log.note || "").toLowerCase().includes(search.value.toLowerCase()) ||
      (log.admin_name || "").toLowerCase().includes(search.value.toLowerCase());
    const matchType =
      typeFilter.value === "All" ||
      (log.target_type || "").toUpperCase() === typeFilter.value;
    const matchAdmin =
      adminFilter.value === "All" ||
      (log.admin_name || "") === adminFilter.value;
    return matchSearch && matchType && matchAdmin;
  });

  if (actionFilter.value !== "All") {
    result = result.filter((log) => {
      const a = (log.action_type || "").toUpperCase();
      if (actionFilter.value === "DELETE_JOB") return a === "DELETE_JOB" || a === "DELETE";
      return a === actionFilter.value;
    });
  }

  if (targetSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.target_name || "").localeCompare(b.target_name || "");
      return targetSort.value === "desc" ? -cmp : cmp;
    });
  } else if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime() || 0;
      const dateB = new Date(b.created_at).getTime() || 0;
      return dateSort.value === "desc" ? dateB - dateA : dateA - dateB;
    });
  } else {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at).getTime() || 0;
      const dateB = new Date(b.created_at).getTime() || 0;
      return dateB - dateA;
    });
  }

  return result;
});

onUnmounted(() => {
  document.removeEventListener("click", handleOutsideClick);
});


const targetModal = ref(null);
const targetModalType = ref('');
const targetModalLoading = ref(false);
const deletedJobModal = ref(null); // { target_name, target_id, note, created_at, admin_name }
const deletedJobModalLoading = ref(false);

const openTargetModal = async (log) => {
  const type = (log.target_type || '').toUpperCase();
  const action = (log.action_type || '').toUpperCase();
  const id = log.target_id;
  if (!['FREELANCER','EMPLOYER','JOB','DOCUMENT'].includes(type)) return;
  if (type !== 'DOCUMENT' && !id) return;

  // DOCUMENT type → match user by target_name and show UserMiniModal
  if (type === 'DOCUMENT') {
    targetModal.value = null;
    targetModalType.value = '';
    targetModalLoading.value = true;
    try {
      const name = (log.target_name || '').trim().toLowerCase();
      const [flRes, emRes] = await Promise.all([
        fetch(`${API_BASE}/freelancers?limit=500`),
        fetch(`${API_BASE}/employers?limit=500`),
      ]);
      const [flData, emData] = await Promise.all([flRes.json(), emRes.json()]);
      const flUser = (flData.items || []).find(f =>
        (f.fl_name || '').toLowerCase() === name || (f.fl_username || '').toLowerCase() === name
      );
      if (flUser) {
        targetModal.value = flUser;
        targetModalType.value = 'FREELANCER';
      } else {
        const emUser = (emData.items || []).find(e =>
          (e.em_name || '').toLowerCase() === name || (e.em_username || '').toLowerCase() === name
        );
        if (emUser) {
          targetModal.value = emUser;
          targetModalType.value = 'EMPLOYER';
        }
      }
    } catch (e) {
      console.error('Failed to load document target user:', e);
    } finally {
      targetModalLoading.value = false;
    }
    return;
  }

  // If this log is a delete action on a JOB → show deleted modal with brief loading
  if (type === 'JOB' && (action === 'DELETE_JOB' || action === 'DELETE')) {
    deletedJobModalLoading.value = true;
    deletedJobModal.value = null;
    await new Promise(r => setTimeout(r, 350));
    deletedJobModal.value = log;
    deletedJobModalLoading.value = false;
    return;
  }

  targetModal.value = null;
  targetModalType.value = type;
  targetModalLoading.value = true;
  try {
    let url = '';
    if (type === 'FREELANCER') url = `${API_BASE}/freelancers/${id}`;
    else if (type === 'EMPLOYER') url = `${API_BASE}/employers/${id}`;
    else if (type === 'JOB') url = `${API_BASE}/jobs?limit=500`;
    const res = await fetch(url);
    const data = await res.json();
    if (type === 'JOB') {
      const job = (data.items || []).find(j => String(j.job_id) === String(id));
      if (job) {
        // fetch languages
        const langRes = await fetch(`${API_BASE}/job-required-languages?limit=500`);
        const langData = await langRes.json();
        const langs = (langData.items || [])
          .filter(l => l.job_id === job.job_id)
          .map(l => l.language_name);
        targetModal.value = { ...job, languages: langs };
      }
    } else {
      targetModal.value = data;
    }
    targetModalType.value = type;
  } catch (e) {
    console.error('Failed to load target:', e);
  } finally {
    targetModalLoading.value = false;
  }
};

const fetchLogs = async () => {
  isLoading.value = true;
  try {
    const [logsRes, adminsRes] = await Promise.all([
      fetch(`${API_BASE}/admin/logs?limit=500`),
      fetch(`${API_BASE}/admin/admins?limit=500`),
    ]);
    const logsData = await logsRes.json();
    const adminsData = await adminsRes.json();
    logs.value = logsData.items || [];
    admins.value = adminsData.items || [];
  } catch (e) {
    console.error("Failed to load logs:", e);
    logs.value = [];
    admins.value = [];
  } finally {
    isLoading.value = false;
  }
};

const route = useRoute();

// Re-fetch every time user navigates to this page
watch(() => route.fullPath, async (newPath) => {
  if (newPath.includes('/logs')) {
    await fetchLogs();
  }
});

onMounted(async () => {
  document.addEventListener("click", handleOutsideClick);
  await fetchLogs();
});
</script>