<template>
  <div>
    <div class="header">
      <h1 class="title">Admin Logs</h1>
      <span class="more-icon">...</span>
    </div>
    
    <div class="filter-row">
      <div class="date-input">
        <input type="text" value="04/20/2026" class="date-field" />
        <span class="calendar-icon">📅</span>
      </div>
      <select v-model="actionFilter" class="filter-select">
        <option value="All">All Actions</option>
        <option value="VERIFY">VERIFY</option>
        <option value="REJECT">REJECT</option>
        <option value="BAN">BAN</option>
        <option value="DELETE">DELETE</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ADMIN</th>
            <th>ACTION</th>
            <th>TARGET</th>
            <th>TIME</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in filteredLogs" :key="log.id">
            <td>{{ log.admin }}</td>
            <td>
              <span class="action-badge" :class="log.action.toLowerCase()">{{ log.action }}</span>
            </td>
            <td>{{ log.target }}</td>
            <td>{{ log.time }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { mockLogs } from '../data/mockData'

const actionFilter = ref('All')

const filteredLogs = computed(() => {
  if (actionFilter.value === 'All') return mockLogs
  return mockLogs.filter(log => log.action === actionFilter.value)
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.more-icon {
  font-size: 24px;
  cursor: pointer;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.date-input {
  position: relative;
}

.date-field {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  width: 180px;
}

.calendar-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
}

.filter-select {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  min-width: 140px;
}

.table-container {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.table th {
  font-size: 12px;
  color: #666;
  font-weight: 600;
  background: #f9f9f9;
}

.action-badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.action-badge.verify {
  background: #e8f5e9;
  color: #2e7d32;
}

.action-badge.reject {
  background: #ffebee;
  color: #c62828;
}

.action-badge.ban {
  background: #fff3e0;
  color: #f57c00;
}

.action-badge.delete {
  background: #ffebee;
  color: #c62828;
}
</style>