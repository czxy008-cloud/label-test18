import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import App from './App.vue'
import router from './router'
import { useAuthStore } from '@/stores/auth'
import './assets/main.css'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

const pinia = createPinia()
app.use(pinia)
app.use(router)
app.use(ElementPlus)

async function restoreAuthState() {
  const authStore = useAuthStore()
  if (authStore.token) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      console.error('Failed to restore auth state:', error)
    }
  }
}

restoreAuthState().then(() => {
  app.mount('#app')
})
