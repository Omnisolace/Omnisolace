<template>
  <div class="min-h-screen pb-20 page-container">
    <!-- 移动端顶部导航 -->
    <header class="lg:hidden shadow-sm border-b safe-area-inset-top" style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);">
      <div class="px-3 sm:px-4">
        <div class="flex items-center justify-between h-14" :class="{ 'h-16': userStore.isElderMode }">
          <!-- 左侧：返回按钮和简化标题 -->
          <div class="flex items-center min-w-0 flex-1">
            <button
              @click="$router.back()"
              class="mr-2 p-1.5 text-gray-400 hover:text-gray-600 rounded-lg flex-shrink-0"
              :class="{ 'p-2 mr-3': userStore.isElderMode }"
            >
              <ArrowLeftIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
            </button>
            <div class="min-w-0 flex-1">
              <h1 class="text-sm font-semibold text-gray-900 truncate"
                  :class="{ 'text-base': userStore.isElderMode }">
                个人中心
              </h1>
            </div>
          </div>
          
          <!-- 右侧：操作按钮组 -->
          <div class="flex items-center space-x-1 flex-shrink-0" :class="{ 'space-x-2': userStore.isElderMode }">
            <!-- 语言切换组件 -->
            <LanguageSwitcher />
            
            <!-- 紧急求助按钮 -->
            <button
              @click="showEmergencyModal = true"
              class="w-6 h-6 bg-red-500 text-white rounded-full shadow-md hover:bg-red-600 transition-all duration-200 flex items-center justify-center flex-shrink-0"
              :class="{ 'w-8 h-8': userStore.isElderMode }"
              :aria-label="t('emergency')"
            >
              <ExclamationTriangleIcon class="h-2.5 w-2.5" :class="{ 'h-3 w-3': userStore.isElderMode }" />
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 桌面端页面标题 -->
    <div class="hidden lg:block border-b" style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);">
      <div class="px-6 lg:px-8 py-4">
        <div class="flex justify-between items-center">
          <div>
            <h1 class="text-xl font-semibold text-gray-900" :class="{ 'text-elder-xl': userStore.isElderMode }">
              {{ t('personalCenter') }}
            </h1>
            <p class="text-sm text-gray-500 mt-1" :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('managePersonalInfo') }}
            </p>
          </div>
          
          <!-- 桌面端语言切换和紧急求助按钮 -->
          <div class="flex items-center space-x-4">
            <!-- 语言切换组件 -->
            <LanguageSwitcher />
            
            <!-- 紧急求助按钮 -->
            <button
              @click="showEmergencyModal = true"
              class="w-8 h-8 bg-red-500 text-white rounded-full shadow-md hover:bg-red-600 transition-all duration-200 flex items-center justify-center"
              :class="{ 'w-10 h-10': userStore.isElderMode }"
              :aria-label="t('emergency')"
            >
              <ExclamationTriangleIcon class="h-4 w-4" :class="{ 'h-5 w-5': userStore.isElderMode }" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <main class="px-4 sm:px-6 lg:px-8 py-6">
      <!-- 用户信息卡片 -->
      <div class="rounded-lg shadow-sm border p-6 mb-6 card-bg">
        <div class="flex items-center">
          <!-- 头像 -->
          <div class="h-16 w-16 rounded-full flex items-center justify-center text-white text-xl font-bold mr-4 overflow-hidden"
               :class="{ 'h-20 w-20 text-2xl': userStore.isElderMode }"
               :style="userStore.user?.avatar ? `background-image: url(${userStore.user.avatar}); background-size: cover; background-position: center;` : 'background-color: var(--color-primary-500);'">
            <img v-if="userStore.user?.avatar" 
                 :src="userStore.user.avatar" 
                 :alt="userStore.user?.nickname || '头像'"
                 class="w-full h-full object-cover rounded-full" />
            <span v-else>{{ getInitials() }}</span>
          </div>
          
          <div class="flex-1">
            <h2 class="text-xl font-semibold text-gray-900"
                :class="{ 'text-elder-xl': userStore.isElderMode }">
              {{ userStore.user?.nickname || userStore.user?.username || userStore.user?.name || t('user') }}
            </h2>
            <p class="text-gray-500"
               :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ userStore.userAgeConfig.name }} ({{ userStore.userAgeConfig.ageRange }})
            </p>
            <!-- 个人简介 -->
            <div v-if="userStore.user?.profile?.bio" class="mt-2">
              <p class="text-gray-600 text-sm italic"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                "{{ userStore.user.profile.bio }}"
              </p>
            </div>
            <div v-if="userStore.user?.isGuest" class="mt-2">
              <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                {{ t('guestMode') }}
              </span>
            </div>
          </div>
          
          <button
            @click="showEditProfile = true"
            class="btn-secondary"
            :class="{ 'px-4 py-3 text-elder-base': userStore.isElderMode }"
          >
            {{ t('edit') }}
          </button>
        </div>
      </div>

      <!-- 心理档案卡片 -->
      <div class="rounded-lg shadow-sm border p-6 mb-6 card-bg">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-900"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('psychologicalProfile') }}
          </h3>
          <button
            @click="showPsychProfile = true"
            class="text-primary-600 hover:text-primary-500 text-sm font-medium"
            :class="{ 'text-elder-sm': userStore.isElderMode }"
          >
            {{ t('viewDetails') }}
          </button>
        </div>

        <!-- 情绪统计概览 -->
        <div class="grid grid-cols-2 gap-4 mb-4">
          <div class="text-center p-4 rounded-lg" style="background-color: var(--color-primary-50);">
            <div class="text-2xl font-bold text-primary-600"
                 :class="{ 'text-elder-xl': userStore.isElderMode }">
              {{ totalChats }}
            </div>
            <div class="text-sm text-gray-600"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('conversationCount') }}
            </div>
          </div>
          <div class="text-center p-4 rounded-lg" style="background-color: var(--color-primary-50);">
            <div class="text-2xl font-bold text-green-600"
                 :class="{ 'text-elder-xl': userStore.isElderMode }">
              {{ continuousDays }}
            </div>
            <div class="text-sm text-gray-600"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ t('continuousDays') }}
            </div>
          </div>
        </div>

        <!-- 最近情绪趋势 -->
        <div class="mb-4">
          <h4 class="text-sm font-medium text-gray-700 mb-2"
              :class="{ 'text-elder-base': userStore.isElderMode }">
            {{ t('emotionTrendLast7Days') }}
          </h4>
          <div class="flex items-end space-x-1 h-20">
            <div
              v-for="(day, index) in emotionTrendData"
              :key="index"
              class="flex-1 bg-primary-200 rounded-t"
              :style="{ height: `${day.score}%` }"
              :title="`${day.date}: ${day.emotion}`"
            ></div>
          </div>
        </div>

        <button
          @click="generateReport"
          :disabled="loading"
          class="w-full btn-primary"
          :class="{ 'py-3 text-elder-base': userStore.isElderMode }"
        >
          {{ t('generateReport') }}
        </button>
      </div>

      <!-- 功能设置 -->
      <div class="space-y-6">

        <!-- 主题色选择 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('themeColors') }}
          </h3>
          <div class="space-y-4">
            <div
              v-for="(theme, key) in userStore.colorThemes"
              :key="key"
              @click="switchColorTheme(key)"
              class="flex items-center justify-between p-4 border border-gray-200 rounded-lg cursor-pointer hover:border-primary-500 transition-colors"
              :class="{ 'border-primary-500 bg-primary-50': userStore.colorTheme === key }"
            >
              <div class="flex items-center">
                <!-- 主题色预览 -->
                <div class="w-8 h-8 rounded-full mr-3 border-2 border-gray-200"
                     :style="{ backgroundColor: theme.primary }"
                     :class="{ 'w-10 h-10': userStore.isElderMode }">
                </div>
                <div>
                  <h4 class="font-medium text-gray-900"
                      :class="{ 'text-elder-base': userStore.isElderMode }">
                    {{ theme.name }}
                  </h4>
                  <p class="text-sm text-gray-500"
                     :class="{ 'text-elder-sm': userStore.isElderMode }">
                    {{ theme.description }}
                  </p>
                </div>
              </div>
              <div v-if="userStore.colorTheme === key"
                   class="w-5 h-5 bg-primary-500 rounded-full flex items-center justify-center">
                <CheckIcon class="h-3 w-3 text-white" />
              </div>
            </div>
          </div>
        </div>

        <!-- 青少年特殊设置 -->
        <div v-if="userStore.ageGroup === 'teen'" class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            青少年设置
          </h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-gray-900"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  家长监督模式
                </h4>
                <p class="text-sm text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  允许家长查看使用情况摘要
                </p>
              </div>
              <button
                @click="userStore.toggleParentalMode()"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  userStore.isParentalMode ? 'bg-primary-500' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    userStore.isParentalMode ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <h4 class="font-medium text-gray-900 mb-2"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                家长联系方式
              </h4>
              <p class="text-sm text-gray-600 mb-2"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ userStore.user?.parentPhone || '未设置' }}
              </p>
              <button
                @click="showEditParentContact = true"
                class="text-primary-600 hover:text-primary-500 text-sm font-medium"
                :class="{ 'text-elder-sm': userStore.isElderMode }"
              >
                {{ t('modifyContact') }}
              </button>
            </div>
          </div>
        </div>

        <!-- 老年特殊设置 -->
        <div v-if="userStore.ageGroup === 'elder'" class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            老年用户设置
          </h3>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-gray-900"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  语音优先模式
                </h4>
                <p class="text-sm text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  优先使用语音输入和播放
                </p>
              </div>
              <button
                @click="toggleVoicePriority()"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  voicePriority ? 'bg-primary-500' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    voicePriority ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>
            
            <div class="pt-4 border-t border-gray-200">
              <h4 class="font-medium text-gray-900 mb-2"
                  :class="{ 'text-elder-base': userStore.isElderMode }">
                {{ t('childrenContact') }}
              </h4>
              <p class="text-sm text-gray-600 mb-2"
                 :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ userStore.user?.helperPhone || t('notSet') }}
              </p>
              <button
                @click="showEditHelperContact = true"
                class="text-primary-600 hover:text-primary-500 text-sm font-medium"
                :class="{ 'text-elder-sm': userStore.isElderMode }"
              >
                {{ t('modifyContact') }}
              </button>
            </div>
          </div>
        </div>

        <!-- 通用设置 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('generalSettings') }}
          </h3>
          <div class="space-y-4">
            <!-- 推送通知 -->
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-gray-900"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ t('pushNotifications') }}
                </h4>
                <p class="text-sm text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('pushNotificationsDesc') }}
                </p>
              </div>
              <button
                @click="toggleNotifications()"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  notificationsEnabled ? 'bg-primary-500' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    notificationsEnabled ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>

            <!-- 数据同步 -->
            <div class="flex items-center justify-between">
              <div>
                <h4 class="font-medium text-gray-900"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ t('dataSync') }}
                </h4>
                <p class="text-sm text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ t('dataSyncDesc') }}
                </p>
              </div>
              <button
                @click="toggleDataSync()"
                :class="[
                  'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                  dataSyncEnabled ? 'bg-primary-500' : 'bg-gray-200'
                ]"
              >
                <span
                  :class="[
                    'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                    dataSyncEnabled ? 'translate-x-6' : 'translate-x-1'
                  ]"
                />
              </button>
            </div>
          </div>
        </div>

        <!-- 紧急联系人设置 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900"
                :class="{ 'text-elder-lg': userStore.isElderMode }">
              {{ t('emergencyContacts') }}
            </h3>
            <button
              @click="showAddEmergencyContact = true"
              class="text-primary-600 hover:text-primary-500 text-sm font-medium"
              :class="{ 'text-elder-sm': userStore.isElderMode }"
            >
              {{ t('addContact') }}
            </button>
          </div>

          <div v-if="emergencyContacts.length > 0" class="space-y-3">
            <div
              v-for="contact in emergencyContacts"
              :key="contact.id"
              class="flex items-center justify-between p-4 border border-gray-200 rounded-lg"
            >
              <div>
                <h4 class="font-medium text-gray-900"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ contact.name }}
                </h4>
                <p class="text-sm text-gray-500"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ contact.relationship }} - {{ contact.phone }}
                </p>
              </div>
              <div class="flex items-center space-x-2">
                <button
                  @click="editEmergencyContact(contact)"
                  class="text-primary-600 hover:text-primary-500 text-sm"
                >
                  {{ t('edit') }}
                </button>
                <button
                  @click="deleteEmergencyContact(contact.id)"
                  class="text-red-600 hover:text-red-500 text-sm"
                >
                  {{ t('delete') }}
                </button>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-6 text-gray-500">
            <p :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ t('noEmergencyContacts') }}
            </p>
          </div>
        </div>

        <!-- 其他操作 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('otherOperations') }}
          </h3>
          <div class="space-y-3">
            <button
              @click="exportData"
              class="w-full text-left p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              :class="{ 'text-elder-base p-4': userStore.isElderMode }"
            >
              {{ t('exportMyData') }}
            </button>
            <button
              @click="clearData"
              class="w-full text-left p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              :class="{ 'text-elder-base p-4': userStore.isElderMode }"
            >
              {{ t('clearChatRecords') }}
            </button>
            <button
              @click="showAbout = true"
              class="w-full text-left p-3 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors"
              :class="{ 'text-elder-base p-4': userStore.isElderMode }"
            >
              {{ t('aboutOmnisolace') }}
            </button>
            <button
              @click="logout"
              class="w-full text-left p-3 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
              :class="{ 'text-elder-base p-4': userStore.isElderMode }"
            >
              {{ t('logout') }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- 各种弹窗组件 -->
    <EditProfileModal v-if="showEditProfile" @close="showEditProfile = false" />
    <PsychProfileModal v-if="showPsychProfile" @close="showPsychProfile = false" />
    <AboutModal v-if="showAbout" @close="showAbout = false" />
    <EmergencyModal v-if="showEmergencyModal" @close="showEmergencyModal = false" />
    
    <!-- 清空聊天记录确认弹窗 -->
    <ClearChatConfirmModal v-if="showClearChatModal" ref="clearChatModal" @close="showClearChatModal = false" @success="handleClearChatSuccess" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import { chatApi } from '@/utils/api'
import {
  ArrowLeftIcon,
  CheckIcon,
  UserIcon,
  SparklesIcon,
  HeartIcon,
  AcademicCapIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import EditProfileModal from '@/components/EditProfileModal.vue'
import PsychProfileModal from '@/components/PsychProfileModal.vue'
import AboutModal from '@/components/AboutModal.vue'
import EmergencyModal from '@/components/EmergencyModal.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import ClearChatConfirmModal from '@/components/ClearChatConfirmModal.vue'
import { t } from '@/stores/language'

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()

// 响应式状态
const loading = ref(false)
const showEditProfile = ref(false)
const showPsychProfile = ref(false)
const showAbout = ref(false)
const showEditParentContact = ref(false)
const showEditHelperContact = ref(false)
const showAddEmergencyContact = ref(false)
const showEmergencyModal = ref(false)
const showClearChatModal = ref(false)
const clearChatModal = ref(null)

// 设置状态
const voicePriority = ref(userStore.user?.voicePriority || false)
const notificationsEnabled = ref(true)
const dataSyncEnabled = ref(true)

// 紧急联系人
const emergencyContacts = ref([
  // 示例数据
  // { id: 1, name: '张医生', phone: '138****8888', relationship: '心理咨询师' }
])

// 显示模式选项已移除，现在在编辑个人信息中设置

// 计算属性
const totalChats = computed(() => chatStore.chatHistory.length)
const continuousDays = computed(() => {
  // 计算连续使用天数的逻辑
  return 7 // 示例数据
})

const emotionTrendData = computed(() => {
  // 生成最近7天的情绪趋势数据
  const days = []
  for (let i = 6; i >= 0; i--) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    days.push({
      date: date.toLocaleDateString(),
      score: Math.floor(Math.random() * 80) + 20,
      emotion: [t('happy'), t('neutral'), t('anxious'), t('sad')][Math.floor(Math.random() * 4)]
    })
  }
  return days
})

// 方法
const getInitials = () => {
  const name = userStore.user?.nickname || userStore.user?.username || userStore.user?.name || t('user')
  return name.slice(0, 2).toUpperCase()
}

// switchDisplayMode方法已移除，现在在编辑个人信息中设置

const switchColorTheme = (themeKey) => {
  userStore.setColorTheme(themeKey)
  const themeName = userStore.colorThemes[themeKey]?.name
  if (window.$notification) {
    window.$notification.success(t('switchedToTheme', { theme: themeName }))
  }
}

const toggleVoicePriority = () => {
  voicePriority.value = !voicePriority.value
  // 这里应该调用API更新用户设置
  if (window.$notification) {
    window.$notification.info(voicePriority.value ? t('voicePriorityEnabled') : t('voicePriorityDisabled'))
  }
}

const toggleNotifications = async () => {
  if (!notificationsEnabled.value) {
    // 请求通知权限
    if ('Notification' in window) {
      const permission = await Notification.requestPermission()
      if (permission === 'granted') {
        notificationsEnabled.value = true
        if (window.$notification) {
          window.$notification.success(t('notificationsEnabled'))
        }
      } else {
        if (window.$notification) {
          window.$notification.error(t('notificationsDenied'))
        }
      }
    }
  } else {
    notificationsEnabled.value = false
    if (window.$notification) {
      window.$notification.info(t('notificationsDisabled'))
    }
  }
}

const toggleDataSync = () => {
  dataSyncEnabled.value = !dataSyncEnabled.value
  if (window.$notification) {
    window.$notification.info(dataSyncEnabled.value ? t('dataSyncEnabled') : t('dataSyncDisabled'))
  }
}

const generateReport = async () => {
  loading.value = true
  try {
    // 模拟生成报告
    await new Promise(resolve => setTimeout(resolve, 2000))
    if (window.$notification) {
      window.$notification.success(t('reportSuccess'), t('reportSentToEmail'))
    }
  } catch (error) {
    if (window.$notification) {
      window.$notification.error(t('reportFailed'))
    }
  } finally {
    loading.value = false
  }
}

const editEmergencyContact = (contact) => {
  // 编辑紧急联系人
  console.log('编辑联系人:', contact)
}

const deleteEmergencyContact = (contactId) => {
  if (confirm(t('deleteContactConfirm'))) {
    emergencyContacts.value = emergencyContacts.value.filter(c => c.id !== contactId)
    if (window.$notification) {
      window.$notification.success(t('emergencyContactDeleted'))
    }
  }
}

const exportData = () => {
  // 导出用户数据
  if (window.$notification) {
    window.$notification.info(t('dataExportComingSoon'))
  }
}

const clearData = () => {
  // 显示清空聊天记录确认弹窗
  showClearChatModal.value = true
}

const handleClearChatSuccess = () => {
  // 清空聊天记录成功后的处理
  console.log('聊天记录已清空')
}

const logout = async () => {
  if (confirm(t('confirmLogout'))) {
    // 先清除用户状态
    await userStore.logout()
    
    // 使用 nextTick 确保状态更新后再导航
    await nextTick()
    
    // 导航到登录页
    router.push('/login')
    
    if (window.$notification) {
      window.$notification.info(t('loggedOut'))
    }
  }
}

// 生命周期
onMounted(async () => {
  console.log('个人中心加载完成')
  // 获取最新的用户信息
  try {
    await userStore.fetchUserProfile()
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})
</script>

<style scoped>
/* 切换按钮样式 */
.relative.inline-flex {
  transition: background-color 0.2s ease;
}

.relative.inline-flex span {
  transition: transform 0.2s ease;
}

/* 情绪趋势图 */
.flex.items-end > div {
  transition: height 0.3s ease;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .border {
    border-width: 2px;
  }
  
  .border-primary-500 {
    border-color: rgb(29 78 216);
  }
}
</style>
