import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JobListView from '../views/JobListView.vue'
import JobDetailView from '../views/JobDetailView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import ChangePinView from '../views/ChangePinView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/profile', component: ProfileView },
    { path: '/profile/change-pin', component: ChangePinView },
    { path: '/jobs', component: JobListView },
    { path: '/jobs/:id', component: JobDetailView },
  ]
})

export default router