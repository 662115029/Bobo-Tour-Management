<template>
  <div>
    <BreadcrumbBar :label="em?.em_name" />

    <div class="px-5 pb-6">
      <!-- Topbar -->
      <div class="flex items-center justify-between py-3 mb-4">
        <span class="text-sm cursor-pointer" @click="router.back()">← Back</span>
        <button v-if="em" class="btn-action !px-4 !py-1.5 !text-[13px] !rounded-lg"
          :class="em.em_is_active ? 'ban' : 'unban'" @click="showBanModal = true">
          {{ em.em_is_active ? "🚫 Ban" : "✅ Unban" }}
        </button>
      </div>

      <div v-if="loading" class="empty">⏳ Loading...</div>

      <div v-else-if="em">
        <!-- Hero Card -->
        <div class="bg-white rounded-xl p-7 flex justify-between items-start mb-4">
          <div class="flex items-start gap-4">
            <img v-if="em.em_profile_image_url" :src="em.em_profile_image_url"
              class="w-[72px] h-[72px] rounded-full object-cover shrink-0" />
            <div v-else
              class="w-[72px] h-[72px] rounded-full bg-[#f3e5f5] text-[#7b1fa2] flex items-center justify-center text-[28px] font-bold shrink-0">
              {{ em.em_name?.[0] || "?" }}
            </div>
            <div>
              <span class="badge" :class="em.em_verify_status?.toLowerCase()">{{ em.em_verify_status }}</span>
              <h2 class="text-xl font-semibold mt-1 mb-0">{{ em.em_name }}</h2>
              <p v-if="em.em_bio" class="text-[13px] text-[#666] mt-1 mb-0 leading-relaxed max-w-[400px]">{{ em.em_bio
                }}</p>
              <p v-else class="text-[13px] text-[#bbb] italic mt-1 mb-0">No bio</p>
            </div>
          </div>
          <div class="flex flex-col items-end gap-1 shrink-0">
            <span class="text-[11px] text-[#999] font-semibold uppercase tracking-wide">RATING</span>
            <span class="text-[22px] font-bold">⭐ {{ em.em_rating_avg ?? "-" }}</span>
          </div>
        </div>

        <div class="flex flex-col gap-4">

          <!-- 1. Basic Info -->
          <section>
            <h3 class="section-title">🏢 Basic Info</h3>
            <div class="mini-grid px-5 pt-4">
              <div class="mini-item">
                <label>Username</label>
                <span>@{{ em.em_username }}</span>
              </div>
              <div class="mini-item">
                <label>Phone</label>
                <span>{{ em.em_phone || "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Active</label>
                <span>{{ em.em_is_active ? "✅ Active" : "❌ Inactive" }}</span>
              </div>
              <div class="mini-item">
                <label>Rating</label>
                <span>⭐ {{ em.em_rating_avg ?? "-" }}</span>
              </div>
              <div class="mini-item">
                <label>Created</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(em.em_created_at) }}</span>
              </div>
              <div class="mini-item">
                <label>Last Updated</label>
                <span class="text-muted text-[12px]">{{ formatDateTime(em.em_updated_at) }}</span>
              </div>
            </div>
            <div v-if="em.em_address" class="px-5 pt-4">
              <div class="mini-item">
                <label>Address</label>
                <span>{{ em.em_address }}</span>
              </div>
            </div>
          </section>

          <!-- 2. Documents -->
          <section v-if="documents.length">
            <h3 class="section-title">📄 Documents</h3>
            <div class="px-5 pt-4 grid gap-4" style="grid-template-columns: repeat(auto-fill, minmax(200px, 1fr))">
              <div v-for="d in documents" :key="d.em_doc_id"
                class="border border-[#eee] rounded-[10px] overflow-hidden flex flex-col">
                <div class="bg-[#f9f9f9] h-[140px] flex items-center justify-center overflow-hidden">
                  <a :href="d.file_url" target="_blank">
                    <img v-if="isImage(d.file_url)" :src="d.file_url" class="w-full h-full object-cover"
                      @error="(e) => (e.target.style.display = 'none')" />
                    <div v-else class="text-4xl">📄</div>
                  </a>
                </div>
                <div class="p-3 flex flex-col gap-1.5">
                  <p class="text-xs font-semibold text-[#444] m-0">{{ d.em_doc_type }}</p>
                  <span class="badge" :class="{
                    verified: d.em_doc_status === 'APPROVED',
                    cancelled: d.em_doc_status === 'REJECTED',
                    pending: d.em_doc_status === 'PENDING',
                  }">{{ d.em_doc_status }}</span>
                  <p class="text-[11px] text-muted m-0">{{ formatDateTime(d.em_uploaded_at) }}</p>
                  <a :href="d.file_url" target="_blank" class="text-[#0066cc] text-xs">View File →</a>
                </div>
              </div>
            </div>
          </section>

          <!-- 3. Jobs -->
          <section v-if="jobs.length">
            <h3 class="section-title flex items-center gap-2">
              💼 Jobs
              <span
                class="inline-flex items-center justify-center bg-[#f0f4ff] text-[#3d5afe] rounded-full text-[11px] font-bold px-2 py-0.5">{{
                jobs.length }}</span>
            </h3>
            <div class="px-5 pt-4 overflow-x-auto">
              <table class="w-full border-collapse text-sm">
                <thead>
                  <tr>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]">
                      Job Title</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:12%">Status</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:16%">Start</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:16%">End</th>
                    <th
                      class="text-left text-[11px] font-semibold text-[#999] uppercase px-3 py-2 border-b-2 border-[#eee]"
                      style="width:12%">Price</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="j in jobs" :key="j.job_id" class="border-b border-[#f5f5f5] last:border-0">
                    <td class="px-3 py-2.5 text-[#333]">{{ j.job_title }}</td>
                    <td class="px-3 py-2.5">
                      <span class="badge" :class="j.job_status?.toLowerCase()">{{ j.job_status }}</span>
                    </td>
                    <td class="px-3 py-2.5 text-muted text-[12px]">{{ formatDate(j.job_start_date) }}</td>
                    <td class="px-3 py-2.5 text-muted text-[12px]">{{ formatDate(j.job_end_date) }}</td>
                    <td class="px-3 py-2.5 text-[#333]">{{ j.job_price ? "฿" + Number(j.job_price).toLocaleString() :
                      "-" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

        </div>
      </div>

      <div v-else class="empty">Employer not found.</div>
    </div>

    <!-- Ban Modal -->
    <div v-if="showBanModal" class="modal-overlay" @click.self="showBanModal = false">
      <div class="modal">
        <div class="modal-icon">{{ em?.em_is_active ? "🚫" : "✅" }}</div>
        <h3>{{ em?.em_is_active ? "Ban Employer" : "Unban Employer" }}</h3>
        <p>Are you sure you want to {{ em?.em_is_active ? "ban" : "unban" }} <strong>{{ em?.em_name }}</strong>?</p>
        <p v-if="em?.em_is_active" class="modal-warning">This will prevent them from using the platform.</p>
        <div class="modal-actions">
          <button class="btn-cancel" @click="showBanModal = false">Cancel</button>
          <button class="btn-confirm" :class="em?.em_is_active ? 'ban' : 'unban'" @click="confirmBan">
            {{ em?.em_is_active ? "Ban" : "Unban" }}
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
const em = ref(null);
const documents = ref([]);
const jobs = ref([]);
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
  if (!em.value) return;
  try {
    const res = await fetch(`${API_BASE}/employers/${em.value.em_id}/ban`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ is_active: !em.value.em_is_active, admin_id: localStorage.getItem('admin_id') || '' }),
    });
    const data = await res.json();
    if (data.status === "updated") {
      em.value.em_is_active = !em.value.em_is_active;
    }
  } catch (e) {
    console.error("Failed to ban/unban employer:", e);
  } finally {
    showBanModal.value = false;
  }
};

onMounted(async () => {
  const id = route.params.id;
  try {
    const [emRes, docRes, jobsRes] = await Promise.all([
      fetch(`${API_BASE}/employers?limit=500`),
      fetch(`${API_BASE}/em-documents?limit=500`),
      fetch(`${API_BASE}/jobs?limit=500`),
    ]);
    const [emData, docData, jobsData] = await Promise.all([emRes.json(), docRes.json(), jobsRes.json()]);
    em.value = (emData.items || []).find((e) => e.em_id === id) || null;
    documents.value = (docData.items || []).filter((d) => d.em_id === id);
    jobs.value = (jobsData.items || []).filter((j) => j.em_id === id);
  } catch (e) {
    console.error("Failed to load employer:", e);
  } finally {
    loading.value = false;
  }
});
</script>