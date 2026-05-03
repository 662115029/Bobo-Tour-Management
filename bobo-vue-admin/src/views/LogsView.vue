<template>
  <div>
    <h1 class="title">Admin Logs</h1>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search action or target..." class="search-input" />
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width:14%">
              ACTION
              <button class="col-filter-btn" :class="{ active: actionSort !== '' }" @click.stop="toggleActionDropdown($event)">
                {{ actionSort === 'asc' ? 'A→Z ▼' : actionSort === 'desc' ? 'Z→A ▼' : 'All ▼' }}
              </button>
            </th>
            <th style="width:14%">
              TYPE
              <button class="col-filter-btn" :class="{ active: typeFilter !== 'All' }" @click.stop="toggleTypeDropdown($event)">
                {{ typeFilter === 'All' ? 'All ▼' : typeFilter + ' ▼' }}
              </button>
            </th>
            <th style="width:22%">TARGET</th>
            <th style="width:30%">NOTE</th>
            <th style="width:12%">ADMIN</th>
            <th style="width:16%">
              LAST UPDATED
              <button class="col-filter-btn" :class="{ active: dateSort !== '' }" @click.stop="toggleDateDropdown($event)">
                {{ dateSort === 'desc' ? 'Latest ▼' : dateSort === 'asc' ? 'Oldest ▼' : 'All ▼' }}
              </button>
              <button v-if="actionSort || typeFilter !== 'All' || dateSort" class="reset-btn" @click="resetAllFilters">Reset</button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in filteredLogs" :key="log.log_id">
            <td>
              <span class="action-badge" :class="getActionClass(log.action_type)">
                {{ log.action_type || '-' }}
              </span>
            </td>
            <td>
              <span class="type-tag" :class="getTypeClass(log.target_type)">
                {{ log.target_type || '-' }}
              </span>
            </td>
            <td class="truncate-cell" :title="log.target_name">{{ log.target_name || log.target_id || '-' }}</td>
            <td class="truncate-cell text-muted" :title="log.note">{{ log.note || '-' }}</td>
            <td>{{ log.admin_name || '-' }}</td>
            <td class="text-muted">{{ formatDateTime(log.created_at) }}</td>
          </tr>
          <tr v-if="filteredLogs.length === 0">
            <td colspan="6" class="empty">No logs found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Column Filter Dropdowns -->
    <div v-if="showActionDropdown" class="col-dropdown" :style="actionDropdownStyle">
      <button class="col-dropdown-item" @click="setActionSort('')">All</button>
      <button class="col-dropdown-item" @click="setActionSort('asc')">A → Z</button>
      <button class="col-dropdown-item" @click="setActionSort('desc')">Z → A</button>
    </div>

    <div v-if="showTypeDropdown" class="col-dropdown" :style="typeDropdownStyle">
      <button class="col-dropdown-item" @click="setTypeFilter('All')">All</button>
      <button class="col-dropdown-item" @click="setTypeFilter('FREELANCER')">Freelancer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('EMPLOYER')">Employer</button>
      <button class="col-dropdown-item" @click="setTypeFilter('JOB')">Job</button>
      <button class="col-dropdown-item" @click="setTypeFilter('ADMIN')">Admin</button>
    </div>

    <div v-if="showDateDropdown" class="col-dropdown" :style="dateDropdownStyle">
      <button class="col-dropdown-item" @click="setDateSort('')">All</button>
      <button class="col-dropdown-item" @click="setDateSort('desc')">Latest</button>
      <button class="col-dropdown-item" @click="setDateSort('asc')">Oldest</button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const search = ref('')
const typeFilter = ref(localStorage.getItem('logs_typeFilter') || 'All')
const actionSort = ref(localStorage.getItem('logs_actionSort') || '')
const dateSort = ref(localStorage.getItem('logs_dateSort') || '')
const logs = ref([])

const showActionDropdown = ref(false)
const showTypeDropdown = ref(false)
const showDateDropdown = ref(false)
const actionDropdownStyle = ref({})
const typeDropdownStyle = ref({})
const dateDropdownStyle = ref({})

const saveFilters = () => {
  localStorage.setItem('logs_actionSort', actionSort.value)
  localStorage.setItem('logs_typeFilter', typeFilter.value)
  localStorage.setItem('logs_dateSort', dateSort.value)
}

