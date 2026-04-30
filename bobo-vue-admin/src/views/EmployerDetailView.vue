<template>
  <div>
    <div class="topbar">
      <span class="back-link" @click="router.back()">← Back</span>
    </div>

    <div v-if="loading" class="loading">⏳ Loading...</div>

    <div v-else-if="em">

      <!-- Hero Card -->
      <div class="hero-card">
        <div class="hero-left">
          <img v-if="em.em_profile_image_url" :src="em.em_profile_image_url" class="avatar" />
          <div v-else class="avatar-placeholder">{{ em.em_name?.[0] || '?' }}</div>
          <div>
            <span class="badge" :class="em.em_verify_status?.toLowerCase()">{{ em.em_verify_status }}</span>
            <h2 class="name">{{ em.em_name }}</h2>
            <p v-if="em.em_bio" class="bio">{{ em.em_bio }}</p>
            <p v-else class="bio muted">No bio</p>
          </div>
        </div>
        <div class="rating-box">
          <span class="rating-label">RATING</span>
          <span class="rating-value">⭐ {{ em.em_rating_avg ?? '-' }}</span>
        </div>
      </div>

      <div class="sections">

        <!-- 1. Basic Info -->
        <div class="section-card">
          <h3 class="section-title">🏢 Basic Info</h3>
          <div class="mini-grid">
            <div class="mini-item"><label>Username</label>
              <span>@{{ em.em_username }}</span>
            </div>
            <div class="mini-item"><label>Phone</label>
              <span>{{ em.em_phone || '-' }}</span>
            </div>
            <div class="mini-item"><label>Active</label>
              <span>{{ em.em_is_active ? '✅ Active' : '❌ Inactive' }}</span>
            </div>
            <div class="mini-item"><label>Rating</label>
              <span>⭐ {{ em.em_rating_avg ?? '-' }}</span>
            </div>
            <div class="mini-item"><label>Created</label>
              <span class="muted">{{ formatDateTime(em.em_created_at) }}</span>
            </div>
            <div class="mini-item"><label>Last Updated</label>
              <span class="muted">{{ formatDateTime(em.em_updated_at) }}</span>
            </div>
          </div>
          <div v-if="em.em_address" style="margin-top:16px;">
            <div class="mini-item"><label>Address</label><span>{{ em.em_address }}</span></div>
          </div>
        </div>

        <!-- 2. Documents -->
        <div class="section-card" v-if="documents.length">
          <h3 class="section-title">📄 Documents</h3>
          <div class="doc-grid">
            <div v-for="d in documents" :key="d.em_doc_id" class="doc-card">
              <div class="doc-preview">
                <a :href="d.file_url" target="_blank">
                  <img v-if="isImage(d.file_url)" :src="d.file_url" class="doc-img"
                    @error="e => e.target.style.display='none'" />
                  <div v-else class="doc-icon">📄</div>
                </a>
              </div>
              <div class="doc-info">
                <p class="doc-type">{{ d.em_doc_type }}</p>
                <span class="tag" :class="{
                  green: d.em_doc_status === 'APPROVED',
                  red: d.em_doc_status === 'REJECTED',
                  gray: d.em_doc_status === 'PENDING'
                }">{{ d.em_doc_status }}</span>
                <p class="doc-date">{{ formatDateTime(d.em_uploaded_at) }}</p>
                <a :href="d.file_url" target="_blank" class="link">View File →</a>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Jobs -->
        <div class="section-card" v-if="jobs.length">
          <h3 class="section-title">💼 Jobs <span class="count-badge">{{ jobs.length }}</span></h3>
          <table class="data-table">
            <thead>
              <tr>
                <th>Job Title</th>
                <th style="width:12%">Status</th>
                <th style="width:16%">Start</th>
                <th style="width:16%">End</th>
                <th style="width:12%">Price</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="j in jobs" :key="j.job_id">
                <td>{{ j.job_title }}</td>
                <td>
                  <span class="tag" :class="{
                    blue: j.job_status === 'OPEN' || j.job_status === 'MATCHING',
                    purple: j.job_status === 'SELECTED',
                    orange: j.job_status === 'IN_PROGRESS',
                    gray: j.job_status === 'COMPLETED',
                    red: j.job_status === 'CANCELLED'
                  }">{{ j.job_status }}</span>
                </td>
                <td class="muted">{{ formatDate(j.job_start_date) }}</td>
                <td class="muted">{{ formatDate(j.job_end_date) }}</td>
                <td>{{ j.job_price ? '฿' + Number(j.job_price).toLocaleString() : '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
    </div>

    <div v-else class="loading">Employer not found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const route = useRoute()
const router = useRouter()
const em = ref(null)
const documents = ref([])
const jobs = ref([])
const loading = ref(true)

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

const formatDateTime = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('en-GB', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })
}

