<template>
  <div>
    <BreadcrumbBar :label="fl?.fl_name" />

    <div class="px-5 pb-6">
      <!-- Topbar -->
      <div class="flex items-center justify-between py-3 mb-4">
        <span class="text-sm cursor-pointer" @click="router.back()">← Back</span>
        <button v-if="fl" class="btn-action !px-4 !py-1.5 !text-[13px] !rounded-lg"
          :class="fl.fl_is_active ? 'ban' : 'unban'" @click="showBanModal = true">
          {{ fl.fl_is_active ? "🚫 Ban" : "✅ Unban" }}
        </button>
      </div>

      <div v-if="loading" class="empty">⏳ Loading...</div>

      <div v-else-if="fl">
        <!-- Hero Card -->
        <div class="bg-white rounded-xl p-7 flex justify-between items-start mb-4">
          <div class="flex items-start gap-4">
            <img v-if="fl.fl_profile_image_url" :src="fl.fl_profile_image_url"
              class="w-[72px] h-[72px] rounded-full object-cover shrink-0" />
            <div v-else
              class="w-[72px] h-[72px] rounded-full bg-[#e3f2fd] text-[#1976d2] flex items-center justify-center text-[28px] font-bold shrink-0">
              {{ fl.fl_name?.[0] || "?" }}
            </div>
            <div>
              <span class="badge" :class="fl.fl_verify_status?.toLowerCase()">{{ fl.fl_verify_status }}</span>
              <h2 class="text-xl font-semibold mt-1 mb-0">{{ fl.fl_name }}</h2>
              <p v-if="fl.fl_bio" class="text-[13px] text-[#666] mt-1 mb-0 leading-relaxed max-w-[400px]">{{ fl.fl_bio
                }}</p>
              <p v-else class="text-[13px] text-[#bbb] italic mt-1 mb-0">No bio</p>
            </div>
          </div>
          <div class="flex flex-col items-end gap-1 shrink-0">
            <span class="text-[11px] text-[#999] font-semibold uppercase tracking-wide">RATING</span>
            <span class="text-[22px] font-bold">⭐ {{ fl.fl_rating_avg ?? "-" }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-4">

          <!-- 1. Basic Info -->
          <section>
            <h3 class="section-title">👤 Basic Info</h3>
            <div class="mini-grid px-5 pt-4">
              <div class="mini-item">
                <label>Languages</label>
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span v-for="l in languages" :key="l.fl_language_id" class="badge open">{{ l.fl_language_name
                    }}</span>
                  <span v-if="!languages.length" class="text-[#ccc] text-[13px]">-</span>
                </div>
              </div>
              <div class="mini-item">
                <label>Pickup Areas</label>
                <div class="flex flex-wrap gap-1.5 mt-1">
                  <span v-for="a in pickupAreas" :key="a.fl_area_id" class="badge in_progress">{{ a.fl_area_name
                    }}</span>
                  <span v-if="!pickupAreas.length" class="text-[#ccc] text-[13px]">-</span>
                </div>
              </div>
              <div class="mini-item">
                <label>Active</label>
                <span>{{ fl.fl_is_active ? "✅ Active" : "❌ Inactive" }}</span>
              </div>
              <div class="mini-item">
                <label>Date of Birth</label>
                <span>{{ formatDate(fl.fl_date_of_birth) }}</span>
              </div>
              <div class="mini-item">
                <label>Created</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(fl.fl_created_at) }}</span>
              </div>
              <div class="mini-item">
                <label>Last Updated</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(fl.fl_updated_at) }}</span>
              </div>
            </div>

            <div v-if="fl.fl_address" class="px-5 pt-4">
              <div class="mini-item">
                <label>Address</label>
                <span>{{ fl.fl_address }}</span>
              </div>
            </div>

            <!-- Availability -->
            <div v-if="availability.length" class="px-5 pt-5">
              <p class="text-xs font-semibold text-[#666] mb-3">📅 Availability</p>
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Start Date</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      End Date</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="a in availability" :key="a.fl_available_id"
                    class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ formatDate(a.fl_available_start_date) }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ formatDate(a.fl_available_end_date) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          <!-- 2. Vehicle -->
          <section v-if="vehicle">
            <h3 class="section-title">🚐 Vehicle</h3>
            <div class="mini-grid px-5 pt-4">
              <div class="mini-item">
                <label>Type</label>
                <span>{{ vehicle.fl_vehicle_type }}</span>
              </div>
              <div class="mini-item">
                <label>Brand / Model</label>
                <span>{{ vehicle.fl_vehicle_brand }} {{ vehicle.fl_vehicle_model }}</span>
              </div>
              <div class="mini-item">
                <label>Year</label>
                <span>{{ vehicle.fl_vehicle_year }}</span>
              </div>
              <div class="mini-item">
                <label>Seats</label>
                <span>{{ vehicle.fl_vehicle_seat_capa }} seats</span>
              </div>
              <div class="mini-item">
                <label>License Plate</label>
                <span>{{ vehicle.fl_vehicle_license_plate }}</span>
              </div>
            </div>
            <div v-if="vehicleImages.length" class="px-5 pt-5">
              <p class="text-xs font-semibold text-[#666] mb-3">📸 Vehicle Photos ({{ vehicleImages.length }})</p>
              <div class="grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))">
                <div v-for="img in vehicleImages" :key="img.fl_vehicle_image_id"
                  class="border border-[#eee] rounded-[10px] overflow-hidden flex flex-col">
                  <div class="bg-[#f9f9f9] h-[140px] flex items-center justify-center overflow-hidden">
                    <a :href="img.fl_vehicle_image_url" target="_blank">
                      <img :src="img.fl_vehicle_image_url" class="w-full h-full object-cover"
                        @error="(e) => (e.target.style.display = 'none')" />
                    </a>
                  </div>
                  <div class="p-3 flex flex-col gap-1.5">
                    <p class="text-xs font-semibold text-[#444] m-0">Vehicle Photo</p>
                    <a :href="img.fl_vehicle_image_url" target="_blank" class="text-[#0066cc] text-xs">View →</a>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <!-- 3. Documents -->
          <section v-if="documents.length">
            <h3 class="section-title">📄 Documents</h3>
            <div class="px-5 pt-4 grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))">
              <div v-for="d in documents" :key="d.fl_doc_id"
                class="border border-[#eee] rounded-[10px] overflow-hidden flex flex-col">
                <div class="bg-[#f9f9f9] h-[140px] flex items-center justify-center overflow-hidden">
                  <a :href="d.file_url" target="_blank">
                    <img v-if="isImage(d.file_url)" :src="d.file_url" class="w-full h-full object-cover"
                      @error="(e) => (e.target.style.display = 'none')" />
                    <div v-else class="text-4xl">📄</div>
                  </a>
                </div>
                <div class="p-3 flex flex-col gap-1.5">
                  <p class="text-xs font-semibold text-[#444] m-0">{{ d.fl_doc_type }}</p>
                  <span class="badge" :class="{
                    verified: d.fl_doc_status === 'APPROVED',
                    cancelled: d.fl_doc_status === 'REJECTED',
                    pending: d.fl_doc_status === 'PENDING',
                  }">{{ d.fl_doc_status }}</span>
                  <p class="text-[11px] text-muted m-0">{{ formatDateTime(d.fl_uploaded_at) }}</p>
                  <a :href="d.file_url" target="_blank" class="text-[#0066cc] text-xs">View File →</a>
                </div>
              </div>
            </div>
          </section>

        </div>
      </div>

      <div v-else class="empty">Freelancer not found.</div>
    </div>

    <!-- Ban Modal -->
    <div v-if="showBanModal" class="modal-overlay" @click.self="showBanModal = false">
      <div class="modal">
        <div class="modal-icon">{{ fl?.fl_is_active ? "🚫" : "✅" }}</div>
        <h3>{{ fl?.fl_is_active ? "Ban Freelancer" : "Unban Freelancer" }}</h3>
        <p>Are you sure you want to {{ fl?.fl_is_active ? "ban" : "unban" }} <strong>{{ fl?.fl_name }}</strong>?</p>
        <p v-if="fl?.fl_is_active" class="modal-warning">This will prevent them from using the platform.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showBanModal = false">Cancel</button>
          <button class="btn-confirm" :class="fl?.fl_is_active ? 'ban' : 'unban'" @click="confirmBan">
            {{ fl?.fl_is_active ? "Ban" : "Unban" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import BreadcrumbBar from '../components/BreadcrumbBar.vue'
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { API_BASE } from "../data/api";

const route = useRoute();
const router = useRouter();
const showBanModal = ref(false);
const fl = ref(null);
const languages = ref([]);
const vehicle = ref(null);
const vehicleImages = ref([]);
const pickupAreas = ref([]);
const availability = ref([]);
const documents = ref([]);
const loading = ref(true);

const formatDate = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
};

const formatDateTime = (date) => {
  if (!date) return "-";
  return new Date(date).toLocaleString("en-GB", { day: "2-digit", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" });
};

const isImage = (url) => {
  if (!url) return false;
  return /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(url);
};

const confirmBan = async () => {
  if (!fl.value) return;
  try {
    const res = await fetch(`${API_BASE}/freelancers/${fl.value.fl_id}/ban`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ is_active: !fl.value.fl_is_active, admin_id: localStorage.getItem('admin_id') || '' }),
    });
    const data = await res.json();
    if (data.status === "updated") {
      fl.value.fl_is_active = !fl.value.fl_is_active;
    }
  } catch (e) {
    console.error("Failed to ban/unban freelancer:", e);
  } finally {
    showBanModal.value = false;
  }
};

