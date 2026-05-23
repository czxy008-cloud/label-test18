import api from './request'

export function login(username, password) {
  return api.post('/auth/login', { username, password })
}

export function register(userData) {
  return api.post('/auth/register', userData)
}

export function getCurrentUser() {
  return api.get('/users/me')
}

export function updateCurrentUser(data) {
  return api.put('/users/me', data)
}
