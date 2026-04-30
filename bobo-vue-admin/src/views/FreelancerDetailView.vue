<template>
  <div>
    <div class="topbar">
      <span class="back-link" @click="router.back()">← Back</span>
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
            <p v-if="fl.fl_bio" class="bio">{{ fl.fl_bio }}</p>
            <p v-else class="bio muted">No bio</p>
          </div>
        </div>
        <div class="rating-box">
          <span class="rating-label">RATING</span>
          <span class="rating-value">⭐ {{ fl.fl_rating_avg ?? '-' }}</span>
        </div>
      </div>

      <div class="sections">

        <!-- 1. Basic Info -->
        <div class="section-card">
          <h3 class="section-title">👤 Basic Info</h3>
          <div class="mini-grid">
            <div class="mini-item">
              <label>Languages</label>
              <div class="tag-row" style="margin-top:4px;">
                <span v-for="l in languages" :key="l.fl_language_id" class="tag blue">{{ l.fl_language_name }}</span>
                <span v-if="!languages.length" class="empty-val">-</span>
              </div>
            </div>
            <div class="mini-item">
              <label>Pickup Areas</label>
              <div class="tag-row" style="margin-top:4px;">
                <span v-for="a in pickupAreas" :key="a.fl_area_id" class="tag orange">{{ a.fl_area_name }}</span>
                <span v-if="!pickupAreas.length" class="empty-val">-</span>
              </div>
            </div>
            <div class="mini-item"><label>Active</label>
              <span>{{ fl.fl_is_active ? '✅ Active' : '❌ Inactive' }}</span>
            </div>
            <div class="mini-item"><label>Date of Birth</label>
              <span>{{ formatDate(fl.fl_date_of_birth) }}</span>
            </div>
            <div class="mini-item"><label>Created</label>
              <span class="muted">{{ formatDateTime(fl.fl_created_at) }}</span>
            </div>
            <div class="mini-item"><label>Last Updated</label>
              <span class="muted">{{ formatDateTime(fl.fl_updated_at) }}</span>
            </div>
          </div>
          <div v-if="fl.fl_address" style="margin-top:16px;">
            <div class="mini-item"><label>Address</label><span>{{ fl.fl_address }}</span></div>
          </div>

          <!-- Availability inside Basic Info -->
          <div v-if="availability.length" style="margin-top:20px;">
            <p class="sub-section-label">📅 Availability</p>
            <table class="data-table">
              <thead>
                <tr>
                  <th>Start Date</th>
                  <th>End Date</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="a in availability" :key="a.fl_available_id">
                  <td>{{ formatDate(a.fl_available_start_date) }}</td>
                  <td>{{ formatDate(a.fl_available_end_date) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 2. Vehicle -->
        <div class="section-card" v-if="vehicle">
          <h3 class="section-title">🚐 Vehicle</h3>
          <div class="mini-grid">
            <div class="mini-item"><label>Type</label>
              <span>{{ vehicle.fl_vehicle_type }}</span>
            </div>
            <div class="mini-item"><label>Brand / Model</label>
              <span>{{ vehicle.fl_vehicle_brand }} {{ vehicle.fl_vehicle_model }}</span>
            </div>
            <div class="mini-item"><label>Year</label>
              <span>{{ vehicle.fl_vehicle_year }}</span>
            </div>
            <div class="mini-item"><label>Seats</label>
              <span>{{ vehicle.fl_vehicle_seat_capa }} seats</span>
            </div>
            <div class="mini-item"><label>License Plate</label>
              <span>{{ vehicle.fl_vehicle_license_plate }}</span>
            </div>
          </div>
          <!-- Vehicle Images -->
          <div v-if="vehicleImages.length" style="margin-top:20px;">
            <p class="sub-section-label">📸 Vehicle Photos ({{ vehicleImages.length }})</p>
            <div class="image-grid">
              <a v-for="img in vehicleImages" :key="img.fl_vehicle_image_id"
                :href="img.fl_vehicle_image_url" target="_blank" class="image-wrap">
                <img :src="img.fl_vehicle_image_url" class="vehicle-img"
                  @error="e => e.target.src=''" />
              </a>
            </div>
          </div>
        </div>

        <!-- 3. Documents -->
        <div class="section-card" v-if="documents.length">
          <h3 class="section-title">📄 Documents</h3>
          <div class="doc-grid">
            <div v-for="d in documents" :key="d.fl_doc_id" class="doc-card">
              <div class="doc-preview">
                <a :href="d.file_url" target="_blank">
                  <img v-if="isImage(d.file_url)" :src="d.file_url" class="doc-img"
                    @error="e => e.target.style.display='none'" />
                  <div v-else class="doc-icon">📄</div>
                </a>
              </div>
              <div class="doc-info">
                <p class="doc-type">{{ d.fl_doc_type }}</p>
                <span class="tag" :class="{
                  green: d.fl_doc_status === 'APPROVED',
                  red: d.fl_doc_status === 'REJECTED',
                  gray: d.fl_doc_status === 'PENDING'
                }">{{ d.fl_doc_status }}</span>
                <p class="doc-date">{{ formatDateTime(d.fl_uploaded_at) }}</p>
                <a :href="d.file_url" target="_blank" class="link">View File →</a>
              </div>
            </div>
          </div>
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
const vehicleImages = ref([])
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

const isImage = (url) => {
  if (!url) return false
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url)
}