const toggleActionDropdown = (e) => {
  closeAllDropdowns()
  showActionDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  actionDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setActionSort = (val) => { actionSort.value = val; showActionDropdown.value = false; saveFilters() }

const toggleTypeDropdown = (e) => {
  closeAllDropdowns()
  showTypeDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  typeDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setTypeFilter = (val) => { typeFilter.value = val; showTypeDropdown.value = false; saveFilters() }

const toggleDateDropdown = (e) => {
  closeAllDropdowns()
  showDateDropdown.value = true
  const rect = e.target.getBoundingClientRect()
  dateDropdownStyle.value = { position: 'fixed', top: (rect.bottom + window.scrollY) + 'px', left: rect.left + 'px' }
}

const setDateSort = (val) => { dateSort.value = val; showDateDropdown.value = false; saveFilters() }

const closeAllDropdowns = () => {
  showActionDropdown.value = false
  showTypeDropdown.value = false
  showDateDropdown.value = false
}

const resetAllFilters = () => {
  actionSort.value = ''
  typeFilter.value = 'All'
  dateSort.value = ''
  saveFilters()
}

const handleOutsideClick = (e) => {
  if (!e.target.closest('.col-dropdown') && !e.target.closest('.col-filter-btn')) {
    closeAllDropdowns()
  }
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const getActionClass = (action) => {
  const a = (action || '').toUpperCase()
  if (a === 'APPROVE') return 'green'
  if (a === 'REJECT') return 'red'
  if (a === 'BAN') return 'red'
  if (a === 'UNBAN') return 'green'
  if (a === 'DELETE') return 'red'
  if (a === 'UPDATE') return 'blue'
  return 'gray'
}

const getTypeClass = (type) => {
  const t = (type || '').toUpperCase()
  if (t === 'FREELANCER') return 'blue'
  if (t === 'EMPLOYER') return 'purple'
  if (t === 'JOB') return 'orange'
  return 'gray'
}

const filteredLogs = computed(() => {
  let result = logs.value.filter(log => {
    const matchSearch = search.value === '' ||
      (log.action_type || '').toLowerCase().includes(search.value.toLowerCase()) ||
      (log.target_name || '').toLowerCase().includes(search.value.toLowerCase()) ||
      (log.note || '').toLowerCase().includes(search.value.toLowerCase())
    const matchType = typeFilter.value === 'All' || (log.target_type || '').toUpperCase() === typeFilter.value
    return matchSearch && matchType
  })

  if (actionSort.value) {
    result = [...result].sort((a, b) => {
      const cmp = (a.action_type || '').localeCompare(b.action_type || '')
      return actionSort.value === 'desc' ? -cmp : cmp
    })
  }

  if (dateSort.value) {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at) || 0
      const dateB = new Date(b.created_at) || 0
      return dateSort.value === 'desc' ? dateB - dateA : dateA - dateB
    })
  } else {
    result = [...result].sort((a, b) => {
      const dateA = new Date(a.created_at) || 0
      const dateB = new Date(b.created_at) || 0
      return dateB - dateA
    })
  }

  return result
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
})

onMounted(async () => {
  document.addEventListener('click', handleOutsideClick)
  try {
    const res = await fetch(`${API_BASE}/admin/logs?limit=500`)
    const data = await res.json()
    logs.value = data.items || []
  } catch (e) {
    console.error('Failed to load logs:', e)
    logs.value = []
  }
})
</script>

<style scoped>
.title {
  font-size: 15px;
  font-weight: 500;
  margin: 0 0 24px 0;
  background: #1a1a2e;
  padding: 15px 20px;
  color: white;
  letter-spacing: 0.2px;
}

.filter-row {
  display: flex; justify-content: space-between;
  align-items: center; margin-bottom: 16px;
}
.filter-group { display: flex; gap: 8px; }
.search-input {
  padding: 10px 14px; border: 1px solid #ddd;
  border-radius: 6px; width: 280px; font-size: 14px;
}
.filter-select {
  padding: 10px 14px; border: 1px solid #ddd;
  border-radius: 6px; font-size: 14px; min-width: 130px;
}

.table-container { background: white; border-radius: 8px; overflow: hidden; }
.table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.table th, .table td {
  padding: 12px 14px; text-align: left;
  border-bottom: 1px solid #eee; overflow: hidden;
}
.table th { font-size: 12px; color: #666; font-weight: 600; background: #f9f9f9; }

.truncate-cell {
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

.action-badge {
  display: inline-block; padding: 3px 10px;
  border-radius: 20px; font-size: 11px; font-weight: 600;
}
.type-tag {
  display: inline-block; padding: 3px 10px;
  border-radius: 20px; font-size: 11px; font-weight: 600;
}

.green { background: #f0fdf4; color: #166534; }
.red { background: #fef2f2; color: #991b1b; }
.blue { background: #e3f2fd; color: #1976d2; }
.purple { background: #f3e5f5; color: #7b1fa2; }
.orange { background: #fff3e0; color: #f57c00; }
.gray { background: #f5f5f5; color: #666; }

.text-muted { color: #999; font-size: 12px; }
.empty { text-align: center; color: #999; padding: 32px; }

.col-filter-btn {
  margin-left: 8px; padding: 4px 10px; border: 1px solid #ccc;
  border-radius: 20px; font-size: 11px; background: transparent; color: #888;
  cursor: pointer; font-weight: 500;
}
.col-filter-btn:hover { color: #06C755; }
.col-filter-btn.active { color: #06C755; font-weight: 600; }

.reset-btn {
  margin-left: 6px; padding: 4px 8px; border: none;
  border-radius: 4px; font-size: 10px; background: #ffebee;
  color: #c62828; cursor: pointer; font-weight: 500;
}
.reset-btn:hover { background: #ffcdd2; }

.col-dropdown {
  background: white; border: 1px solid #ddd; border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 50; min-width: 120px;
}
.col-dropdown-item {
  display: block; width: 100%; padding: 8px 14px; border: none;
  background: none; text-align: left; font-size: 13px; cursor: pointer;
}
.col-dropdown-item:hover { background: #f5f5f5; }
.col-dropdown-item:first-child { border-radius: 6px 6px 0 0; }
.col-dropdown-item:last-child { border-radius: 0 0 6px 6px; }

@media (max-width: 1024px) {
  .table th, .table td { padding: 10px 8px; }
  .table th { font-size: 11px; }
  .action-badge, .type-tag { padding: 2px 8px; font-size: 10px; }
}

@media (max-width: 640px) {
  .filter-row { flex-direction: column; align-items: stretch; gap: 10px; }
  .search-input { width: 100%; }
  .title { font-size: 20px; }
}
</style>