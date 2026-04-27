import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import liff from '@line/liff'

await liff.init({
  liffId: '2009771168-w9BjE7bI',
  mock: false
})

const app = createApp(App)
app.use(router)
app.mount('#app')
