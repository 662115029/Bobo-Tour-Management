import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import LoginView from './views/LoginView.vue'
import RegisterView from './views/RegisterView.vue'
import MyToursView from './views/MyToursView.vue'
import ProfileView from './views/ProfileView.vue'
import CreateTourView from './views/CreateTourView.vue'
import TourDetailsView from './views/TourDetailsView.vue'

const routes = [
  { path: '/', redirect: '/my-tours' },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  {
    path: '/my-tours',
    name: 'my-tours',
    component: MyToursView,
    meta: { requiresAuth: true }
  },
  {
    // FIX: Added missing tour-detail route. Param is :id (matches MyToursView's viewJob call)
    path: '/tours/:id',
    name: 'tour-detail',
    component: TourDetailsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/create-tour',
    name: 'create-tour',
    component: CreateTourView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

// Auth guard
router.beforeEach((to, from, next) => {
  const em_id = localStorage.getItem('em_id')
  if (to.meta.requiresAuth && !em_id) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && em_id) {
    next('/my-tours')
  } else {
    next()
  }
})

// Browser tab title per page
const PAGE_TITLES = {
  'login': 'Login',
  'register': 'Register',
  'my-tours': 'My Tours',
  'create-tour': 'Create Tour',
  'tour-detail': 'Tour Detail',
  'profile': 'Profile',
}

router.afterEach((to) => {
  const title = PAGE_TITLES[to.name]
  document.title = title ? `${title} | Bobo Tour` : 'Bobo Tour'
})

const app = createApp(App)
app.use(router)
app.mount('#app')