<template>
  <div>
    <h1 class="title">Admins</h1>
    
    <div class="table-container">
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>NAME</th>
            <th>STATUS</th>
            <th>CREATED AT</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="admin in admins" :key="admin.admin_id">
            <td>{{ admin.admin_id }}</td>
            <td>{{ admin.name }}</td>
            <td>
              <span class="badge" :class="admin.status">{{ admin.status }}</span>
            </td>
            <td>{{ formatDate(admin.created_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'
const admins = ref([])

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { 
    day: '2-digit', 
    month: 'short', 
    year: 'numeric'
  })
}

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/admin/admins`)
    const data = await res.json()
    admins.value = data.items || []
  } catch (e) {
    console.error('Failed to load admins:', e)
  }
})
</script>

<style scoped>
.title {
  font-size: 24px;
  margin-bottom: 24px;
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

.badge.inactive {
  background: #ffebee;
  color: #c62828;
}
</style>