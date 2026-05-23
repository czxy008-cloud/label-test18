<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>评论管理</span>
          <el-select
            v-model="filterStatus"
            placeholder="筛选状态"
            style="width: 150px"
            @change="fetchComments"
          >
            <el-option label="全部" :value="null" />
            <el-option label="已审核" :value="true" />
            <el-option label="待审核" :value="false" />
          </el-select>
        </div>
      </template>

      <el-table :data="comments" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户" width="150">
          <template #default="{ row }">
            <div style="display: flex; align-items: center; gap: 8px;">
              <el-avatar :size="24" :src="row.user?.avatar_url">
                {{ row.user?.username?.charAt(0)?.toUpperCase() }}
              </el-avatar>
              <span>{{ row.user?.username }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="content" label="内容" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_approved ? 'success' : 'warning'">
              {{ row.is_approved ? '已审核' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_approved"
              type="success"
              link
              @click="handleApprove(row, true)"
            >
              通过
            </el-button>
            <el-button
              v-if="row.is_approved"
              type="warning"
              link
              @click="handleApprove(row, false)"
            >
              取消审核
            </el-button>
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
          @current-change="fetchComments"
          @size-change="handlePageSizeChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getComments, approveComment, deleteComment } from '@/api/comments'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'

const loading = ref(false)
const comments = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(10)
const filterStatus = ref(null)

onMounted(() => {
  fetchComments()
})

async function fetchComments() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value
    }
    if (filterStatus.value !== null) {
      params.is_approved = filterStatus.value
    }
    const data = await getComments(params)
    comments.value = data.items
    total.value = data.total
  } catch (error) {
    console.error('获取评论失败', error)
  } finally {
    loading.value = false
  }
}

function handlePageSizeChange() {
  page.value = 1
  fetchComments()
}

async function handleApprove(row, isApproved) {
  try {
    await approveComment(row.id, isApproved)
    ElMessage.success(isApproved ? '审核通过' : '已取消审核')
    fetchComments()
  } catch (error) {
    console.error('操作失败', error)
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteComment(row.id)
    ElMessage.success('删除成功')
    fetchComments()
  } catch (e) {
    if (e !== 'cancel') {
      console.error('删除评论失败', e)
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
