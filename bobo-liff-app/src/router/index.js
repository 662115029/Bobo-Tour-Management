import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JobListView from '../views/JobListView.vue'
import TourDetailsView from '../views/TourDetailsView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/jobs', component: JobListView },
    { path: '/jobs/:id', component: JobDetailView }
  ]
})

export default router
