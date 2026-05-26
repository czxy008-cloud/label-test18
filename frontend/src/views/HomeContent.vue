<template>
  <div>
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">欢迎来到个人博客</h1>
        <p class="hero-subtitle">分享技术、生活与思考</p>
        <el-button type="primary" size="large" @click="$router.push('/articles')">
          浏览文章
        </el-button>
      </div>
    </div>

    <div class="section">
      <div class="section-header">
        <h2 class="section-title">最新文章</h2>
        <el-link type="primary" @click="$router.push('/articles')">查看全部 →</el-link>
      </div>
      
      <div v-loading="loading">
        <template v-if="articles.length > 0">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" v-for="article in articles" :key="article.id">
              <el-card class="article-card" shadow="hover" @click="goToDetail(article.id)">
                <div v-if="article.cover_image" class="card-cover">
                  <img :src="article.cover_image" :alt="article.title" />
                </div>
                <div class="card-content">
                  <h3 class="card-title">{{ article.title }}</h3>
                  <p v-if="article.summary" class="card-summary">{{ article.summary }}</p>
                  <div class="card-meta">
                    <span>{{ formatDate(article.created_at) }}</span>
                    <span><el-icon><View /></el-icon> {{ article.views_count }}</span>
                  </div>
                  <div class="card-tags">
                    <el-tag
                      v-for="tag in article.tags.slice(0, 3)"
                      :key="tag.id"
                      :color="tag.color"
                      effect="light"
                      size="small"
                    >
                      {{ tag.name }}
                    </el-tag>
                  </div>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </template>
        <div v-else class="empty-state">
          <el-empty description="暂无文章" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles } from '@/api/articles'
import { View } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const router = useRouter()
const loading = ref(false)
const articles = ref([])

onMounted(() => {
  fetchLatestArticles()
})

async function fetchLatestArticles() {
  loading.value = true
  try {
    const data = await getArticles({ page: 1, page_size: 6, is_published: true })
    articles.value = data.items
  } catch (error) {
    console.error('获取最新文章失败', error)
  } finally {
    loading.value = false
  }
}

function goToDetail(id) {
  router.push(`/article/${id}`)
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD')
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 80px 20px;
  text-align: center;
  color: #fff;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 32px;
}

.section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.article-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: all 0.3s;
  height: 100%;
}

.article-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
}

.card-cover {
  height: 160px;
  overflow: hidden;
  border-radius: 4px 4px 0 0;
}

.card-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-content {
  padding: 16px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-summary {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #909399;
  font-size: 13px;
  margin-bottom: 12px;
}

.card-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.empty-state {
  padding: 60px 0;
}
</style>
