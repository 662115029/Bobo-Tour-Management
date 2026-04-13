import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import liff from '@line/liff'
import { LiffMockPlugin } from '@line/liff-mock'

liff.use(new LiffMockPlugin())

await liff.init({
  liffId: '2009771168-w9BjE7bI',
  mock: true
})

const app = createApp(App)
app.use(router)
app.mount('#app')
