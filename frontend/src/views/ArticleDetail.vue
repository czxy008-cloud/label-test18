<template>
  <div v-loading="loading">
    <template v-if="article">
      <el-card class="article-detail-card">
        <template v-if="article.cover_image" #header>
          <div class="article-cover-image">
            <img :src="article.cover_image" :alt="article.title" />
          </div>
        </template>
        <h1 class="article-title">{{ article.title }}</h1>
        <div class="article-meta">
          <el-avatar :size="32" :src="article.author?.avatar_url">
            {{ article.author?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <span>{{ article.author?.username }}</span>
          <span>·</span>
          <span>{{ formatDate(article.created_at) }}</span>
          <span>·</span>
          <span><el-icon><View /></el-icon> {{ article.views_count }} 阅读</span>
          <span>·</span>
          <el-button
            type="primary"
            size="small"
            :icon="Star"
            @click="handleLike"
          >
            {{ article.likes_count }} 点赞
          </el-button>
        </div>
        <div class="article-tags">
          <el-tag
            v-for="tag in article.tags"
            :key="tag.id"
            :color="tag.color"
            effect="light"
          >
            {{ tag.name }}
          </el-tag>
        </div>
        <div class="article-content" v-html="article.content"></div>
      </el-card>

      <el-card class="comments-card">
        <template #header>
          <div class="comments-header">
            <span>评论 ({{ commentsTotal }})</span>
          </div>
        </template>

        <div v-if="authStore.isLoggedIn" class="comment-input-area">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="3"
            placeholder="发表你的评论..."
            maxlength="500"
            show-word-limit
          />
          <div class="comment-submit">
            <el-button
              type="primary"
              :loading="submitting"
              @click="handleSubmitComment"
            >
              发表评论
            </el-button>
          </div>
        </div>
        <div v-else class="comment-login-prompt">
          <el-empty description="登录后可以发表评论">
            <el-button type="primary" @click="$router.push('/login')">去登录</el-button>
          </el-empty>
        </div>

        <div v-loading="commentsLoading" class="comments-list">
          <template v-if="comments.length > 0">
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="comment-item"
            >
              <CommentItem
                :comment="comment"
                :article-id="article.id"
                @submitted="handleCommentSubmitted"
              />
            </div>
          </template>
          <div v-else class="empty-state">
            <el-empty description="暂无评论，快来抢沙发吧！" />
          </div>
        </div>
      </el-card>
    </template>
    <div v-else-if="!loading" class="empty-state">
      <el-empty description="文章不存在" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getArticleById, likeArticle } from '@/api/articles'
import { getArticleComments, createComment } from '@/api/comments'
import { ElMessage } from 'element-plus'
import { View, Star } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import CommentItem from '@/components/CommentItem.vue'

const route = useRoute()
const authStore = useAuthStore()

const loading = ref(true)
const article = ref(null)
const comments = ref([])
const commentsTotal = ref(0)
const commentsLoading = ref(false)
const newComment = ref('')
const submitting = ref(false)

onMounted(async () => {
  await fetchArticle()
  await fetchComments()
})

async function fetchArticle() {
  loading.value = true
  try {
    article.value = await getArticleById(route.params.id)
  } catch (error) {
    console.error('获取文章失败', error)
  } finally {
    loading.value = false
  }
}

async function fetchComments() {
  commentsLoading.value = true
  try {
    const data = await getArticleComments(route.params.id, { page: 1, page_size: 100 })
    comments.value = data.items
    commentsTotal.value = data.total
  } catch (error) {
    console.error('获取评论失败', error)
  } finally {
    commentsLoading.value = false
  }
}

async function handleLike() {
  try {
    const result = await likeArticle(article.value.id)
    article.value.likes_count = result.likes_count
    ElMessage.success('点赞成功')
  } catch (error) {
    console.error('点赞失败', error)
  }
}

async function handleSubmitComment() {
  if (!newComment.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }
  
  submitting.value = true
  try {
    await createComment(article.value.id, { content: newComment.value })
    ElMessage.success('评论发表成功')
    newComment.value = ''
    await fetchComments()
  } catch (error) {
    console.error('发表评论失败', error)
  } finally {
    submitting.value = false
  }
}

function handleCommentSubmitted() {
  fetchComments()
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.article-detail-card {
  margin-bottom: 20px;
}

.article-cover-image {
  height: 300px;
  overflow: hidden;
  border-radius: 4px;
}

.article-cover-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
  margin-bottom: 16px;
}

.article-tags {
  margin-bottom: 20px;
  display: flex;
  gap: 8px;
}

.article-content {
  line-height: 1.8;
  color: #303133;
}

.article-content :deep(img) {
  max-width: 100%;
  height: auto;
}

.article-content :deep(pre) {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  overflow-x: auto;
}

.article-content :deep(code) {
  background: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Consolas', 'Monaco', monospace;
}

.comments-card {
  margin-bottom: 20px;
}

.comments-header {
  font-weight: 600;
}

.comment-input-area {
  margin-bottom: 20px;
}

.comment-submit {
  display: flex;
  justify-content: flex-end;
  margin-top: 12px;
}

.comment-login-prompt {
  margin-bottom: 20px;
}

.comment-item {
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 16px;
  margin-bottom: 16px;
}

.comment-item:last-child {
  border-bottom: none;
}
</style>
