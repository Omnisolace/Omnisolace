<template>
  <Teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-2" :class="{ 'top-20': userStore.isElderMode }">
      <TransitionGroup name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
          :class="getNotificationClass(notification.type)"
          @click="removeNotification(notification.id)"
        >
          <div class="flex items-start">
            <component
              :is="getNotificationIcon(notification.type)"
              class="notification-icon flex-shrink-0"
              :class="getIconColorClass(notification.type)"
            />
            <div class="ml-3 flex-1">
              <h4 v-if="notification.title" class="notification-title">
                {{ notification.title }}
              </h4>
              <p class="notification-message">
                {{ notification.message }}
              </p>
            </div>
            <button
              @click.stop="removeNotification(notification.id)"
              class="ml-4 flex-shrink-0 text-gray-400 hover:text-gray-600"
              aria-label="关闭通知"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import {
  CheckCircleIcon,
  ExclamationCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

const userStore = useUserStore()

// 通知列表
const notifications = ref([])

// 通知类型图标映射
const iconMap = {
  success: CheckCircleIcon,
  error: ExclamationCircleIcon,
  warning: ExclamationTriangleIcon,
  info: InformationCircleIcon
}

// 方法
const addNotification = (notification) => {
  const id = Date.now() + Math.random()
  const newNotification = {
    id,
    type: notification.type || 'info',
    title: notification.title,
    message: notification.message,
    duration: notification.duration || 5000,
    persistent: notification.persistent || false
  }
  
  notifications.value.push(newNotification)
  
  // 自动移除（除非是持久化通知）
  if (!newNotification.persistent) {
    setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
  }
  
  return id
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
}

const clearAllNotifications = () => {
  notifications.value = []
}

const getNotificationClass = (type) => {
  const baseClass = 'max-w-sm w-full bg-white shadow-lg rounded-lg border-l-4 cursor-pointer hover:shadow-xl transition-shadow duration-200'
  
  const typeClasses = {
    success: 'border-green-500',
    error: 'border-red-500',
    warning: 'border-yellow-500',
    info: 'border-blue-500'
  }
  
  return `${baseClass} ${typeClasses[type] || typeClasses.info}`
}

const getNotificationIcon = (type) => {
  return iconMap[type] || iconMap.info
}

const getIconColorClass = (type) => {
  const colorClasses = {
    success: 'text-green-500',
    error: 'text-red-500',
    warning: 'text-yellow-500',
    info: 'text-blue-500'
  }
  
  return colorClasses[type] || colorClasses.info
}

// 暴露方法给全局使用
const useNotification = () => {
  return {
    success: (message, title = '成功', options = {}) => 
      addNotification({ type: 'success', title, message, ...options }),
    error: (message, title = '错误', options = {}) => 
      addNotification({ type: 'error', title, message, ...options }),
    warning: (message, title = '警告', options = {}) => 
      addNotification({ type: 'warning', title, message, ...options }),
    info: (message, title = '提示', options = {}) => 
      addNotification({ type: 'info', title, message, ...options }),
    clear: clearAllNotifications
  }
}

// 全局注册通知方法
window.$notification = useNotification()

defineExpose({
  addNotification,
  removeNotification,
  clearAllNotifications
})
</script>

<style scoped>
.notification {
  padding: 1rem;
}

.notification-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-top: 0.125rem;
}

/* 通知图标颜色样式 */

.notification-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: rgb(17 24 39);
  margin-bottom: 0.25rem;
}

.notification-message {
  font-size: 0.875rem;
  color: rgb(55 65 81);
}

/* 老年模式样式 */
.elder-mode .notification {
  padding: 1.5rem;
  max-width: 28rem;
}

.elder-mode .notification-icon {
  width: 2rem;
  height: 2rem;
}

.elder-mode .notification-title {
  font-size: 1rem;
  font-weight: 500;
}

.elder-mode .notification-message {
  font-size: 1rem;
}

/* 通知动画 */
.notification-enter-active {
  transition: all 0.3s ease-out;
}

.notification-leave-active {
  transition: all 0.3s ease-in;
}

.notification-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.notification-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.notification-move {
  transition: transform 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .fixed.top-4.right-4 {
    top: 0.5rem;
    right: 0.5rem;
    left: 0.5rem;
  }
  
  .notification {
    max-width: none;
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .notification {
    border-width: 2px;
  }
}

/* 减少动画支持 */
@media (prefers-reduced-motion: reduce) {
  .notification-enter-active,
  .notification-leave-active,
  .notification-move {
    transition: none;
  }
}
</style>
