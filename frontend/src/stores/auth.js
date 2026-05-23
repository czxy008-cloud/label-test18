import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('blog_token') || '')
  const user = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('blog_token', newToken)
  }

  function clearToken() {
    token.value = ''
    user.value = null
    localStorage.removeItem('blog_token')
  }

  async function login(username, password) {
    try {
      const response = await apiLogin(username, password)
      setToken(response.access_token)
      await fetchUser()
      return response
    } catch (error) {
      throw error
    }
  }

  async function register(userData) {
    try {
      const response = await apiRegister(userData)
      return response
    } catch (error) {
      throw error
    }
  }

  async function fetchUser() {
    if (!token.value) return
    try {
      const response = await getCurrentUser()
      user.value = response
      return response
    } catch (error) {
      clearToken()
      throw error
    }
  }

  function logout() {
    clearToken()
  }

  return {
    token,
    user,
    isLoggedIn,
    isAdmin,
    login,
    register,
    fetchUser,
    logout
  }
})
