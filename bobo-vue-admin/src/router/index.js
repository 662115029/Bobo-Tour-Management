import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/DashboardView.vue'
import Jobs from '../views/JobsView.vue'
import JobDetail from '../views/JobDetailView.vue'
import Verification from '../views/VerificationView.vue'
import FreelancerDetail from '../views/FreelancerDetailView.vue'
import EmployerDetail from '../views/EmployerDetailView.vue'
import Users from '../views/UsersView.vue'
import Logs from '../views/LogsView.vue'

const routes = [
  { path: '/', name: 'Dashboard', component: Dashboard },
  { path: '/jobs', name: 'Jobs', component: Jobs },
  { path: '/jobs/:id', name: 'JobDetail', component: JobDetail },
  { path: '/verification', name: 'Verification', component: Verification },
  { path: '/freelancers/:id', name: 'FreelancerDetail', component: FreelancerDetail },
  { path: '/employers/:id', name: 'EmployerDetail', component: EmployerDetail },
  { path: '/users', name: 'Users', component: Users },
  { path: '/logs', name: 'Logs', component: Logs }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router