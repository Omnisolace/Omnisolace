<template>
  <div class="min-h-screen lg:pb-0 pb-20 page-container">
    <!-- 移动端顶部导航栏 -->
    <header class="lg:hidden shadow-sm border-b safe-area-inset-top" style="background-color: var(--color-primary-50); border-color: var(--color-primary-100);">
      <div class="px-3 sm:px-4">
        <div class="flex justify-between items-center h-14" :class="{ 'h-16': userStore.isElderMode }">
          <!-- 左侧：应用图标和简化标题 -->
          <div class="flex items-center min-w-0 flex-1">
            <div class="h-6 w-6 bg-primary-500 rounded-full flex items-center justify-center mr-2 flex-shrink-0"
                 :class="{ 'h-8 w-8 mr-3': userStore.isElderMode }">
              <HeartIcon class="h-3 w-3 text-white" :class="{ 'h-4 w-4': userStore.isElderMode }" />
            </div>
            <div class="min-w-0 flex-1">
              <img 
                v-if="logoUrl"
                :src="logoUrl" 
                alt="Omnisolace Logo" 
                class="h-4 w-auto object-contain"
                :class="{ 'h-5': userStore.isElderMode }"
                @error="handleLogoError"
              />
              <span v-else class="text-sm font-semibold text-gray-900 truncate" :class="{ 'text-base': userStore.isElderMode }">
                Omnisolace
              </span>
            </div>
          </div>
          
          <!-- 右侧：操作按钮组 -->
          <div class="flex items-center space-x-1 flex-shrink-0" :class="{ 'space-x-2': userStore.isElderMode }">
            <!-- 情绪状态指示器 -->
            <div class="flex items-center space-x-1 bg-white/50 rounded-full px-2 py-1"
                 :class="{ 'px-3 py-1.5': userStore.isElderMode }">
              <div class="emotion-indicator w-2.5 h-2.5"
                   :class="[
                     chatStore.currentEmotionLabel.bgColor,
                     { 'w-3 h-3': userStore.isElderMode }
                   ]">
              </div>
              <span class="text-xs font-medium"
                    :class="[
                      chatStore.currentEmotionLabel.color,
                      { 'text-sm': userStore.isElderMode }
                    ]">
                {{ chatStore.currentEmotionLabel.name }}
              </span>
            </div>
            
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
              {{ t('welcome') }}
            </h1>
            <p class="text-sm text-gray-500 mt-1" :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ userStore.user?.name || t('user') }}，{{ t('welcomeBack') }}
            </p>
          </div>
          
          <!-- 桌面端语言切换和情绪状态指示器 -->
          <div class="flex items-center space-x-4">
            <!-- 语言切换组件 -->
            <LanguageSwitcher />
            
            <div class="flex items-center space-x-2">
              <div class="emotion-indicator"
                   :class="[
                     chatStore.currentEmotionLabel.bgColor,
                     { 'w-6 h-6': userStore.isElderMode }
                   ]">
              </div>
              <span class="text-sm font-medium"
                    :class="[
                      chatStore.currentEmotionLabel.color,
                      { 'text-elder-sm': userStore.isElderMode }
                    ]">
                {{ chatStore.currentEmotionLabel.name }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <main class="px-4 sm:px-6 lg:px-8 py-6">
      <!-- 欢迎卡片 -->
      <div class="rounded-lg p-6 mb-6 card-bg"
           :class="{ 'p-8': userStore.isElderMode }"
           style="background-color: var(--color-primary); color: white;">
        <h2 class="text-xl font-bold mb-2" :class="{ 'text-elder-xl': userStore.isElderMode }">
          {{ getWelcomeMessage() }}
        </h2>
        <p class="mb-4 opacity-90" :class="{ 'text-elder-base': userStore.isElderMode }">
          {{ getWelcomeDescription() }}
        </p>
        <button
          @click="startNewChat"
          class="px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          :class="{ 'px-8 py-4 text-elder-base': userStore.isElderMode }"
          style="background-color: var(--color-background); color: var(--color-text);"
        >
          {{ t('startChat') }}
        </button>
      </div>

      <!-- 分年龄段功能区域 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- 快捷功能 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('quickFeatures') }}
          </h3>
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="feature in quickFeatures"
              :key="feature.id"
              @click="handleFeatureClick(feature)"
              class="feature-card"
              :class="{ 'p-4': userStore.isElderMode }"
            >
              <component :is="feature.icon" 
                        class="h-6 w-6 text-primary-500 mb-2"
                        :class="{ 'h-8 w-8': userStore.isElderMode }" />
              <span class="text-sm font-medium text-gray-900"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ feature.name }}
              </span>
            </button>
          </div>
        </div>

        <!-- 情绪统计 -->
        <div class="rounded-lg shadow-sm border p-6 card-bg">
          <h3 class="text-lg font-semibold text-gray-900 mb-4"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('recentEmotions') }}
          </h3>
          <div class="space-y-3">
            <div v-for="emotion in recentEmotions" :key="emotion.label"
                 class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="emotion-indicator mr-3"
                     :class="[emotion.bgColor, { 'w-5 h-5': userStore.isElderMode }]">
                </div>
                <span class="text-sm text-gray-700"
                      :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ emotion.name }}
                </span>
              </div>
              <span class="text-sm font-medium text-gray-900"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ emotion.percentage }}%
              </span>
            </div>
          </div>
          
          <!-- 情绪趋势 -->
          <div class="mt-4 pt-4 border-t border-gray-200">
            <div class="flex items-center justify-between">
              <span class="text-sm text-gray-600"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ t('overallTrend') }}
              </span>
              <div class="flex items-center">
                <ArrowTrendingUpIcon v-if="chatStore.emotionTrend === 'improving'" 
                               class="h-4 w-4 text-green-500 mr-1"
                               :class="{ 'h-5 w-5': userStore.isElderMode }" />
                <ArrowTrendingDownIcon v-else-if="chatStore.emotionTrend === 'declining'" 
                                 class="h-4 w-4 text-red-500 mr-1"
                                 :class="{ 'h-5 w-5': userStore.isElderMode }" />
                <MinusIcon v-else 
                          class="h-4 w-4 text-gray-500 mr-1"
                          :class="{ 'h-5 w-5': userStore.isElderMode }" />
                <span class="text-sm font-medium"
                      :class="[
                        getTrendColor(),
                        { 'text-elder-sm': userStore.isElderMode }
                      ]">
                  {{ getTrendText() }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近对话 -->
      <div class="rounded-lg shadow-sm border p-6 card-bg">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-semibold text-gray-900"
              :class="{ 'text-elder-lg': userStore.isElderMode }">
            {{ t('recentChats') }}
          </h3>
          <button
            @click="$router.push('/chat')"
            class="text-primary-600 hover:text-primary-500 text-sm font-medium"
            :class="{ 'text-elder-sm': userStore.isElderMode }"
          >
            {{ t('viewAll') }}
          </button>
        </div>

        <div v-if="recentChats.length > 0" class="space-y-3">
          <div
            v-for="chat in recentChats.slice(0, 3)"
            :key="chat.id"
            @click="loadChat(chat.id)"
            class="chat-item"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h4 class="font-medium text-gray-900 mb-1"
                    :class="{ 'text-elder-base': userStore.isElderMode }">
                  {{ chat.title }}
                </h4>
                <p class="text-sm text-gray-500 line-clamp-2"
                   :class="{ 'text-elder-sm': userStore.isElderMode }">
                  {{ getLastMessage(chat) }}
                </p>
              </div>
              <span class="text-xs text-gray-400 ml-4"
                    :class="{ 'text-elder-sm': userStore.isElderMode }">
                {{ formatTime(chat.updatedAt) }}
              </span>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-8">
          <ChatBubbleLeftRightIcon class="h-12 w-12 text-gray-300 mx-auto mb-4"
                                  :class="{ 'h-16 w-16': userStore.isElderMode }" />
          <p class="text-gray-500"
             :class="{ 'text-elder-base': userStore.isElderMode }">
            {{ t('noConversationHistory') }}
          </p>
          <button
            @click="startNewChat"
            class="mt-4 btn-primary"
            :class="{ 'px-6 py-3 text-elder-base': userStore.isElderMode }"
          >
            {{ t('startChat') }}
          </button>
        </div>
      </div>

      <!-- 年龄段特殊内容 -->
      <div v-if="ageSpecificContent" class="mt-6 rounded-lg shadow-sm border p-6 card-bg">
        <h3 class="text-lg font-semibold text-gray-900 mb-4"
            :class="{ 'text-elder-lg': userStore.isElderMode }">
          {{ ageSpecificContent.title }}
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="item in ageSpecificContent.items"
            :key="item.id"
            @click="handleContentClick(item)"
            class="content-card"
          >
            <component :is="item.icon" 
                      class="h-6 w-6 text-primary-500 mb-2"
                      :class="{ 'h-8 w-8': userStore.isElderMode }" />
            <h4 class="font-medium text-gray-900 mb-1"
                :class="{ 'text-elder-base': userStore.isElderMode }">
              {{ item.title }}
            </h4>
            <p class="text-sm text-gray-500"
               :class="{ 'text-elder-sm': userStore.isElderMode }">
              {{ item.description }}
            </p>
          </div>
        </div>
      </div>
    </main>
    
    <!-- 紧急求助弹窗 -->
    <EmergencyModal v-if="showEmergencyModal" @close="showEmergencyModal = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { useChatStore } from '@/stores/chat'
import {
  HeartIcon,
  ChatBubbleLeftRightIcon,
  FaceSmileIcon,
  BookOpenIcon,
  UserGroupIcon,
  CogIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
  MinusIcon,
  AcademicCapIcon,
  BriefcaseIcon,
  HomeIcon as HomeIconSolid,
  SparklesIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import EmergencyModal from '@/components/EmergencyModal.vue'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import { t } from '@/stores/language'

const router = useRouter()
const userStore = useUserStore()
const chatStore = useChatStore()

// 响应式状态
const recentChats = computed(() => chatStore.chatHistory)
const showEmergencyModal = ref(false)

// Logo URL
const logoUrl = ref('/images/Omnisolace_logo_wor.png')

// Logo错误处理
const handleLogoError = () => {
  console.error('Logo加载失败，尝试备用路径')
  // 尝试不同的路径
  logoUrl.value = './images/Omnisolace_logo_wor.png'
}

// 获取问候语
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 6) return t('nightRest')
  if (hour < 12) return t('goodMorning')
  if (hour < 14) return t('goodNoon')
  if (hour < 18) return t('goodAfternoon')
  if (hour < 22) return t('goodEvening')
  return t('nightRest')
}

