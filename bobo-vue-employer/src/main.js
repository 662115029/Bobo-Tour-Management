import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import CreateJobView from './views/CreateJobView.vue'

const routes = [
  { path: '/', name: 'home', redirect: '/create-job' },
  { path: '/create-job', name: 'create-job', component: CreateJobView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')