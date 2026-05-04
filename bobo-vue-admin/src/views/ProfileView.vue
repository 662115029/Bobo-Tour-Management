<template>
  <div>
    <h1 class="title">Profile</h1>
    <div class="content">
      <div class="profile-card">
        <div class="profile-header">
          <div class="avatar">{{ initials }}</div>
          <div class="profile-info">
            <h2>{{ admin.name }}</h2>
          </div>
        </div>
        <div class="profile-details">
          <div class="detail-row">
            <label>Admin ID</label>
            <span>{{ admin.admin_id }}</span>
          </div>
          <div class="detail-row">
            <label>Status</label>
            <span class="badge" :class="admin.status?.toLowerCase()">{{ admin.status }}</span>
          </div>
          <div class="detail-row">
            <label>Created</label>
            <span>{{ formatDate(admin.created_at) }}</span>
          </div>
          <div class="detail-row">
            <label>Last Updated</label>
            <span>{{ formatDate(admin.updated_at) }}</span>
          </div>
        </div>
      </div>
      <button class="logout-btn" @click="handleLogout">Logout</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const admin = ref({})
const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const initials = ref('')

onMounted(async () => {
  const adminId = localStorage.getItem('admin_id')
  if (!adminId) {
    router.push('/login')
    return
  }
  
  try {
    const res = await fetch(`${API_BASE}/admin/me?admin_id=${adminId}`)
    const data = await res.json()
    
    if (data.admin_id) {
      admin.value = data
      initials.value = data.name?.split(' ').map(w => w[0]).join('').toUpperCase() || '?'    }
  } catch (e) {
    console.error('Failed to load admin:', e)
  }
})

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', {
    day: '2-digit', month: 'short', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })
}

const handleLogout = () => {
  localStorage.removeItem('admin_id')
  localStorage.removeItem('admin_name')
  localStorage.removeItem('admin_username')
  router.push('/login')
}
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

.content {
  background: white;
  padding: 24px;
  border-radius: 8px;
  margin: 0 20px;
}

.profile-card {
  background: #f9f9f9;
  border-radius: 12px;
  padding: 24px;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: #1a1a2e;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 600;
}

.profile-info h2 {
  margin: 0 0 4px;
  font-size: 20px;
  color: #1a1a2e;
}

.profile-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.detail-row label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.detail-row span {
  font-size: 14px;
  color: #333;
}

.badge {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.logout-btn {
  margin-top: 24px;
  padding: 12px 24px;
  background: #ffebee;
  color: #c62828;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.logout-btn:hover {
  background: #ffcdd2;
}
</style>