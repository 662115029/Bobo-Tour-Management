<template>
  <div>
    <h1 class="title">Admin Logs</h1>

    <div class="filter-row">
      <input type="text" v-model="search" placeholder="Search action or target..." class="search-input" />
      <div class="filter-group">
        <select v-model="typeFilter" class="filter-select">
          <option value="All">All Types</option>
          <option value="FREELANCER">Freelancer</option>
          <option value="EMPLOYER">Employer</option>
          <option value="JOB">Job</option>
          <option value="ADMIN">Admin</option>
        </select>
        <select v-model="actionFilter" class="filter-select">
          <option value="All">All Actions</option>
          <option value="APPROVE">Approve</option>
          <option value="REJECT">Reject</option>
          <option value="BAN">Ban</option>
          <option value="UNBAN">Unban</option>
          <option value="DELETE">Delete</option>
          <option value="UPDATE">Update</option>
        </select>
      </div>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th style="width:14%">ACTION</th>
            <th style="width:14%">TYPE</th>
            <th style="width:22%">TARGET</th>
            <th style="width:30%">NOTE</th>
            <th style="width:12%">ADMIN</th>
            <th style="width:16%">WHEN</th>
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
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const search = ref('')
const typeFilter = ref('All')
const actionFilter = ref('All')
const logs = ref([])

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
  return logs.value.filter(log => {
    const matchSearch = search.value === '' ||
      (log.action_type || '').toLowerCase().includes(search.value.toLowerCase()) ||
      (log.target_name || '').toLowerCase().includes(search.value.toLowerCase()) ||
      (log.note || '').toLowerCase().includes(search.value.toLowerCase())
    const matchType = typeFilter.value === 'All' || (log.target_type || '').toUpperCase() === typeFilter.value
    const matchAction = actionFilter.value === 'All' || (log.action_type || '').toUpperCase() === actionFilter.value
    return matchSearch && matchType && matchAction
  })
})

onMounted(async () => {
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
.title { font-size: 24px; margin-bottom: 24px; }

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
</style>