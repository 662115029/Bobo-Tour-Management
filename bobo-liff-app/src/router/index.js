import { createRouter, createWebHashHistory } from 'vue-router'
import JobsView from '../views/JobsView.vue'
import RegisterView from '../views/RegisterView.vue'
import ProfileView from '../views/ProfileView.vue'
import LoginView from '../views/LoginView.vue'
import ChangePinView from '../views/ChangePinView.vue'
import AvailabilityView from '../views/AvailabilityView.vue'

const router = createRouter({
  history: createWebHashHistory(),
  routes: [
    // No standalone Home page — App.vue's init() always routes to /login,
    // /register, or a specific target before this ever needs to resolve.
    { path: '/', redirect: '/profile' },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/profile', component: ProfileView },
    { path: '/profile/change-pin', component: ChangePinView },
    { path: '/jobs', component: JobsView },
    { path: '/availability', component: AvailabilityView },
  ]
})

export default router