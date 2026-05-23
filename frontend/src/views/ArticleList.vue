<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">文章列表</h1>
    </div>
    
    <div class="filter-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文章..."
        clearable
        style="width: 240px"
        @keyup.enter="handleSearch"
        @clear="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <el-select
        v-model="selectedTag"
        placeholder="选择标签筛选"
        clearable
        style="width: 180px"
        @change="handleTagFilter"
        @clear="handleTagFilter"
      >
        <el-option
          v-for="tag in tags"
          :key="tag.id"
          :label="tag.name"
          :value="tag.id"
        />
      </el-select>
    </div>

    <div v-loading="loading">
      <template v-if="articles.length > 0">
        <el-card
          v-for="article in articles"
          :key="article.id"
          class="article-card"
          shadow="hover"
          @click="goToDetail(article.id)"
        >
          <div class="article-content-wrapper">
            <div v-if="article.cover_image" class="article-cover">
              <img :src="article.cover_image" :alt="article.title" />
            </div>
            <div class="article-info">
              <h2 class="article-title">{{ article.title }}</h2>
              <p v-if="article.summary" class="article-summary">{{ article.summary }}</p>
              <div class="article-meta">
                <el-avatar :size="20" :src="article.author?.avatar_url">
                  {{ article.author?.username?.charAt(0)?.toUpperCase() }}
                </el-avatar>
                <span>{{ article.author?.username }}</span>
                <span>·</span>
                <span>{{ formatDate(article.created_at) }}</span>
                <span>·</span>
                <span><el-icon><View /></el-icon> {{ article.views_count }}</span>
                <span>·</span>
                <span><el-icon><ChatDotRound /></el-icon> {{ article.likes_count }}</span>
              </div>
              <div class="article-tags">
                <el-tag
                  v-for="tag in article.tags"
                  :key="tag.id"
                  :color="tag.color"
                  effect="light"
                  size="small"
                  class="tag-item"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>
          </div>
        </el-card>
      </template>
      <div v-else class="empty-state">
        <el-empty description="暂无文章" />
      </div>
    </div>

    <div v-if="total > 0" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[5, 10, 20, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="fetchArticles"
        @size-change="handlePageSizeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles } from '@/api/articles'
import { getTags } from '@/api/tags'
import { Search, View, ChatDotRound } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const articles = ref([])
const tags = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const searchKeyword = ref('')
const selectedTag = ref(null)

onMounted(() => {
  fetchTags()
  fetchArticles()
})

async function fetchTags() {
  try {
    tags.value = await getTags()
  } catch (error) {
    console.error('获取标签失败', error)
  }
}

async function fetchArticles() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      is_published: true
    }
    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }
    if (selectedTag.value) {
      params.tag_id = selectedTag.value
    }
    const data = await getArticles(params)
    articles.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('获取文章失败', error)
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  page.value = 1
  fetchArticles()
}

function handleTagFilter() {
  page.value = 1
  fetchArticles()
}

function handlePageSizeChange() {
  page.value = 1
  fetchArticles()
}

function goToDetail(id) {
  router.push(`/article/${id}`)
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.article-card {
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.article-card:hover {
  transform: translateY(-2px);
}

.article-content-wrapper {
  display: flex;
  gap: 20px;
}

.article-cover {
  width: 200px;
  height: 140px;
  flex-shrink: 0;
  border-radius: 4px;
  overflow: hidden;
}

.article-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.article-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.article-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.article-summary {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #909399;
  font-size: 13px;
  margin-bottom: 12px;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