// 获取欢迎消息
const getWelcomeMessage = () => {
  const messages = {
    teen: t('youthNotConfused'),
    young: t('workplaceJourney'),
    middle: t('middleAgePressure'),
    elder: t('sunsetBeautiful')
  }
  return messages[userStore.ageGroup] || t('psychologicalHealth')
}

// 获取欢迎描述
const getWelcomeDescription = () => {
  const descriptions = {
    teen: t('studyPressureRelation'),
    young: t('workplaceCompetition'),
    middle: t('workFamilyHealth'),
    elder: t('enjoyLaterLife')
  }
  return descriptions[userStore.ageGroup] || t('professionalAI')
}

// 快捷功能
const quickFeatures = computed(() => {
  const commonFeatures = [
    { id: 'mood', name: t('moodAssessment'), icon: FaceSmileIcon, action: 'mood-test' },
    { id: 'chat', name: t('startChat'), icon: ChatBubbleLeftRightIcon, action: 'start-chat' },
    { id: 'community', name: t('interestCommunity'), icon: UserGroupIcon, action: 'community' },
    { id: 'settings', name: t('personalSettings'), icon: CogIcon, action: 'settings' }
  ]

  const ageSpecificFeatures = {
    teen: [
      { id: 'study', name: t('studyStressRelief'), icon: BookOpenIcon, action: 'study-help' },
      { id: 'social', name: t('socialGuidance'), icon: UserGroupIcon, action: 'social-help' }
    ],
    young: [
      { id: 'career', name: t('careerPlanning'), icon: BriefcaseIcon, action: 'career-help' },
      { id: 'relationship', name: t('relationshipConsultation'), icon: HeartIcon, action: 'relationship-help' }
    ],
    middle: [
      { id: 'family', name: t('familyBalance'), icon: HomeIconSolid, action: 'family-help' },
      { id: 'health', name: t('healthManagement'), icon: SparklesIcon, action: 'health-help' }
    ],
    elder: [
      { id: 'memory', name: t('memoryTraining'), icon: AcademicCapIcon, action: 'memory-training' },
      { id: 'family', name: t('intergenerationalCommunication'), icon: UserGroupIcon, action: 'family-communication' }
    ]
  }

  return [...commonFeatures.slice(0, 2), ...(ageSpecificFeatures[userStore.ageGroup] || []), ...commonFeatures.slice(2)]
})

