import api from './request'

export function getUsers(params = {}) {
  return api.get('/users', { params })
}

export function getUserById(userId) {
  return api.get(`/users/${userId}`)
}

export function getAllUsers() {
  return api.get('/users', { params: { page: 1, page_size: 9999 } })
}
