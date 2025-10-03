<template>
  <nav 
    class="fixed bottom-0 left-0 right-0 border-t safe-area-inset-bottom z-40"
    :class="{ 'elder-nav': userStore.isElderMode }"
    style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);"
    :style="{
      minHeight: dynamicNavHeight.minHeight,
      height: dynamicNavHeight.height
    }"
  >
    <div class="flex items-center h-full" :class="navHeight">
      <!-- 首页 -->
      <router-link
        to="/"
        class="nav-item flex-1"
        :class="{ 'nav-item-active': $route.name === 'Home' }"
      >
        <HomeIcon class="nav-icon" />
        <span class="nav-label">{{ t('home') }}</span>
      </router-link>

      <!-- 对话 -->
      <router-link
        to="/chat"
        class="nav-item flex-1"
        :class="{ 'nav-item-active': $route.name === 'Chat' }"
      >
        <ChatBubbleLeftRightIcon class="nav-icon" />
        <span class="nav-label">{{ t('chat') }}</span>
        <!-- 未读消息提示 -->
        <div v-if="hasUnreadMessages" class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full"></div>
      </router-link>

      <!-- 个人中心 -->
      <router-link
        to="/profile"
        class="nav-item flex-1"
        :class="{ 'nav-item-active': $route.name === 'Profile' }"
      >
        <UserIcon class="nav-icon" />
        <span class="nav-label">{{ t('profile') }}</span>
      </router-link>
    </div>

  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { t } from '@/stores/language'
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  UserIcon
} from '@heroicons/vue/24/outline'

const userStore = useUserStore()
const chatStore = useChatStore()

// 响应式状态

// 计算属性
const navHeight = computed(() => {
  return userStore.isElderMode ? 'py-3' : 'py-2'
})

// 动态计算导航栏高度
const dynamicNavHeight = computed(() => {
  const baseHeight = userStore.isElderMode ? 80 : 60 // 基础高度（px）
  const minHeight = userStore.isElderMode ? 60 : 50 // 最低高度（px）
  
  // 获取视窗高度
  const vh = window.innerHeight
  const calculatedHeight = Math.max(minHeight, vh * 0.08) // 视窗高度的8%，但不少于最低高度
  
  return {
    minHeight: `${minHeight}px`,
    height: `${Math.min(calculatedHeight, baseHeight)}px`
  }
})


const hasUnreadMessages = computed(() => {
  // 这里可以添加未读消息的逻辑
  return false
})

// 响应式状态
const windowHeight = ref(window.innerHeight)

// 监听窗口大小变化
const handleResize = () => {
  windowHeight.value = window.innerHeight
}

// 生命周期
onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: rgb(107 114 128);
  transition: color 200ms;
  position: relative;
  min-width: 60px;
  padding: 0.5rem;
}

.nav-item:hover {
  color: var(--color-primary);
}

.nav-item-active {
  color: var(--color-primary);
}

.nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-bottom: 0.25rem;
}

.nav-label {
  font-size: 0.75rem;
  font-weight: 500;
}

.emergency-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  color: white;
  transition: all 200ms;
  transform: scale(1);
  position: relative;
  min-width: 60px;
}

.emergency-btn:hover {
  transform: scale(1.05);
}

.emergency-btn:active {
  transform: scale(0.95);
}

.emergency-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-bottom: 0.25rem;
}

/* 老年模式样式 */
.elder-nav .nav-item {
  min-width: 80px;
  padding: 0.75rem;
}

.elder-nav .nav-icon {
  width: 2rem;
  height: 2rem;
  margin-bottom: 0.5rem;
}

.elder-nav .nav-label {
  font-size: 0.875rem;
  font-weight: 500;
}

.elder-nav .emergency-icon {
  width: 2rem;
  height: 2rem;
  margin-bottom: 0.5rem;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .nav-label {
    font-size: 0.75rem;
  }
  
  .elder-nav .nav-label {
    font-size: 0.875rem;
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .nav-item {
    border: 1px solid transparent;
  }
  
  .nav-item:hover {
    border-color: rgb(156 163 175);
  }
  
  .emergency-btn {
    border: 2px solid white;
  }
}

/* 安全区域适配 */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  nav {
    padding-bottom: calc(0.5rem + env(safe-area-inset-bottom));
  }
}
</style>
