<template>
    <div>
        <div class="topbar">
            <span class="back-link" @click="router.back()">← Back to Verification</span>
        </div>

        <div v-if="loading" class="loading">⏳ Loading...</div>

        <div v-else-if="fl">

            <!-- Hero Card -->
            <div class="hero-card">
                <div class="hero-left">
                    <img v-if="fl.fl_profile_image_url" :src="fl.fl_profile_image_url" class="avatar" />
                    <div v-else class="avatar-placeholder">{{ fl.fl_name?.[0] || '?' }}</div>
                    <div>
                        <span class="badge" :class="fl.fl_verify_status?.toLowerCase()">{{ fl.fl_verify_status }}</span>
                        <h2 class="name">{{ fl.fl_name }}</h2>
                        <p class="sub">{{ fl.line_user_id || '-' }}</p>
                    </div>
                </div>
                <div class="rating-box">
                    <span class="rating-label">RATING</span>
                    <span class="rating-value">⭐ {{ fl.fl_rating_avg ?? '-' }}</span>
                </div>
            </div>

            <div class="sections">

                <!-- Basic Info -->
                <div class="section-card">
                    <h3 class="section-title">👤 Basic Info</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Freelancer ID</label>
                            <span class="muted">{{ fl.fl_id }}</span>
                        </div>
                        <div class="info-item">
                            <label>Date of Birth</label>
                            <span>{{ formatDate(fl.fl_date_of_birth) }}</span>
                        </div>
                        <div class="info-item">
                            <label>Active</label>
                            <span>{{ fl.fl_is_active ? '✅ Active' : '❌ Inactive' }}</span>
                        </div>
                        <div class="info-item">
                            <label>Created At</label>
                            <span class="muted">{{ formatDateTime(fl.fl_created_at) }}</span>
                        </div>
                        <div class="info-item">
                            <label>Last Updated</label>
                            <span class="muted">{{ formatDateTime(fl.fl_updated_at) }}</span>
                        </div>
                    </div>
                    <div class="info-item mt" v-if="fl.fl_address">
                        <label>Address</label>
                        <span>{{ fl.fl_address }}</span>
                    </div>
                    <div class="info-item mt" v-if="fl.fl_bio">
                        <label>Bio</label>
                        <span>{{ fl.fl_bio }}</span>
                    </div>
                </div>

                <!-- Languages -->
                <div class="section-card" v-if="languages.length">
                    <h3 class="section-title">🌐 Languages</h3>
                    <div class="tag-row">
                        <span v-for="l in languages" :key="l.fl_language_id" class="tag blue">{{ l.fl_language_name
                            }}</span>
                    </div>
                </div>

                <!-- Vehicle -->
                <div class="section-card" v-if="vehicle">
                    <h3 class="section-title">🚐 Vehicle</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Type</label>
                            <span>{{ vehicle.fl_vehicle_type }}</span>
                        </div>
                        <div class="info-item">
                            <label>Brand / Model</label>
                            <span>{{ vehicle.fl_vehicle_brand }} {{ vehicle.fl_vehicle_model }}</span>
                        </div>
                        <div class="info-item">
                            <label>Year</label>
                            <span>{{ vehicle.fl_vehicle_year }}</span>
                        </div>
                        <div class="info-item">
                            <label>Seats</label>
                            <span>{{ vehicle.fl_vehicle_seat_capa }} seats</span>
                        </div>
                        <div class="info-item">
                            <label>License Plate</label>
                            <span>{{ vehicle.fl_vehicle_license_plate }}</span>
                        </div>
                    </div>
                </div>

                <!-- Pickup Areas -->
                <div class="section-card" v-if="pickupAreas.length">
                    <h3 class="section-title">📍 Pickup Areas</h3>
                    <div class="tag-row">
                        <span v-for="a in pickupAreas" :key="a.fl_area_id" class="tag orange">{{ a.fl_area_name
                            }}</span>
                    </div>
                </div>

                <!-- Availability -->
                <div class="section-card" v-if="availability.length">
                    <h3 class="section-title">📅 Availability</h3>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Start Date</th>
                                <th>End Date</th>
                                <th>Active</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="a in availability" :key="a.fl_available_id">
                                <td>{{ formatDate(a.fl_available_start_date) }}</td>
                                <td>{{ formatDate(a.fl_available_end_date) }}</td>
                                <td>{{ a.is_active ? '✅' : '❌' }}</td>
                            </tr>
                        </tbody>
                    </table>
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
                            <tr v-for="d in documents" :key="d.fl_doc_id">
                                <td>{{ d.fl_doc_type }}</td>
                                <td>
                                    <span class="tag" :class="{
                                        green: d.fl_doc_status === 'APPROVED',
                                        red: d.fl_doc_status === 'REJECTED',
                                        gray: d.fl_doc_status === 'PENDING'
                                    }">{{ d.fl_doc_status }}</span>
                                </td>
                                <td class="muted">{{ formatDateTime(d.fl_uploaded_at) }}</td>
                                <td><a :href="d.file_url" target="_blank" class="link">View</a></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

            </div>
        </div>

        <div v-else class="loading">Freelancer not found.</div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { API_BASE } from '../data/api'

const route = useRoute()
const router = useRouter()
const fl = ref(null)
const languages = ref([])
const vehicle = ref(null)
const pickupAreas = ref([])
const availability = ref([])
const documents = ref([])
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
        const [flRes, langRes, vehicleRes, areaRes, availRes, docRes] = await Promise.all([
            fetch(`${API_BASE}/freelancers?limit=500`),
            fetch(`${API_BASE}/fl-languages?limit=500`),
            fetch(`${API_BASE}/fl-vehicle?limit=500`),
            fetch(`${API_BASE}/fl-pickup-areas?limit=500`),
            fetch(`${API_BASE}/fl-availability?limit=500`),
            fetch(`${API_BASE}/fl-documents?limit=500`),
        ])
        const [flData, langData, vehicleData, areaData, availData, docData] = await Promise.all([
            flRes.json(), langRes.json(), vehicleRes.json(),
            areaRes.json(), availRes.json(), docRes.json(),
        ])

        fl.value = (flData.items || []).find(f => f.fl_id === id) || null
        languages.value = (langData.items || []).filter(l => l.fl_id === id)
        vehicle.value = (vehicleData.items || []).find(v => v.fl_id === id) || null
        pickupAreas.value = (areaData.items || []).filter(a => a.fl_id === id)
        availability.value = (availData.items || []).filter(a => a.fl_id === id)
        documents.value = (docData.items || []).filter(d => d.fl_id === id)
    } catch (e) {
        console.error('Failed to load freelancer:', e)
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
    background: #e3f2fd;
    color: #1976d2;
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

.tag.orange {
    background: #fff3e0;
    color: #f57c00;
}

.tag.green {
    background: #f0fdf4;
    color: #166534;
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