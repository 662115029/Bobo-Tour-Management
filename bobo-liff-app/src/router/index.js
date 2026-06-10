import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import JobsView from '../views/JobsView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import ChangePinView from '../views/ChangePinView.vue'
import AvailabilityView from '../views/AvailabilityView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/profile', component: ProfileView },
    { path: '/profile/change-pin', component: ChangePinView },
    { path: '/jobs', component: JobsView },
    { path: '/availability', component: AvailabilityView },
  ]
})

export default router