// 近期情绪统计
const recentEmotions = computed(() => {
  // 这里应该基于真实的情绪历史数据计算
  return [
    { label: 'happy', name: t('happy'), bgColor: 'bg-emotion-happy', percentage: 35 },
    { label: 'neutral', name: t('neutral'), bgColor: 'bg-emotion-neutral', percentage: 40 },
    { label: 'anxious', name: t('anxious'), bgColor: 'bg-emotion-anxious', percentage: 20 },
    { label: 'sad', name: t('sad'), bgColor: 'bg-emotion-sad', percentage: 5 }
  ]
})

// 年龄段特殊内容
const ageSpecificContent = computed(() => {
  const contents = {
    teen: {
      title: t('teenZone'),
      items: [
        { id: 1, title: t('studyStressManagement'), description: t('studyMethods'), icon: BookOpenIcon },
        { id: 2, title: t('adolescentConfusion'), description: t('bodyMindDevelopment'), icon: UserGroupIcon },
        { id: 3, title: t('parentChildCommunication'), description: t('improveParentRelationship'), icon: HeartIcon },
        { id: 4, title: t('interestDevelopment'), description: t('discoverSelf'), icon: SparklesIcon }
      ]
    },
    young: {
      title: t('youngZone'),
      items: [
        { id: 1, title: t('workplaceAdaptation'), description: t('workplaceAdaptationDesc'), icon: BriefcaseIcon },
        { id: 2, title: t('emotionalLife'), description: t('loveMarriage'), icon: HeartIcon },
        { id: 3, title: t('selfGrowth'), description: t('personalValue'), icon: AcademicCapIcon },
        { id: 4, title: t('lifeBalance'), description: t('workLifeBalance'), icon: SparklesIcon }
      ]
    },
    middle: {
      title: t('middleAgeZone'),
      items: [
        { id: 1, title: t('careerBottleneck'), description: t('middleAgeCareer'), icon: BriefcaseIcon },
        { id: 2, title: t('familyResponsibilities'), description: t('coupleChildrenElderly'), icon: HomeIconSolid },
        { id: 3, title: t('healthManagement'), description: t('physicalMentalHealth'), icon: SparklesIcon },
        { id: 4, title: t('lifePlanning'), description: t('midlifeCrisis'), icon: AcademicCapIcon }
      ]
    },
    elder: {
      title: t('elderlyZone'),
      items: [
        { id: 1, title: t('lonelinessRelief'), description: t('socialActivities'), icon: UserGroupIcon },
        { id: 2, title: t('intergenerationalCommunication'), description: t('childrenRelationship'), icon: HeartIcon },
        { id: 3, title: t('healthPreservation'), description: t('healthAdaptation'), icon: SparklesIcon },
        { id: 4, title: t('lifeAdaptation'), description: t('retirementAdaptationDesc'), icon: HomeIconSolid }
      ]
    }
  }
  
  return contents[userStore.ageGroup] || null
})

