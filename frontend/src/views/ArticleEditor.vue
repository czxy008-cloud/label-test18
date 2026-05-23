<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">{{ isEdit ? '编辑文章' : '撰写文章' }}</h1>
    </div>

    <el-card v-loading="loading">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入文章标题"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入文章摘要"
            maxlength="1000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="封面图" prop="cover_image">
          <el-input
            v-model="form.cover_image"
            placeholder="请输入封面图片URL"
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-select
            v-model="form.tag_ids"
            multiple
            placeholder="选择标签"
            style="width: 100%"
          >
            <el-option
              v-for="tag in tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            >
              <div style="display: flex; align-items: center;">
                <el-tag
                  :color="tag.color"
                  effect="light"
                  size="small"
                  style="margin-right: 8px;"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="发布状态">
          <el-switch
            v-model="form.is_published"
            active-text="立即发布"
            inactive-text="存为草稿"
          />
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <div class="editor-container">
            <Toolbar
              style="border-bottom: 1px solid #ccc"
              :editor="editorRef"
              :defaultConfig="toolbarConfig"
              mode="default"
            />
            <Editor
              v-model="form.content"
              style="height: 500px; overflow-y: hidden;"
              :defaultConfig="editorConfig"
              mode="default"
              @onCreated="handleCreated"
            />
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" :loading="submitting" @click="handleSubmit">
            {{ isEdit ? '保存修改' : '发布文章' }}
          </el-button>
          <el-button @click="handleCancel">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, shallowRef, onBeforeUnmount } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getTags } from '@/api/tags'
import { getArticleById, createArticle, updateArticle } from '@/api/articles'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import '@wangeditor/editor/dist/css/style.css'

const router = useRouter()
const route = useRoute()

const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)
const isEdit = ref(!!route.params.id)
const tags = ref([])

const form = ref({
  title: '',
  summary: '',
  content: '',
  cover_image: '',
  is_published: true,
  tag_ids: []
})

const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

const editorRef = shallowRef()

const toolbarConfig = {
  excludeKeys: []
}

const editorConfig = {
  placeholder: '请输入文章内容...',
  MENU_CONF: {
    uploadImage: {
      customUpload(file, insertFn) {
        const reader = new FileReader()
        reader.onload = (e) => {
          insertFn(e.target.result, file.name, e.target.result)
        }
        reader.readAsDataURL(file)
      }
    }
  }
}

function handleCreated(editor) {
  editorRef.value = editor
}

onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})

onMounted(async () => {
  await fetchTags()
  if (isEdit.value) {
    await fetchArticle()
  }
})

async function fetchTags() {
  try {
    tags.value = await getTags()
  } catch (error) {
    console.error('获取标签失败', error)
  }
}

async function fetchArticle() {
  loading.value = true
  try {
    const article = await getArticleById(route.params.id)
    form.value = {
      title: article.title,
      summary: article.summary || '',
      content: article.content,
      cover_image: article.cover_image || '',
      is_published: article.is_published,
      tag_ids: article.tags.map(tag => tag.id)
    }
  } catch (error) {
    console.error('获取文章失败', error)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  if (!formRef.value) return

  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }

  if (!form.value.content || form.value.content === '<p><br></p>') {
    ElMessage.warning('请输入文章内容')
    return
  }

  submitting.value = true
  try {
    if (isEdit.value) {
      await updateArticle(route.params.id, form.value)
      ElMessage.success('文章更新成功')
    } else {
      const result = await createArticle(form.value)
      ElMessage.success('文章发布成功')
    }
    router.push('/articles')
  } catch (error) {
    console.error('保存文章失败', error)
  } finally {
    submitting.value = false
  }
}

function handleCancel() {
  router.back()
}
</script>

<style scoped>
.editor-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  z-index: 100;
  width: 100%;
}

:deep(.w-e-text-container) {
  min-height: 500px !important;
}

:deep(.w-e-toolbar) {
  flex-wrap: wrap;
}
</style>
