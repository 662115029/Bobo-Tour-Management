<template>
  <div class="job-list">
    <div class="header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h2>Available Jobs</h2>
    </div>

    <div v-if="jobs.length === 0" class="empty">
      No available jobs at the moment.
    </div>

    <div
      v-for="job in jobs"
      :key="job.id"
      class="job-card"
      @click="goToDetail(job.id)"
    >
      <div class="job-header">
        <span class="job-title">{{ job.title }}</span>
        <span class="job-status">Available</span>
      </div>

      <div class="job-info">
        <div class="info-row">
          <span class="label">📅 Date</span>
          <span>{{ formatDate(job.date) }}</span>
        </div>
        <div class="info-row">
          <span class="label">⏰ Time</span>
          <span>{{ job.time }}</span>
        </div>
        <div class="info-row">
          <span class="label">📍 Pickup</span>
          <span>{{ job.pickup }}</span>
        </div>
        <div class="info-row">
          <span class="label">🏁 Drop-off</span>
          <span>{{ job.destination }}</span>
        </div>
        <div class="info-row">
          <span class="label">👥 Passengers</span>
          <span>{{ job.passengers }} people</span>
        </div>
      </div>

      <div class="job-footer">
        <span class="employer">{{ job.employer }}</span>
        <span class="view-detail">View Details →</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const jobs = ref([])

onMounted(async () => {
  try {
    const res = await fetch(`${API_BASE}/jobs`)
    const data = await res.json()
    jobs.value = (data.items || []).map(j => ({
      id: j.job_id,
      title: j.job_title,
      date: j.job_start_date,
      time: '08:00',
      pickup: 'TBD',
      destination: 'TBD',
      passengers: j.job_required_seat,
      employer: j.company
    }))
  } catch (e) {
    console.error('Failed to fetch jobs:', e)
  }
})

function goBack() {
  router.push('/')
}

function goToDetail(id) {
  router.push(`/jobs/${id}`)
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.job-list {
  padding: 16px;
  max-width: 480px;
  margin: 0 auto;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.header h2 {
  margin: 0;
  font-size: 18px;
}

.back-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #06C755;
  padding: 0;
}

.job-card {
  background: white;
  border-radius: 16px;
  padding: 16px;
  margin-bottom: 12px;
  border: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.1s;
}

.job-card:active {
  transform: scale(0.98);
}

.job-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.job-title {
  font-weight: bold;
  font-size: 16px;
}

.job-status {
  background: #e6f9ee;
  color: #06C755;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.job-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.label {
  color: #888;
}

.job-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 10px;
  font-size: 13px;
}

.employer {
  color: #555;
}

.view-detail {
  color: #06C755;
  font-weight: bold;
}

.empty {
  text-align: center;
  color: #999;
  margin-top: 48px;
}
</style>
