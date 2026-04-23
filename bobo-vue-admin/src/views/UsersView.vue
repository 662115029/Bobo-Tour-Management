<template>
  <div>
    <h1 class="title">Users Management</h1>
    
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

    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>NAME</th>
            <th>STATUS</th>
            <th>SCORE</th>
            <th>JOBS</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in mockUsers" :key="user.id">
            <td>
              <div class="user-cell">
                <span class="avatar">{{ user.initials }}</span>
                <span>{{ user.name }}</span>
              </div>
            </td>
            <td>
              <span class="badge" :class="user.status.toLowerCase()">{{ user.status }}</span>
            </td>
            <td>{{ user.score.toFixed(1) }}</td>
            <td>{{ user.jobs }}</td>
            <td>
              <span class="action-link">View</span>
              <span class="action-link delete">{{ user.status === 'Active' ? 'Ban' : 'Unban' }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { mockUsers } from '../data/mockData'

const activeTab = ref('Freelancer')
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
}

.tabs {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  border-bottom: 2px solid #eee;
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
  color: #06C755;
  border-bottom: 2px solid #06C755;
  margin-bottom: -2px;
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

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
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

.badge.banned {
  background: #ffebee;
  color: #c62828;
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