const isImage = (url) => {
  if (!url) return false
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url)
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [emRes, docRes, jobsRes] = await Promise.all([
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/em-documents?limit=500`),
      fetch(`${API_BASE}/jobs?limit=500`),
    ])
    const [emData, docData, jobsData] = await Promise.all([
      emRes.json(), docRes.json(), jobsRes.json(),
    ])

    em.value = (emData.items || []).find(e => e.em_id === id) || null
    documents.value = (docData.items || []).filter(d => d.em_id === id)
    jobs.value = (jobsData.items || []).filter(j => j.em_id === id)
  } catch (e) {
    console.error('Failed to load employer:', e)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.topbar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.back-link { color: #0066cc; cursor: pointer; font-size: 14px; }
.loading { color: #999; padding: 40px 0; text-align: center; }

.hero-card {
  background: white; border-radius: 12px; padding: 28px;
  display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;
}
.hero-left { display: flex; align-items: flex-start; gap: 16px; }
.avatar { width: 72px; height: 72px; border-radius: 50%; object-fit: cover; }
.avatar-placeholder {
  width: 72px; height: 72px; border-radius: 50%;
  background: #f3e5f5; color: #7b1fa2;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px; font-weight: 700; flex-shrink: 0;
}
.name { font-size: 20px; margin: 4px 0 0; }
.bio { font-size: 13px; color: #666; margin: 4px 0 0; line-height: 1.5; max-width: 400px; }
.bio.muted { color: #bbb; font-style: italic; }
.rating-box { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; }
.rating-label { font-size: 11px; color: #999; font-weight: 600; text-transform: uppercase; }
.rating-value { font-size: 22px; font-weight: 700; }

.sections { display: flex; flex-direction: column; gap: 16px; }
.section-card { background: white; border-radius: 12px; padding: 24px; }
.section-title {
  font-size: 14px; font-weight: 600; color: #444;
  margin: 0 0 20px; padding-bottom: 12px; border-bottom: 1px solid #eee;
  display: flex; align-items: center; gap: 8px;
}
.count-badge {
  display: inline-flex; align-items: center; justify-content: center;
  background: #f0f4ff; color: #3d5afe; border-radius: 20px;
  font-size: 11px; font-weight: 700; padding: 2px 8px;
}

.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.mini-item { display: flex; flex-direction: column; gap: 4px; }
.mini-item label { font-size: 10px; color: #999; font-weight: 600; text-transform: uppercase; }
.mini-item span { font-size: 13px; color: #222; }
.muted { color: #888 !important; font-size: 12px !important; }
.link { color: #0066cc; font-size: 12px; }

.tag { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.tag.blue { background: #e3f2fd; color: #1976d2; }
.tag.purple { background: #f3e5f5; color: #7b1fa2; }
.tag.orange { background: #fff3e0; color: #f57c00; }
.tag.gray { background: #f5f5f5; color: #666; }
.tag.red { background: #fef2f2; color: #991b1b; }
.tag.green { background: #f0fdf4; color: #166534; }

/* Documents */
.doc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.doc-card { border: 1px solid #eee; border-radius: 10px; overflow: hidden; display: flex; flex-direction: column; }
.doc-preview { background: #f9f9f9; height: 140px; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.doc-img { width: 100%; height: 100%; object-fit: cover; }
.doc-icon { font-size: 40px; }
.doc-info { padding: 12px; display: flex; flex-direction: column; gap: 6px; }
.doc-type { font-size: 12px; font-weight: 600; color: #444; margin: 0; }
.doc-date { font-size: 11px; color: #999; margin: 0; }

.data-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.data-table th { text-align: left; font-size: 11px; font-weight: 600; color: #999; text-transform: uppercase; padding: 8px 12px; border-bottom: 2px solid #eee; }
.data-table td { padding: 10px 12px; border-bottom: 1px solid #f5f5f5; color: #333; }
.data-table tr:last-child td { border-bottom: none; }

.badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; width: fit-content; }
.badge.pending { background: #fff3e0; color: #f57c00; }
.badge.verified { background: #e8f5e9; color: #2e7d32; }
.badge.not_verified { background: #ffebee; color: #c62828; }
</style>