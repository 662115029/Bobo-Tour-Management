import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/DashboardView.vue'
import Jobs from '../views/JobsView.vue'
import Verification from '../views/VerificationView.vue'
import Users from '../views/UsersView.vue'
import Logs from '../views/LogsView.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/jobs', name: 'Jobs', component: Jobs },
  { path: '/verification', name: 'Verification', component: Verification },
  { path: '/users', name: 'Users', component: Users },
  { path: '/logs', name: 'Logs', component: Logs }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router