// 方法
const startNewChat = () => {
  chatStore.createNewChat()
  router.push('/chat')
}

const handleFeatureClick = (feature) => {
  switch (feature.action) {
    case 'start-chat':
      startNewChat()
      break
    case 'mood-test':
      // 跳转到情绪测评
      if (window.$notification) {
        window.$notification.info(t('featureComingSoon', { feature: t('moodAssessment') }))
      }
      break
    case 'community':
      // 跳转到社区
      if (window.$notification) {
        window.$notification.info(t('featureComingSoon', { feature: t('interestCommunity') }))
      }
      break
    case 'settings':
      router.push('/profile')
      break
    default:
      if (window.$notification) {
        window.$notification.info(t('featureComingSoon', { feature: feature.name }))
      }
  }
}

const loadChat = (chatId) => {
  chatStore.loadChat(chatId)
  router.push('/chat')
}

const getLastMessage = (chat) => {
  if (chat.messages && chat.messages.length > 0) {
    const lastMessage = chat.messages[chat.messages.length - 1]
    return lastMessage.content
  }
  return t('noMessages')
}

const formatTime = (timestamp) => {
  const now = Date.now()
  const diff = now - timestamp
  
  if (diff < 60000) return t('justNow')
  if (diff < 3600000) return `${Math.floor(diff / 60000)}${t('minutesAgo')}`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}${t('hoursAgo')}`
  if (diff < 604800000) return `${Math.floor(diff / 86400000)}${t('daysAgo')}`
  
  return new Date(timestamp).toLocaleDateString()
}

const getTrendColor = () => {
  switch (chatStore.emotionTrend) {
    case 'improving': return 'text-green-600'
    case 'declining': return 'text-red-600'
    default: return 'text-gray-600'
  }
}

const getTrendText = () => {
  switch (chatStore.emotionTrend) {
    case 'improving': return t('improving')
    case 'declining': return t('needsAttention')
    default: return t('stable')
  }
}

const handleContentClick = (item) => {
  // 根据内容类型跳转或执行相应操作
  if (window.$notification) {
    window.$notification.info(t('featureComingSoon', { feature: item.title }))
  }
}

// 生命周期
onMounted(() => {
  // 初始化数据
  console.log('首页加载完成')
})
</script>

<style scoped>
.feature-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem;
  border: 1px solid rgb(229 231 235);
  border-radius: 0.5rem;
  transition: all 200ms;
  cursor: pointer;
}

.feature-card:hover {
  border-color: rgb(147 197 253);
  box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
}

.chat-item {
  padding: 1rem;
  border: 1px solid rgb(229 231 235);
  border-radius: 0.5rem;
  transition: all 200ms;
  cursor: pointer;
}

.chat-item:hover {
  border-color: rgb(147 197 253);
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}

.content-card {
  padding: 1rem;
  border: 1px solid rgb(229 231 235);
  border-radius: 0.5rem;
  transition: all 200ms;
  cursor: pointer;
}

.content-card:hover {
  border-color: rgb(147 197 253);
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 老年模式特殊样式 */
.elder-mode .feature-card {
  padding: 1.5rem;
}

.elder-mode .chat-item {
  padding: 1.5rem;
}

.elder-mode .content-card {
  padding: 1.5rem;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  
  .elder-mode .grid-cols-2 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

/* 高对比度支持 */
@media (prefers-contrast: high) {
  .feature-card,
  .chat-item,
  .content-card {
    border-width: 2px;
    border-color: rgb(156 163 175);
  }
  
  .feature-card:hover,
  .chat-item:hover,
  .content-card:hover {
    border-color: rgb(37 99 235);
  }
}
</style>
