<template>
  <div class="home">
    <div class="profile-card">
      <img
        :src="user.pictureUrl"
        :alt="user.displayName"
        class="avatar"
        @error="handleImageError"
      />
      <h2>{{ user.displayName }}</h2>
      <p class="subtitle">Freelance Van Driver</p>
    </div>

    <div class="availability-card">
      <h3>Your Availability</h3>
      <p v-if="availability">{{ availability }}</p>
      <p v-else class="not-set">Not set yet</p>
      <button @click="goToAvailability" class="btn-secondary">
        Edit Availability
      </button>
    </div>

    <button @click="goToJobs" class="btn-primary">
      View Available Jobs
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  user: Object
})

const router = useRouter()
const availability = ref(null) // will connect to backend later

function goToJobs() {
  router.push('/jobs')
}

function goToAvailability() {
  router.push('/availability')
}

function handleImageError(e) {
  // fallback if LINE profile picture fails to load
  e.target.src = 'https://via.placeholder.com/80'
}
</script>

<style scoped>
.home {
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  max-width: 480px;
  margin: 0 auto;
}

.profile-card {
  background: #06C755;
  color: white;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid white;
  margin-bottom: 12px;
}

.profile-card h2 {
  margin: 0;
  font-size: 20px;
}

.subtitle {
  margin: 4px 0 0;
  opacity: 0.85;
  font-size: 14px;
}

.availability-card {
  background: #f9f9f9;
  border-radius: 16px;
  padding: 16px;
  border: 1px solid #eee;
}

.availability-card h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.not-set {
  color: #999;
  font-size: 14px;
}

.btn-primary {
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

.btn-secondary {
  background: white;
  color: #06C755;
  border: 2px solid #06C755;
  border-radius: 12px;
  padding: 10px 16px;
  font-size: 14px;
  width: 100%;
  cursor: pointer;
  margin-top: 8px;
}
</style>
