<template>
    <div>
        <div class="topbar">
            <span class="back-link" @click="router.back()">← Back to Verification</span>
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
                        <p class="sub">@{{ em.em_username }}</p>
                    </div>
                </div>
                <div class="rating-box">
                    <span class="rating-label">RATING</span>
                    <span class="rating-value">⭐ {{ em.em_rating_avg ?? '-' }}</span>
                </div>
            </div>

            <div class="sections">

                <!-- Basic Info -->
                <div class="section-card">
                    <h3 class="section-title">🏢 Basic Info</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Employer ID</label>
                            <span class="muted">{{ em.em_id }}</span>
                        </div>
                        <div class="info-item">
                            <label>Phone</label>
                            <span>{{ em.em_phone || '-' }}</span>
                        </div>
                        <div class="info-item">
                            <label>Active</label>
                            <span>{{ em.em_is_active ? '✅ Active' : '❌ Inactive' }}</span>
                        </div>
                        <div class="info-item">
                            <label>Created At</label>
                            <span class="muted">{{ formatDateTime(em.em_created_at) }}</span>
                        </div>
                        <div class="info-item">
                            <label>Last Updated</label>
                            <span class="muted">{{ formatDateTime(em.em_updated_at) }}</span>
                        </div>
                    </div>
                    <div class="info-item mt" v-if="em.em_address">
                        <label>Address</label>
                        <span>{{ em.em_address }}</span>
                    </div>
                    <div class="info-item mt" v-if="em.em_bio">
                        <label>Bio</label>
                        <span>{{ em.em_bio }}</span>
                    </div>
                </div>

                <!-- Documents -->
                <div class="section-card" v-if="documents.length">
                    <h3 class="section-title">📄 Documents</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Type</th>
                                <th>Status</th>
                                <th>Uploaded At</th>
                                <th>File</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="d in documents" :key="d.em_doc_id">
                                <td>{{ d.em_doc_type }}</td>
                                <td>
                                    <span class="tag" :class="{
                                        green: d.em_doc_status === 'APPROVED',
                                        red: d.em_doc_status === 'REJECTED',
                                        gray: d.em_doc_status === 'PENDING'
                                    }">{{ d.em_doc_status }}</span>
                                </td>
                                <td class="muted">{{ formatDateTime(d.em_uploaded_at) }}</td>
                                <td><a :href="d.file_url" target="_blank" class="link">View</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Jobs posted by this employer -->
                <div class="section-card" v-if="jobs.length">
                    <h3 class="section-title">💼 Jobs ({{ jobs.length }})</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Job Title</th>
                                <th>Status</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Price</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="j in jobs" :key="j.job_id">
                                <td>{{ j.job_title }}</td>
                                <td>
                                    <span class="tag" :class="{
                                        blue: j.job_status === 'OPEN' || j.job_status === 'MATCHING',
                                        green: j.job_status === 'SELECTED' || j.job_status === 'COMPLETED',
                                        orange: j.job_status === 'IN_PROGRESS',
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
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.back-link {
    color: #0066cc;
    cursor: pointer;
    font-size: 14px;
}

.loading {
    color: #999;
    padding: 40px 0;
    text-align: center;
}

.hero-card {
    background: white;
    border-radius: 12px;
    padding: 28px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 16px;
}

.hero-left {
    display: flex;
    align-items: center;
    gap: 16px;
}

.avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    object-fit: cover;
}

.avatar-placeholder {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #e8f5e9;
    color: #2e7d32;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: 700;
}

.name {
    font-size: 20px;
    margin: 4px 0 0;
}

.sub {
    color: #888;
    font-size: 13px;
    margin: 2px 0 0;
}

.rating-box {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 4px;
}

.rating-label {
    font-size: 11px;
    color: #999;
    font-weight: 600;
    text-transform: uppercase;
}

.rating-value {
    font-size: 22px;
    font-weight: 700;
}

.sections {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.section-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
}

.section-title {
    font-size: 14px;
    font-weight: 600;
    color: #444;
    margin: 0 0 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid #eee;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.info-item.mt {
    margin-top: 16px;
}

.info-item label {
    font-size: 11px;
    color: #999;
    font-weight: 600;
    text-transform: uppercase;
}

.info-item span {
    font-size: 15px;
    color: #222;
}

.muted {
    color: #888 !important;
    font-size: 13px !important;
}

.link {
    color: #0066cc;
    font-size: 13px;
}

.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.tag {
    display: inline-block;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
}

.tag.blue {
    background: #e3f2fd;
    color: #1976d2;
}

.tag.green {
    background: #f0fdf4;
    color: #166534;
}

.tag.orange {
    background: #fff3e0;
    color: #f57c00;
}

.tag.red {
    background: #fef2f2;
    color: #991b1b;
}

.tag.gray {
    background: #f5f5f5;
    color: #666;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 14px;
}

.data-table th {
    text-align: left;
    font-size: 11px;
    font-weight: 600;
    color: #999;
    text-transform: uppercase;
    padding: 8px 12px;
    border-bottom: 2px solid #eee;
}

.data-table td {
    padding: 10px 12px;
    border-bottom: 1px solid #f5f5f5;
    color: #333;
}

.data-table tr:last-child td {
    border-bottom: none;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    width: fit-content;
}

.badge.pending {
    background: #fff3e0;
    color: #f57c00;
}

.badge.verified {
    background: #e8f5e9;
    color: #2e7d32;
}

.badge.not_verified {
    background: #ffebee;
    color: #c62828;
}
</style>