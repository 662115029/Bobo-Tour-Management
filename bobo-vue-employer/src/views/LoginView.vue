<template>
  <div
    class="min-h-screen flex items-center justify-center p-4"
    style="background-color: #fefcfb"
  >
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="flex justify-center mb-8">
        <img
          src="@/assets/logo_motto.png"
          alt="Bobo Tour Management"
          class="h-48 w-auto object-contain"
        />
      </div>

      <!-- Card -->
      <div class="bg-white rounded-2xl shadow-lg p-8">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">
          Sign in to your account
        </h2>

        <div
          v-if="error"
          class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm"
        >
          {{ error }}
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Username</label
            >
            <input
              v-model="form.em_username"
              type="text"
              required
              placeholder="your_username"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Password</label
            >
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                placeholder="••••••••"
                class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition pr-10"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.97 9.97 0 012.187-3.592M6.53 6.533A9.97 9.97 0 0112 5c4.477 0 8.268 2.943 9.542 7a10.05 10.05 0 01-4.423 5.294M3 3l18 18" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.477 0 8.268 2.943 9.542 7-1.274 4.057-5.065 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </button>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full py-3 text-white font-semibold rounded-2xl transition disabled:opacity-50 disabled:cursor-not-allowed mt-2"
            style="background-color: #bd8e71"
          >
            {{ loading ? "Signing in..." : "Sign In" }}
          </button>
        </form>

        <p class="text-center text-sm text-gray-500 mt-6">
          Don't have an account?
          <router-link
            to="/register"
            class="text-gray-800 font-medium hover:underline"
            >Register here</router-link
          >
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const API_BASE = "/api";
const router = useRouter();

const form = reactive({ em_username: "", password: "" });
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);

const handleLogin = async () => {
  loading.value = true;
  error.value = "";

  try {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("em_id", data.em_id);
      localStorage.setItem("em_name", data.em_name);
      localStorage.setItem("em_username", data.em_username);
      localStorage.setItem('em_email', data.em_email)
      router.push("/my-tours");
    } else {
      error.value = data.message || "Invalid username or password.";
    }
  } catch (e) {
    error.value = "Unable to connect. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>
