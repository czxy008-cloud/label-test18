<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.articles }}</div>
          <div class="stat-label">文章总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.comments }}</div>
          <div class="stat-label">评论总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.tags }}</div>
          <div class="stat-label">标签总数</div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-value">{{ stats.users }}</div>
          <div class="stat-label">用户总数</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px;">
      <template #header>
        <span>最近文章</span>
      </template>
      <el-table :data="recentArticles" v-loading="loading">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="views_count" label="浏览" width="100" />
        <el-table-column prop="likes_count" label="点赞" width="100" />
        <el-table-column prop="created_at" label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getArticles } from '@/api/articles'
import { getTags } from '@/api/tags'
import { getComments } from '@/api/comments'
import dayjs from 'dayjs'

const loading = ref(false)
const recentArticles = ref([])
const stats = ref({
  articles: 0,
  comments: 0,
  tags: 0,
  users: 0
})

onMounted(async () => {
  await loadData()
})

async function loadData() {
  loading.value = true
  try {
    const [articlesData, tagsData, commentsData] = await Promise.all([
      getArticles({ page: 1, page_size: 5, is_published: true }),
      getTags(),
      getComments({ page: 1, page_size: 1 })
    ])
    recentArticles.value = articlesData.items
    stats.value.articles = articlesData.total
    stats.value.tags = tagsData.length
    stats.value.comments = commentsData.total
  } catch (error) {
    console.error('加载数据失败', error)
  } finally {
    loading.value = false
  }
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 36px;
  font-weight: 600;
  color: #409eff;
}

.stat-label {
  color: #909399;
  margin-top: 8px;
}
</style>
