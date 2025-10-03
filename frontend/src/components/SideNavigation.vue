<template>
  <nav 
    class="fixed left-0 top-0 h-full border-r shadow-sm z-40 transition-transform duration-300"
    style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);"
    :class="[
      isCollapsed ? (userStore.isElderMode ? 'w-20' : 'w-16') : 'w-64',
      { 'elder-sidebar': userStore.isElderMode }
    ]"
  >
    <!-- 顶部品牌区域 -->
    <div class="flex items-center justify-between p-4 border-b" :class="{ 'p-6': userStore.isElderMode }" style="border-color: var(--color-primary-100);">
      <div v-if="!isCollapsed" class="flex items-center">
        <div class="h-8 w-8 bg-primary-500 rounded-full flex items-center justify-center mr-3"
             :class="{ 'h-10 w-10': userStore.isElderMode }">
          <HeartIcon class="h-5 w-5 text-white" :class="{ 'h-6 w-6': userStore.isElderMode }" />
        </div>
        <div class="flex items-center">
          <img 
            v-if="logoUrl"
            :src="logoUrl" 
            alt="Omnisolace Logo" 
            class="h-6 w-auto object-contain"
            :class="{ 'h-8': userStore.isElderMode }"
            @error="handleLogoError"
          />
          <span v-else class="text-lg font-semibold text-gray-900" :class="{ 'text-elder-lg': userStore.isElderMode }">
            Omnisolace
          </span>
        </div>
      </div>
      <button
        @click="toggleCollapse"
        class="p-2 text-gray-400 hover:text-gray-600 rounded-lg transition-colors"
        :class="{ 'p-3': userStore.isElderMode }"
      >
        <ChevronLeftIcon v-if="!isCollapsed" class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
        <ChevronRightIcon v-else class="h-5 w-5" :class="{ 'h-6 w-6': userStore.isElderMode }" />
      </button>
    </div>

    <!-- 导航菜单 -->
    <div class="flex-1 overflow-y-auto py-4">
      <div class="space-y-1" :class="isCollapsed ? 'px-2' : 'px-3'">
        <!-- 主要导航项 -->
        <router-link
          v-for="item in navigationItems"
          :key="item.name"
          :to="item.to"
          class="nav-item group"
          :class="{ 
            'nav-item-active': $route.name === item.routeName,
            'nav-item-collapsed': isCollapsed
          }"
        >
          <component :is="item.icon" class="nav-icon" :class="{ 'nav-icon-collapsed': isCollapsed }" />
          <span v-if="!isCollapsed" class="nav-label">{{ item.name }}</span>
          <!-- 活动指示器（仅在侧边栏展开时显示） -->
          <div v-if="$route.name === item.routeName && !isCollapsed" class="active-indicator"></div>
        </router-link>
      </div>

      <!-- 分隔线 -->
      <div class="my-4 border-t border-gray-200"></div>

      <!-- 紧急求助按钮 -->
      <div :class="isCollapsed ? 'px-2' : 'px-3'">
        <button
          @click="showEmergencyModal = true"
          class="emergency-nav-btn group w-full"
          :class="{ 
            'justify-center': isCollapsed,
            'emergency-nav-btn-collapsed': isCollapsed
          }"
        >
          <ExclamationTriangleIcon class="emergency-nav-icon" :class="{ 'emergency-nav-icon-collapsed': isCollapsed }" />
          <span v-if="!isCollapsed" class="nav-label text-white">{{ t('emergency') }}</span>
        </button>
      </div>

      <!-- 主题色彩选择（仅桌面端显示） -->
      <div v-if="!isCollapsed" class="px-3 mt-4">
        <div class="text-xs font-medium text-gray-500 mb-2" :class="{ 'text-elder-sm': userStore.isElderMode }">
          {{ t('themeColors') }}
        </div>
        <div class="space-y-1">
          <button
            v-for="(theme, key) in userStore.colorThemes"
            :key="key"
            @click="userStore.setColorTheme(key)"
            :class="[
              'w-full text-left px-3 py-2 text-sm rounded-lg transition-colors flex items-center',
              userStore.colorTheme === key 
                ? 'bg-primary-50 text-primary-600 border border-primary-100' 
                : 'text-gray-600 hover:bg-gray-50',
              { 'px-4 py-3 text-elder-sm': userStore.isElderMode }
            ]"
          >
            <!-- 主题色预览 -->
            <div class="w-4 h-4 rounded-full mr-2 border border-gray-300"
                 :style="{ backgroundColor: theme.primary }"
                 :class="{ 'w-5 h-5': userStore.isElderMode }">
            </div>
            {{ theme.name }}
          </button>
        </div>
      </div>
    </div>

    <!-- 底部用户信息 -->
    <div class="border-t p-4" :class="{ 'p-6': userStore.isElderMode }" style="border-color: var(--color-primary-100);">
      <router-link
        to="/profile"
        class="flex items-center space-x-3 text-gray-700 hover:text-gray-900 transition-colors"
        :class="{ 'justify-center': isCollapsed }"
      >
        <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 overflow-hidden"
             :class="{ 'w-10 h-10': userStore.isElderMode }"
             :style="getAvatarStyle()">
          <img v-if="userStore.user?.avatar && !avatarLoadError" 
               :src="userStore.user.avatar" 
               :alt="userStore.user?.nickname || userStore.user?.username || '头像'"
               class="w-full h-full object-cover rounded-full"
               @error="handleAvatarError"
               @load="handleAvatarLoad" />
          <span v-else-if="!userStore.user?.avatar || avatarLoadError" class="text-white font-bold text-sm" :class="{ 'text-base': userStore.isElderMode }">
            {{ getInitials() }}
          </span>
        </div>
        <div v-if="!isCollapsed" class="flex-1 min-w-0">
          <p class="text-sm font-medium truncate" :class="{ 'text-elder-sm': userStore.isElderMode }">
            {{ userStore.user?.nickname || userStore.user?.username || userStore.user?.name || '用户' }}
          </p>
          <p class="text-xs text-gray-500 truncate" :class="{ 'text-elder-sm': userStore.isElderMode }">
            {{ getGreeting() }}
          </p>
        </div>
      </router-link>
    </div>

    <!-- 紧急求助弹窗 -->
    <Teleport to="body">
      <EmergencyModal v-if="showEmergencyModal" @close="showEmergencyModal = false" />
    </Teleport>
  </nav>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useUserStore } from '@/stores/user'
