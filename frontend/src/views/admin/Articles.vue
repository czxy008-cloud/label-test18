<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>文章管理</span>
          <el-button type="primary" @click="goToCreate">
            <el-icon><Plus /></el-icon>
            新建文章
          </el-button>
        </div>
      </template>

      <el-table :data="articles" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'">
              {{ row.is_published ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="views_count" label="浏览" width="100" />
        <el-table-column prop="likes_count" label="点赞" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="goToEdit(row.id)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next"
          @current-change="fetchArticles"
          @size-change="handlePageSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getArticles, deleteArticle } from '@/api/articles'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const router = useRouter()

const loading = ref(false)
const articles = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)

onMounted(() => {
  fetchArticles()
})

async function fetchArticles() {
  loading.value = true
  try {
    const data = await getArticles({
      page: page.value,
      page_size: pageSize.value
    })
    articles.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('获取文章失败', error)
  } finally {
    loading.value = false
  }
}

function handlePageSizeChange() {
  page.value = 1
  fetchArticles()
}

function goToCreate() {
  router.push('/editor')
}

function goToEdit(id) {
  router.push(`/editor/${id}`)
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除文章"${row.title}"吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteArticle(row.id)
    ElMessage.success('删除成功')
    fetchArticles()
  } catch (e) {
    if (e !== 'cancel') {
      console.error('删除文章失败', e)
    }
  }
}

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
