<template>
  <div class="login-page">
    <div class="login-box">
      <h1>Admin Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="username" placeholder="Username" required />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" placeholder="Password" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const API_BASE = import.meta.env.VITE_API_BASE || 'http://127.0.0.1:8000'

const handleLogin = async () => {
  error.value = ''
  loading.value = true
  
  try {
    const res = await fetch(`${API_BASE}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    const data = await res.json()
    
    if (data.success) {
      localStorage.setItem('admin_id', data.admin.admin_id)
      localStorage.setItem('admin_name', data.admin.name)
      router.push('/')
    } else {
      error.value = data.error || 'Login failed'
    }
  } catch (e) {
    error.value = 'Connection error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1a1a2e;
}

.login-box {
  background: white;
  padding: 40px;
  border-radius: 12px;
  width: 360px;
}

.login-box h1 {
  margin: 0 0 24px;
  font-size: 24px;
  color: #1a1a2e;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.form-group input {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
}

.form-group input:focus {
  outline: none;
  border-color: #1a1a2e;
}

.error {
  color: #dc3545;
  font-size: 14px;
  margin-bottom: 16px;
}

button {
  width: 100%;
  padding: 14px;
  background: #1a1a2e;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
}

button:hover {
  background: #2a2a4e;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>