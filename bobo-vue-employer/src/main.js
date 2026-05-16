import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import LoginView from "./views/LoginView.vue";
import RegisterView from "./views/RegisterView.vue";
import MyToursView from "./views/MyToursView.vue";
import ProfileView from "./views/ProfileView.vue";
import CreateJobView from "./views/CreateJobView.vue";
import MatchingView from "./views/MatchingView.vue";
import ApplicationView from "./views/ApplicationView.vue";
import JobDetailView from './views/JobDetailView.vue'


const routes = [
  { path: "/", redirect: "/my-tours" },
  { path: "/login", name: "login", component: LoginView },
  { path: "/register", name: "register", component: RegisterView },
  {
    path: "/my-tours",
    name: "my-tours",
    component: MyToursView,
    meta: { requiresAuth: true },
  },
  {
    path: "/profile",
    name: "profile",
    component: ProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: "/create-job",
    name: "create-job",
    component: CreateJobView,
    meta: { requiresAuth: true },
  },
  {
    path: "/matching",
    name: "matching",
    component: MatchingView,
    meta: { requiresAuth: true },
  },
  {
    path: "/applications",
    name: "applications",
    component: ApplicationView,
    meta: { requiresAuth: true },
  },
  { path: '/my-tours/:job_id',
    name: 'JobDetail',
    component: JobDetailView,
    meta: { requiresAuth: true },
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Auth guard
router.beforeEach((to, from, next) => {
  const em_id = localStorage.getItem("em_id");
  if (to.meta.requiresAuth && !em_id) {
    next("/login");
  } else if ((to.path === "/login" || to.path === "/register") && em_id) {
    next("/my-tours");
  } else {
    next();
  }
});

const app = createApp(App);
app.use(router);
app.mount("#app");
