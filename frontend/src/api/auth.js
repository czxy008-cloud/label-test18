import api from './request'

export function login(username, password, rememberMe = false) {
  return api.post('/auth/login', { username, password, remember_me: rememberMe })
}

export function register(userData) {
  return api.post('/auth/register', userData)
}

export function forgotPassword(email) {
  return api.post('/auth/forgot-password', { email })
}

export function resetPassword(data) {
  return api.post('/auth/reset-password', data)
}

export function getCurrentUser() {
  return api.get('/users/me')
}

export function updateCurrentUser(data) {
  return api.put('/users/me', data)
}
