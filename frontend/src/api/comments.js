import api from './request'

export function getArticleComments(articleId, params) {
  return api.get(`/comments/article/${articleId}`, { params })
}

export function getComments(params) {
  return api.get('/comments', { params })
}

export function createComment(articleId, data) {
  return api.post('/comments', data, { params: { article_id: articleId } })
}

export function approveComment(id, isApproved) {
  return api.put(`/comments/${id}/approve`, { is_approved: isApproved })
}

export function deleteComment(id) {
  return api.delete(`/comments/${id}`)
}
