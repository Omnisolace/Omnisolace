<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
    <div class="text-center">
      <!-- 404 图标 -->
      <div class="mx-auto h-24 w-24 bg-gray-200 rounded-full flex items-center justify-center mb-8"
           :class="{ 'h-32 w-32': userStore.isElderMode }">
        <ExclamationTriangleIcon class="h-12 w-12 text-gray-400"
                                :class="{ 'h-16 w-16': userStore.isElderMode }" />
      </div>

      <!-- 错误信息 -->
      <h1 class="text-4xl font-bold text-gray-900 mb-4"
          :class="{ 'text-6xl': userStore.isElderMode }">
        404
      </h1>
      <h2 class="text-xl font-semibold text-gray-700 mb-4"
          :class="{ 'text-elder-xl': userStore.isElderMode }">
        页面未找到
      </h2>
      <p class="text-gray-500 mb-8 max-w-md"
         :class="{ 'text-elder-base': userStore.isElderMode }">
        抱歉，您访问的页面不存在或已被移动。请检查网址是否正确，或返回首页继续浏览。
      </p>

      <!-- 操作按钮 -->
      <div class="space-y-4 sm:space-y-0 sm:space-x-4 sm:flex sm:justify-center">
        <button
          @click="goBack"
          class="w-full sm:w-auto btn-secondary"
          :class="{ 'py-3 px-6 text-elder-base': userStore.isElderMode }"
        >
          <ArrowLeftIcon class="h-5 w-5 mr-2 inline"
                        :class="{ 'h-6 w-6': userStore.isElderMode }" />
          返回上页
        </button>
        <button
          @click="goHome"
          class="w-full sm:w-auto btn-primary"
          :class="{ 'py-3 px-6 text-elder-base': userStore.isElderMode }"
        >
          <HomeIcon class="h-5 w-5 mr-2 inline"
                   :class="{ 'h-6 w-6': userStore.isElderMode }" />
          回到首页
        </button>
      </div>

      <!-- 快捷链接 -->
      <div class="mt-12">
        <h3 class="text-sm font-medium text-gray-900 mb-4"
            :class="{ 'text-elder-base': userStore.isElderMode }">
          您可能在寻找：
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-lg mx-auto">
          <router-link
            v-for="link in quickLinks"
            :key="link.path"
            :to="link.path"
            class="quick-link"
            :class="{ 'p-4': userStore.isElderMode }"
          >
            <component :is="link.icon" 
                      class="h-6 w-6 text-primary-500 mb-2"
                      :class="{ 'h-8 w-8': userStore.isElderMode }" />
            <span class="text-sm font-medium text-gray-900"
                  :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ link.name }}
            </span>
          </router-link>
        </div>
      </div>

      <!-- 联系支持 -->
      <div class="mt-12 p-4 bg-blue-50 rounded-lg max-w-md mx-auto"
           :class="{ 'p-6': userStore.isElderMode }">
        <h3 class="text-sm font-medium text-blue-900 mb-2"
            :class="{ 'text-elder-base': userStore.isElderMode }">
          需要帮助？
        </h3>
        <p class="text-sm text-blue-700 mb-3"
           :class="{ 'text-elder-sm': userStore.isElderMode }">
          如果您认为这是一个错误，请联系我们的客服团队
        </p>
        <button
          @click="contactSupport"
          class="w-full btn-primary"
          :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
        >
          联系客服
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  ExclamationTriangleIcon,
  ArrowLeftIcon,
  HomeIcon,
  ChatBubbleLeftRightIcon,
  UserIcon,
  PhoneIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const userStore = useUserStore()

// 快捷链接
const quickLinks = [
  { path: '/', name: '首页', icon: HomeIcon },
  { path: '/chat', name: '对话', icon: ChatBubbleLeftRightIcon },
  { path: '/profile', name: '个人中心', icon: UserIcon }
]

// 方法
const goBack = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push('/')
  }
}

const goHome = () => {
  router.push('/')
}

const contactSupport = () => {
  // 打开客服电话
  window.open('tel:400-161-9995')
  
  if (window.$notification) {
    window.$notification.info('客服电话：400-161-9995')
  }
}
</script>

<style scoped>
.quick-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid rgb(229 231 235);
  border-radius: 0.5rem;
  transition: all 200ms;
  text-align: center;
}

.quick-link:hover {
  border-color: rgb(147 197 253);
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}

/* 响应式设计 */
@media (max-width: 640px) {
  .sm\:grid-cols-3 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .quick-link {
    border-width: 2px;
    border-color: rgb(156 163 175);
  }
  
  .quick-link:hover {
    border-color: rgb(37 99 235);
  }
}
</style>