onMounted(async () => {
  const id = route.params.id;
  try {
    const [flRes, langRes, vehicleRes, imgRes, areaRes, availRes, docRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers?limit=500`),
      fetch(`${API_BASE}/fl-languages?limit=500`),
      fetch(`${API_BASE}/fl-vehicle?limit=500`),
      fetch(`${API_BASE}/fl-vehicle-images?limit=500`),
      fetch(`${API_BASE}/fl-pickup-areas?limit=500`),
      fetch(`${API_BASE}/fl-availability?limit=500`),
      fetch(`${API_BASE}/fl-documents?limit=500`),
    ]);
    const [flData, langData, vehicleData, imgData, areaData, availData, docData] = await Promise.all([
      flRes.json(), langRes.json(), vehicleRes.json(), imgRes.json(), areaRes.json(), availRes.json(), docRes.json(),
    ]);

    fl.value = (flData.items || []).find((f) => f.fl_id === id) || null;
    languages.value = (langData.items || []).filter((l) => l.fl_id === id);
    vehicle.value = (vehicleData.items || []).find((v) => v.fl_id === id) || null;
    const vId = vehicle.value?.fl_vehicle_id;
    vehicleImages.value = vId ? (imgData.items || []).filter((i) => i.fl_vehicle_id === vId) : [];
    pickupAreas.value = (areaData.items || []).filter((a) => a.fl_id === id);
    availability.value = (availData.items || []).filter((a) => a.fl_id === id);
    documents.value = (docData.items || []).filter((d) => d.fl_id === id);
  } catch (e) {
    console.error("Failed to load freelancer:", e);
  } finally {
    loading.value = false;
  }
});
</script>