import { t } from '@/stores/language'
import {
  HeartIcon,
  HomeIcon,
  ChatBubbleLeftRightIcon,
  UserIcon,
  ExclamationTriangleIcon,
  ChevronLeftIcon,
  ChevronRightIcon
} from '@heroicons/vue/24/outline'
import EmergencyModal from './EmergencyModal.vue'

const userStore = useUserStore()

// 定义事件发射器
const emit = defineEmits(['sidebar-toggle'])

// 响应式状态
const isCollapsed = ref(false)
const showEmergencyModal = ref(false)
const avatarLoadError = ref(false)

// Logo URL - 尝试多种路径
const logoUrl = ref('/images/Omnisolace_logo_wor.png')

// Logo错误处理
const handleLogoError = () => {
  console.error('Logo加载失败，尝试备用路径')
  // 尝试不同的路径
  if (logoUrl.value === '/images/Omnisolace_logo_wor.png') {
    logoUrl.value = './images/Omnisolace_logo_wor.png'
  } else if (logoUrl.value === './images/Omnisolace_logo_wor.png') {
    logoUrl.value = '/public/images/Omnisolace_logo_wor.png'
  } else {
    // 如果所有路径都失败，显示文字作为备用
    logoUrl.value = ''
  }
}

// 导航项配置
const navigationItems = computed(() => [
  {
    name: t('home'),
    to: '/',
    routeName: 'Home',
    icon: HomeIcon
  },
  {
    name: t('chat'),
    to: '/chat',
    routeName: 'Chat',
    icon: ChatBubbleLeftRightIcon
  },
  {
    name: t('profile'),
    to: '/profile',
    routeName: 'Profile',
    icon: UserIcon
  }
])

// 年龄模式选项已移除，现在在编辑个人信息中设置

