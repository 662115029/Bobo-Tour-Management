import { createRouter, createWebHashHistory } from "vue-router";
import AdminLayout from "../layouts/AdminLayout.vue";
import Dashboard from "../views/DashboardView.vue";
import Jobs from "../views/JobsView.vue";
import JobDetail from "../views/JobDetailView.vue";
import Verification from "../views/VerificationView.vue";
import FreelancerDetail from "../views/FreelancerDetailView.vue";
import EmployerDetail from "../views/EmployerDetailView.vue";
import Users from "../views/UsersView.vue";
import Logs from "../views/LogsView.vue";
import MatchingWeights from "../views/MatchingWeightsView.vue";
import Profile from "../views/ProfileView.vue";
import Login from "../views/LoginView.vue";
import Register from "../views/RegisterView.vue";

export const pageNames = {
  Jobs: "Jobs Management",
  Verification: "Verification",
  Users: "Users",
  Logs: "Admin Logs",
  MatchingWeights: "Matching Weights",
  Profile: "Profile",
  Dashboard: "Dashboard",
};

const routes = [
  { path: "/login", name: "Login", component: Login },
  { path: "/register", name: "Register", component: Register },
  {
    path: "/",
    component: AdminLayout,
    children: [
      { path: "", name: "Dashboard", component: Dashboard },
      { path: "jobs", name: "Jobs", component: Jobs },
      {
        path: "jobs/:id",
        name: "JobDetail",
        component: JobDetail,
        meta: { parent: "Jobs Management", parentTo: "/jobs" },
      },
      { path: "verification", name: "Verification", component: Verification },
      {
        path: "freelancers/:id",
        name: "FreelancerDetail",
        component: FreelancerDetail,
        meta: { isDynamic: true, parent: "Verification", parentTo: "/verification" },
      },
      {
        path: "employers/:id",
        name: "EmployerDetail",
        component: EmployerDetail,
        meta: { isDynamic: true, parent: "Verification", parentTo: "/verification" },
      },
      { path: "users", name: "Users", component: Users },
      { path: "logs", name: "Logs", component: Logs },
      { path: "matching-weights", name: "MatchingWeights", component: MatchingWeights },
      { path: "profile", name: "Profile", component: Profile },
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from) => {
  const adminId = localStorage.getItem("admin_id");
  const publicPaths = ["/login", "/register"];

  if (!publicPaths.includes(to.path) && !adminId) {
    return "/login";
  } else if (publicPaths.includes(to.path) && adminId) {
    return { name: "Dashboard" };
  } else {
    if (to.meta?.isDynamic && from.name) {
      to.meta.parent = pageNames[from.name] || from.name;
      to.meta.parentTo = from.fullPath;
    }
    return true;
  }
});

export default router;