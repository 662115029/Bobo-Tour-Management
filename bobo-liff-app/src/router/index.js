import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JobListView from '../views/JobListView.vue'
import JobDetailView from '../views/JobDetailView.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/jobs', component: JobListView },
    { path: '/jobs/:id', component: JobDetailView }
  ]
})

export default router
