import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import liff from '@line/liff'
import { LiffMockPlugin } from '@line/liff-mock'

const IS_MOCK = import.meta.env.VITE_LIFF_MOCK === 'true'

if (IS_MOCK) {
  liff.use(new LiffMockPlugin())
}

await liff.init({
  liffId: '2009771168-w9BjE7bI',
  mock: IS_MOCK
})

const app = createApp(App)
app.use(router)
app.mount('#app')
