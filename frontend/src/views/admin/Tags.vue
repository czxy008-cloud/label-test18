<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>标签管理</span>
          <el-button type="primary" @click="openCreateDialog">
            <el-icon><Plus /></el-icon>
            新建标签
          </el-button>
        </div>
      </template>

      <el-table :data="tags" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="标签名" width="200">
          <template #default="{ row }">
            <el-tag :color="row.color" effect="light">{{ row.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="slug" label="Slug" width="150" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑标签' : '新建标签'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标签名" prop="name">
          <el-input v-model="form.name" placeholder="请输入标签名" maxlength="100" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="2"
            placeholder="请输入标签描述"
            maxlength="500"
          />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="form.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTags, createTag, updateTag, deleteTag } from '@/api/tags'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const loading = ref(false)
const tags = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const editId = ref(null)

const form = ref({
  name: '',
  description: '',
  color: '#1890ff'
})

const rules = {
  name: [
    { required: true, message: '请输入标签名', trigger: 'blur' }
  ]
}

onMounted(() => {
  fetchTags()
})

async function fetchTags() {
  loading.value = true
  try {
    tags.value = await getTags()
  } catch (error) {
    console.error('获取标签失败', error)
  } finally {
    loading.value = false
  }
}

function openCreateDialog() {
  isEdit.value = false
  editId.value = null
  form.value = {
    name: '',
    description: '',
    color: '#1890ff'
  }
  dialogVisible.value = true
}

function openEditDialog(row) {
  isEdit.value = true
  editId.value = row.id
  form.value = {
    name: row.name,
    description: row.description || '',
    color: row.color || '#1890ff'
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      await updateTag(editId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await createTag(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchTags()
  } catch (error) {
    console.error('保存标签失败', error)
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确定要删除标签"${row.name}"吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteTag(row.id)
    ElMessage.success('删除成功')
    fetchTags()
  } catch (e) {
    if (e !== 'cancel') {
      console.error('删除标签失败', e)
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
</style>
