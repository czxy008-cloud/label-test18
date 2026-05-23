<template>
  <div class="comment-container">
    <div class="comment-item">
      <div class="comment-header">
        <div class="comment-user">
          <el-avatar :size="32" :src="comment.user?.avatar_url">
            {{ comment.user?.username?.charAt(0)?.toUpperCase() }}
          </el-avatar>
          <div>
            <div class="comment-username">{{ comment.user?.username }}</div>
            <div class="comment-time">{{ formatDate(comment.created_at) }}</div>
          </div>
        </div>
        <el-button
          v-if="authStore.isLoggedIn"
          type="primary"
          link
          size="small"
          @click="showReply = true"
        >
          回复
        </el-button>
      </div>
      <div class="comment-content">{{ comment.content }}</div>
      
      <div v-if="showReply" class="reply-input-area">
        <el-input
          v-model="replyContent"
          type="textarea"
          :rows="2"
          placeholder="回复评论..."
          maxlength="500"
        />
        <div class="reply-actions">
          <el-button size="small" @click="showReply = false; replyContent = ''">取消</el-button>
          <el-button
            type="primary"
            size="small"
            :loading="submitting"
            @click="handleReply"
          >
            回复
          </el-button>
        </div>
      </div>
    </div>

    <div v-if="comment.replies?.length > 0" class="replies">
      <div
        v-for="reply in comment.replies"
        :key="reply.id"
        class="reply-item"
      >
        <div class="reply-header">
          <div class="comment-user">
            <el-avatar :size="24" :src="reply.user?.avatar_url">
              {{ reply.user?.username?.charAt(0)?.toUpperCase() }}
            </el-avatar>
            <div>
              <span class="reply-username">{{ reply.user?.username }}</span>
              <span class="reply-time">{{ formatDate(reply.created_at) }}</span>
            </div>
          </div>
        </div>
        <div class="comment-content">{{ reply.content }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { createComment } from '@/api/comments'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  articleId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['submitted'])

const authStore = useAuthStore()
const showReply = ref(false)
const replyContent = ref('')
const submitting = ref(false)

function formatDate(date) {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}

async function handleReply() {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }

  submitting.value = true
  try {
    await createComment(props.articleId, {
      content: replyContent.value,
      parent_id: props.comment.id
    })
    ElMessage.success('回复成功')
    replyContent.value = ''
    showReply.value = false
    emit('submitted')
  } catch (error) {
    console.error('回复失败', error)
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.comment-container {
  margin-bottom: 16px;
}

.comment-item {
  padding: 12px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.comment-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.comment-username {
  font-weight: 500;
  color: #303133;
}

.comment-time {
  font-size: 12px;
  color: #909399;
}

.comment-content {
  color: #606266;
  line-height: 1.6;
  white-space: pre-wrap;
  word-break: break-word;
  padding-left: 42px;
}

.reply-input-area {
  margin-top: 12px;
  padding-left: 42px;
}

.reply-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 8px;
}

.replies {
  margin-left: 42px;
  background: #f5f7fa;
  border-radius: 4px;
  padding: 8px 0;
}

.reply-item {
  padding: 12px;
  border-bottom: 1px solid #ebeef5;
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-header {
  margin-bottom: 6px;
}

.reply-username {
  font-weight: 500;
  color: #303133;
  margin-right: 8px;
}

.reply-time {
  font-size: 12px;
  color: #909399;
}
</style>
