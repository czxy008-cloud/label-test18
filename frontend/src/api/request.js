import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import router from '@/router'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

const publicPaths = ['/auth/login', '/auth/register', '/health']

function isPublicPath(url) {
  return publicPaths.some(path => url.includes(path))
}

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token && !isPublicPath(config.url || '')) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      const status = error.response.status
      const message = error.response.data?.detail || '请求失败'
      const url = error.config?.url || ''

      if (status === 401 && !isPublicPath(url)) {
        const authStore = useAuthStore()
        authStore.logout()
        router.push('/login')
        ElMessage.error('登录已过期，请重新登录')
      } else if (status === 401 && isPublicPath(url)) {
        ElMessage.error(message)
      } else if (status === 403) {
        ElMessage.error('没有权限执行此操作')
      } else if (status === 404) {
        ElMessage.error('资源不存在')
      } else if (status === 422) {
        ElMessage.error('请求参数错误')
      } else {
        ElMessage.error(message)
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default api
