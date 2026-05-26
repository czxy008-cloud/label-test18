<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 class="login-title">忘记密码</h2>
      <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent>
        <el-form-item prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入注册邮箱"
            size="large"
            :prefix-icon="Message"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleSubmit"
            style="width: 100%"
          >
            发送验证码
          </el-button>
        </el-form-item>
      </el-form>
      <div class="login-footer">
        <span>想起密码了？</span>
        <el-link type="primary" @click="$router.push('/login')">返回登录</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessage } from 'element-plus'
import { Message } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const formRef = ref(null)
const loading = ref(false)
const form = ref({
  email: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

async function handleSubmit() {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
  } catch (e) {
    return
  }
  
  loading.value = true
  try {
    await authStore.forgotPassword(form.value.email)
    ElMessage.success('验证码已发送到您的邮箱，请注意查收')
    router.push({
      name: 'ResetPassword',
      query: { email: form.value.email }
    })
  } catch (error) {
    console.error('发送验证码失败', error)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 32px;
  color: #303133;
}

.login-footer {
  text-align: center;
  margin-top: 16px;
  color: #909399;
}
</style>
