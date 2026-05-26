import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, forgotPassword as apiForgotPassword, resetPassword as apiResetPassword, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('blog_token') || '')
  const user = ref(null)
  const rememberMe = ref(localStorage.getItem('blog_remember_me') === 'true')

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.is_admin || false)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('blog_token', newToken)
  }

  function setRememberMe(value) {
    rememberMe.value = value
    localStorage.setItem('blog_remember_me', value ? 'true' : 'false')
  }

  function clearToken() {
    token.value = ''
    user.value = null
    rememberMe.value = false
    localStorage.removeItem('blog_token')
    localStorage.removeItem('blog_remember_me')
  }

  async function login(username, password, rememberMeOption = false) {
    try {
      const response = await apiLogin(username, password, rememberMeOption)
      setToken(response.access_token)
      setRememberMe(rememberMeOption)
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

  async function forgotPassword(email) {
    try {
      const response = await apiForgotPassword(email)
      return response
    } catch (error) {
      throw error
    }
  }

  async function resetPassword(data) {
    try {
      const response = await apiResetPassword(data)
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
    rememberMe,
    isLoggedIn,
    isAdmin,
    login,
    register,
    forgotPassword,
    resetPassword,
    fetchUser,
    logout
  }
})
