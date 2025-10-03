import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由懒加载
const Login = () => import('@/views/Login.vue')
const Home = () => import('@/views/Home.vue')
const Chat = () => import('@/views/Chat.vue')
const Profile = () => import('@/views/Profile.vue')
const NotFound = () => import('@/views/NotFound.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { 
      requiresAuth: false,
      title: '首页'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { 
      requiresAuth: false,
      title: '登录注册'
    }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat,
    meta: { 
      requiresAuth: true,
      title: '心理疏导'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { 
      requiresAuth: true,
      title: '个人中心'
    }
  },
  {
    path: '/404',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '页面未找到'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 保持滚动位置或回到顶部
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - Omnisolace` : 'Omnisolace'
  
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 如果用户未认证，重定向到登录页
    if (!userStore.isAuthenticated) {
      next('/login')
      return
    }
  }
  
  // 特殊处理：如果用户未认证且访问首页，重定向到登录页
  if (to.path === '/' && !userStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // 如果用户已认证且访问登录页，重定向到首页
  if (to.path === '/login' && userStore.isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

// 路由错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  // 可以添加错误上报逻辑
})

export default router
