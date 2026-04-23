<template>
  <div>
    <h1 class="title">Jobs Management</h1>
    
    <div class="filter-row">
      <input 
        type="text" 
        v-model="search" 
        placeholder="Search job title..." 
        class="search-input"
      />
      <select v-model="statusFilter" class="filter-select">
        <option value="All">All Status</option>
        <option value="Active">Active</option>
        <option value="Closed">Closed</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>JOB TITLE</th>
            <th>COMPANY</th>
            <th>DATE</th>
            <th>STATUS</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="job in filteredJobs" :key="job.id">
            <td>{{ job.title }}</td>
            <td>{{ job.company }}</td>
            <td>{{ job.date }}</td>
            <td>
              <span class="badge" :class="job.status.toLowerCase()">{{ job.status }}</span>
            </td>
            <td>
              <span class="action-link">View</span>
              <span class="action-link delete">Delete</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { mockJobs } from '../data/mockData'

const search = ref('')
const statusFilter = ref('All')

const filteredJobs = computed(() => {
  return mockJobs.filter(job => {
    const matchSearch = job.title.toLowerCase().includes(search.value.toLowerCase())
    const matchStatus = statusFilter.value === 'All' || job.status === statusFilter.value
    return matchSearch && matchStatus
  })
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.filter-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.search-input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  width: 280px;
  font-size: 14px;
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

.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.badge.closed {
  background: #f5f5f5;
  color: #666;
}

.action-link {
  color: #0066cc;
  cursor: pointer;
  margin-right: 12px;
}

.action-link.delete {
  color: #dc3545;
}
</style>