import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册', public: true }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: () => import('@/views/ForgotPassword.vue'),
    meta: { title: '忘记密码', public: true }
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('@/views/ResetPassword.vue'),
    meta: { title: '重置密码', public: true }
  },
  {
    path: '/',
    component: () => import('@/views/Home.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/HomeContent.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'articles',
        name: 'ArticleList',
        component: () => import('@/views/ArticleList.vue'),
        meta: { title: '文章列表' }
      },
      {
        path: 'article/:id',
        name: 'ArticleDetail',
        component: () => import('@/views/ArticleDetail.vue'),
        meta: { title: '文章详情' }
      },
      {
        path: 'editor',
        name: 'ArticleEditor',
        component: () => import('@/views/ArticleEditor.vue'),
        meta: { title: '撰写文章', requiresAuth: true }
      },
      {
        path: 'editor/:id',
        name: 'ArticleEdit',
        component: () => import('@/views/ArticleEditor.vue'),
        meta: { title: '编辑文章', requiresAuth: true }
      }
    ]
  },
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: { title: '管理后台', requiresAuth: true, requiresAdmin: true },
    redirect: '/admin/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'articles',
        name: 'AdminArticles',
        component: () => import('@/views/admin/Articles.vue'),
        meta: { title: '文章管理' }
      },
      {
        path: 'tags',
        name: 'AdminTags',
        component: () => import('@/views/admin/Tags.vue'),
        meta: { title: '标签管理' }
      },
      {
        path: 'comments',
        name: 'AdminComments',
        component: () => import('@/views/admin/Comments.vue'),
        meta: { title: '评论管理' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '用户管理' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到', public: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  document.title = `${to.meta.title || '个人博客'} - 博客系统`

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'Home' })
    return
  }

  if ((to.name === 'Login' || to.name === 'Register' || to.name === 'ForgotPassword' || to.name === 'ResetPassword') && authStore.isLoggedIn) {
    next({ name: 'Home' })
    return
  }

  next()
})

export default router
