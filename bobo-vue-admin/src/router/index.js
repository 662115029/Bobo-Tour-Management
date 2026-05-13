import { createRouter, createWebHistory } from "vue-router";
import AdminLayout from "../layouts/AdminLayout.vue";
import Dashboard from "../views/DashboardView.vue";
import Jobs from "../views/JobsView.vue";
import JobDetail from "../views/JobDetailView.vue";
import Verification from "../views/VerificationView.vue";
import FreelancerDetail from "../views/FreelancerDetailView.vue";
import EmployerDetail from "../views/EmployerDetailView.vue";
import Users from "../views/UsersView.vue";
import Logs from "../views/LogsView.vue";
import Profile from "../views/ProfileView.vue";
import Login from "../views/LoginView.vue";

const pageNames = {
  Jobs: "Jobs Management",
  Verification: "Verification",
  Users: "Users",
  Logs: "Admin Logs",
  Profile: "Profile",
  Dashboard: "Dashboard",
};

const routes = [
  { path: "/login", name: "Login", component: Login },
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
        meta: { isDynamic: true },
      },
      {
        path: "employers/:id",
        name: "EmployerDetail",
        component: EmployerDetail,
        meta: { isDynamic: true },
      },
      { path: "users", name: "Users", component: Users },
      { path: "logs", name: "Logs", component: Logs },
      { path: "profile", name: "Profile", component: Profile },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const adminId = localStorage.getItem("admin_id");

  if (to.path !== "/login" && !adminId) {
    next("/login");
  } else if (to.path === "/login" && adminId) {
    next({ name: "Dashboard" });
  } else {
    // For dynamic detail pages, store the parent info from the previous route
    if (to.meta?.isDynamic && from.name) {
      to.meta.parent = pageNames[from.name] || from.name;
      to.meta.parentTo = from.fullPath;
    }
    next();
  }
});

export default router;
