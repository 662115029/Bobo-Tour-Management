<template>
  <div class="job-detail">
    <div class="header">
      <button @click="goBack" class="back-btn">← Back</button>
      <h2>Job Details</h2>
    </div>

    <div v-if="!job" class="not-found">
      Job not found.
    </div>

    <div v-else>
      <div class="detail-card">
        <h3>{{ job.title }}</h3>
        <span class="status-badge">Available</span>

        <div class="section">
          <h4>Schedule</h4>
          <div class="info-row">
            <span class="label">📅 Date</span>
            <span>{{ formatDate(job.date) }}</span>
          </div>
          <div class="info-row">
            <span class="label">⏰ Time</span>
            <span>{{ job.time }}</span>
          </div>
        </div>

        <div class="section">
          <h4>Route</h4>
          <div class="info-row">
            <span class="label">📍 Pickup</span>
            <span>{{ job.pickup }}</span>
          </div>
          <div class="info-row">
            <span class="label">🏁 Drop-off</span>
            <span>{{ job.destination }}</span>
          </div>
        </div>

        <div class="section">
          <h4>Details</h4>
          <div class="info-row">
            <span class="label">👥 Passengers</span>
            <span>{{ job.passengers }} people</span>
          </div>
          <div class="info-row">
            <span class="label">🏢 Employer</span>
            <span>{{ job.employer }}</span>
          </div>
        </div>
      </div>

      <!-- action buttons -->
      <div v-if="!responded" class="actions">
        <button
          @click="handleAccept"
          class="btn-accept"
          :disabled="submitting"
        >
          {{ submitting ? 'Processing...' : '✅ Accept Job' }}
        </button>
        <button
          @click="handleDecline"
          class="btn-decline"
          :disabled="submitting"
        >
          ❌ Decline
        </button>
      </div>

      <!-- response confirmation -->
      <div v-else class="response-card" :class="responseType">
        <p v-if="responseType === 'accepted'">
          ✅ You have accepted this job. The employer will be notified.
        </p>
        <p v-else>
          ❌ You have declined this job.
        </p>
        <button @click="goToJobs" class="btn-secondary">
          Back to Job List
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { mockJobs } from '../mockData.js'

const router = useRouter()
const route = useRoute()
const FASTAPI_URL = import.meta.env.VITE_FASTAPI_URL

const props = defineProps({
  user: Object
})

const job = computed(() =>
  mockJobs.find(j => j.id === parseInt(route.params.id))
)

const submitting = ref(false)
const responded = ref(false)
const responseType = ref(null)

function goBack() {
  router.push('/jobs')
}

function goToJobs() {
  router.push('/jobs')
}

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleDateString('th-TH', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

async function handleAccept() {
  submitting.value = true
  try {
    await fetch(`${FASTAPI_URL}/jobs/${job.value.id}/accept`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        line_user_id: props.user.lineUserId,
        job_id: job.value.id
      })
    })
    responded.value = true
    responseType.value = 'accepted'
  } catch {
    alert('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง')
  } finally {
    submitting.value = false
  }
}

async function handleDecline() {
  submitting.value = true
  try {
    await fetch(`${FASTAPI_URL}/jobs/${job.value.id}/decline`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        line_user_id: props.user.lineUserId,
        job_id: job.value.id
      })
    })
    responded.value = true
    responseType.value = 'declined'
  } catch {
    alert('เกิดข้อผิดพลาด กรุณาลองใหม่อีกครั้ง')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.job-detail {
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

.detail-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  border: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  margin-bottom: 16px;
}

.detail-card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}

.status-badge {
  background: #e6f9ee;
  color: #06C755;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  display: inline-block;
  margin-bottom: 16px;
}

.section {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.section h4 {
  margin: 0 0 10px;
  font-size: 14px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 8px;
}

.label {
  color: #888;
}

.actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-accept {
  background: #06C755;
  color: white;
  border: none;
  border-radius: 12px;
  padding: 16px;
  font-size: 16px;
  font-weight: bold;
  width: 100%;
  cursor: pointer;
}

.btn-accept:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-decline {
  background: white;
  color: #e53935;
  border: 2px solid #e53935;
  border-radius: 12px;
  padding: 14px;
  font-size: 16px;
  width: 100%;
  cursor: pointer;
}

.btn-decline:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.response-card {
  border-radius: 16px;
  padding: 20px;
  text-align: center;
}

.response-card.accepted {
  background: #e6f9ee;
  border: 1px solid #06C755;
}

.response-card.declined {
  background: #fdecea;
  border: 1px solid #e53935;
}

.btn-secondary {
  background: white;
  color: #06C755;
  border: 2px solid #06C755;
  border-radius: 12px;
  padding: 12px 24px;
  font-size: 14px;
  cursor: pointer;
  margin-top: 12px;
}

.not-found {
  text-align: center;
  color: #999;
  margin-top: 48px;
}
</style>
