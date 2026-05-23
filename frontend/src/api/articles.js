import api from './request'

export function getArticles(params) {
  return api.get('/articles', { params })
}

export function getArticleById(id) {
  return api.get(`/articles/${id}`)
}

export function getArticleBySlug(slug) {
  return api.get(`/articles/slug/${slug}`)
}

export function createArticle(data) {
  return api.post('/articles', data)
}

export function updateArticle(id, data) {
  return api.put(`/articles/${id}`, data)
}

export function deleteArticle(id) {
  return api.delete(`/articles/${id}`)
}

export function likeArticle(id) {
  return api.post(`/articles/${id}/like`)
}
