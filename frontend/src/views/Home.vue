<template>
  <div class="app-container">
    <el-container>
      <el-header class="header">
        <div class="header-inner">
          <div class="logo" @click="$router.push('/')">
            <el-icon :size="28"><Edit /></el-icon>
            <span>个人博客</span>
          </div>
          <el-menu mode="horizontal" :default-active="activeMenu" class="nav-menu" @select="handleMenuSelect">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/articles">文章</el-menu-item>
            <el-menu-item index="/editor" v-if="authStore.isLoggedIn">撰写</el-menu-item>
            <el-menu-item index="/admin" v-if="authStore.isAdmin">管理</el-menu-item>
          </el-menu>
          <div class="user-area">
            <template v-if="authStore.isLoggedIn">
              <el-dropdown @command="handleUserCommand">
                <span class="user-info">
                  <el-avatar :size="32" :src="authStore.user?.avatar_url">
                    {{ authStore.user?.username?.charAt(0)?.toUpperCase() }}
                  </el-avatar>
                  <span class="username">{{ authStore.user?.username }}</span>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                    <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <el-button type="primary" @click="$router.push('/login')">登录</el-button>
              <el-button @click="$router.push('/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>
      <el-main>
        <div class="main-content">
          <router-view />
        </div>
      </el-main>
      <el-footer class="footer">
        <p>© 2024 个人博客系统 - Powered by FastAPI & Vue3</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox, ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const activeMenu = computed(() => route.path)

onMounted(async () => {
  if (authStore.token && !authStore.user) {
    try {
      await authStore.fetchUser()
    } catch (e) {
      console.error('获取用户信息失败', e)
    }
  }
})

function handleMenuSelect(index) {
  if (index !== route.path) {
    router.push(index)
  }
}

function handleUserCommand(command) {
  if (command === 'logout') {
    ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    }).then(() => {
      authStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
    }).catch(() => {})
  } else if (command === 'profile') {
    ElMessage.info('个人中心功能开发中')
  }
}
</script>

<style scoped>
.header {
  background: #fff;
  padding: 0;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
  cursor: pointer;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
  margin-left: 40px;
}

.user-area {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  color: #606266;
}

.footer {
  text-align: center;
  color: #909399;
  padding: 20px;
  background: #fff;
  border-top: 1px solid #ebeef5;
}

.footer p {
  margin: 0;
}
</style>
