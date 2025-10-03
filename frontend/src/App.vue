<template>
  <div id="app" :class="[themeClass, { 'elder-mode': userStore.isElderMode, 'teen-mode': userStore.isTeenMode }]">
    <!-- 全局加载状态 -->
    <Transition name="fade">
      <div v-if="isInitializing" class="fixed inset-0 bg-white z-50 flex items-center justify-center">
        <div class="text-center">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p class="text-gray-600">正在初始化...</p>
        </div>
      </div>
    </Transition>

    <!-- 主要内容 -->
    <div v-if="!isInitializing" class="min-h-screen">
      <!-- 桌面端布局 -->
      <div class="hidden lg:flex">
        <!-- 侧边栏导航 -->
        <SideNavigation 
          v-if="userStore.isAuthenticated && route.name !== 'Login'" 
          @sidebar-toggle="handleSidebarToggle"
        />
        
        <!-- 主内容区域 -->
        <main class="flex-1 transition-all duration-300" :class="sidebarMargin">
          <router-view v-slot="{ Component, route }">
            <Transition :name="getTransitionName(route)" mode="out-in">
              <component :is="Component" :key="route.fullPath" />
            </Transition>
          </router-view>
        </main>
      </div>

      <!-- 移动端布局 -->
      <div class="lg:hidden flex flex-col min-h-screen">
        <!-- 路由视图 -->
        <router-view v-slot="{ Component, route }">
          <Transition :name="getTransitionName(route)" mode="out-in">
            <component :is="Component" :key="route.fullPath" />
          </Transition>
        </router-view>

        <!-- 底部导航（仅在已登录且非登录页时显示） -->
        <BottomNavigation v-if="userStore.isAuthenticated && route.name !== 'Login'" />
      </div>
    </div>

    <!-- 全局通知 -->
    <NotificationContainer />
    
    <!-- 紧急求助弹窗 -->
    <EmergencyModal v-if="showEmergencyModal" @close="showEmergencyModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { initializeLanguage } from '@/stores/language'
import { ExclamationTriangleIcon } from '@heroicons/vue/24/outline'
import BottomNavigation from '@/components/BottomNavigation.vue'
import SideNavigation from '@/components/SideNavigation.vue'
import NotificationContainer from '@/components/NotificationContainer.vue'
import EmergencyModal from '@/components/EmergencyModal.vue'

const route = useRoute()
const userStore = useUserStore()

// 响应式状态
const isInitializing = ref(true)
const showEmergencyModal = ref(false)
const sidebarCollapsed = ref(false)

// 计算属性
const themeClass = computed(() => userStore.userAgeConfig.theme)

// 侧边栏边距计算
const sidebarMargin = computed(() => {
  if (userStore.isAuthenticated && route.name !== 'Login') {
    // 根据侧边栏收起状态和用户模式动态调整边距
    if (sidebarCollapsed.value) {
      return userStore.isElderMode ? 'ml-20' : 'ml-16'
    }
    return 'ml-64'
  }
  return ''
})

// 处理侧边栏切换事件
const handleSidebarToggle = (collapsed) => {
  sidebarCollapsed.value = collapsed
}

// 页面转场动画名称
const getTransitionName = (route) => {
  if (userStore.isElderMode) {
    return 'fade' // 老年模式使用简单的淡入淡出
  }
  return 'slide' // 其他模式使用滑动效果
}

// 初始化应用
const initializeApp = async () => {
  try {
    // 初始化用户数据
    userStore.initializeUser()
    
    // 初始化主题色系统
    userStore.applyThemeColors()
    
    // 初始化语言系统
    initializeLanguage()
    
    // 请求通知权限（PWA推送通知）
    if ('Notification' in window && Notification.permission === 'default') {
      await Notification.requestPermission()
    }
    
    // 检查网络状态
    if (navigator.onLine === false) {
      console.warn('当前处于离线状态')
    }
    
    // 模拟初始化延迟（实际项目中可能需要加载配置等）
    await new Promise(resolve => setTimeout(resolve, 1000))
    
  } catch (error) {
    console.error('应用初始化失败:', error)
  } finally {
    isInitializing.value = false
  }
}

// 全局错误处理
const handleGlobalError = (error) => {
  console.error('全局错误:', error)
  // 这里可以添加错误上报逻辑
}

// 网络状态监听
const handleOnline = () => {
  console.log('网络已连接')
}

const handleOffline = () => {
  console.log('网络已断开')
}

// 生命周期
onMounted(() => {
  initializeApp()
  
  // 添加全局事件监听
  window.addEventListener('error', handleGlobalError)
  window.addEventListener('online', handleOnline)
  window.addEventListener('offline', handleOffline)
  
  // 监听紧急求助快捷键（Ctrl+Shift+H）
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'H') {
      showEmergencyModal.value = true
    }
  })
})

// 清理事件监听
onUnmounted(() => {
  window.removeEventListener('error', handleGlobalError)
  window.removeEventListener('online', handleOnline)
  window.removeEventListener('offline', handleOffline)
})
</script>

<style scoped>
/* 页面转场动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

/* 老年模式特殊样式 */
.elder-mode {
  font-size: 18px;
  line-height: 1.6;
}

.elder-mode * {
  transition-duration: 0.1s; /* 减少动画时间，避免老年用户不适 */
}

/* 青少年模式样式 */
.teen-mode {
  --primary-color: #10b981;
}

.teen-mode .btn-primary {
  background-color: var(--primary-color);
}

/* 确保应用占满全屏 */
#app {
  min-height: 100vh;
  min-height: 100dvh; /* 动态视窗高度，适配移动端 */
}

/* 安全区域适配 */
@supports (padding: env(safe-area-inset-top)) {
  #app {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
}
</style>