onMounted(async () => {
  const id = route.params.id
  try {
    const [flRes, langRes, vehicleRes, imgRes, areaRes, availRes, docRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers?limit=500`),
      fetch(`${API_BASE}/fl-languages?limit=500`),
      fetch(`${API_BASE}/fl-vehicle?limit=500`),
      fetch(`${API_BASE}/fl-vehicle-images?limit=500`),
      fetch(`${API_BASE}/fl-pickup-areas?limit=500`),
      fetch(`${API_BASE}/fl-availability?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
    ])
    const [flData, langData, vehicleData, imgData, areaData, availData, docData] = await Promise.all([
      flRes.json(), langRes.json(), vehicleRes.json(), imgRes.json(),
      areaRes.json(), availRes.json(), docRes.json(),
    ])

    fl.value = (flData.items || []).find(f => f.fl_id === id) || null
    languages.value = (langData.items || []).filter(l => l.fl_id === id)
    vehicle.value = (vehicleData.items || []).find(v => v.fl_id === id) || null
    const vId = vehicle.value?.fl_vehicle_id
    vehicleImages.value = vId ? (imgData.items || []).filter(i => i.fl_vehicle_id === vId) : []
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
  background: #e3f2fd; color: #1976d2;
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
.section-title { font-size: 14px; font-weight: 600; color: #444; margin: 0 0 20px; padding-bottom: 12px; border-bottom: 1px solid #eee; }
.sub-section-label { font-size: 12px; font-weight: 600; color: #666; margin: 0 0 12px; }

.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.mini-item { display: flex; flex-direction: column; gap: 4px; }
.mini-item label { font-size: 10px; color: #999; font-weight: 600; text-transform: uppercase; }
.mini-item span { font-size: 13px; color: #222; }
.muted { color: #888 !important; font-size: 12px !important; }
.empty-val { font-size: 13px; color: #ccc; }
.link { color: #0066cc; font-size: 12px; }

.tag-row { display: flex; flex-wrap: wrap; gap: 6px; }
.tag { display: inline-block; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 500; }
.tag.blue { background: #e3f2fd; color: #1976d2; }
.tag.orange { background: #fff3e0; color: #f57c00; }
.tag.green { background: #f0fdf4; color: #166534; }
.tag.red { background: #fef2f2; color: #991b1b; }
.tag.gray { background: #f5f5f5; color: #666; }

/* Vehicle Images */
.image-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.image-wrap { display: block; border-radius: 8px; overflow: hidden; border: 1px solid #eee; }
.vehicle-img { width: 140px; height: 100px; object-fit: cover; display: block; }

/* Documents */
.doc-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.doc-card {
  border: 1px solid #eee; border-radius: 10px; overflow: hidden;
  display: flex; flex-direction: column;
}
.doc-preview {
  background: #f9f9f9; height: 140px;
  display: flex; align-items: center; justify-content: center; overflow: hidden;
}
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