// 方法
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
  // 发射事件通知父组件侧边栏状态变化
  emit('sidebar-toggle', isCollapsed.value)
}

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return t('lateNight')
  if (hour < 12) return t('goodMorning')
  if (hour < 14) return t('goodNoon')
  if (hour < 18) return t('goodAfternoon')
  if (hour < 22) return t('goodEvening')
  return t('lateNight')
}

// 头像相关方法
const getAvatarStyle = () => {
  if (userStore.user?.avatar && !avatarLoadError.value) {
    return `background-image: url(${userStore.user.avatar}); background-size: cover; background-position: center;`
  }
  return 'background-color: var(--color-primary-500);'
}

const getInitials = () => {
  const name = userStore.user?.nickname || userStore.user?.username || userStore.user?.name || t('user')
  return name.slice(0, 2).toUpperCase()
}

const handleAvatarError = () => {
  console.warn('头像加载失败，使用默认显示')
  avatarLoadError.value = true
}

const handleAvatarLoad = () => {
  avatarLoadError.value = false
}

// 监听用户头像变化，重置错误状态
watch(() => userStore.user?.avatar, (newAvatar) => {
  if (newAvatar) {
    avatarLoadError.value = false
  }
}, { immediate: true })
</script>

<style scoped>
.nav-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  color: rgb(107 114 128);
  border-radius: 0.5rem;
  transition: all 200ms;
  position: relative;
  text-decoration: none;
}

.nav-item:hover {
  background-color: var(--color-primary-50);
  color: var(--color-primary);
}

.nav-item-active {
  background-color: var(--color-primary-50);
  color: var(--color-primary);
}

.nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

/* 收起状态下的导航项样式 */
.nav-item-collapsed {
  justify-content: center;
  padding: 0.75rem 0.25rem;
}

.nav-icon-collapsed {
  margin-right: 0;
}

.nav-label {
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.active-indicator {
  position: absolute;
  right: 0.5rem;
  width: 0.5rem;
  height: 0.5rem;
  background-color: var(--color-primary);
  border-radius: 50%;
}

.emergency-nav-btn {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background-color: rgb(239 68 68);
  color: white;
  border-radius: 0.5rem;
  transition: all 200ms;
  border: none;
  cursor: pointer;
}

.emergency-nav-btn:hover {
  background-color: rgb(220 38 38);
  transform: translateY(-1px);
}

.emergency-nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  margin-right: 0.75rem;
  flex-shrink: 0;
}

/* 收起状态下的紧急求助按钮样式 */
.emergency-nav-btn-collapsed {
  justify-content: center;
  padding: 0.75rem 0.25rem;
}

.emergency-nav-icon-collapsed {
  margin-right: 0;
}

/* 老年模式样式 */
.elder-sidebar .nav-item {
  padding: 1rem;
}

.elder-sidebar .nav-icon {
  width: 1.75rem;
  height: 1.75rem;
  margin-right: 1rem;
}

.elder-sidebar .nav-label {
  font-size: 1rem;
}

.elder-sidebar .emergency-nav-btn {
  padding: 1rem;
}

.elder-sidebar .emergency-nav-icon {
  width: 1.75rem;
  height: 1.75rem;
  margin-right: 1rem;
}

/* 老年模式收起状态样式 */
.elder-sidebar .nav-item-collapsed {
  justify-content: center;
  padding: 1rem 0.25rem;
}

.elder-sidebar .emergency-nav-btn-collapsed {
  justify-content: center;
  padding: 1rem 0.25rem;
}

/* 老年模式收起状态下的图标尺寸调整 */
.elder-sidebar .nav-icon-collapsed {
  width: 1.5rem;
  height: 1.5rem;
}

.elder-sidebar .emergency-nav-icon-collapsed {
  width: 1.5rem;
  height: 1.5rem;
}

/* 响应式设计 */
@media (max-width: 1024px) {
  nav {
    transform: translateX(-100%);
  }
  
  nav.mobile-open {
    transform: translateX(0);
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .nav-item {
    border: 1px solid transparent;
  }
  
  .nav-item:hover,
  .nav-item-active {
    border-color: rgb(59 130 246);
  }
  
  .emergency-nav-btn {
    border: 2px solid white;
  }
}

/* 移除导航项动画效果 */
</style>
